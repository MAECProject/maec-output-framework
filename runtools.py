import importlib
from maec.misc.options import ScriptOptions
from maec.package.package import Package
import maec.utils.merge
import config
import argparse
import traceback

parser = argparse.ArgumentParser(description="MAEC Multi-Tool Translator")
parser.add_argument("input", help="the path to the binary file to be analyzed")
parser.add_argument("output", help="the path to the binary file to be analyzed")
parser.add_argument("--md5", "--hash", help="indicates input is an MD5 hash of the file to be fetched and analyzed", action="store_true", default=False)
parser.add_argument("--verbose", "-v", help="enable verbose output mode", action="store_true", default=False)
args = parser.parse_args()

output_packages = []

for module_data in config.modules:
    opts = module_data["options"]
    
    # import module and set its proxy and API key if applicable
    module = importlib.import_module(module_data["import_path"])
    if hasattr(module, "set_api_key") and "api_key" in module_data:
        module.set_api_key(module_data["api_key"])
    if hasattr(module, "set_proxies") and "proxies" in config.global_config and len(config.global_config["proxies"]) > 0:
        module.set_proxies(config.global_config["proxies"])
    
    if args.md5:
        # if MD5 is specified and the module accepts MD5s
        if hasattr(module, "generate_package_from_md5"):
            try:
                output_packages.append(
                             module.generate_package_from_md5(args.input, opts)
                             )
                print "Completed operation for module " + module_data["import_path"]
            except Exception, e:
                print "Module " + module_data["import_path"] + " failed MD5 lookup/conversion: " + str(e)
                if args.verbose: print traceback.format_exc()
        else:
            print "Module " + module_data["import_path"] + " does not support MD5 lookup; skipping"
    else:
        # if binary path is specified and the module supports it
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
            

merged_package = maec.utils.merge.merge_packages(output_packages)

merged_package.to_xml_file(args.output)

print "Wrote output to " + args.output
