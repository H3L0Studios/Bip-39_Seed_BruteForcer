# Bip-39_Seed_BruteForcer
A simple Python script used to bruteforce BIP39 12 word recovery seeds.
**********************
If this helps you, please tip:
Bitcoin: bc1qgq9rqlryrfcz7tvtehg6k7s354ah4rcn27akah
**********************
Features:
-Uses all available CPU cores

-Adjustable memory consumption

-simple setup

-tested against a know wallet and seed address successfully.

How it works:
Once the python script is run, it will read candidate words from the 12 input files and start generating batches of different permutations of the words supplied. It will rearrange the words based on the order constant set in the code. It will take each candidate seed phrase and do a checksum to weed out invalid seeds. If the seed is valid, then it continues to do the wallet derivation process where the output is a wallet address. It then check the wallet address derived against the target wallet address and writes that to the console allong with the matching seed. If that happens, you now have the seed for that target wallet.  

Why did I make this?
As part of a treasure hunt to recover a bitcoin wallet. Part of the puzzle involved 12 chapters each with hints to 1 of 12 seed words. The discovered chapter words would need to be arronged in a different order (which was another puzzle). The author didnt build in easy to very solutions so I had 8-10 words per chapter that could be the valid seed words. So, I wrote those try try all those options fast.

**********************
A word on realisticly finding a seed phrase:

BIP39 was made to make it unreasonable to try and bruteforce private keys. So this is only useful if you have a partial seed, not a completely unknown one.

To run all permutations in a reasonable time, you need to see how many possible word arrangements there would be. so in the case that I knew 6 words, but had a short list of 8 words for the remaining 6, the math is: 1x1x1x1x1x1x8x8x8x8x8x8 = 8^6 = 262,144 arrangments....this will finish in seconds. However, there are 2048 words options for each seed word so if you have no idea on some word slots, its still doable but you have to check the math first. realistically you could get away with 2 or 3 words with that situation. Example: 1x1x1x1x1x1x8x8x8x8x2048x2048 = ~17 billion arrangements. On a later model 16 core cpu, that will take a couple/few days. Anything a trillion or beyond starts to become unrealistic to solve with a single CPU in under a month. And hope automatic system updates dont reboot you 5 days in =P
***********************

Prereqs:
-Python 3 (I used 3.12.9 during the development of this.
-BIP-utils Python library
-itertools Python library

Ive run this on both Windows and Ubuntu Linux with no issues.

Setup Instructions:
1) Install Python
2) Have a IDE or Text Editor that can read Python code nicely (Notepad++ is fine...)
3) Once Python is installed, install the libraries using pip (or pip3):
   pip install bip-utils
   pip install itertools
4) Open bf-cpu.py on the ide or text editor
5) Set the Constants:
   Target_address: This is the address of the wallet you are trying to crack

   Max_Combos_Per_Batch: Adjust this based on how much RAM you have. 100,000,000 consumes about 32-33
   GB of RAM. So if you had only 16 GB, set it to maybe 40,000,000. Launch it and then cancel and
   adjust. What you dont want is it using all of your RAM and then starting to utilize swap space on
   you hard drive because that can really slow things down.

   Order: if the input files are in the right order, then leave it as is, other wise you can specify a
   difference word order. This was only useful for the puzzle I was trying to solve.
6) SAVE THE FILE.
7) Make sure input1.txt - input12.txt are in the same directory as the python file.
8) If you know a word for a specific slot, simply add the word to the appropriate text file by itself.
9) For seed words you are unsure of, past in a list of BIP39 seed words with one word per row. Examples
   given in the default lists.

10) RUN IT. From a command line, browse to the folder with the files, and type: python bf-cpu.py

Your CPU will be 100% consumed. As a precaution, monitor CPU temperatures to make sure your fans are cooling it properly. a properly cooled CPU should not get above 75 degrees celcius. 90 is the danger zone where you are definitly risking permanent damage to the CPU. Do not use this if your cooling is insufficient. I am not responsible for overheating machines. 
