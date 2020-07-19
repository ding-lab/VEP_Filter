Currently testing on katmai, with test data on /home/mwyczalk_test/Projects/GermlineCaller/C3L-00001

To start, do,

bash ./0_start_docker.sh /home/mwyczalk_test/Projects/GermlineCaller/C3L-00001

TODO: provide test data which can be distributed (1000 Genomes?)

Testing the following filters:
* `vaf_filter` - Filters VCF files according to tumor, normal VAF values
  * `/opt/VLD_FilterVCF/src/vaf_filter.py`
  * GATK implemented
* `length_filter` - Filters VCF files according to indel length:
  * `/opt/VLD_FilterVCF/src/length_filter.py`
  * does not have caller argument
* `depth_filter` - Filters VCF files according to tumor, normal read depth
  * `/opt/VLD_FilterVCF/src/depth_filter.py`
  * GATK is calculated same way as mutect
* `allele_depth_filter` - Filters VCF files according to allelic depth for alternate allele
  * `/opt/VLD_FilterVCF/src/allele_depth_filter.py`
  * has "VCF" or "varscan" as caller, and handling of remapped varscan is described

Each of these will be tested with script `src/run_vaf_length_depth_filters.sh` on the following datasets:
* GATK
  * `/data/GATK.indel.Final.vcf`
  * `/data/GATK.snp.Final.vcf`
* varscan
  * `/data/varscan_remapped/varscan.indel.vcf-remapped.vcf`
  * `/data/varscan_remapped/varscan.snp.vcf-remapped.vcf`
* pindel
  * `/data/pindel_sifted.out.CvgVafStrand_pass.Homopolymer_pass.vcf`

## Errors running

Errors like this, indicative of a Python 2 / 3 issue:
```
root@6d4a076576a2:/opt/VEP_Filter/testing/direct_call# bash 1_run_af_filter.sh
[ Sun Jul 19 22:48:04 UTC 2020 ] Running: mkdir -p output
[ Sun Jul 19 22:48:04 UTC 2020 ] Completed successfully
[ Sun Jul 19 22:48:04 UTC 2020 ] Running: /usr/local/bin/vcf_filter.py --local-script af_filter.py /data/testing/demo_data-local/C3L-00908.output_vep.vcf af --config /data/params/af_filter_config.ini --input_vcf /data/testing/demo_data-local/C3L-00908.output_vep.vcf
Traceback (most recent call last):
  File "/usr/local/bin/vcf_filter.py", line 168, in <module>
    if __name__ == '__main__': main()
  File "/usr/local/bin/vcf_filter.py", line 129, in main
    inp = vcf.Reader(args.input)
  File "/usr/local/lib/python3.8/site-packages/vcf/parser.py", line 300, in __init__
    self._parse_metainfo()
  File "/usr/local/lib/python3.8/site-packages/vcf/parser.py", line 318, in _parse_metainfo
    while line.startswith('##'):
TypeError: startswith first arg must be bytes or a tuple of bytes, not str
[ Sun Jul 19 22:48:05 UTC 2020 ] run_af_filter.sh Fatal ERROR. Exiting.
```

### TinDaisy 
```
docker run -it "mwyczalkowski/tindaisy-core:20191108" bash
# /usr/bin/python --version
Python 2.7.12
```

### VEP_Filter
```
# python --version
Python 3.8.3
```

How did `VLD_FilterVCF` deal with this?

###  VLD_FilterVCF
Python is also 3.8.3

