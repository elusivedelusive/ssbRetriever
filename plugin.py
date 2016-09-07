import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from SSBRequester import ssbRequest
from jinja2 import Environment

def test():
	return "hello world"

def show_query_form(url):
	query = '''{
	  "query": [
	    {
	      "code": "Region",
	      "selection": {
		"filter": "item",
		"values": [
		  "1103"
		]
	      }
	    }
	  ],
	  "response": {
	    "format": "json-stat"
	  }
	}'''

	response = ssbRequest(url, query)

	return response

class ssbRetriever(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
	toolkit.add_resource('templates/js','js')

    def get_helpers(self):
	return {'ssbRetriever_test':test,
	'ssbRetriever_show_query': show_query_form,
	}
