"""
Configuration data for modules used by the framework
"""

from maec.misc.options import ScriptOptions

modules = [
    {
        "import_path":"threatexpert_to_maec",
        "options": {
                    "deduplicate_bundles": True,
                    "dereference_bundles": False,
                    "normalize_bundles": True
        }
    },
    {
        "import_path":"virustotal_to_maec",
        "options": {
                    "deduplicate_bundles": True,
                    "dereference_bundles": False,
                    "normalize_bundles": True
        },
        "api_key":""
    },      
]

global_config = {
    "proxies": {
        #"http":"",
        #"https":""
    }
}

# turn options dicts into ScriptOptions objects
for module in modules:
    options_object = ScriptOptions()
    options_dict = module['options']
    options_object.deduplicate_bundles = options_dict['deduplicate_bundles']
    options_object.dereference_bundles = options_dict['dereference_bundles']
    options_object.normalize_bundles = options_dict['normalize_bundles']
    module['options'] = options_object

