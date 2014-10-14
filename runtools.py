import importlib
from maec.misc.options import ScriptOptions
from maec.package.package import Package
import maec.utils.merge
import config
import argparse

parser = argparse.ArgumentParser(description="MAEC Multi-Tool Translator")
parser.add_argument("input", help="the path to the binary file to be analyzed")
parser.add_argument("output", help="the path to the binary file to be analyzed")
parser.add_argument("--md5", "--hash", help="indicates input is an MD5 hash of the file to be fetched and analyzed", action="store_true", default=False)
parser.add_argument("--verbose", "-v", help="enable verbose output mode", action="store_true", default=False)
args = parser.parse_args()

output_packages = []

for module_data in config.modules:
    opts = ScriptOptions()
    opts.deduplicate_bundles = module_data["options"].get("deduplicate_bundles", False)
    opts.dereference_bundles = module_data["options"].get("dereference_bundles", False)
    opts.normalize_bundles = module_data["options"].get("normalize_bundles", False)
    
    module = importlib.import_module(module_data["import_path"])
    if hasattr(module, "set_api_key"): module.set_api_key(module_data["api_key"])
    if hasattr(module, "set_proxies"): module.set_proxies(config.global_config["proxies"])
    
    if args.md5:
        if hasattr(module, "generate_package_from_md5"):
            try:
                output_packages.append(
                             module.generate_package_from_md5(args.input, opts)
                             )
                print "Completed operation for module " + module_data["import_path"]
            except Exception, e:
                print "Module " + module_data["import_path"] + " failed MD5 lookup/conversion: " + str(e)
        else:
            print "Module " + module_data["import_path"] + " does not support MD5 lookup; skipping"
    else:
        if hasattr(module, "generate_package_from_binary_filepath"):
            try:
                output_packages.append(
                             module.generate_package_from_binary_filepath(args.input, opts)
                             )
                print "Completed operation for module " + module_data["import_path"]
            except Exception, e:
                print "Module " + module_data["import_path"] + " failed binary-to-MAEC conversion: " + str(e)
        else:
            print "Module " + module_data["import_path"] + " does not support binary conversion; skipping"
            

master_package = Package()
output_subjects = []

for package in output_packages:
    output_subjects.append(package.malware_subjects[0])
    
print maec.utils.merge.merge_malware_subjects(output_subjects)
    
    