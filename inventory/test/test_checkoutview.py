from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item, Checkout, Family, AgeRange

class CheckoutTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        family = Family.objects.create(lname="ValidFamily")
        family.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

        ageRange = AgeRange.objects.create(low=3, high=5) # will have value 1
        ageRange.save()

    def test_invalid_not_logged_in(self):
        response = self.client.get("/checkout/")

        # Check for redirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/checkout/')

        # Check for redirect
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.get("/checkout/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Check Out</h1>")

    def test_invalid_no_items(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post('/checkout/', data={"checkout": "", "family":"ValidFamily : (None)", "child": "Big Chungus", "age": "1"}})

        # Check if invalid
        self.assertEqual(response.status_code, 400)

        # Check if created
        self.assertEqual(Checkout.objects.filter().count(), 0)

        # Check for error message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Could not create checkout: No items added')

    def test_post_success(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

<<<<<<< HEAD
        response = self.client.post('/checkout/', data={"checkout": "", "family": "ValidFamily : (None)"}, follow=True)
=======
        response = self.client.post('/checkout/', data={"checkout": "", "family": "ValidFamily", "child": "Big Chungus", "age": "1"}, follow=True)
>>>>>>> master

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkout.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkout created.')
