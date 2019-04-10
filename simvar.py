#!/usr/bin/env python3.6

import click
import pysam
import sys
import logging
import re
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

    # get the logger to log the progress of the program
    logger = configure_logging()

    logger.info(msg="Generate pysam FASTA file object - Start")

    # create pysam object to read FASTA file
    fasta_file = pysam.FastaFile(ref_file, ref_idx_file)

    logger.info(msg="Generate pysam FASTA file object - Complete")

    logger.info(msg="Check the output file existence - Start")

    # create the Path file object
    output_file_obj = Path(output_file)

    # if the output file exists, remove it and create it again to avoid file existence issue
    if output_file_obj.is_file():

        logger.info(msg="Provided output file exists, removing the output file - Start")

        output_file_obj.unlink()

        logger.info(msg="Removal of the output file - Complete")

    logger.info(msg="Check the output file existence - Complete")

    # header for the output file
    header = ','.join(["chr", "start", "end", "ref", "alt"])

    logger.info(msg="Open the output file to write the variants..")

    # open the output file to write the header
    with open(output_file, 'w') as ofh:

        logger.info(msg="Print the header information in the output file..")

        ofh.write(header + "\n")

        # Extract the fasta sequence for a given region and process it
        with open(bed_file, "r") as bed:

            logger.info(msg="Reading and processing of genomic regions - Start")

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

                    pattern = re.compile('\'(.+)\'')

                    e = pattern.search(str(e)).group()

                    logger.warning(msg=f'Genomic region {e} not found in reference genome')
                    logger.info(msg=f'Skipping the region {e}')

                    continue

                # iterate through region and sequence to generate possible variants
                for index, base in enumerate(fetch_seq):

                    # iterate throght all possible alt alleles
                    for alt_allele in MUTATION_UNIVERSE[base]:
                        ofh.write(",".join([chrom, str(start + index), str(start + index), base, alt_allele]) + "\n")

            logger.info(msg="Reading and processing of genomic regions - Complete")

            logger.info(msg="Procee Complete!!!")

def configure_logging():

    # Configure the logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)

    # Create a custom logger
    logger = logging.getLogger("SimVar")

    return logger

if __name__ == '__main__':
    main()
