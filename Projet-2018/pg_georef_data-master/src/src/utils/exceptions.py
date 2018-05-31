# define Python user-defined exceptions


class Error(Exception):
	"""Base class for other exceptions"""
	pass



"""KWARGS AND OPTIONAL PARAMETERS EXCEPTIONS"""

class OptionNotFound(Error):
	"""Raised when an option is defined, but any value is corresponding"""
	pass


class ValueNotMatchOption(Error):
	"""Raised when an option is defined, but any value is corresponding"""
	pass


class FolderAlreadyExists(Error):
	"""Raised when an option is defined, but any value is corresponding"""
	pass


