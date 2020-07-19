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
