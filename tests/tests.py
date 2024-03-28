import unittest
from include import pihole

class MyTest(unittest.TestCase):
	# This test is an example 
	def test(self):
		self.assertEqual(2+2,4)

	def testPiHoleAuth(self):
		p = pihole.Auth()
		self.assertISInstance(p.auth(), 'Class')
		