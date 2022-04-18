from django.test import TestCase

from inventory.forms import AddItemForm
from inventory.models import Item

class AddItemFormTestCase(TestCase):
    def setUp(self):
        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

    def test_invalid_required_fields(self):
        form = AddItemForm(data={})

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["item"], ["This field is required."]
        )

    def test_invalid_long_name(self):
        form = AddItemForm(data={"item": "This is a very long name that is over fifty characters"})

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["item"], ["Ensure this value has at most 50 characters (it has 54)."]
        )

    def test_invalid_does_not_exist(self):
        form = AddItemForm(data={"item": "InvalidItem"})

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["item"], ["Item does not exist."]
        )
        
    def test_invalid_used_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": -1})

        self.assertEqual(
            form.errors["used_quantity"], ["Quantity must be above zero."]
        )

    def test_invalid_new_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "new_quantity": -1})

        self.assertEqual(
            form.errors["new_quantity"], ["Quantity must be above zero."]
        )

    def test_success_used_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": 1})

        self.assertTrue(form.is_valid())

    def test_success_new_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "new_quantity": 1})

        self.assertTrue(form.is_valid())

    def test_success_used_and_new_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": 1,
                                 "new_quantity": 1})

        self.assertTrue(form.is_valid())

    def test_invalid_used_and_new_quantity(self):
        form = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": -1,
                                 "new_quantity": 1})

        form2 = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": 1,
                                 "new_quantity": -1})

        form3 = AddItemForm(data={"item": "ValidItem",
                                 "used_quantity": -1,
                                 "new_quantity": -1})

        self.assertFalse(form.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())

