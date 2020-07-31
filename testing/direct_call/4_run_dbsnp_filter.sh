
OUTD="output"
mkdir -p $OUTD

VCF="/data/call-vep_annotate/execution/results/vep/output_vep.vcf"

# NOTE: C3L-00908 does not have ClinVar CSQ option, so clinvar rescue is not available
OUT="$OUTD/C3L-00908.dbSnP.vcf"

#RESCUE="-c -l"
RESCUE="-c"

# will add ID and use cosmic, clinvar rescue
CMD="bash ../../src/run_dbsnp_filter.sh $@ $RESCUE -I all $ARG -o $OUT $VCF "
>&2 echo Running : $CMD
eval $CMD


