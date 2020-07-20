
OUTD="output"
mkdir -p $OUTD

VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"
CONFIG="/data/params/classification_filter_config.ini"

OUT="$OUTD/C3L-00908.classification.vcf"

bash ../../src/run_classification_filter.sh $@ $ARG -o $OUT $VCF $CONFIG

