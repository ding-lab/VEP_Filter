
OUTD="output"
mkdir -p $OUTD

#VCF="/data/call-vep_annotate/execution/results/vep/output_vep.vcf"
# Testing on ClinVar-annotated VCF
#VCF="/data/ClinVar/output_vep.vcf"
BASE="/data/TinDaisy2/run5"
VCF="$BASE/call-dbsnp_filter/inputs/-874954319/classification_filter.output.vcf"

OUT="$OUTD/C3L-00908.CV.id.vcf"

CMD="bash ../../src/run_dbsnp_filter.sh $@ -o $OUT -I all -l -c $VCF "
>&2 echo Running : $CMD
eval $CMD


----

# From run5/call-dbsnp_filter/execution/script,
# '/bin/bash' '/opt/VEP_Filter/src/run_dbsnp_filter.sh' '-o' 'dbsnp_filter.output.vcf' '-I' 'all' '-l' '-c' '/cromwell-executions/tindaisy2-restart_postcall.cwl/5281f45b-ae70-473b-abc6-64d445ccfe11/call-dbsnp_filter/inputs/-874954319/classification_filter.output.vcf'


