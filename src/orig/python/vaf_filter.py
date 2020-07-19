from common_filter import *
import sys

# Filter VCF files according to VAF values
# Include only variants with min_vaf < VAF <= max_vaf and 
# For multi-sample VCFs this criterion is applied to all samples
#
# This is called from pyvcf's `vcf_filter.py` with `vaf` module.
# the following parameters are required:
# * min_vaf
# * max_vaf
# * caller - specifies tool used for variant call. 'strelka', 'varscan', 'pindel', 'merged', 'mutect', 'GATK'
#
# These may be specified on the command line (e.g., --min_vaf 0.05) or in
# configuration file, as specified by --config config.ini  Sample contents of config file:
#   [vaf]
#   min_vaf = 0.05
#
# optional command line parameters
# --debug
# --config config.ini
# --bypass
# --pass_only

# For files with multiple samples, we loop over all of them and apply same criteria to all samples
# for somatic calls, may need to implement per-sample vaf_min and vaf_max 

# Details of how VAF is calculated per caller:
# * GATK: VAF = AD[var] / DP
# * varscan: VAF = FREQ
# * ...

# based on https://github.com/ding-lab/TinDaisy-Core/blob/master/src/vcf_filters/vaf_filter.py
# However, the above is specific to somatic calls with tumor and normal samples in VCF, 
# while this class is designed for germline
class TumorNormal_VAF(ConfigFileFilter):
    'Filter variant sites by variant allele frequency (VAF)'

    name = 'vaf'

    @classmethod
    def customize_parser(self, parser):
        # super(TumorNormal_VAF, cls).customize_parser(parser)

        parser.add_argument('--min_vaf', type=float, help='Retain sites where VAF > min_vaf')
        parser.add_argument('--max_vaf', type=float, help='Retain sites where VAF <= max_vaf')
        parser.add_argument('--caller', type=str, choices=['strelka', 'varscan', 'mutect', 'pindel', 'GATK', 'merged'], help='Caller type')
        parser.add_argument('--config', type=str, help='Optional configuration file')
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')
        parser.add_argument('--pass_only', action="store_true", default=False, help='Retain only variants with passing FILTER values')
        
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
        self.set_args(config, args, "min_vaf", arg_type="float")
        self.set_args(config, args, "max_vaf", arg_type="float")
        self.set_args(config, args, "pass_only")

        # below becomes Description field in VCF
        if self.bypass:
            if self.pass_only:
                self.__doc__ = "Bypassing VAF filter, retaining all variants where FILTER=PASS.  Caller = %s" % (self.caller)
            else:
                self.__doc__ = "Bypassing VAF filter, retaining all variants.  Caller = %s" % (self.caller)
        else:
            if self.pass_only:
                self.__doc__ = "Retain variants %f < VAF <= %f and FILTER=PASS.  Caller = %s " % (self.min_vaf, self.max_vaf, self.caller)
            else:
                self.__doc__ = "Retain variants where %f < VAF <= %f.  Caller = %s " % (self.min_vaf, self.max_vaf, self.caller)
            
    def filter_name(self):
        return self.name

    def get_snv_vaf_strelka(self, VCF_record, VCF_data):
        # this tested for both Strelka1 and Strelka2
        # read counts, as dictionary. e.g. {'A': 0, 'C': 0, 'T': 0, 'G': 25}
        # based on : https://github.com/Illumina/strelka/blob/v2.9.x/docs/userGuide/README.md#somatic-variant-allele-frequencies
        tier=0  # corresponds to "tier1" 
        rc = {'A':VCF_data.AU[tier], 'C':VCF_data.CU[tier], 'G':VCF_data.GU[tier], 'T':VCF_data.TU[tier]}

        # Sum read counts across all variants. In some cases, multiple variants are separated by , in ALT field
        #   Note we convert vcf.model._Substitution to its string representation to use as key
        rc_var = sum( [rc[v] for v in map(str, VCF_record.ALT) ] )
        #  per definition here https://github.com/Illumina/strelka/blob/v2.9.x/docs/userGuide/README.md#somatic-variant-allele-frequencies
        # VCF denominator is ref + alt counts
        rc_tot = rc_var + rc[str(VCF_record.REF)]
        if rc_tot == 0:
            vaf = 0.
        else:
            vaf = float(rc_var) / float(rc_tot) # Deal with rc_tot == 0
        if self.debug:
            eprint("REF=%s, ALT=%s, rc: %s, rc_var: %d, rc_tot: %d, vaf: %f" % (VCF_record.REF, VCF_record.ALT, str(rc), rc_var, rc_tot, vaf))
        return vaf

    def get_indel_vaf_strelka(self, VCF_record, VCF_data):
        # this tested for Strelka2
        # based on : https://github.com/Illumina/strelka/blob/v2.9.x/docs/userGuide/README.md#somatic-variant-allele-frequencies
        tier=0  # corresponds to "tier1" 
        rc = VCF_data.TAR[tier]  # RefCounts
        ac = VCF_data.TIR[tier]  # AltCounts
        if rc + ac == 0:
            vaf = 0.
        else:
            vaf = float(ac) / float(ac + rc) # Deal with rc_tot == 0
        if self.debug:
            eprint("REF=%s, ALT=%s, RefCounts: %d, AltCounts: %d, vaf: %f" % (VCF_record.REF, VCF_record.ALT, rc, ac, vaf))
        return vaf 

    def get_vaf_strelka(self, VCF_record, VCF_data):
        # If both are zero, avoid division by zero and return 0
        # pass VCF_record only to extract info (like ALT and is_snp) not available in VCF_data
        if VCF_record.is_snp:
            return self.get_snv_vaf_strelka(VCF_record, VCF_data)
        else:
            return self.get_indel_vaf_strelka(VCF_record, VCF_data)

    def get_vaf_varscan(self, VCF_record, VCF_data):
        # We'll take advantage of pre-calculated VAF
        # Varscan: CallData(GT=0/0, GQ=None, DP=96, RD=92, AD=1, FREQ=1.08%, DP4=68,24,1,0)
        ##FORMAT=<ID=FREQ,Number=1,Type=String,Description="Variant allele frequency">
        # This works for both snp and indel calls
        vaf = VCF_data.FREQ
        if self.debug:
            eprint("VCF_data.FREQ = %s" % vaf)
        return float(vaf.strip('%'))/100.

    def get_vaf_mutect(self, VCF_record, VCF_data):
        # We'll take advantage of pre-calculated VAF
        # ##FORMAT=<ID=FA,Number=A,Type=Float,Description="Allele fraction of the alternate allele with regard to reference">
        vaf = VCF_data.FA
        if self.debug:
            eprint("VCF_data.FA = %s" % vaf)
        # This could equivalently be calculated with,
        #rc_ref, rc_var = VCF_data.AD
        #depth = rc_ref + rc_var
        #vaf_calc= float(rc_var) / depth
        
        return float(vaf)

    def get_vaf_pindel(self, VCF_record, VCF_data):
        # read counts supporting reference, variant, resp.
        # If both are zero, avoid division by zero and return 0
        rc_ref, rc_var = VCF_data.AD
        rc_tot = float(rc_var + rc_ref)
        if rc_tot == 0:
            vaf = 0
        else:
            vaf = rc_var / rc_tot
        if self.debug:
            eprint("pindel VCF = %f" % vaf)
        return vaf

    def get_vaf_GATK(self, VCF_record, VCF_data):
        # This works for both snp and indel calls
        # VAF = AD / DP per https://gatkforums.broadinstitute.org/gatk/discussion/6202/vcf-file-and-allele-frequency
        # from VCF 
            ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">
            ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">
        # if there are multiple alternate alleles we use the greatest value

        AD_ref = VCF_data.AD[0]
        AD_var = max(VCF_data.AD[1:])
        DP = VCF_data.DP
        if DP == 0:
            vaf = 0.
        else:
            vaf = float(AD_var) / float(DP)
        if self.debug:
            eprint("GATK VAF = %d / %d = %f" % (AD_var, DP, vaf)) 
        return vaf

    def get_vaf(self, VCF_record, call_data, variant_caller=None):
        if variant_caller is None:
            variant_caller = self.caller  # we permit the possibility that each line has a different caller

        if variant_caller == 'strelka':
            return self.get_vaf_strelka(VCF_record, call_data)
        elif variant_caller == 'varscan':
            return self.get_vaf_varscan(VCF_record, call_data)
        elif variant_caller == 'mutect':
            return self.get_vaf_mutect(VCF_record, call_data)
        elif variant_caller == 'pindel':
            return self.get_vaf_pindel(VCF_record, call_data)
        elif variant_caller == 'GATK':
            return self.get_vaf_GATK(VCF_record, call_data)
        elif variant_caller == 'merged':
            # Caller is contained in 'set' INFO field
            merged_caller = VCF_record.INFO['set'][0]
            # TODO: It would be better to parse merged_caller to primary_caller, where merged set=A-B-C corresponds to primary_caller "A"
            if merged_caller == 'strelka':
                return self.get_vaf_strelka(VCF_record, call_data)
            elif merged_caller == 'varscan':
                return self.get_vaf_varscan(VCF_record, call_data)
            elif merged_caller == 'varindel':
                return self.get_vaf_varscan(VCF_record, call_data)
            elif merged_caller == 'strelka-varscan':
                return self.get_vaf_strelka(VCF_record, call_data)
            elif merged_caller == 'pindel':
                return self.get_vaf_pindel(VCF_record, call_data)
            else:
                raise Exception( "Unknown caller in INFO set field: " + merged_caller)
        else:
            raise Exception( "Unknown caller: " + variant_caller)

    def __call__(self, record):
        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return

    # filter to exclude any calls except PASS
    # This is from /home/mwyczalk_test/Projects/TinDaisy/mutect-tool/src/mutect-tool.py
        # specific code borrowed from https://pyvcf.readthedocs.io/en/latest/_modules/vcf/model.html#_Record
        if record.FILTER is not None and len(record.FILTER) != 0:
            msg = "record.FILTER = %s" % str(record.FILTER)
            if self.debug: 
                eprint(msg)
            if self.pass_only:
                return msg

       # loop over all genotypes so that this code can work for both germline and somatic calls
        for call in record.samples:
            sample_name=call.sample
            sample_data=call.data

            vaf = self.get_vaf(call, sample_data)

            if self.debug:
                eprint("sample: %s  vaf: %f" % (sample_name, vaf))


            if vaf <= self.min_vaf:
                if (self.debug):
                    eprint("** FAIL vaf <= min_vaf **")
                return "Sample %s VAF: %f" % (sample_name, vaf)
            if vaf > self.max_vaf:
                if (self.debug):
                    eprint("** FAIL vaf > max_vaf **")
                return "Sample %s VAF: %f" % (sample_name, vaf)

        if (self.debug):
            eprint("** PASS VAF filter **")

