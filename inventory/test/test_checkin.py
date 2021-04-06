from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

from inventory.models import Item, Checkin

class CheckinTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

    def test_invalid_not_logged_in(self):
        response = self.client.get("/checkin/")

        # Check for redirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/checkin/')

        # Check for redirect
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        logged_in = self.client.login(username='testuser', password='12345')

        response = self.client.get("/checkin/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Check In Items:</h1>")

    def test_invalid_no_items(self):
        logged_in = self.client.login(username='testuser', password='12345')

        response = self.client.post('/checkin/')

        # Check if invalid
        self.assertEqual(response.status_code, 400)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 0)

        # Check for error message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Could not create checkin: No items added')

    def test_post_success(self):
        logged_in = self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/checkin/', follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkin created.')
