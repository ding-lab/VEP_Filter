
OUTD="output"
mkdir -p $OUTD

#VCF="/data/call-vep_annotate/execution/results/vep/output_vep.vcf"
# Testing on ClinVar-annotated VCF
VCF="/data/ClinVar/output_vep.vcf"
CONFIG="/params/af_filter_config.ini"

OUT="$OUTD/C3L-00908.CV.af.vcf"

CMD="bash ../../src/run_af_filter.sh $@ $ARG -o $OUT $VCF $CONFIG"
>&2 echo Running : $CMD
eval $CMD

