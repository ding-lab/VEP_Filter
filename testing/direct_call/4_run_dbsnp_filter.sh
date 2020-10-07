
OUTD="output"
mkdir -p $OUTD

#VCF="/data/call-vep_annotate/execution/results/vep/output_vep.vcf"
# Testing on ClinVar-annotated VCF
VCF="/data/ClinVar/output_vep.vcf"

# NOTE: C3L-00908 now does have ClinVar CSQ option, so clinvar rescue is available
OUT="$OUTD/C3L-00908.CV.dbSnP.vcf"

RESCUE="-c -l"
#RESCUE="-c"

# will add ID and use cosmic, clinvar rescue
CMD="bash ../../src/run_dbsnp_filter.sh $@ $RESCUE -I all $ARG -o $OUT $VCF "
>&2 echo Running : $CMD
eval $CMD


