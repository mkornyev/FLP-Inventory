
from django.test import TestCase

from inventory.management.commands import trans

class CheckoutMapTestCase(TestCase):
    def test_invalid_input(self):
        invalidName1 = "shoes"
        invalidName2 = "shoes"
        self.assertRaises(Exception, trans.Command.itemMap, invalidName1)
        self.assertRaises(Exception, trans.Command.itemMap, invalidName2)

    def test_valid_input(self):
        validName1 = "shorts (baby boy)"
        validName2 = "girls shoes kid 6"
        item1, size1 = trans.Command.itemMap(validName1)
        item2, size2 = trans.Command.itemMap(validName2)
        self.assertEqual(item1, "shorts")
        self.assertEqual(size1, "baby")
        self.assertEqual(item2, "shoes")
        self.assertEqual(size2, "kid")