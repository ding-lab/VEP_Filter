
DATAD="/home/mwyczalk_test/Projects/TinDaisy/testing/C3L-00908-data/dat"

# changing directories so entire project directory is mapped by default
cd ../..
OUTD="testing/direct_call/results"  # output dir relative to ../..
mkdir -p $OUTD

PARAMD="params"

source docker/docker_image.sh
IMAGE=$IMAGE

bash docker/WUDocker/start_docker.sh $@ -I $IMAGE $DATAD:/data $PARAMD:/params $OUTD:/results

