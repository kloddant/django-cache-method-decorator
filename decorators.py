from django.core.cache import cache
from hashlib import md5
from functools import wraps
import psutil

def cache_method(timeout=300):

	def outer_wrapper(view_func):

		@wraps(view_func)
		def inner_wrapper(*args, **kwargs):

			key = md5(repr(view_func).encode('utf-8'))
			for arg in args:
				key.update(repr(arg).encode('utf-8'))
				if hasattr(arg, 'pk'):
					key.update(str(arg.pk).encode('utf-8'))
			for kwarg_key, kwarg_value in kwargs.items():
				key.update(repr(kwarg_key).encode('utf-8'))
				key.update(repr(kwarg_value).encode('utf-8'))
			key = key.hexdigest()
			result = cache.get(key)
			if not result:
				result = view_func(*args, **kwargs)
				percent_memory_usage = psutil.virtual_memory()[2]
				if percent_memory_usage < 90:
					cache.set(key, result, timeout)

			return result

		return inner_wrapper

	return outer_wrapper
