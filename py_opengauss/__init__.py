##
# py-postgresql root package
# http://github.com/python-postgres/fe
##
"""
py-postgresql is a Python package for using PostgreSQL. This includes low-level
protocol tools, a driver(PG-API and DB-API 2.0), and cluster management tools.

See <http://postgresql.org> for more information about PostgreSQL and <http://python.org>
for information about Python.
"""
__all__ = [
	'__author__',
	'__date__',
	'__version__',
	'__docformat__',
	'version',
	'version_info',
	'open',
]

#: The version string of py-postgresql.
version = '' # overridden by subsequent import from .project.

#: The version triple of py-postgresql: (major, minor, patch).
version_info = () # overridden by subsequent import from .project.

# Optional.
try:
	from .project import version_info, version, \
		author as __author__, date as __date__
	__version__ = version
except ImportError:
	pass

# Check that the given connection is the primary instance
def is_primary(c):
	sql = "SELECT local_role,db_state FROM pg_stat_get_stream_replications()"
	r = c.prepare(sql)()
	if r:
		# 主备实例时角色为 Primary，单实例时为 Normal
		if r[0][0] in ('Primary', 'Normal') and r[0][1] == 'Normal':
			return True
	return False

# Avoid importing these until requested.
_pg_iri = _pg_driver = _pg_param = None
def open(iri = None, prompt_title = None, **kw):
	"""
	Create a `postgresql.api.Connection` to the server referenced by the given
	`iri`::

		>>> import py_opengauss
		# General Format:
		>>> db = py_opengauss.open('pq://user:password@host:port/database')

		# Also support opengauss scheme:
		>>> db = py_opengauss.open('opengauss://user:password@host:port/database')

		# multi IP support:
		>>> db = py_opengauss.open('opengauss://user:password@host1:123,host2:456/database')

		# Connect to 'postgres' at localhost.
		>>> db = py_opengauss.open('localhost/postgres')

	Connection keywords can also be used with `open`. See the narratives for
	more information.

	The `prompt_title` keyword is ignored. `open` will never prompt for
	the password unless it is explicitly instructed to do so.

	(Note: "pq" is the name of the protocol used to communicate with PostgreSQL)
	"""
	global _pg_iri, _pg_driver, _pg_param
	if _pg_iri is None:
		from . import iri as _pg_iri
		from . import driver as _pg_driver
		from . import clientparameters as _pg_param

	return_connector = False
	if iri is not None:
		if iri.startswith('&'):
			return_connector = True
			iri = iri[1:]
		iri_params = _pg_iri.parse(iri)
		[p.pop('path', None) for p in iri_params]
	else:
		iri_params = []

	std_params = _pg_param.collect(prompt_title = None)

	# Traversal connect host for search primary
	errs = []
	for iri_param in iri_params:
		# If unix is specified, it's going to conflict with any standard
		# settings, so remove them right here.
		if 'unix' in kw or 'unix' in iri_param:
			std_params.pop('host', None)
			std_params.pop('port', None)
		params = _pg_param.normalize(
			list(_pg_param.denormalize_parameters(std_params)) + \
			list(_pg_param.denormalize_parameters(iri_param)) + \
			list(_pg_param.denormalize_parameters(kw))
		)
		_pg_param.resolve_password(params)

		C = _pg_driver.default.fit(**params)
		c = C()
		if len(iri_params) == 1:
			if return_connector:
				return C
			else:
				c.connect()
				return c
		try:
			c.connect()
		except Exception as e:
			errs.append({params.get('host'): e})
			continue
		if is_primary(c):
			return C if return_connector is True else c
		else:
			c.close()
			errs.append({params.get('host'): "not primary instance"})

	raise ConnectionError(errs)

__docformat__ = 'reStructuredText'
