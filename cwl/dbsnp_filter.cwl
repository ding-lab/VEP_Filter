class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: dbsnp_filter
baseCommand:
  - /bin/bash
  - /opt/VEP_Filter/src/run_dbsnp_filter.sh
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
  - id: rescue_cosmic
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-c'
    label: Retain COSMIC variants
  - id: rescue_clinvar
    type: boolean?
    inputBinding:
      position: 0
      prefix: '-l'
    label: Retain ClinVar variants
outputs:
  - id: output
    type: File
    outputBinding:
      glob: dbsnp_filter.output.vcf
label: DBSNP_Filter
arguments:
  - position: 0
    prefix: '-o'
    valueFrom: dbsnp_filter.output.vcf
  - position: 0
    prefix: '-I'
    valueFrom: all
requirements:
  - class: ResourceRequirement
    ramMin: 2000
  - class: DockerRequirement
    dockerPull: 'mwyczalkowski/vep_filter:20200719'
  - class: InlineJavascriptRequirement
