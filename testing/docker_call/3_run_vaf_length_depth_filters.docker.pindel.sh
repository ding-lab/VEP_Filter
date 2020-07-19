IMAGE="mwyczalkowski/vld_filter_vcf:latest"
DATD="/home/mwyczalk_test/Projects/GermlineCaller/C3L-00001"

# Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
# see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)

# paths relative to container
VCF="/data/pindel_sifted.out.CvgVafStrand_pass.Homopolymer_pass.vcf"
OUTD="/data/docker.test.out"
OUT="$OUTD/pindel.filtered.vcf"
CONFIG="/opt/VLD_FilterVCF/params/VLD_FilterVCF-pindel.config.ini"

CMD="bash /opt/VLD_FilterVCF/src/run_vaf_length_depth_filters.sh $@ -o $OUT $VCF $CONFIG"

docker run -v $ADATD:/data -it $IMAGE $CMD

