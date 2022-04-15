from django.test import TestCase
from django.contrib.auth.models import User
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from inventory.models import Checkout

class ExportDriveTestCase(TestCase):
    def setUp(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        

    def test_checkout(self):
        qs = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=ItemReport ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'


    def test_checkin(self):
        response = self.client.post('/checkout/', data={"checkout": "", "family":"ValidFamily : (None)", "child": "Big Chungus", "age": "1"})

    def test_checkout_by_item(self):
        response = self.client.post('/checkout/', data={"checkout": "", "family":"ValidFamily : (None)", "child": "Big Chungus", "age": "1"})

    def test_checkin_by_item(self):
        response = self.client.post('/checkout/', data={"checkout": "", "family":"ValidFamily : (None)", "child": "Big Chungus", "age": "1"})

    def test_invalid_not_logged_in(self):
        response = self.client.get("/checkout/")

        # Check for redirect
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/checkout/')

        # Check for redirect
        self.assertEqual(response.status_code, 302)


    def test_invalid_no_items(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post('/checkout/', data={"checkout": "", "family":"ValidFamily : (None)", "child": "Big Chungus", "age": "1"})

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

        response = self.client.post('/checkout/', data={"checkout": "", "family": "ValidFamily : (None)", "child": "Big Chungus", "age": "1"}, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkout.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkout created.')
