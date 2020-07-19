#/bin/bash

read -r -d '' USAGE <<'EOF'
Run VAF, length, read depth, and allele depth filters on a VCF and optionaly rename sample names

Usage:
  bash run_vaf_length_depth_filters.sh [options] VCF CONFIG_FN

Options:
-h: Print this help message
-d: Dry run - output commands but do not execute them
-o OUT_VCF: Output VCF.  Default writes to STDOUT
-O TMPD: Directory for intermediate output, used when -N specified. Default: ./output
-N: Write out intermediate VCFs rather than using pipes
-e: VAF filter debug mode
-E: VAF filter bypass
-f: Length filter debug mode
-F: Length filter bypass
-g: Depth filter debug mode
-G: Depth filter bypass
-j: Allele depth filter debug mode
-J: Allele depth filter bypass
-s SAMPLE_NAMES: rename sample names in VCF header with values from comma-separated list
-R: remove filtered variants.  Default is to retain filtered variants with filter name in VCF FILTER field

VCF is input VCF file
CONFIG_FN is configuration file used by all filters

Script successively executes vaf, length, depth, and AD filters with unix pipes as,
  python vaf_filter ... | python length_filter ... | python depth_filter ... | python allele_depth_filter ... > output.vcf
Alternatively, with -N specified intermediate files like TMPD/vaf_output.vcf are written for each step

All calls which do not have PASS filter are rejected
...
EOF

source /opt/VLD_FilterVCF/src/utils.sh
SCRIPT=$(basename $0)

PYTHON=""
export PYTHONPATH="/opt/VLD_FilterVCF/src:$PYTHONPATH"
OUT_VCF="-"
TMPD="./output"

# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":hdO:o:NeEfFgGjJs:R" opt; do
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
    N)  # binary argument
      NO_PIPE=1
      ;;
    e)
      VAF_ARG="$VAF_ARG --debug"
      ;;
    E)
      VAF_ARG="$VAF_ARG --bypass"
      ;;
    f)
      LENGTH_ARG="$LENGTH_ARG --debug"
      ;;
    F)
      LENGTH_ARG="$LENGTH_ARG --bypass"
      ;;
    g)
      DEPTH_ARG="$DEPTH_ARG --debug"
      ;;
    G)
      DEPTH_ARG="$DEPTH_ARG --bypass"
      ;;
    j)
      AD_ARG="$AD_ARG --debug"
      ;;
    J)
      AD_ARG="$AD_ARG --bypass"
      ;;
    s)
      SAMPLE_NAMES="$OPTARG"
      ;;
    R)
      FILTER_ARG="--no-filtered"
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

VCF_EXT=${VCF##*.}
if [ $VCF_EXT == "gz" ]; then
    VCF_GZ=1
fi

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

# Arguments to VAF filter.  
VAF_FILTER="vcf_filter.py $FILTER_ARG --local-script vaf_filter.py"  # filter module
VAF_FILTER_ARGS="vaf $VAF_ARG $CONFIG "

# Arguments to length filter
LENGTH_FILTER="vcf_filter.py $FILTER_ARG --local-script length_filter.py"  # filter module
LENGTH_FILTER_ARGS="length $LENGTH_ARG $CONFIG" 

# Arguments to depth filter
DEPTH_FILTER="vcf_filter.py $FILTER_ARG --local-script depth_filter.py"  # filter module
DEPTH_FILTER_ARGS="read_depth $DEPTH_ARG $CONFIG " 

# Arguments to AD filter
AD_FILTER="vcf_filter.py $FILTER_ARG --local-script allele_depth_filter.py"  # filter module
AD_FILTER_ARGS="allele_depth $AD_ARG $CONFIG " 

# Remap sample names in VCF by changing column names in header line
# We replace commas with tabs in SAMPLE_NAME and write that as all columns past 9
if [ "$SAMPLE_NAMES" ]; then
    SNT=$( echo $SAMPLE_NAMES | tr ',' '\t'  )
    REMAP="awk -v snt=\"$SNT\" 'BEGIN{FS=\"\\t\";OFS=\"\\t\"}{if (\$1 == \"#CHROM\") print \$1, \$2, \$3, \$4, \$5, \$6, \$7, \$8, \$9, snt; else print}' "
else
    REMAP="cat "
fi

# zcat is necessary if remapping sample names, not needed for filters.
if [ "$VCF_GZ" == 1 ]; then
    CAT="zcat"
else
    CAT="cat"
fi


if [ -z $NO_PIPE ]; then
    CMD="$CAT $VCF | $REMAP | $VAF_FILTER - $VAF_FILTER_ARGS | $LENGTH_FILTER - $LENGTH_FILTER_ARGS | $DEPTH_FILTER - $DEPTH_FILTER_ARGS | $AD_FILTER - $AD_FILTER_ARGS"
    if [ $OUT_VCF != "-" ]; then
        CMD="$CMD > $OUT_VCF"
    fi
    run_cmd "$CMD" $DRYRUN
else
    OUT1="$TMPD/vaf_filter_out.vcf"
    CMD1="$CAT $VCF | $REMAP | $VAF_FILTER - $VAF_FILTER_ARGS > $OUT1"
    run_cmd "$CMD1" $DRYRUN

# passing $OUT as argument doesn't work, but `cat OUT | filter - ` does work
    OUT2="$TMPD/length_filter_out.vcf"
    CMD2="cat $OUT1 | $LENGTH_FILTER - $LENGTH_FILTER_ARGS > $OUT2"
    run_cmd "$CMD2" $DRYRUN

    OUT3="$TMPD/depth_filter_out.vcf"
    CMD3="cat $OUT2 | $DEPTH_FILTER - $DEPTH_FILTER_ARGS > $OUT3"
    run_cmd "$CMD3" $DRYRUN

    CMD4="cat $OUT3 | $AD_FILTER - $AD_FILTER_ARGS"
    if [ $OUT_VCF != "-" ]; then
        CMD4="$CMD4 > $OUT_VCF"
    fi
    run_cmd "$CMD4" $DRYRUN
fi

if [ $OUT_VCF != "-" ]; then
    >&2 echo Written to $OUT_VCF
fi

