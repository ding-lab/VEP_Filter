Filtering based on pyVCF filters described here: 
    https://pyvcf.readthedocs.io/en/latest/FILTERS.html#adding-a-filter

3 filters implemented here:
* AF (allele frequency) filter
* Consequence filter
* dbSnP filter with cosmic and clinvar rescue

All 3 filters rely on VCF annotation provided by VEP annotation

## Development notes

Filters in [VLD_FilterVCF][1] are closely based on those here
These projects could in fact be merged, since both use same python libraries
(principal difference is that VEP Filter parses CSQ fields)

[1]: https://github.com/ding-lab/VLD_FilterVCF.git
