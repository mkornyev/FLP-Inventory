from django.test import TestCase

# name other test files test_*.py in this directory to have them run
class SampleTestCase(TestCase):
    def setUp(self):
        pass

    def test_true(self):
        assert(True)
