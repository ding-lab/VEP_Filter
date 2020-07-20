
OUTD="output"
mkdir -p $OUTD

VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"

OUT="$OUTD/C3L-00908.dbSnP"

bash ../../src/run_dbsnp_filter.sh $@ $ARG -o $OUT $VCF 

