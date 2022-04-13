from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item, Checkout, Family, AgeRange
from inventory.views import generate_report
from django.core.handlers.wsgi import WSGIRequest
from django.http import QueryDict
from io import StringIO

class GenerateReportTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        family = Family.objects.create(lname="ValidFamily")
        family.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

        ageRange = AgeRange.objects.create(low=3, high=5) # will have value 1
        ageRange.save()
        

    # def test_checkin_report(self):
    #     response = self.client.get("/checkin/")

    #     # Check for redirect
    #     self.assertEqual(response.status_code, 302)

    #     response = self.client.post('/checkin/')

    #     # Check for redirect
    #     self.assertEqual(response.status_code, 302)

    def test_checkout_report(self):
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

        reportResponse = self.client.post('/report/', 
            data={
                'POST': 
                    QueryDict('tx-type=Checkout&start-date=2022-03-18&end-date=2022-03-25&csrfmiddlewaretoken=gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R&export_table='),
                'REQUEST_METHOD': 'POST',
                'PATH_INFO': '/report/',
                'wsgi.input': StringIO()
            }, follow=True)
        # body = QueryDict('tx-type=Checkout&start-date=2022-03-18&end-date=2022-03-25&csrfmiddlewaretoken=gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R&export_table=')
        # req = {
        #   'user': 'admin',
        #   'REQUEST_METHOD': 'POST',
        #   'PATH_INFO': '/report/',
        #   'wsgi.input': StringIO(),
        #   'POST': body}

        # reportResponse = generate_report(req)

        # Check if valid
        # self.assertEqual(reportResponse.status_code, 200)
        # self.assertEqual(reportResponse['Content-Disposition'], 'attachment; filename=CheckoutReport 2022-03-18 to 2022-03-25.csv')
        # self.assertEqual(reportResponse.content, )
        # print("TESTING: " + str(reportResponse.content))

    # def test_checkingbi_report(self):
        # self.client.login(username='testuser', password='12345')

        # response = self.client.post('/checkin/', data={"checkin": ""})

        # # Check if invalid
        # self.assertEqual(response.status_code, 400)

        # # Check if created
        # self.assertEqual(Checkin.objects.filter().count(), 0)

        # # Check for error message
        # messages = list(response.context['messages'])
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), 'Could not create checkin: No items added')

    # def test_checkoutgbi_report(self):
        # self.client.login(username='testuser', password='12345')

        # # Add item transaction
        # session = self.client.session
        # session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        # session.save()

        # response = self.client.post('/checkin/', data={"checkin": ""}, follow=True)

        # # Check if valid
        # self.assertEqual(response.status_code, 200)

        # # Check if created
        # self.assertEqual(Checkin.objects.filter().count(), 1)

        # # Check for message
        # messages = list(response.context['messages'])
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), 'Checkin created.')
