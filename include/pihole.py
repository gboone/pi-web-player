import requests
from include import loadconfig

class Auth(object):
	"""docstring for Auth
A set of methods for accessing the auth endpoints on a pi hole
	"""
	def __init__(self, arg):
		super(Auth, self).__init__()
		if arg:
			self.arg = arg
		else:
			self.arg = loadconfig.loadconfig("config.yml")

	def auth(self):
		pass

class Metrics(object):
	"""docstring for Metrics"""
	def __init__(self, arg, **kwargs):
		super(Metrics, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class DNS(object):
	"""docstring for DNS"""
	def __init__(self, arg, **kwargs):
		super(DNS, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class Groups(object):
	"""docstring for Groups"""
	def __init__(self, arg, **kwargs):
		super(Groups, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class Domains(object):
	"""docstring for Domains"""
	def __init__(self, arg, **kwargs):
		super(Domains, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class Clients(object):
	"""docstring for Clients"""
	def __init__(self, arg, **kwargs):
		super(Clients, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class Lists(object):
	"""docstring for Lists"""
	def __init__(self, arg, **kwargs):
		super(Lists, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class FTL(object):
	"""docstring for FTL"""
	def __init__(self, arg, **kwargs):
		super(FTL, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class Teleporter(object):
	"""docstring for Teleporter"""
	def __init__(self, arg, **kwargs):
		super(Teleporter, self).__init__()
		self.arg = arg
		self.kwargs = kwargs
		
class Network(object):
	"""docstring for Network"""
	def __init__(self, arg, **kwargs):
		super(Network, self).__init__()
		self.arg = arg
		self.kwargs = kwargs
		
class Actions(object):
	"""docstring for Actions"""
	def __init__(self, arg, **kwargs):
		super(Actions, self).__init__()
		self.arg = arg
		self.kwargs = kwargs
		
class Config(object):
	"""docstring for Config"""
	def __init__(self, arg, **kwargs):
		super(Config, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

	def getHosts():
		print("hello")
		
class DHCP(object):
	"""docstring for DHCP"""
	def __init__(self, arg, **kwargs):
		super(DHCP, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

class requestAPI(object):
	"""docstring for requestAPI"""
	def __init__(self, arg, **kwargs):
		super(requestAPI, self).__init__()
		self.arg = arg
		self.kwargs = kwargs

	def get(url, **kwargs):
		requests.get(url, args)
		pass

	def post(url, **kwargs):
		requests.post(url, data=args)
		pass

	def patch(url, **kwargs):
		requsets.patch(url, data=args)
		pass

	def put(url, **kwargs):
		requests.put(url, args)
		pass

	def delete(url, **kwargs):
		requests.delete(url, args)
		pass

