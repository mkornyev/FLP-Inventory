from django.test import TestCase

from inventory.forms import AddItemForm
from inventory.models import Item

class AddItemFormTestCase(TestCase):
    def setUp(self):
        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

    def test_invalid_required_fields(self):
        form = AddItemForm(data={})

        self.assertEqual(
            form.errors["item"], ["This field is required."]
        )

        self.assertEqual(
            form.errors["quantity"], ["This field is required."]
        )

    def test_invalid_long_name(self):
        form = AddItemForm(data={"item": "This is a very long name that is over fifty characters"})

        self.assertEqual(
            form.errors["item"], ["Ensure this value has at most 50 characters (it has 54)."]
        )

    def test_invalid_does_not_exist(self):
        form = AddItemForm(data={"item": "InvalidItem"})

        self.assertEqual(
            form.errors["item"], ["Item does not exist."]
        )
        
    def test_invalid_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "quantity": -1})

        self.assertEqual(
            form.errors["quantity"], ["Quantity must be above zero."]
        )
