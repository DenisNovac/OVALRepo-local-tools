import modules.submodules.Validator as Validator
import logging

e_log = logging.getLogger()
e_log.setLevel(logging.ERROR)

i_log = logging.getLogger()
i_log.setLevel(logging.INFO)


def validate_definition(args):
    v = Validator.Validator()
    xml = vars(args)['xml']
    xsd = vars(args)['xsd']

    res = v.validate(xml, xsd)
    if res[0] == 0:
        i_log.info('Validation successful')
    else:
        e_log.error("Validation failure")
    v.clear_wrapper()


def validate_definition_cli(xml_path, xsd_path) -> bool:
    v = Validator.Validator()
    res = v.validate(xml_path, xsd_path)
    if res[0] == 0:
        i_log.info('Validation successful')
    else:
        e_log.error("Validation failure")

    v.clear_wrapper()
    return res
