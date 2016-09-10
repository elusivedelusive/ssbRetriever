import logging
from urllib import urlencode
import datetime
import mimetypes
import cgi

from pylons import config
from paste.deploy.converters import asbool
import paste.fileapp

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.maintain as maintain
import ckan.lib.i18n as i18n
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.plugins as p
import ckan.lib.render
import requests,json

from ckan.common import OrderedDict, _, json, request, c, g, response
from ckan.controllers.package import PackageController
from ckanext.ssbRetriever.utils import execute_simple_post_query, multipart_post

log = logging.getLogger(__name__)

render = base.render
abort = base.abort
redirect = base.redirect

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin

log = logging.getLogger(__name__)

class SSBController(PackageController):
    def new_resource_ssb(self):
	packageID = request.params.get('id')
	#unpack variables from the request object
	log.warning("================CONTROLLER=====================")
	if request.params.get('url') != " ":
		redirect(h.url_for(controller='package', action='new_resource', id=packageID))
	queryUrl = request.params.get('query-url')
	queryText = request.params.get('query-text')
	name = request.params.get('name')
	description = request.params.get('description')

	#query ssb using the input query text and url
	ssbResponse = execute_simple_post_query(queryUrl, queryText)
	#set the upload parameter to be the responsetext. This uploads data from the memory as if it was a file
	filesRequests ={'upload': ('ssbData.csv', ssbResponse.text)}
	
	#the admin users authorization key
	headers = {"Authorization": "f65b83f5-c14a-4440-b07f-3be58acb686a"}
	
	#the url to the resource_create action api 
	ckanurl = "http://localhost/api/action/resource_create"

	#parameters NB url has to be an empty string to successfully post a file
	params= {'description': description,'package_id': packageID,'name': name, "url": " "}
	
	#use the multipart_post function to perform a post
	postResponse = multipart_post(ckanurl, filesRequests, headers, params)

	log.warning("PACKAGEID: " + packageID)
	log.warning("URL: " + queryUrl)
	log.warning("QUERY: " + queryText)
	log.warning("SSBRESPONSE: " + ssbResponse.text)
	log.warning("POSTRESPONSE: " + postResponse.text)
	log.warning("================CONTROLLER=====================")

	#redirect user to the dataset overview page
        redirect(h.url_for(controller='package', action='read', id=packageID))

