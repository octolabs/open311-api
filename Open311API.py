import json
from pymongo import json_util
from OpenAPI.OpenAPI import APIHandler


class Open311Service(APIHandler):
	enforceAPIKey = True
	apiKeyType = 'Open311 Write'

	def getServiceTypes(self):
		raise NotImplementedError('getServiceTypes should be defined in the subclass.')


	def getServiceTypeDefinitions(self, servicecode):
		raise NotImplementedError('getServiceTypeDefinitions should be defined in the subclass.')


	def submitServiceRequest(self, ):
		raise NotImplementedError('submitServiceRequest should be defined in the subclass.')


	#returns service request based on service request ID
	def _get(self, args):
		pass


	#returns list of service request types
	def meta_getTypesList(self, args):
		if self.format() == "json":
			self.write( json.dumps( self.getServiceTypes(),
				default=json_util.default ) )
		elif self.format() == "xml":
			self.write("<msg>n/a</msg>")


	def meta_getTypeDefinition(self, args):
	#returns list of all fields in requested SR type
		if self.format() == "json":
			self.write( json.dumps( self.getServiceTypeDefinitions(args.get('servicecode', [None])[0]),
				default=json_util.default ) )
		elif self.format() == "xml":
			self.write("<msg>n/a</msg>")


	#submits service request to 311 system	
	def submit(self, args):
		try:
			serviceType = self.getServiceTypeDefinitions(args.get('servicecode', [None])[0])
		except:
			raise error.HTTPError(400, 
				"Open311 submitServiceRequest failed, Invalid ServiceType.")

		address = args.get('address')
		if not address:
			raise error.HTTPError(400, 
				"Open311 submitServiceRequest failed, address parameter missing")

		description = args.get('description')
		if not description:
			raise error.HTTPError(400, 
				"Open311 submitServiceRequest failed, description parameter missing")

		self.submitServiceRequest(serviceType, address, description)
		
		#self.write(data)
