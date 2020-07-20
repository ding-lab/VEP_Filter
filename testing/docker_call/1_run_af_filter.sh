source ../../docker/docker_image.sh

DATAD="/home/mwyczalk_test/Projects/TinDaisy/VEP_Filter"

### AF filter from direct
OUTD="/data/testing/demo_data-local/docker_output"
mkdir -p $OUTD

VCF="/data/testing/demo_data-local/C3L-00908.output_vep.vcf"
CONFIG="/data/params/af_filter_config.ini"

OUT="$OUTD/C3L-00908.af.vcf"

# This is what we want to run in docker
CMD_INNER="/bin/bash /opt/VEP_Filter/src/run_af_filter.sh $@ -o $OUT $VCF $CONFIG"

SYSTEM=docker   # docker MGI or compute1
START_DOCKERD="../../docker/WUDocker"  # https://github.com/ding-lab/WUDocker.git

VOLUME_MAPPING="$DATAD:/data"

>&2 echo Launching $IMAGE on $SYSTEM
CMD_OUTER="bash $START_DOCKERD/start_docker.sh -I $IMAGE -M $SYSTEM -c \"$CMD_INNER\" $VOLUME_MAPPING "
echo Running: $CMD_OUTER
eval $CMD_OUTER

>&2 echo Written to $OUT
