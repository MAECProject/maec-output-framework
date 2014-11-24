# MAEC Output Framework

A framework for producing MAEC output from multiple tools at once. Given a binary file or an MD5, the framework script will run the input through a list of MAEC-producing modules and aggregate the output into a single MAEC Package.

## Usage

    python runtools.py (--md5 | --file) <input file path or MD5> <output XML file path> [--verbose]
    
## Configuration

Per-module configuration and global configuration options can be set in `config.py`.

The configuration dictionary for a module in the `modules` list looks like:

    {
        "import_path":"virustotal_to_maec",        # package identifier, used with importlib.import_module
        
        "options": {                               # options used to build the ScriptOptions object
                    "deduplicate_bundles": True,   # implies MalewareSubject::deduplicate_bundles
                    "dereference_bundles": False,  # implies MalewareSubject::dereference_bundles
                    "normalize_bundles": True      # implies MalewareSubject::normalize_bundles
        },
        
        "api_key":"1a2b3c4d5e6f7"                  # API key used by this module when contacting a service
    }
    
The `global_config` dictionary currently only uses a `proxies` entry, which should have a dictionary value. The `global_config` dictionary therefore looks like:

    {
        "proxies": {
            "http":"http://example.com:80",
            "https":"http://example.com:80"
        }
    }

## Tool Interface

A conversion module may define any of the following methods, to be called by the framework:

  * `generate_package_from_binary_filepath` - given an filepath, the function returns a python-maec Pacakge object
  * `generate_package_from_md5` - given an MD5 string, the function returns a python-maec Pacakge object
  * `set_proxies` - optionally called to supply proxy information to the module; supplied as a dictionary like `{ "http": "http://example.com:80", ... }`
  * `set_api_key` - optionally called to supply API key information to the module
  
If the framework attempts a particular operation, and the module does not support the particular method required for that operation, the module will simply be skipped for that operation.
