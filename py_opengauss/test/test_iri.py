##
# .test.test_iri
##
import unittest
import py_opengauss.iri as pg_iri

value_errors = (
	# Invalid scheme.
	'http://user@host/index.html',
)

iri_samples = (
	'host/dbname/path?param=val#frag',
	'#frag',
	'?param=val',
	'?param=val#frag',
	'user@',
	':pass@',
	'u:p@h',
	'u:p@h:1',
	'postgres://host/database',
	'pq://user:password@host:port/database?setting=value#public,private',
	'pq://fæm.com:123/õéf/á?param=val',
	'pq://l»»@fæm.com:123/õéf/á?param=val',
	'pq://fæᎱᏋm.com/õéf/á?param=val',
	'pq://fæᎱᏋm.com/õéf/á?param=val&[setting]=value',
)

sample_structured_parameters = [
	{
		'host' : 'hostname',
		'port' : '1234',
		'database' : 'foo_db',
	},
	{
		'user' : 'username',
		'database' : 'database_name',
		'settings' : {'foo':'bar','feh':'bl%,23'},
	},
	{
		'user' : 'username',
		'database' : 'database_name',
	},
	{
		'database' : 'database_name',
	},
	{
		'user' : 'user_name',
	},
	{
		'host' : 'hostname',
	},
	{
		'user' : 'username',
		'password' : 'pass',
		'host' : '',
		'port' : '4321',
		'database' : 'database_name',
		'path' : ['path'],
	},
	{
		'user' : 'user',
		'password' : 'secret',
		'host' : '',
		'port' : 'ssh',
		'database' : 'database_name',
		'settings' : {
			'set1' : 'val1',
			'set2' : 'val2',
		},
	},
	{
		'user' : 'user',
		'password' : 'secret',
		'host' : '',
		'port' : 'ssh',
		'database' : 'database_name',
		'settings' : {
			'set1' : 'val1',
			'set2' : 'val2',
		},
		'connect_timeout' : '10',
		'sslmode' : 'prefer',
	},
]

class test_iri(unittest.TestCase):
	def testAlternateSchemes(self):
		field = pg_iri.parse("postgres://host")['host']
		self.assertEqual(field, 'host')

		field = pg_iri.parse("postgresql://host")['host']
		self.assertEqual(field, 'host')

		try:
			pg_iri.parse("reject://host")
		except ValueError:
			pass
		else:
			self.fail("unacceptable IRI scheme not rejected")

	def testIP6Hosts(self):
		"""
		Validate that IPv6 hosts are properly extracted.
		"""
		s = [
			('pq://[::1]/db', '::1'),
			('pq://[::1]:1234/db', '::1'),
			('pq://[1:2:3::1]/db', '1:2:3::1'),
			('pq://[1:2:3::1]:1234/db', '1:2:3::1'),
			('pq://[]:1234/db', ''),
			('pq://[]/db', ''),
		]
		for i, h in s:
			p = pg_iri.parse(i)
			self.assertEqual(p['host'], h)

	def testPresentPasswordObscure(self):
		"""
		Password is present in IRI, and obscure it.
		"""
		s = 'pq://user:pass@host:port/dbname'
		o = 'pq://user:***@host:port/dbname'
		p = pg_iri.parse(s)
		ps = pg_iri.serialize(p, obscure_password = True)
		self.assertEqual(ps, o)

	def testPresentPasswordObscure(self):
		"""
		Password is *not* present in IRI, and do nothing.
		"""
		s = 'pq://user@host:port/dbname'
		o = 'pq://user@host:port/dbname'
		p = pg_iri.parse(s)
		ps = pg_iri.serialize(p, obscure_password = True)
		self.assertEqual(ps, o)

	def testValueErrors(self):
		for x in value_errors:
			self.assertRaises(ValueError,
				pg_iri.parse, x
			)

	def testParseSerialize(self):
		scheme = 'pq://'
		for x in iri_samples:
			px = pg_iri.parse(x)
			spx = pg_iri.serialize(px)
			pspx = pg_iri.parse(spx)
			self.assertTrue(
				pspx == px,
				"parse-serialize incongruity, %r -> %r -> %r : %r != %r" %(
					x, px, spx, pspx, px
				)
			)
			spspx = pg_iri.serialize(pspx)
			self.assertTrue(
				spx == spspx,
				"parse-serialize incongruity, %r -> %r -> %r -> %r : %r != %r" %(
					x, px, spx, pspx, spspx, spx
				)
			)

	def testSerializeParse(self):
		for x in sample_structured_parameters:
			xs = pg_iri.serialize(x)
			uxs = pg_iri.parse(xs)
			self.assertTrue(
				x == uxs,
				"serialize-parse incongruity, %r -> %r -> %r" %(
					x, xs, uxs,
				)
			)

if __name__ == '__main__':
	unittest.main()
