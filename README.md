# Local OVAL repository managment tool

Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>

ScriptsEnvironment/scripts copyright: https://github.com/CISecurity/OVALRepo .

This tool is a wrapper for CISecurity OVALRepo modules:

- oval_decomposition.py

- build_oval_definitions_file.py

This tool adds features:

- build one xml after another;

- decompose whole folder of OVAL definitions;

- list repository by type of file (definitions, tests, etc);

- add valid `<oval_repository>` tag to file or folder;

- validate definition with xsd-schemas.

See ./docs/ for usage reference (Russian including) or help in utility.
