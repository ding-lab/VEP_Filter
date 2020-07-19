All relative paths in YAML file are relative to the YAML file itself,
so if it is moved, relative paths may need to be updated

Note:

Template YAML files can be created from CWL code with,
    cwltool --make-template ../../../cwl/VLD_FilterVCF.cwl > VLD_FilterVCF-template.yaml
