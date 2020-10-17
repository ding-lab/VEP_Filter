class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: af_filter
baseCommand:
  - /bin/bash
  - /opt/VEP_Filter/src/run_af_filter.sh
inputs:
  - id: debug
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
  - id: bypass
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-E'
    label: Bypass filter
outputs:
  - id: output
    type: File
    outputBinding:
      glob: af_filter.output.vcf
label: AF_Filter
arguments:
  - position: 0
    prefix: '-o'
    valueFrom: af_filter.output.vcf
requirements:
  - class: ResourceRequirement
    ramMin: 2000
  - class: DockerRequirement
    dockerPull: 'mwyczalkowski/vep_filter:20201017'
  - class: InlineJavascriptRequirement
