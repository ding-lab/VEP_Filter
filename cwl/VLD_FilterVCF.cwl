class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: _v_l_d__filter_v_c_f
baseCommand:
  - /bin/bash
  - /opt/VLD_FilterVCF/src/run_vaf_length_depth_filters.sh
inputs:
  - id: dryrun
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-d'
    label: dryrun
    doc: Output commands but do not execute them
  - id: no_pipe
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-N'
    label: No Pipe
    doc: Write out intermediate VCFs rather than using pipes for debugging
  - id: debug_VAF
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-e'
    label: Debug VAF
    doc: VAF Filter debug mode
  - id: VCF
    type: File
    inputBinding:
      position: 1
    label: VCF
    doc: VCF input file to filter
  - id: config
    type: File
    inputBinding:
      position: 2
    label: config
    doc: configuration file used by all filters
  - id: remove_filtered
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-R'
    doc: >-
      Remove filtered variants.  Default is to retain filtered variants with
      filter name in VCF FILTER field
outputs:
  - id: output
    type: File
    outputBinding:
      glob: VLD_FilterVCF_output.vcf
label: VLD_FilterVCF
arguments:
  - position: 0
    prefix: '-o'
    valueFrom: VLD_FilterVCF_output.vcf
  - position: 0
    prefix: '-s'
    valueFrom: SAMPLE
requirements:
  - class: ResourceRequirement
    ramMin: 2000
  - class: DockerRequirement
    dockerPull: 'mwyczalkowski/vld_filter_vcf:20200614'
  - class: InlineJavascriptRequirement
