"""
Configuration data for modules used by the framework
"""
modules = [
    {
        "import_path":"threatexpert_to_maec",
        "options": {
                    "deduplicate_bundles": True,
                    "dereference_bundles": True,
                    "normalize_bundles": True
        }
    },
    {
        "import_path":"virustotal_to_maec",
        "options": {
                    "deduplicate_bundles": True,
                    "dereference_bundles": True,
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