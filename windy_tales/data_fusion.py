'''
Created on May 11, 2013

@author: dorisip
'''
from cloudy_tales.database.connection import DbConnection
from windy_tales.database.collections.genericCollection import GenericCollection
import json
from bson import json_util
from cloudy_tales.data_fusion.translate import generate_templated_json
from cloudy_tales.utils.exporter import export


def template_json(data):
    # Temporary template the flat file's data and save to /tmp/template.json
    with DbConnection('sunny') as sunny_connection:
        template_col = GenericCollection(sunny_connection, 'templates')
        templ = json.dumps(template_col.find_one(), default=json_util.default)
        # use mustache
        generated = generate_templated_json(templ, data['metadata'])
        # Write to /tmp/template.json
        export(json.loads(generated))
