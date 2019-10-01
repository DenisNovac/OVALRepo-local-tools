import modules.submodules.Validator as Validator

def validate_definition ( args ):
    v = Validator.Validator()
    xml = vars(args)['xml']
    xsd = vars(args)['xsd']
    if v.isValid(xml, xsd):
        print('Validation successful.')
    v.clear_wrapper()
    return