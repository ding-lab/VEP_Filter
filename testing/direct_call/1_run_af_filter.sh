
OUTD="output"
mkdir -p $OUTD

VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"
CONFIG="/data/params/af_filter_config.ini"

OUT="$OUTD/C3L-00908.af.vcf"

bash ../../src/run_af_filter.sh $@ $ARG -o $OUT $VCF $CONFIG

