
OUTD="/data/VLD_FilterVCF.out"
mkdir -p $OUTD

VCF="/data/GATK.indel.Final.vcf.gz"
CONFIG="../../params/VLD_FilterVCF-GATK.config.ini"

OUT="$OUTD/GATK.indel.VLD.SAMPLE.vcf"
ARG="-s SAMPLE"

bash ../../src/run_vaf_length_depth_filters.sh $@ $ARG -o $OUT $VCF $CONFIG

