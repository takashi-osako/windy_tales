'''
Created on May 5, 2013

@author: dorisip
'''
import os
from pycparser import parse_file
import copy
from pycparser.c_ast import ArrayDecl, IdentifierType, Struct,\
    TypeDecl
from collections import OrderedDict


class HeaderParser():
    '''
    Parser for C header file
    Parses to json format
    '''

    # Just make these everything static for now
    # Parsed_template is an ordered dictionary
    parsed_template = None
    ast = None

    @staticmethod
    def generate_tempate():
        # Assumption: we only have one header file
        os.environ['PATH'] += os.pathsep + '/usr/bin'
        here = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(here, '..', 'resources', 'test.h')

        HeaderParser.__parse_c_header_file(file_name)

    @staticmethod
    def get_template():
        '''
        Return a deep copy version of it
        '''
        return copy.deepcopy(HeaderParser.parsed_template)

    @staticmethod
    def __parse_c_header_file(file_name):
        '''
        Parses a C header file, returning an AST representation
        '''
        os.environ['PATH'] += os.pathsep + '/usr/bin'

        # Calls pycparser to precompile and parse the C header file
        HeaderParser.ast = parse_file(file_name, use_cpp=True, cpp_path='/usr/bin/cpp-4.2')
        # Prints out parsed file structure for debugging
        #ast.show(attrnames=True, nodenames=True)

        # Theoretically there should only be one struct per header file
        if len(HeaderParser.ast.ext) > 1:
            print("Warning, header file has more than 1 struct.  Only the first one will be used")

        result = HeaderParser.__parse_ast_to_json(HeaderParser.ast.ext[0])

        # result is an ordered dictionary
        HeaderParser.parsed_template = result

    @staticmethod
    def __parse_ast_to_json(node):
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
                    struct_result = HeaderParser.__parse_ast_to_json(decl_type.type)
                    result[struct_name][__name] = []
                    for i in range(__size):
                        # Make a deep copy of the json object
                        result[struct_name][__name].append(copy.deepcopy(struct_result))
            elif type(decl_type) is TypeDecl:
                __name = decl_type.declname
                if type(decl_type.type) is Struct:
                    struct_result = HeaderParser.__parse_ast_to_json(decl_type)
                    result[struct_name][__name] = struct_result
                elif type(decl_type.type) is IdentifierType:
                    # datatypes such as int falls into here
                    pass
        return result
