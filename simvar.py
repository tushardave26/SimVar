#!/usr/bin/env python3.6

import click
import pysam
import sys
from pathlib import Path

MUTATION_UNIVERSE = {
    'A': ['T', 'C', 'G'],
    'T': ['A', 'C', 'G'],
    'G': ['A', 'C', 'T'],
    'C': ['T', 'A', 'G'],
}

@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)

@click.option('-b', '--bed', 'bed_file', required=True, help='BED file containing the genomic location',
              type=click.Path(exists=True, readable=True, resolve_path=True))
@click.option('-r', '--ref', 'ref_file', required=True, help='Reference genome file in FASTA format',
              type=click.Path(exists=True, readable=True, resolve_path=True))
@click.option('-i', '--ref-idx', 'ref_idx_file', required=True, help='Index file for reference genome',
              type=click.Path(exists=True, readable=True, resolve_path=True))
@click.option('-o', '--out', 'output_file', required=False, default=sys.stdout, help='an ouptput file name [default: '
                                                                                     'STDOUT]',
              type=click.Path(exists=False, readable=True, resolve_path=True))

@click.command()
def main(bed_file, ref_file, ref_idx_file, output_file):
    """Simple program that generate the universe of variants for given genomic location."""

    # create pysam object to read FASTA file
    fasta_file = pysam.FastaFile(ref_file, ref_idx_file)

    # create the Path file object
    output_file_obj = Path(output_file)

    # if the output file exists, remove it and create it again to avoid file existence issue
    if output_file_obj.is_file():
        output_file_obj.unlink()

    # header for the output file
    header = ','.join(["chr", "start", "end", "ref", "alt"])

    # open the output file to write the header
    with open(output_file, 'w') as ofh:
        ofh.write(header + "\n")

        # Extract the fasta sequence for a given region and process it
        with open(bed_file, "r") as bed:

            # iterate over the BED file
            for region in bed:

                # extract the required information from BED file
                chrom, start, end, gene = region.strip().split('\t')

                # convert start and end positions to int
                start = int(start)
                end = int(end)

                # fetch the sequence for given genomic region
                try:
                    fetch_seq = fasta_file.fetch(reference = chrom, start = start, end = end)
                except KeyError as e:
                    print(str(e))
                    continue

                # iterate through region and sequence to generate possible variants
                for index, base in enumerate(fetch_seq):

                    # iterate throght all possible alt alleles
                    for alt_allele in MUTATION_UNIVERSE[base]:
                        ofh.write(",".join([chrom, str(start + index), str(start + index), base, alt_allele]) + "\n")

if __name__ == '__main__':
    main()
