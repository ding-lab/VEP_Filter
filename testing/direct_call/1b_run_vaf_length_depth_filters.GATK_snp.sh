
OUTD="/data/VLD_FilterVCF.out"
mkdir -p $OUTD

VCF="/data/GATK.snp.Final.vcf"
CONFIG="../../params/VLD_FilterVCF-GATK.config.ini"

OUT="$OUTD/GATK.snp.VLD.vcf"

bash ../../src/run_vaf_length_depth_filters.sh $@ -o $OUT $VCF $CONFIG

