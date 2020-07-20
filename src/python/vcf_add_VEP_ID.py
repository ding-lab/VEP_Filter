# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

# add information about variant ID from various databases to VCF ID field
# How to determine id type based on VEP Existing_variation value is unclear.  
# See /gscuser/mwyczalk/projects/TinDaisy/testing/dbSnP-filter-dev/dbSnP-filter-dev/README.md
# for now, assume that "rs" is dbsnp and "COSV" is COSMIC.  Also, assume that if a value exists
# for ClinVar CSQ field, that variant is a ClinVar variant

import vcf
import argparse
import pysam
import sys
import os
import collections
from common_filter import *

def add_ID_vcf(f, o, id_policy):
    vcf_reader = vcf.Reader(filename=f)
    vcf_writer = vcf.Writer(open(o, "w"), vcf_reader)

    CSQ_header = VEPFilter.get_CSQ_header(f)

    # Make sure CSQ field Existing_variation exists.  Don't worry if ClinVar information not provided
    if "Existing_variation" not in CSQ_header: 
        raise Exception( "CSQ field %s not found in %s." % ("Existing_variation", f) )

    for record in vcf_reader:
        # CSQ has all VCF CSQ INFO entries as dictionary
        CSQ = VEPFilter.parse_CSQ(record, CSQ_header)

        (is_dbsnp, is_cosmic, is_clinvar) = VEPFilter.get_id_type(CSQ)
        id_name = VEPFilter.get_id_name(CSQ, id_policy)

        record.ID=id_name

        vcf_writer.write_record(record)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AD fields in varscan VCF file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging information to stderr")
    parser.add_argument("-i", "--input", dest="infn", help="Input vcf file name")
    parser.add_argument("-o", "--output", dest="outfn", help="Output file name")
    parser.add_argument("-I", "--id_policy", dest="id_policy", default="dbsnp", choices=['dbsnp', 'all'], help="Types of IDs to retain")
        # this will change in the future as we better know what we want to retain


    args = parser.parse_args()

    print("Input VCF: {}".format(args.infn), file=sys.stderr)
    print("Output VCF: {}".format(args.outfn), file=sys.stderr)

    add_ID_vcf(args.infn, args.outfn, args.id_policy)

