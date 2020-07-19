# VLD_FilterVCF

A series of VCF filters which exclude calls based on specific criteria.  The filters are,
* vaf_filter - Filters VCF files according to tumor, normal VAF values
* length_filter - Filters VCF files according to indel length:
* depth_filter - Filters VCF files according to tumor, normal read depth
* AD_filter - Filters VCF files according to allelic depth for alternate allele

Note that varscan VCFs must first pass through a remapping to normalize AD and RD fields.
See https://github.com/ding-lab/varscan_vcf_remap.git

Code based on https://github.com/ding-lab/TinDaisy-Core  TinDaisy-Core/src/vcf_filters

## Installation

Uses `start_docker.sh` from [WUDocker](https://github.com/ding-lab/WUDocker.git)
Obtain with,
```
git clone https://github.com/ding-lab/WUDocker.git
```

## Contact

Matt Wyczalkowski (m.wyczalkowski@wustl.edu)


