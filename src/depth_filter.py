from common_filter import *
import sys

# Filter VCF files according to read depth
# For multi-sample VCFs this criterion is applied to all samples
#
# the following parameters are required:
# * min_depth
# * caller caller - specifies tool used for variant call. 'strelka', 'varscan', 'pindel', 'mutect', 'GATK'
#
# These may be specified on the command line (e.g., --min_depth_normal 10) or in
# configuration file, as specified by --config config.ini  Sample contents of config file:
#   [read_depth]
#   min_depth = 10
#
# optional command line parameters
# --debug
# --config config.ini
# --bypass
#
# Note, parser just needs the leading unique string, so --bypass will generally work

class DepthFilter(ConfigFileFilter):
    'Filter variant sites by read depth'
    # Normally we would be able to use the built-in filter "dps"; however, pindel does not write the DP tag and depth filtering fails

    name = 'read_depth'

    @classmethod
    def customize_parser(self, parser):

        parser.add_argument('--min_depth', type=int, help='Retain sites where read depth > min_depth')
        parser.add_argument('--caller', type=str, choices=['strelka', 'varscan', 'pindel', 'mutect', 'GATK'], help='Caller type')
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--config', type=str, help='Optional configuration file')
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
        self.set_args(config, args, "min_depth", arg_type="int")

        # below becomes Description field in VCF
        if self.bypass:
            self.__doc__ = "Bypassing Depth filter, retaining all reads. Caller = %s" % (self.caller)
        else:
            self.__doc__ = "Retain calls where read depth > %s . Caller = %s " % (self.min_depth, self.caller)

    def filter_name(self):
        return self.name

    def get_depth_strelka(self, VCF_data):
        depth = VCF_data.DP
        if self.debug:
            eprint("strelka depth = %d" % depth)
        return depth

    def get_depth_varscan(self, VCF_data):
        depth = VCF_data.DP
        if self.debug:
            eprint("varscan depth = %d" % depth)
        return depth

    def get_depth_pindel(self, VCF_data):
        AD_ref, AD_var = VCF_data.AD
        depth = AD_ref + AD_var
        if self.debug:
            eprint("pindel depth = %d" % depth)
        return depth

    def get_depth_mutect_GATK(self, VCF_data):
        # Depth can be obtained in one of two ways, with AD (allelic depths) or DP (read depth) values in VCF:
            # FORMAT=<ID=AD,Number=.,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">
            # FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">
        # Testing for mutect indicates these are very similar.  SomaticWrapper uses AD, so we'll use AD here too
        # GATK is calculated same way
        # if there are multiple alternate alleles we use the greatest value

        AD_ref = VCF_data.AD[0]
        AD_var = max(VCF_data.AD[1:])

        depth = AD_ref + AD_var

#        depth_DP = VCF_data.DP
        if self.debug:
            eprint("mutect / GATK depth = %d" % depth)
#            eprint("mutect / GATK depth_AD = %d, depth_DP = %d " % (depth, depth_DP) )
        return depth

    def get_depth(self, call_data):
        variant_caller = self.caller  
        if variant_caller == 'strelka':
            return self.get_depth_strelka(call_data)
        elif variant_caller == 'varscan':
            return self.get_depth_varscan(call_data)
        elif variant_caller == 'pindel':
            return self.get_depth_pindel(call_data)
        elif variant_caller == 'mutect' or variant_caller == 'GATK':
            return self.get_depth_mutect_GATK(call_data)
        else:
            raise Exception( "Unknown caller: " + variant_caller)

    def __call__(self, record):

        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return

       # loop over all genotypes so that this code can work for both germline and somatic calls
        for call in record.samples:
            sample_name=call.sample
            sample_data=call.data

            depth = self.get_depth(sample_data)

            if self.debug:
                eprint("sample: %s  depth: %f" % (sample_name, depth))

            if depth < self.min_depth:
                if (self.debug): eprint("** FAIL min_depth = %d ** " % depth)
                return "sample %s depth: %d" % (sample_name, depth)

        if (self.debug):
            eprint("** PASS read depth filter **")
