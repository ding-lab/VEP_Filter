cd ../../..
CWL="cwl/VLD_FilterVCF.cwl"
YAML="testing/cwl_call/yaml/VLD_FilterVCF.varscan_indel.yaml"

mkdir -p results
RABIX_ARGS="--basedir results"

rabix $RABIX_ARGS $CWL $YAML
