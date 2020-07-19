
OUTD="/data/VLD_FilterVCF.out"
mkdir -p $OUTD

VCF="/data/varscan_remapped/varscan.snp.vcf-remapped.vcf"
CONFIG="../../params/VLD_FilterVCF-varscan.config.ini"

OUT="$OUTD/varscan.snp.VLD.vcf"

bash ../../src/run_vaf_length_depth_filters.sh $@ -o $OUT $VCF $CONFIG

