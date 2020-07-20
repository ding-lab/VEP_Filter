#/bin/bash

read -r -d '' USAGE_CLASS <<'EOF'
Run allele frequency filters on a VCF 

Usage:
  bash run_dbsnp_filter.sh [options] VCF

Options:
-h: Print this help message
-d: Dry run - output commands but do not execute them
-o OUT_VCF: Output VCF.  Default writes to STDOUT
-e: filter debug mode
-E: filter bypass
-R: remove filtered variants.  Default is to retain filtered variants with filter name in VCF FILTER field
-I ID_POLICY: Add variant ID to VCF ID field.  Permitted values:
    'dbsnp' add dbsnp ID only
    'all' add IDs, including ClinVar if available
    'none' - do not modify ID field
-c: rescue variants which appear in COSMIC
-l: rescue variants which appear in ClinVar

VCF is input VCF file
...
EOF

FILTER_SCRIPT="dbsnp_filter.py"  # filter module
FILTER_NAME="dbsnp"
USAGE="$USAGE_DBSNP"

### aim is to have all filter-specific details above

# No provision is made for executing multiple consequtive filters using UNIX pipes
# (e.g., cmd1 | cmd2).  See https://github.com/ding-lab/VLD_FilterVCF for example of pipes

# call format
# cat VCF | vcf_filter.py CMD_ARGS --local-script FILTER_SCRIPT - $FILTER_NAME $FILTER_ARGS $CONFIG
# filter description: https://pyvcf.readthedocs.io/en/latest/FILTERS.html#adding-a-filter

source /opt/VEP_Filter/src/utils.sh
SCRIPT=$(basename $0)

PYTHON_BIN="/usr/local/bin/python"

export PYTHONPATH="/opt/VEP_Filter/src/python:$PYTHONPATH"
OUT_VCF="-"
ID_POLICY="none"

# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":hdo:eERI:cl" opt; do
  case $opt in
    h)
      echo "$USAGE"
      exit 0
      ;;
    d)  # binary argument
      DRYRUN=1
      ;;
    o)
      OUT_VCF="$OPTARG"
      ;;
    e)
      FILTER_ARGS="$FILTER_ARGS --debug"
      ID_ARGS="$ID_ARGS --debug"
      ;;
    E)
      FILTER_ARGS="$FILTER_ARGS --bypass"
      ;;
    R)
      CMD_ARGS="--no-filtered"
      ;;
    I)
      ID_POLICY="$OPTARG"
      ;;
    c)
      FILTER_ARGS="$FILTER_ARGS -c"
      ;;
    l)
      FILTER_ARGS="$FILTER_ARGS -l"
      ;;
    \?)
      >&2 echo "Invalid option: -$OPTARG"
      >&2 echo "$USAGE"
      exit 1
      ;;
    :)
      >&2 echo "Option -$OPTARG requires an argument."
      >&2 echo "$USAGE"
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

if [ "$#" -ne 1 ]; then
    >&2 echo Error: Wrong number of arguments
    >&2 echo "$USAGE"
    exit 1
fi

VCF=$1 ; confirm $VCF

# Create output paths if necessary
if [ $OUT_VCF != "-" ]; then
    OUTD=$(dirname $OUT_VCF)
    run_cmd "mkdir -p $OUTD" $DRYRUN
fi

if [[ $ID_POLICY == "dbsnp" || $ID_POLICY == "all" ]]; then
# for simplicity for now, require that OUT_VCF is a file if modifying ID field
# This can be relaxed in the future by making a temp dir or using pipes
    if [ -z $OUTD ]; then
        >&2 echo "ERROR: currently require OUT_VCF be specified when modifying ID field"
        exit 1 
    fi
    TMP_VCF="$OUTD/add_id.tmp.vcf"
    CMD="$PYTHON_BIN /opt/VEP_Filter/src/python/vcf_add_VEP_ID.py $ID_ARGS -i $VCF -o $TMP_VCF -I $ID_POLICY"
    run_cmd "$CMD" $DRYRUN

    VCF="$TMP_VCF"
elif [ $ID_POLICY == "none" ]; then
    :
else
    >&2 echo "ERROR: unknown ID_POLICY $ID_POLICY"
    exit 1
fi
    
# "cat VCF | vcf_filter.py" avoids weird errors

FILTER_CMD="cat $VCF |  /usr/local/bin/vcf_filter.py $CMD_ARGS --local-script $FILTER_SCRIPT - $FILTER_NAME" # filter module
CMD="$FILTER_CMD $FILTER_ARGS --input_vcf $VCF"
    
if [ $OUT_VCF != "-" ]; then
    CMD="$CMD > $OUT_VCF"
fi

run_cmd "$CMD" $DRYRUN

if [ $OUT_VCF != "-" ]; then
    >&2 echo Written to $OUT_VCF
fi

