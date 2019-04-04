from django.core.cache import cache
from hashlib import md5

def cache_method(method, timeout=3600):

	def wrapper(*args, **kwargs):
		
		key = md5(repr(method).encode('utf-8'))
		for arg in args:
			key.update(repr(arg).encode('utf-8'))
		for kwarg_key, kwarg_value in kwargs.items():
			key.update(repr(kwarg_key).encode('utf-8'))
			key.update(repr(kwarg_value).encode('utf-8'))
		key = key.hexdigest()
		result = cache.get(key)
		if not result:
			result = method(*args, **kwargs)
			cache.set(key, result, timeout)

		return result

	return wrapper
