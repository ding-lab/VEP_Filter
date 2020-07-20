
OUTD="output"
mkdir -p $OUTD

#VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"
#VCF="/data/testing/demo_data-local/C3L-00908.test-very-short.vcf"
VCF="/data/testing/demo_data-local/C3L-00908.test-short.vcf"

OUT="$OUTD/C3L-00908.id.vcf"

bash ../../src/run_dbsnp_filter.sh $@ -o $OUT -I all -E $VCF 

