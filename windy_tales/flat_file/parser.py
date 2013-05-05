'''
Created on May 2, 2013

@author: dorisip
'''
import os
from pycparser import parse_file
from pycparser.c_ast import ArrayDecl, IdentifierType, Struct,\
    TypeDecl
from collections import OrderedDict
import json
import copy
from windy_tales.utils.utils import read_file


def flat_file_to_json(flat_file):
    '''
    Parses C header file, Reads flat file, Returns flat file content to json
    '''
    os.environ['PATH'] += os.pathsep + '/usr/bin'
    here = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(here, '..', 'resources', 'test.h')

    # Calls pycparser to precompile and parse the C header file
    ast = parse_c_header_file(file_name)

    # Go through each 'struct' that was parsed
    # Theoretically there should only be one struct per header file
    for child in ast.ext:
        result = parse_ast_to_json(child)
        content = read_file(flat_file)
        # print(json.dumps(result))

        (rtn_result, rtn_content) = fill_values_with_content(result, content)

        if len(rtn_content) != 0:
            print("non zero flat file content! Remaining Content: %s", rtn_content)

    return json.dumps(rtn_result)


def parse_c_header_file(file_name):
    '''
    Parses a C header file, returning an AST representation
    '''
    # TODO:  If header file is static, we should only parse it once and save it
    os.environ['PATH'] += os.pathsep + '/usr/bin'

    # Calls pycparser to precompile and parse the C header file
    ast = parse_file(file_name, use_cpp=True, cpp_path='/usr/bin/cpp-4.2')
    # Prints out parsed file structure for debugging
    #ast.show(attrnames=True, nodenames=True)

    return ast


def parse_ast_to_json(node):
    '''
    Given an AST node, creates an ordered dict representing the structure of the header file
    from header:
    struct address {
        char address_line1[20];
        char country[2];
    };
    generates the following ordered dict: {"address": {"address_line1": 20, "country": 2}}
    '''
    result = OrderedDict()
    node_type = node.type

    if node_type.name:
        struct_name = node_type.name
    elif node_type.declname:
        struct_name = node_type.declname

    result[struct_name] = OrderedDict()
    for decl in node_type.decls:
        decl_type = decl.type
        if type(decl_type) is ArrayDecl:
            __size = int(decl_type.dim.value)
            __type = decl_type.type.type
            __name = decl_type.type.declname
            if type(__type) is IdentifierType:
                __format = __type.names[0]
                result[struct_name][__name] = __size
            elif type(__type) is Struct:
                struct_result = parse_ast_to_json(decl_type.type)
                result[struct_name][__name] = []
                for i in range(__size):
                    # Make a deep copy of the json object
                    result[struct_name][__name].append(copy.deepcopy(struct_result))
        elif type(decl_type) is TypeDecl:
            __name = decl_type.declname
            if type(decl_type.type) is Struct:
                struct_result = parse_ast_to_json(decl_type)
                result[struct_name][__name] = struct_result
            elif type(decl_type.type) is IdentifierType:
                # datatypes such as int falls into here
                pass
    return result


def fill_values_with_content(json_obj, flat_content):
    '''
    Given a ordered dict generated based on interpretation of header file, and the content of the flat file,
    Returns a json ordered dict with values filled in from content in flat file
    '''
    if type(json_obj) is list:
        for i in range(len(json_obj)):
            (json_obj[i], flat_content) = fill_values_with_content(json_obj[i], flat_content)
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
                (json_obj[key], flat_content) = fill_values_with_content(value, flat_content)

    return (json_obj, flat_content)
