
OUTD="/data/VEP_Filter.out"
mkdir -p $OUTD

VCF="/data/GATK.indel.Final.vcf.gz"
CONFIG="../../params/VEP_Filter.config.ini"

OUT="$OUTD/GATK.indel.VLD.SAMPLE.vcf"

bash ../../src/run_vaf_length_depth_filters.sh $@ $ARG -o $OUT $VCF $CONFIG

