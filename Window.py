#!/usr/bin/env python
"""
Get the number of AA differences in a window across an amino acid alignment
"""
import os
import sys
from sys import argv
import optparse
from optparse import OptionParser
try:
    from Bio import SeqIO
except:
    print("Biopython is not installed but needs to be...exiting")
    sys.exit()
from collections import Counter

def test_file(option, opt_str, value, parser):
    try:
        with open(value): setattr(parser.values, option.dest, value)
    except IOError:
        print('%s cannot be opened' % option)
        sys.exit()

def create_range_file(alignment, window, step):
    lengths = []
    # The range file will help look for SNPs in windows
    range_file = open("range_file.tsv", "w")
    for record in SeqIO.parse(alignment, "fasta"):
        lengths.append(len(record.seq))
    my_length = lengths[0]
    for i in range(0, my_length, step):
        end = min(i + window - 1, my_length - 1)
        range_file.write(str(i) + "\t" + str(end) + "\n")
    range_file.close()

def invert_tabs(in_tab, start, end):
    outfile = open(f"{start}.{end}.inverted.xyx", "w")
    fields = []
    with open(in_tab) as infile:
        for line in infile:
            my_fields = line.split()
            tmp_fields = [my_fields[0]] + list(my_fields[1])
            fields.append(tmp_fields)
    test = list(map(list, zip(*fields)))
    names = [x for x in test[0]]
    for x in test:
        outfile.write("\t".join(x) + "\n")
    outfile.close()

def parse_fasta_file(alignment, range_file, output_file):
    with open(output_file, "w") as out_f:
        for line in open(range_file):
            fields = line.split()
            start = int(fields[0])
            end = int(fields[1])
            outfile = open(f"{start}.{end}.tab.xyx", "w")
            with open(alignment) as my_fasta:
                for record in SeqIO.parse(my_fasta, "fasta"):
                    query_seq = record.seq[start:end+1]
                    outfile.write(f"{record.id}\t{query_seq}\n")
            outfile.close()
            # Now I need to create yet another file and count the number of SNPs
            invert_tabs(f"{start}.{end}.tab.xyx", start, end)
            # Let's remove the file that I no longer need
            os.system(f"rm {start}.{end}.tab.xyx")
            with open(f"{start}.{end}.inverted.xyx") as my_tab:
                snp = []
                line = my_tab.readline()
                for line in my_tab:
                    differences = []
                    fields = line.split()
                    num_samples = len(fields)
                    my_counter = Counter(fields)
                    for count in my_counter.items():
                        if int(count[1]) == num_samples:
                            pass
                        else:
                            differences.append("1")
                    if len(differences) > 0:
                        snp.append("1")
                result = f"{start+1}-{end+1}: {len(snp)}\n"
                print(result.strip())
                out_f.write(result)
            os.system(f"rm {start}.{end}.inverted.xyx")

def main(alignment, window, step, output_file):
    create_range_file(alignment, window, step)
    parse_fasta_file(alignment, "range_file.tsv", output_file)
    os.system("rm range_file.tsv")

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 0.0.1")
    parser.add_option("-a", "--alignment", dest="alignment",
                      help="path to AA alignment [REQUIRED]",
                      type="string", action="callback", callback=test_file)
    parser.add_option("-w", "--window", dest="window",
                      help="size of AA window; defaults to 10",
                      type="int", action="store", default=10)
    parser.add_option("-s", "--step", dest="step",
                      help="step size for moving the window; defaults to 2",
                      type="int", action="store", default=2)
    parser.add_option("-o", "--output", dest="output_file",
                      help="path to the output file [REQUIRED]",
                      type="string", action="store")
    options, args = parser.parse_args()
    mandatories = ["alignment", "output_file"]
    for m in mandatories:
        if not getattr(options, m, None):
            print(f"\nMust provide {m}.\n")
            parser.print_help()
            exit(-1)
    main(options.alignment, options.window, options.step, options.output_file)
