
OUTD="output"
mkdir -p $OUTD

#VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"
VCF="/data/testing/demo_data-local/C3L-00908.test-short.vcf"

OUT="$OUTD/C3L-00908.dbSnP.vcf"

# will add ID and use cosmic, clinvar rescue
bash ../../src/run_dbsnp_filter.sh $@ -cl -I all $ARG -o $OUT $VCF 

