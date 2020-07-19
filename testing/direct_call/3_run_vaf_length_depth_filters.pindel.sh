
OUTD="/data/VLD_FilterVCF.out"
mkdir -p $OUTD

VCF="/data/pindel_sifted.out.CvgVafStrand_pass.Homopolymer_pass.vcf"
CONFIG="../../params/VLD_FilterVCF-pindel.config.ini"

OUT="$OUTD/pindel.VLD.vcf"

bash ../../src/run_vaf_length_depth_filters.sh $@ -o $OUT $VCF $CONFIG


# Having problems in length filter with a line like this:
# chr1    146139544   .   C   <DEL>   .   PASS    END=148590500;HOMLEN=0;SVLEN=-2450956;SVTYPE=DEL    GT:AD   0/1:8,9
