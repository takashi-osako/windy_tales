'''
Created on May 2, 2013

@author: dorisip
'''
from windy_tales.utils.utils import read_file
from windy_tales.flat_file.header_parser import HeaderParser


def flat_file_to_json(flat_file):
    '''
    Reads flat file, and returns flat file content to json
    '''
    # Get the Header Template
    template = HeaderParser.get_template()

    # Read flat file
    content = read_file(flat_file)

    (rtn_result, rtn_content) = __fill_values_with_content(template, content)

    if len(rtn_content) != 0:
        print("non zero flat file content! Remaining Content: %s", rtn_content)

    return rtn_result


def __fill_values_with_content(json_obj, flat_content):
    '''
    Given a ordered dict generated based on interpretation of header file, and the content of the flat file,
    Returns a json ordered dict with values filled in from content in flat file
    '''
    if type(json_obj) is list:
        for i in range(len(json_obj)):
            (json_obj[i], flat_content) = __fill_values_with_content(json_obj[i], flat_content)
    else:
        for (key, value) in json_obj.items():
            # leaf nodes have int as values
            if type(value) is int:
                if len(flat_content) == 0:
                    json_obj[key] = ""
                else:
                    if (len(flat_content) < value):
                        value = len(flat_content)
                    # Trim white spaces
                    json_obj[key] = flat_content[0: value].strip()
                    flat_content = flat_content[value:]
            else:
                (json_obj[key], flat_content) = __fill_values_with_content(value, flat_content)

    return (json_obj, flat_content)
