# SimVar [**alpha** version]

**Sim**ulate **Var**iants for provided genomic coordinates

# Description

`SimVar` - a tool that can simulate the variants for a given genomic location/s.

# Pre-requisites

* `bedtools2` [Add bedtools link here]
* `Python 3.6` or greater version [Add python3.6 link here]

## Dependencies

Required `Pyhton3.6` modules

* `click`
* `pybedtools` 

# Input

* `BED` file with all the genomic coordinates of interest
* `Reference Genome` file in `FASTA` format

# Output

Variant file in `TXT` format containing the following columns:

* `CHR` - chromosome name
* `START_POS` - Start position
* `END_POS` - End position
* `REF` - Reference allele
* `ALT` - Alternate allele

# License

Copyright &copy; Tushar Dave