from common_filter import *
import sys

# Filter out variants in VEP-annotated VCF which have dbSnP entries.  
# Optionally rescue variants which have COSMIC and/or ClinVar entries

# optional command line parameters
# --debug
# --config config.ini
# --bypass
# --dump - print out CSQ dictionary for each variant
#
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
        parser.add_argument('--rescue_cosmic', action="store_true", default=False, help='Retain variants in COSMIC')
        parser.add_argument('--rescue_clinvar', action="store_true", default=False, help='Retain variants in ClinVar')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')
        parser.add_argument('--dump', action="store_true", default=False, help='Dump out CSQ dictionary for each read')
        parser.add_argument('--add_id', action="store_true", default=False, help='Add dbSnP, COSMIC, ClinVar IDs to VCF ID field')

    def __init__(self, args):
        self.CSQ_headers = self.get_CSQ_header(args.input_vcf)

        self.debug = args.debug
        self.bypass = args.bypass
        self.dump = args.dump
        self.rescue_cosmic = args.rescue_cosmic
        self.rescue_clinvar = args.rescue_clinvar
        self.add_id = args.add_id

        # Make sure field we're filtering on is in CSQ header info
        # if looking to rescue based on ClinVar, need to have ClinVar info
        if "Existing_variation" not in self.CSQ_headers: 
            raise Exception( "CSQ field %s not found in %s." % ("Existing_variation", args.input_vcf) )
        if args.rescue_clinvar:
            if "ClinVar" not in self.CSQ_headers: 
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
        CSQ = self.parse_CSQ(record)

        eprint(CSQ["Existing_variation"])
        sys.exit()



        if CSQ[self.filter_field]:
            CSQ_values = CSQ[self.filter_field].split("&")
        else:
            CSQ_values = None

        if self.dump:
            eprint("CSQ: " + str(CSQ) )
            eprint("VALUES: " + str(CSQ_values))

        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return


        if self.including: # keep call if observed value(s) in list
            if len(intersection) == 0:
                if (self.debug): eprint("** FAIL: %s not in %s **" % report )
                return " %s not in %s **" % report
            else:
                if (self.debug): eprint("** PASS: %s is in %s **" % report )
                return
        else:                 
            if len(intersection) > 0: # discard call if observed value(w) in list
                if (self.debug): eprint("** FAIL: %s is in %s **" % report )
                return " %s in %s **" % report
            else:
                if (self.debug): eprint("** PASS: %s not in %s **" % report )
                return
