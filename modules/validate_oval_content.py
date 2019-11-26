import modules.submodules.OVALValidator as OVALValidator
import logging

e_log = logging.getLogger('lrm_error')
i_log = logging.getLogger('lrm_info')

def validate_oval_content(args):
    v = OVALValidator.OVALValidator()
    xml = vars(args)['xml']
    xsd = vars(args)['xsd']

    res = v.validate(xml, xsd)
    if res:
        i_log.info('Validation successful')
    else:
        e_log.error("Validation failure")
    v.clear_wrapper()
