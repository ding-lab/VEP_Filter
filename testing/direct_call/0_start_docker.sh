# start docker image with ../demo_data mapped to /data,
# unless another path is passed on command line.  uses
# the start_docker.sh script in /docker

#DATAD="/home/mwyczalk_test/Projects/GermlineCaller/C3L-00001"
DATAD="/home/mwyczalk_test/Projects/GermlineCaller/C3L-00081"
source ../../docker/docker_image.sh

cd ../.. && bash docker/WUDocker/start_docker.sh $@ -I $IMAGE $DATAD:/data


