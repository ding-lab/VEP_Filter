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

CSQ field  - Existing_variation
           - ClinVar - 
           
Adding ClinVar annotation details: https://m.ensembl.org/info/docs/tools/vep/script/vep_custom.html

class ClassificationFilter(VEPFilter):
    'Filter variant sites based on field as provided by VEP annotation'

    name = 'classification'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--config', type=str, help='Optional configuration file')
        parser.add_argument('--input_vcf', type=str, help='Input VCF filename', required=True)
        parser.add_argument('--rescue_cosmic', action="store_true", default=False, help='Retain variants in COSMIC')
        parser.add_argument('--rescue_clinvar', action="store_true", default=False, help='Retain variants in ClinVar')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')
        parser.add_argument('--dump', action="store_true", default=False, help='Dump out CSQ dictionary for each read')



    def __init__(self, args):
        self.CSQ_headers = self.get_CSQ_header(args.input_vcf)

        # These will not be set from config file (though could be)
        self.debug = args.debug
        self.bypass = args.bypass
        self.dump = args.dump

        # Read arguments from config file first, if present.
        # Then read from command line args, if defined
        # Note that default values in command line args would
        #   clobber configuration file values so are not defined
        config = self.read_config_file(args.config)

        # read arguments from config file and/or command line
        self.set_args(config, args, "filter_field")
        self.set_args(config, args, "include", required=False)
        self.set_args(config, args, "exclude", required=False)

        if self.debug:
            eprint("include: " + str(self.include))
            eprint("exclude: " + str(self.exclude))

        # process include / exclude args
        # User defines either include caller or exclude caller, but not both
        if bool(self.include) == bool(self.exclude):
            raise Exception("Must define exactly one of the following: --include, --exclude")

        if self.include is not None:
            self.including = True
            self.classifications = list(map(str.strip, self.include.split(','))) # stripping leading, trailing whitespace from each entry
        else:
            self.including = False
            self.classifications = list(map(str.strip, self.exclude.split(',')))

        # Make sure field we're filtering on is in CSQ header info
        if self.filter_field not in self.CSQ_headers:
            raise Exception( "CSQ field %s not found in %s" % (self.filter_field, args.input_vcf) )

        # below becomes Description field in VCF
        if self.bypass:
            self.__doc__ = "Bypassing Classification filter, retaining all reads"
        elif self.including:
            self.__doc__ = "Retain calls where INFO CSQ field '%s' (in most significant transcript) includes one of %s" % (self.filter_field, str(self.classifications))
        else:
            self.__doc__ = "Exclude calls where INFO CSQ field '%s' (in most significant transcript) includes any of %s" % (self.filter_field, str(self.classifications))

    def filter_name(self):
        return self.name

    def __call__(self, record):

        # CSQ has all VCF CSQ INFO entries as dictionary
        CSQ = self.parse_CSQ(record)


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

        # Evaluate intersection of the two lists, CSQ_values and include/exclude list ("classifications")
        # Then if we had an exclude list we drop the call, and if we have an include list we keep it.
        # https://www.geeksforgeeks.org/python-intersection-two-lists/
        intersection = list(set(CSQ_values) & set(self.classifications))
        report = (str(CSQ_values), str(self.classifications))

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
