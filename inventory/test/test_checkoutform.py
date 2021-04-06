from django.test import TestCase

from inventory.forms import CheckOutForm
from inventory.models import Family

class CheckoutFormTestCase(TestCase):
    def setUp(self):
        family = Family.objects.create(name="ValidFamily")
        family.save()

    def test_invalid_required_fields(self):
        form = CheckOutForm(data={})

        self.assertEqual(
            form.errors["family"], ["This field is required."]
        )

    def test_invalid_family_length(self):
        form = CheckOutForm(data={"family": "This is a very long name that is over fifty characters"})

        self.assertEqual(
            form.errors["family"], ["Ensure this value has at most 50 characters (it has 54)."]
        )

    def test_invalid_family_exists(self):
        form = CheckOutForm(data={"family": "InvalidFamily"})

        self.assertEqual(
            form.errors["family"], ["Family does not exist."]
        )
