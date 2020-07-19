Filtering based on pyVCF filters described here: 
    https://pyvcf.readthedocs.io/en/latest/FILTERS.html#adding-a-filter

3 filters implemented here:
* AF (allele frequency) filter
* Consequence filter
* dbSnP filter with cosmic and clinvar rescue

All 3 filters rely on VCF annotation provided by VEP annotation
