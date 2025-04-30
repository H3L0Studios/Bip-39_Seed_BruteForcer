import itertools
import multiprocessing as mp
from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes, Bip39Languages
)
from itertools import islice, product
from pathlib import Path

# Target address to match
TARGET_ADDRESS = "bc1qsrsrlkckce111dqt3sfpefv2llxqlrc7f8xwnt"

#Set Batch size based on system memory available
MAX_COMBOS_PER_BATCH = 100_000_000 #This batch size consumes about 32 GB of RAM so adjust accordingly.

# Input files and the discovered correct slot order (1-based)
INPUT_FILES = [f"input{i}.txt" for i in range(1, 13)]

ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Use this unless the word order was scrambled
#ORDER = [12, 3, 10, 8, 6, 9, 11, 7, 2, 4, 1, 5]  # Example of a scrambled order

MAX_ADDRESS_INDEX = 9  # Try index 0 through 9 (first 10 addresses)

def chunk_generator(it, size):
    it = iter(it)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk

def load_candidates():
    all_lists = [[line.strip() for line in Path(f).read_text().splitlines() if line.strip()] for f in INPUT_FILES]
    ordered_lists = [all_lists[i - 1] for i in ORDER]
    for idx, lst in enumerate(ordered_lists):
        print(f"[DEBUG] Slot {idx + 1} has {len(lst)} words")
    return ordered_lists

def is_valid_mnemonic(mnemonic: str) -> bool:
    try:
        Bip39MnemonicValidator(Bip39Languages.ENGLISH).Validate(mnemonic)
        return True
    except Exception:
        return False

def derive_address(mnemonic: str, max_index: int = MAX_ADDRESS_INDEX) -> str:
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip84 = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    acct = bip84.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)

    for i in range(max_index):
        addr = acct.AddressIndex(i).PublicKey().ToAddress()
        #print(f"address generated at index {i}: {addr}")
        if addr == TARGET_ADDRESS:
            print(f"[+] Match found at address index {i}")
            return addr
    return None

def worker(combos_chunk, progress_queue, total_combos):
    for words in combos_chunk:
        mnemonic = " ".join(words)
        if not is_valid_mnemonic(mnemonic):
            continue
        address = derive_address(mnemonic)
        if address:
            print("\n[+] FOUND MATCH!")
            print(f"Mnemonic: {mnemonic}")
            return mnemonic
    return None

def chunkify(data, num_chunks):
    chunk_size = max(1, len(data) // num_chunks)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def search(debug=True):
    wordlists = load_candidates()
    total_combos = 1
    for wl in wordlists:
        total_combos *= len(wl)
    print(f"[*] Total combinations to test: {total_combos:,}")

    combo_iter = product(*wordlists)
    batch_idx = 0

    for combos_batch in chunk_generator(combo_iter, MAX_COMBOS_PER_BATCH):
        batch_idx += 1
        print(f"\n[*] Processing batch {batch_idx}, size: {len(combos_batch):,}")

        if debug:
            print("[*] Running in DEBUG mode (single process)...")
            result = worker(combos_batch, None, total_combos)
            if result:
                print("[*] Match found in debug mode:", result)
                return
        else:
            print("[*] Running with multiprocessing...")
            cpu_count = mp.cpu_count()
            print(f"[*] Using {cpu_count} CPU cores")

            chunks = chunkify(combos_batch, cpu_count)
            manager = mp.Manager()
            progress_queue = manager.Queue()

            with mp.Pool(processes=cpu_count) as pool:
                results = pool.starmap(worker, [(chunk, progress_queue, total_combos) for chunk in chunks])

            for result in results:
                if result:
                    print("[*] Match found:", result)
                    return

    print("[-] All batches complete. No match found.")

if __name__ == "__main__":
    # Set debug=False to use multiprocessing
    search(debug=False)