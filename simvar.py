#!/usr/bin/env python3.6

import click
import pybedtools
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
@click.option('-o', '--out', 'output_file', required=True, help='an ouptput file name',
              type=click.Path(exists=False, readable=True, resolve_path=True))

@click.command()
def main(bed_file, ref_file, output_file):
    """Simple program that generate the universe of variants for given genomic location."""

    # Convert the given BED file to FASTA file using pybedtools
    fasta_data = bed_to_fasta(bed_file, ref_file)

    # Generate text file with all the possible variants
    variants = parse_fasta(fasta_data)

    # generate variants
    all_variants = generate_variants(variants)

    # print the variants to the file
    print_variants(all_variants, output_file)

def bed_to_fasta(bed_file, ref_file):
    """
    Covert the given data in BED format to a FASTA format

    Args:
        bed_file (path): a BED file containing all the genomic regions
        ref_file (path): a reference genome file in FASTA format

    Returns:
        str: FASTA data as string
    """

    # Create BED file object
    bed_data = pybedtools.BedTool(fn=bed_file)

    # Create FASTA file object
    ref_fa_data = pybedtools.example_filename(fn=ref_file)

    # Convert the BED to FASTA format
    fasta_data = bed_data.sequence(fi=ref_fa_data)

    # Read the converted FASTA data
    fa_data = (open(fasta_data.seqfn).read())

    return fa_data

def parse_fasta(fasta_data):
    """
    Parse a given FASTA file and generate possible variants

    Args:
        fasta_data (str): FASTA data as string

    Returns:
        variants (list): a list of variants
    """

    # placeholder to store variants
    variants = list()

    # split the fasta data based on new line character
    fa_data = fasta_data.strip().split('\n')

    # loop through header and sequence at the same time
    for header, sequence in zip(fa_data[0::2], fa_data[1::2]):

        # get genomic region information from header
        chrom, pos = header.split(':')

        # remove the '>' from the chromosome
        chrom = chrom.replace('>', '')

        # get start and end pos of a genomic region
        start_pos, end_pos = pos.split("-")
        start_pos = int(start_pos)
        end_pos = int(end_pos)

        # list to hold genomic positions
        pos_list = list(range(start_pos, end_pos, 1))
        seq_list = list(sequence)

        for p, s in zip(pos_list, seq_list):

            # place holder dict to store the variant information
            variant = dict()

            # add chromosome in the variants dict
            variant['chr'] = chrom
            variant['start'] = p
            variant['end'] = p
            variant['ref'] = s
            variant['alt'] = MUTATION_UNIVERSE[s]

            # append to a variants list
            variants.append(variant)

    return variants

def generate_variants(variants):
    """
    Generate possible variants from a given variants list

    Args:
        variants (list): a list of a variants containing variant information

    Returns:
        var_info_list (list): a list of possible variants for a given position
    """

    # a list to hold variants information
    all_variants = list()

    # create a list of variants
    for variant in variants:
        for alt_allele in variant['alt']:
            all_variants.append([variant['chr'], str(variant['start']), str(variant['end']), variant['ref'],
                                 alt_allele])

    return all_variants

def print_variants(variants, output_file):
    """
    Print variants to a file

    Args:
        variants (list): a list of possible variants for a given position
        output_file (path): a path to an output variant file
    """

    # create the Path file object
    output_file_obj = Path(output_file)

    # loop over the variants and print them to a file
    for variant in variants:

        # check the existence of the output file
        if not output_file_obj.is_file():
            header = ','.join(["chr", "start", "end", "ref", "alt"])
            with open(output_file, 'w') as ofh:
                variant_info = ','.join(variant)
                ofh.write(header + "\n")
                ofh.write(variant_info + "\n")
        else:
            with open(output_file, 'a') as ofh:
                variant_info = ','.join(variant)
                ofh.write(variant_info + "\n")

if __name__ == '__main__':
    main()
