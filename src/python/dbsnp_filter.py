from common_filter import *
import sys

# Filter out variants in VEP-annotated VCF which have dbSnP entries.  
# Optionally rescue variants which have COSMIC and/or ClinVar entries

# Note that the input_vcf file will in general be specified twice, once as input into vcf_filter.py
# and once as input into this filter directly.

# Require that the following CSQ fields be present:
# - Existing_variation
# - ClinVar - this is required only for clinvar rescue
#         Adding ClinVar annotation details: https://m.ensembl.org/info/docs/tools/vep/script/vep_custom.html

# Details about fields in CSQ
# /Users/mwyczalk/Projects/TinDaisy/testing/dbSnP-filter-dev/VEP_annotate.testing/BAP1.variant-details.numbers


class ClassificationFilter(VEPFilter):
    'Filter variant sites based on field as provided by VEP annotation'

    name = 'dbsnp'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--input_vcf', type=str, help='Input VCF filename', required=True)
        parser.add_argument('-c', '--rescue_cosmic', action="store_true", default=False, help='Retain variants in COSMIC')
        parser.add_argument('-l', '--rescue_clinvar', action="store_true", default=False, help='Retain variants in ClinVar')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')
        parser.add_argument('--dump', action="store_true", default=False, help='Dump out CSQ dictionary for each read')
        parser.add_argument('--add_id', action="store_true", default=False, help='Add dbSnP and other variant IDs to VCF ID field')

    def __init__(self, args):
        self.CSQ_header = VEPFilter.get_CSQ_header(args.input_vcf)

        self.debug = args.debug
        self.bypass = args.bypass
        self.dump = args.dump
        self.rescue_cosmic = args.rescue_cosmic
        self.rescue_clinvar = args.rescue_clinvar
        self.add_id = args.add_id

        # Make sure field we're filtering on is in CSQ header info
        # if looking to rescue based on ClinVar, need to have ClinVar info
        if "Existing_variation" not in self.CSQ_header: 
            raise Exception( "CSQ field %s not found in %s." % ("Existing_variation", args.input_vcf) )
        if args.rescue_clinvar:
            if "ClinVar" not in self.CSQ_header: 
                raise Exception( "CSQ field %s not found in %s." % ("ClinVar", args.input_vcf) )

        # below becomes Description field in VCF
        if self.bypass:
            self.__doc__ = "Bypassing dbSnP filter, retaining all reads"
        else:
            self.__doc__ = "Exclude calls found in dbSnP based on VEP" 
            if self.rescue_cosmic:
                self.__doc__ = self.__doc__ + ".  Variants in COSMIC retained"
            if self.rescue_clinvar:
                self.__doc__ = self.__doc__ + ".  Variants in ClinVar retained"

    def filter_name(self):
        return self.name

    def __call__(self, record):

        # CSQ has all VCF CSQ INFO entries as dictionary
        CSQ = VEPFilter.parse_CSQ(record, self.CSQ_header)
        (is_dbsnp, is_cosmic, is_clinvar) = VEPFilter.get_id_type(CSQ)

        if self.dump:
            eprint("CSQ: " + str(CSQ) )
            eprint("VALUES: " + str(CSQ_values))

        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return

        reject = False
        status=""
        if is_dbsnp:
            reject = True
            status = "rejected - dbsnp"
            if self.rescue_cosmic:
                if is_cosmic:
                    reject = False
                    status = status + " rescued - cosmic"
            if self.rescue_clinvar:
                if is_clinvar:
                    reject = False
                    status = status + " rescued - clinvar"

        if reject:
            if (self.debug): eprint("** FAIL: %s **" % status )
            return status
        else:
            if (self.debug): eprint("** PASS: %s **" % status )
            return

