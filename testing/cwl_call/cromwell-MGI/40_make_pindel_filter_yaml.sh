# Creates YAML file based on output from pindel_caller run
# Usage: 40_make_pindel_filter_yaml.sh DAT
#  where DAT is the output of pindel_caller, i.e., XXX/pindel_sifted.out

DAT=$1

# this template is appropriate for CPTAC3 hg38 data
# For demo use pindel_filter_demo.template.yaml
TEMPLATE="../yaml/pindel_filter_hg38.template.yaml"

if [ -z $DAT ]; then
    >&2 echo ERROR: please pass DAT file
    exit 1
fi
if [ ! -e $DAT ]; then
    >&2 echo ERROR: $DAT does not exist
    exit 1
fi

OUTD="yaml.generated"
mkdir -p $OUTD
OUT="$OUTD/pindel_filter.yaml"

bash ../cromwell.resources/make_yaml.sh $TEMPLATE $DAT > $OUT

>&2 echo Written to $OUT

#/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions/pindel_caller.Pindel_GermlineCaller.cwl/c2390a04-736f-4765-8172-d2cf9ac7e982/call-pindel_caller.Pindel_GermlineCaller.cwl/execution/output/pindel_sifted.out
