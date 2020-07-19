Notes specific to test runs of C3L-00001

# Run 1:
[2020-02-06 00:12:04,35] [info] SingleWorkflowRunnerActor workflow finished with status 'Succeeded'.
{
  "outputs": {
    "pindel_caller.Pindel_GermlineCaller.cwl.pindel_sifted": {
      "format": null,
      "location": "/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions/pindel_caller.Pindel_GermlineCaller.cwl/d54c10d0-3c99-49a8-bbb8-35c1dd491174/call-pindel_caller.Pindel_GermlineCaller.cwl/execution/output/pindel_sifted.out",
      "size": 19088,
      "secondaryFiles": [],
      "contents": null,
      "checksum": null,
      "class": "File"
    }
  },
  "id": "d54c10d0-3c99-49a8-bbb8-35c1dd491174"
}

{
  "outputs": {
    "pindel_filter.Pindel_GermlineCaller.cwl.indel_vcf": {
      "format": null,
      "location": "/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions/pindel_filter.Pindel_GermlineCaller.cwl/121c6e23-d909-47b2-b66c-1c91a3c589ef/call-pindel_filter.Pindel_GermlineCaller.cwl/execution/filtered/pindel_sifted.out.CvgVafStrand_pass.Homopolymer_pass.vcf",
      "size": 22951,
      "secondaryFiles": [],
      "contents": null,
      "checksum": null,
      "class": "File"
    }
  },
  "id": "121c6e23-d909-47b2-b66c-1c91a3c589ef"
}

-> it appears that all chrom but chrY died silently.  This is most likely because of memory errors.  Increased memory to 28G (same as TinDaisy)
-> Note that silent failure of jobs will manifest as lack of data for certain chrom.  This could cause problems in future when these
are not tested for.  Maybe look for some specific signature in log files to experimentally determine if something died


# Run2

## pindel_caller

[2020-02-06 16:04:09,69] [info] SingleWorkflowRunnerActor workflow finished with status 'Succeeded'.
{
  "outputs": {
    "pindel_caller.Pindel_GermlineCaller.cwl.pindel_sifted": {
      "format": null,
      "location": "/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions/pindel_caller.Pindel_GermlineCaller.cwl/11937496-8df4-4f98-a445-b4499aee2c95/call-pindel_caller.Pindel_GermlineCaller.cwl/execution/output/pindel_sifted.out",
      "size": 18262424,
      "secondaryFiles": [],
      "contents": null,
      "checksum": null,
      "class": "File"
    }
  },
  "id": "11937496-8df4-4f98-a445-b4499aee2c95"
}

Looking at chrom represented in final file may be useful for evaluating if there are memory errors.  Counts of specific chrom in above file:
  12263 ChrID chr1
   4057 ChrID chr10
   5495 ChrID chr11
   5478 ChrID chr12
   2228 ChrID chr13
   3608 ChrID chr14
   3525 ChrID chr15
   5937 ChrID chr16
   6142 ChrID chr17
   1843 ChrID chr18
   5295 ChrID chr19
   7195 ChrID chr2
   2087 ChrID chr20
   2705 ChrID chr21
   2257 ChrID chr22
   5025 ChrID chr3
   4595 ChrID chr4
   5818 ChrID chr5
   5058 ChrID chr6
   8188 ChrID chr7
   4447 ChrID chr8
   3888 ChrID chr9
   4185 ChrID chrX
    120 ChrID chrY

Checking for the largest chromosomes may be most effective, since they're most likely to exist in a good dataset but most likely to die of memory issues

## pindel_filter
[2020-02-06 16:43:24,93] [info] SingleWorkflowRunnerActor workflow finished with status 'Succeeded'.
{
  "outputs": {
    "pindel_filter.Pindel_GermlineCaller.cwl.indel_vcf": {
      "format": null,
      "location": "/gscmnt/gc2541/cptac3_analysis/cromwell-workdir/cromwell-executions/pindel_filter.Pindel_GermlineCaller.cwl/d40396fb-5364-416e-970c-cd414ee8980c/call-pindel_filter.Pindel_GermlineCaller.cwl/execution/filtered/pindel_sifted.out.CvgVafStrand_pass.Homopolymer_pass.vcf",
      "size": 39765793,
      "secondaryFiles": [],
      "contents": null,
      "checksum": null,
      "class": "File"
    }
  },
  "id": "d40396fb-5364-416e-970c-cd414ee8980c"
}
