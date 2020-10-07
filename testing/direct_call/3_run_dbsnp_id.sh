
OUTD="output"
mkdir -p $OUTD

#VCF="/data/call-vep_annotate/execution/results/vep/output_vep.vcf"
# Testing on ClinVar-annotated VCF
VCF="/data/ClinVar/output_vep.vcf"

OUT="$OUTD/C3L-00908.CV.id.vcf"

CMD="bash ../../src/run_dbsnp_filter.sh $@ -o $OUT -I all -E $VCF "
>&2 echo Running : $CMD
eval $CMD


