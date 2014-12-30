import importlib
from maec.misc.options import ScriptOptions
from maec.package.package import Package
from cybox.utils import Namespace
import maec.utils.merge
import config
import argparse
import traceback

__version__ = "v1.0.0-beta1"

def main():
    parser = argparse.ArgumentParser(description="MAEC Multi-Tool Translator " + __version__)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--md5", "--hash", help="Indicates input is an MD5 hash of the file to be fetched", action="store_true", default=False)
    input_group.add_argument("--file", help="Indicates input is a file path", action="store_true", default=False)
    parser.add_argument("input", help="The path to the binary file to be analyzed OR the MD5 hash sum to fetch data for")
    parser.add_argument("output", help="The path to the MAEC XML file to which the tool output will be written")
    parser.add_argument("--verbose", "-v", help="Enable verbose error output mode", action="store_true", default=False)
    parser.add_argument("--progress", "-p", help="Show tool-by-tool output", action="store_true", default=False)
    args = parser.parse_args()
    
    run_tools(args)

def run_tools(args):
    output_packages = []
    
    output_comment_data = []
    output_comment_data.append("Created by: MAEC Output Framework (http://github.com/MAECProject/maec-output-framework)")
    
    for module_data in config.modules:
        opts = module_data["options"]
        
        # import module and set its proxy and API key if applicable
        try:
            module = importlib.import_module(module_data["import_path"])
        except ImportError:
            print "Could not find module " + module_data["import_path"]
            continue
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
                    output_comment_data.append(module_data["import_path"] + " options: " + str(opts.to_dict()))
                    if args.verbose or args.progress: print "Completed operation for module " + module_data["import_path"]
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
                    output_comment_data.append(module_data["import_path"] + " options: " + str(opts.to_dict()))
                    if args.verbose or args.progress: print "Completed operation for module " + module_data["import_path"]
                except Exception, e:
                    print "Module " + module_data["import_path"] + " failed binary-to-MAEC conversion: " + str(e)
                    if args.verbose: print traceback.format_exc()
            else:
                print "Module " + module_data["import_path"] + " does not support binary conversion; skipping"
                
    
    if len(output_packages) > 0:
        merged_package = maec.utils.merge.merge_packages(output_packages, Namespace("https://github.com/MAECProject/maec-output-framework", "maecOutputFramework"))
        merged_package.to_xml_file(args.output, { "https://github.com/MAECProject/maec-output-framework":"maecOutputFramework" }, custom_header=output_comment_data)
        print "Wrote output to " + args.output
    else:
        print "All tools failed to run successfully, so there is no XML to write out."

if __name__ == "__main__":
    main() 