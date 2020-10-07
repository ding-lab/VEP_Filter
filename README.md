# VEP_Filter

Series of TinDaisy modules for filtering VCF files based on attributes from VEP annotation.

Filtering based on pyVCF filters as described [here](https://pyvcf.readthedocs.io/en/latest/FILTERS.html#adding-a-filter)

3 filters implemented:

* AF (allele frequency) filter
* Consequence filter
* dbSnP filter with cosmic and clinvar rescue

All 3 filters rely on VCF annotation provided by VEP annotation

## Installation

`VEP_Filter` is typically installed as a submodule within TinDaisy.  However, an
independent copy can be cloned from GitHub with,
```
git clone --recurse-submodules https://github.com/ding-lab/VEP_Filter.git
```

## Input

Describe configuration files

VEP custom annotation used for ClinVar rescue.  Require custom_filename and custom_args
Described here: http://uswest.ensembl.org/info/docs/tools/vep/script/vep_custom.html

Clinvar database (argument for custom_filename) can be obtained from e.g., 
    ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/

Argument passed to VEP is then,
    --custom $custom_filename,$custom_args

## Testing



## Contact

Matt Wyczalkowski (m.wyczalkowski@wustl.edu)


