from common_filter import *
import sys

# Filter VCF files according to minimum reference or alternate allele depth values
# For multi-sample VCFs this criterion is applied to all samples
#
# the following parameters can be specified [default values]
# * min_depth_alternate [0]
# * min_depth_reference [0]
# * caller [ VCF ]
# * debug
# * config 
# * bypass
#
# These may be specified on the command line (e.g., --min_depth_alternate 5) or in
# configuration file, as specified by --config config.ini  Sample contents of config file:
#   [allele_depth]
#   min_depth_alternate = 5
#

# Caller field provides information about fields available in VCF.  Values:
# * VCF: Standard format (e.g., GATK) has AD INFO field format as A,B with A and B the reference andthe alternate allele depth, respectively
# * varscan: Varscan provides reference allele depth as RD and alternate allele depth as AD INFO fields
#
# Note that in GermlineCaller pipeline, we remap varscan VCF upstream of filtering using 
# varscan_vcf_remap (https://github.com/ding-lab/varscan_vcf_remap); such remapped
# VCFs should use "VCF" format

# Based on depth_filter.py

class AlleleDepthFilter(ConfigFileFilter):
    'Filter variant sites by minimum reference or alternate allele depth'

    name = 'allele_depth'

    @classmethod
    def customize_parser(self, parser):

        parser.add_argument('--min_depth_reference', type=int, help='Retain sites where reference allele depth > given value')
        parser.add_argument('--min_depth_alternate', type=int, help='Retain sites where alternate allele depth > given value')
        parser.add_argument('--caller', type=str, choices=['VCF', 'varscan'], default="VCF", help='Caller type')
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--config', type=str, help='Configuration file')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')

    def __init__(self, args):
        # These will not be set from config file (though could be)
        self.debug = args.debug
        self.bypass = args.bypass

        # Read arguments from config file first, if present.
        # Then read from command line args, if defined
        # Note that default values in command line args would
        #   clobber configuration file values so are not defined
        config = self.read_config_file(args.config)

        self.set_args(config, args, "caller")
        self.set_args(config, args, "min_depth_reference", arg_type="int")
        self.set_args(config, args, "min_depth_alternate", arg_type="int")

        # below becomes Description field in VCF
        if self.bypass:
            self.__doc__ = "Bypassing allele depth filter, retaining all reads. Caller = %s" % (self.caller)
        else:
            self.__doc__ = "Retain calls with allele depth reference > %s and alternate > %s . Caller = %s " % \
                (self.min_depth_reference, self.min_depth_alternate, self.caller)

    def filter_name(self):
        return self.name

    # Useful reference: https://github.com/ding-lab/varscan_vcf_remap
    def get_ad_varscan(self, VCF_data):
        AD_ref = VCF_data.AD
        AD_alt = VCF_data.RD
        if self.debug:
            eprint("Allele Depth ref, alt = %d, %d" % AD_ref, AD_alt)
        return AD_ref, AD_alt

    def get_ad_VCF(self, VCF_data):
        # if there are multiple alternate alleles we use the greatest value
        AD_ref = VCF_data.AD[0]
        AD_alt = max(VCF_data.AD[1:])
        if self.debug:
            eprint("Allele Depth ref, alt = %d, %d" % (AD_ref, AD_alt))
        return AD_ref, AD_alt

    def get_allele_depth(self, call_data):
        variant_caller = self.caller  
        if variant_caller == 'VCF':
            return self.get_ad_VCF(call_data)
        elif variant_caller == 'varscan':
            return self.get_ad_varscan(call_data)
        else:
            raise Exception( "Unknown caller: " + variant_caller)

    def __call__(self, record):
        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return

        for call in record.samples:
            sample_name=call.sample
            sample_data=call.data

            AD_ref, AD_alt = self.get_allele_depth(sample_data)
            if self.debug:
                eprint("sample: %s  AD ref: %f  AD alt: %f" % (sample_name, AD_ref, AD_alt))

            if AD_ref < self.min_depth_reference:
                if (self.debug): eprint("** FAIL reference depth = %d ** " % AD_ref)
                return "Sample %s AD_ref: %d" % (sample_name, AD_ref)
            if AD_alt < self.min_depth_alternate:
                if (self.debug): eprint("** FAIL alternate depth = %d ** " % AD_alt)
                return "Sample %s AD_alt: %d" % (sample_name, AD_alt)

        if (self.debug):
            eprint("** PASS read depth filter **")
