Window Python Script

-Uses biopython version 1.81

-This script takes a consensus FASTA file of at least two sequences.  
- The script will report the number of differences between the sequences within the 'Window'
- The Window is the number of basepairs that will be examined for differences. You specify the size of the window with -w, or --window.
- The is how many basepairs the window will slide up the sequence. You specifcy the step of the window with -s, or --step.
- If you set window and step for 10 the output will show the differences for every 10 base pairs.



Help command python Window.py -h
