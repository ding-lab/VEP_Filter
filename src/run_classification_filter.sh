#/bin/bash

read -r -d '' USAGE_CLASS <<'EOF'
Run allele frequency filters on a VCF 

Usage:
  bash run_classification_filter.sh [options] VCF CONFIG_FN

Options:
-h: Print this help message
-d: Dry run - output commands but do not execute them
-o OUT_VCF: Output VCF.  Default writes to STDOUT
-O TMPD: Directory for intermediate output, used when -N specified. Default: ./output
-e: filter debug mode
-E: filter bypass
-R: remove filtered variants.  Default is to retain filtered variants with filter name in VCF FILTER field

VCF is input VCF file
CONFIG_FN is configuration file with `af` section
...
EOF

FILTER_SCRIPT="classification_filter.py"  # filter module
FILTER_NAME="classification"
USAGE="$USAGE_CLASS"

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
TMPD="./output"

# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":hdO:o:eER" opt; do
  case $opt in
    h)
      echo "$USAGE"
      exit 0
      ;;
    d)  # binary argument
      DRYRUN=1
      ;;
    O)
      TMPD="$OPTARG"
      ;;
    o)
      OUT_VCF="$OPTARG"
      ;;
    e)
      FILTER_ARGS="$FILTER_ARGS --debug"
      ;;
    E)
      FILTER_ARGS="$FILTER_ARGS --bypass"
      ;;
    R)
      CMD_ARGS="--no-filtered"
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

if [ "$#" -ne 2 ]; then
    >&2 echo Error: Wrong number of arguments
    >&2 echo "$USAGE"
    exit 1
fi

VCF=$1 ; confirm $VCF
CONFIG_FN=$2 ; confirm $CONFIG_FN



# Create output paths if necessary
if [ $OUT_VCF != "-" ]; then
    OUTD=$(dirname $OUT_VCF)
    run_cmd "mkdir -p $OUTD" $DRYRUN
fi
if [ "$NO_PIPE" ]; then
    run_cmd "mkdir -p $TMPD" $DRYRUN
fi    

# Common configuration file is used for all filters
CONFIG="--config $CONFIG_FN"


# `cat VCF | vcf_filter.py` avoids weird errors
FILTER_CMD="cat $VCF |  /usr/local/bin/vcf_filter.py $CMD_ARGS --local-script $FILTER_SCRIPT - $FILTER_NAME" # filter module
CMD="$FILTER_CMD  $FILTER_ARGS $CONFIG --input_vcf $VCF"
    
if [ $OUT_VCF != "-" ]; then
    CMD="$CMD > $OUT_VCF"
fi

run_cmd "$CMD" $DRYRUN

if [ $OUT_VCF != "-" ]; then
    >&2 echo Written to $OUT_VCF
fi

