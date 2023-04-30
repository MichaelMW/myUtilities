#!/usr/bin/env python
# encoding: utf-8

import pysam
import sys

def gc_content(seq):
	seq = seq.upper()
	valid_bases = {'A', 'T', 'G', 'C'}
	valid_seq = ''.join([base for base in seq if base in valid_bases])
	gc_count = valid_seq.count("G") + valid_seq.count("C")
	if len(valid_seq) == 0:
		return 0
	return gc_count / len(seq)

def add_gc_content_to_bed(bed_filename, reference_filename, output_filename):
	reference = pysam.FastaFile(reference_filename)

	with open(bed_filename, "r") as bed_file, open(output_filename, "w") as output_file:
		for line in bed_file:
			ls = line.strip().split("\t")
			chrom, start, end = ls[0], ls[1], ls[2]
			start, end = int(start), int(end)
			seq = reference.fetch(chrom, start, end)
			gc = gc_content(seq)
			output_file.write(f"{chrom}\t{start}\t{end}\t{gc}\n")

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: python add_gc_content.py <input_bed> <reference_genome> <output_bed>")
	else:
		input_bed = sys.argv[1]
		reference_genome = sys.argv[2]
		output_bed = sys.argv[3]

		add_gc_content_to_bed(input_bed, reference_genome, output_bed)

