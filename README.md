Window Python Script

-Uses biopython version 1.81

-This script takes a consensus FASTA file of at least two sequences.  
- The script will report the number of differences between the sequences within the 'Window'
- You are required to specify the consensus fasta file with the -a, --alignment argument. 
- The "Window" is the number of basepairs that will be examined for differences. You specify the size of the window with -w, or --window.
- The "Step" variable is the number of basepairs the window will slide up the sequence. You specifcy the step of the window with -s, or --step.
- If you set window and step for 10 the output will show the differences for every 10 base pairs.

Test files are included with the repository. Here is an example command to run the script:  
python Window.py -a TEST.fasta -w 10 -s 10



Help command python Window.py -h
