MAEC Output Framework
=====================

A framework for producing MAEC output from multiple tools at once. Given a binary file or an MD5, the framework script will run the input through a list of MAEC-producing modules and aggregate the output into a single MAEC Package.

BY USING THE MAEC OUTPUT FRAMEWORK, YOU SIGNIFY YOUR ACCEPTANCE OF THE TERMS AND CONDITIONS OF USE. IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE SCRIPT. For more information, please refer to the LICENSE.txt file.

Dependencies
------------

This code has been developed and tested under Python 2.7.x and so may not be compatible with Python 3.x.

There are two dependencies for this script:

1. The python-maec library >= v4.1.0.8: [`PyPI`_\ ] [`GitHub`_\ ]
2. The python-cybox library >= v2.1.0.8:
   [`PyPI <https://pypi.python.org/pypi/cybox>`__\ ]
   [`GitHub <https://github.com/CyboxProject/python-cybox>`__\ ]

For tools that are compatible with the MAEC Output Framework, see "Tool List" below.

Usage
-----

::

    python runtools.py (--md5 | --file) <input file path or MD5> <output XML file path> 
                       [--verbose] [--progress]

Given a file argument, each particular tool either inspects the file locally, or submits the file’s hash to an external analysis service. Currently, no tool submits file contents to an external service.

The ``--progress`` argument enables tool-by-tool success messages.

The ``--verbose`` argument enables verbose error messages, useful for debugging.

Configuration
-------------

Per-module configuration and global configuration options can be set in ``config.py``.

The configuration dictionary for a module in the ``modules`` list looks like:

::

    {
        "import_path":"virustotal_to_maec",        # package identifier, used with importlib.import_module
        
        "options": {                               # options used to build the ScriptOptions object
                    "deduplicate_bundles": True,   # implies MalewareSubject::deduplicate_bundles
                    "dereference_bundles": False,  # implies MalewareSubject::dereference_bundles
                    "normalize_bundles": True      # implies MalewareSubject::normalize_bundles
        },
        
        "api_key":"1a2b3c4d5e6f7"                  # API key used by this module when contacting a service
    }

The ``global_config`` dictionary currently only uses a ``proxies`` entry, which should have a dictionary value. The ``global_config`` dictionary therefore looks like:

::

    {
        "proxies": {
            "http":"http://example.com:80",
            "https":"http://example.com:80"
        }
    }

Tool Interface
--------------

A conversion module may define any of the following methods, to be
called by the framework:

-  ``generate_package_from_binary_filepath`` - given an filepath, the function returns a python-maec Pacakge object
-  ``generate_package_from_md5`` - given an MD5 string, the function returns a python-maec Pacakge object
-  ``set_proxies`` - optionally called to supply proxy information to the module; supplied as a dictionary like ``{ "http": "http://example.com:80", ... }``
-  ``set_api_key`` - optionally called to supply API key information to the module

If the framework attempts a particular operation, and the module does not support the particular method required for that operation, the module will simply be skipped for that operation.

Tool List
---------

Some projects with modules that implement the tool interface are:

-  `PEFile to MAEC`_
-  `ThreatExpert to MAEC`_
-  `VirusTotal to MAEC`_

.. _PyPI: https://pypi.python.org/pypi/maec
.. _GitHub: https://github.com/MAECProject/python-maec
.. _PEFile to MAEC: https://github.com/MAECProject/pefile-to-maec
.. _ThreatExpert to MAEC: https://github.com/MAECProject/threatexpert-to-maec
.. _VirusTotal to MAEC: https://github.com/MAECProject/vt-to-maec
