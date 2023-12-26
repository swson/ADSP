from .pycpuid import *
from types import SimpleNamespace

def get_vendor_name() -> str:
	return cpuid()['vendor']

def get_uarch_list_intel() -> dict[tuple[int, int]: SimpleNamespace]:
	make_data = lambda x, y: SimpleNamespace(directory=x, description=y)
	# may need to be accessed from https://archive.org
	# https://en.wikichip.org/wiki/intel/cpuid
	return {
			(0x06, 0xb7): make_data('meteorlake', "Meteor Lake"),
			(0x06, 0x8e): make_data('skylake', "Kaby Lake (Y, U)"),
			(0x06, 0x56): make_data('broadwell', "Broadwell (Server)")
		}

def get_microarchitecture() -> SimpleNamespace:
	vendor = get_vendor_name()
	proc_info = processor_info()
	family, model = proc_info['family'], proc_info['model']
	match vendor:
		case "GenuineIntel":
			return get_uarch_list_intel()[(family, model)]
		case _:
			raise Exception("unsupported")

def get_pmu_features() -> SimpleNamespace:
	# cpuid.eax = 0Ah, return information about support for architectural
	# performance monitor capabilities
	pmu_data = get_cpuid_leaf(0xa)
	"""
	eax[31:24]	length of ebx bit vector
	eax[23:16]	bit width of general-purpose monitoring counters
	eax[15: 8]	number of general-purpose PMCs per logical processor
	eax[ 7: 0]	version ID of architectural performance monitoring

	edx[12: 5]	number of bits in the fixed counters (width)
	edx[ 4: 0]	number of fixed counters
	"""
	version_id = pmu_data['eax'] & 0xff
	gp_pmu = (pmu_data['eax'] >> 8) & 0xff
	gp_width = (pmu_data['eax'] >> 16) & 0xff
	
	f_counters = pmu_data['edx'] & 0x1f
	f_width = (pmu_data['edx'] >> 5) & 0xff

	return SimpleNamespace(
				version_id=version_id,
				gp_pmu=gp_pmu,
				gp_width=gp_width,
				f_counters=f_counters,
				f_width=f_width
			)
