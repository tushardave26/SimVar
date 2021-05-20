# SimVar [**alpha** version]

**Sim**ulate **Var**iants for provided genomic coordinates

# Description

`SimVar` - a tool that can simulate the variants for a given genomic location/s.

# Pre-requisites

* `Python 3.6` or greater version [Add python3.6 link here]

## Dependencies

Required `Pyhton3.6` modules

* `click-7.0`
* `pysam-0.15.2` 

# Input

* `BED` file with all the genomic coordinates of interest
* `Reference Genome` file in `FASTA` format
* `Reference Genome Index` file (i.e. `fai`)

# Output

Variant file in `CSV` format containing the following columns:

* `chr` - chromosome name
* `start` - Start position
* `end` - End position
* `ref` - Reference allele
* `alt` - Alternate allele

# Usage

```bash
$ ./simvar.py --help
Usage: simvar.py [OPTIONS]

  Simple program that generate the universe of variants for given genomic
  location.

Options:
  -o, --out PATH      an ouptput file name [default: STDOUT]
  -i, --ref-idx PATH  Index file for reference genome  [required]
  -r, --ref PATH      Reference genome file in FASTA format  [required]
  -b, --bed PATH      BED file containing the genomic location  [required]
  --help              Show this message and exit.
```
# License

Copyright &copy; 2019-2021 Tushar Dave
