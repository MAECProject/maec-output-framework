MAEC Output Framework
=====================

A framework for producing `Malware Attribute Enumeration and Characterization (MAEC™) <https://maecproject.github.io/>`_ output from multiple tools at once. 

BY USING THE MAEC OUTPUT FRAMEWORK, YOU SIGNIFY YOUR ACCEPTANCE OF THE TERMS AND CONDITIONS OF USE. IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE SCRIPT. For more information, please refer to the LICENSE.txt file.

Overview
--------
Given a binary file or an MD5, the framework script will run the input through a list of MAEC-producing modules and aggregate the output into a single MAEC Package. More specifically, it will create a single MAEC Malware Subject for the input file or MD5, and will capture the output of each individual tool in its own Finding Bundle in the Malware Subject.

Dependencies
------------

This code has been developed and tested under Python 2.7.x and so may not be compatible with Python 3.x.

There are two dependencies for this utility:

1. The python-maec library >= v4.1.0.10: [`PyPI`_\ ] [`GitHub`_\ ]
2. The python-cybox library >= v2.1.0.9:
   [`PyPI <https://pypi.python.org/pypi/cybox>`__\ ]
   [`GitHub <https://github.com/CyboxProject/python-cybox>`__\ ]

For tools that are compatible with the MAEC Output Framework, see "Tool List" below.

Usage
-----

::

    python runtools.py (--md5 | --file) <input file path or MD5> <output XML file path> 
                       [--verbose] [--progress]

Given a file argument (--file), each particular tool either inspects the file locally, or submits the file’s hash to an external analysis service (to look for any existing analyses for this hash). Currently, no tool submits the actual file contents to an external service.

Given an MD5 hash argument (--md5), each particular tool submits the value to an external analysis service and looks for any existing analyses for this hash.

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
                    "deduplicate_bundles": True,   # implies MalwareSubject::deduplicate_bundles
                    "dereference_bundles": False,  # implies MalwareSubject::dereference_bundles
                    "normalize_bundles": True      # implies MalwareSubject::normalize_bundles
        },
        
        "api_key":"1a2b3c4d5e6f7"                  # API key used by this module when contacting a service
    }

The ``global_config`` dictionary (applicable to all modules) currently contains only a ``proxies`` entry, which represents a dictionary of proxy servers (HTTP or HTTPS) to use. The ``global_config`` dictionary therefore looks like:

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

-  ``generate_package_from_binary_filepath`` - given an filepath, the function returns a python-maec Package object
-  ``generate_package_from_md5`` - given an MD5 string, the function returns a python-maec Package object
-  ``set_proxies`` - optionally called to supply proxy information to the module; supplied as a dictionary like ``{ "http": "http://example.com:80", ... }``
-  ``set_api_key`` - optionally called to supply API key information to the module

If the framework attempts a particular operation, and the module does not support the particular method required for that operation, the module will simply be skipped for that operation.

Tool List
---------

Some projects with modules that currently implement the compatible tool interface are:

-  `PEFile to MAEC`_
-  `ThreatExpert to MAEC`_
-  `VirusTotal to MAEC`_

.. _PyPI: https://pypi.python.org/pypi/maec
.. _GitHub: https://github.com/MAECProject/python-maec
.. _PEFile to MAEC: https://github.com/MAECProject/pefile-to-maec
.. _ThreatExpert to MAEC: https://github.com/MAECProject/threatexpert-to-maec
.. _VirusTotal to MAEC: https://github.com/MAECProject/vt-to-maec

About MAEC
----------

Malware Attribute Enumeration and Characterization (MAEC™) is a standardized language for sharing structured information about malware based upon attributes such as behaviors, artifacts, and attack patterns.

The goal of the MAEC (pronounced "mike") effort is to provide a basis for transforming malware research and response. MAEC aims to eliminate the ambiguity and inaccuracy that currently exists in malware descriptions and to reduce reliance on signatures. In this way, MAEC seeks to improve human-to-human, human-to-tool, tool-to-tool, and tool-to-human communication about malware; reduce potential duplication of malware analysis efforts by researchers; and allow for the faster development of countermeasures by enabling the ability to leverage responses to previously observed malware instances. The MAEC Language enables correlation, integration, and automation.

Please visit the `MAEC website <https://maecproject.github.io/>`_ for more information about the MAEC Language.

Getting Help
------------

Join the public `MAEC Community Email Discussion List <https://maec.mitre.org/community/discussionlist.html>`_.

Email the MAEC Developers at maec@mitre.org.
