# OVAL Validator

OVAL Validator is a standalone module for validation OVAL Content. It may use any OVAL schemas set for validations of any OVAL content. It makes validation in several steps:

- Determine which namespaces are used in file;
- Create "Wrapper" file with import of all OVAL common schemas (such as common, definitions, variables, etc.) and ONLY used in file);
- Import in the Wrapper schemas of used namespaces (such as definitions for windows, linux, etc.);
- Validate given OVAL content through this Wrapper file;
- Remove Wrapper.

Wrapper usage is a common method of XML Validation through several XML-Schemas at one time. When it comes to OVAL - there is always several schemas at one time. For example, if you want to validate OVAL Results file - you'll need to use definition, system characteristics and results schema at one time. 

Example of wrapper for OVAL-results with namespaces "independent" and "windows":
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-definitions-5#independent" schemaLocation="independent-definitions-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-system-characteristics-5#independent" schemaLocation="independent-system-characteristics-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-common-5" schemaLocation="oval-common-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-definitions-5" schemaLocation="oval-definitions-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-directives-5" schemaLocation="oval-directives-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-results-5" schemaLocation="oval-results-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-system-characteristics-5" schemaLocation="oval-system-characteristics-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-variables-5" schemaLocation="oval-variables-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" schemaLocation="windows-definitions-schema.xsd"/>
<xsd:import namespace="http://oval.mitre.org/XMLSchema/oval-system-characteristics-5#windows" schemaLocation="windows-system-characteristics-schema.xsd"/>
</xsd:schema>
```

OVAL Validator may be used in **main lrm.py module** (with option "v") or like standalone app (you'll need to import it in your code).