from credentials import parse_credentials
from parse_rest.connection import register
from parse_rest.datatypes import Object

register(parse_credentials['application_id'], parse_credentials['rest_api_key'])
