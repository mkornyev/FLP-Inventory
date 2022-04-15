from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item, Checkout, Checkin, Family, AgeRange
from django.http.request import QueryDict, MultiValueDict
from datetime import date, timedelta

class GenerateReportLocalTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        family = Family.objects.create(lname="ValidFamily")
        family.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

        ageRange = AgeRange.objects.create(low=3, high=5) # will have value 1
        ageRange.save()

    def test_generate_noitems(self):
        self.client.login(username='testuser', password='12345')

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkin'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(len(response.context['results']), 0)
 
    def test_generate_checkin_report(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/checkin/', data={"checkin": ""}, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkin created.')

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkin'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(str(response.context['results'][0].items.count()), '1')
        self.assertEqual(str(response.context['results'][0].items.first()), '(ValidItem, 2, Used)')

    def test_generate_checkout_report(self):
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

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkout'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(str(response.context['results'][0].items.count()), '1')
        self.assertEqual(str(response.context['results'][0].items.first()), '(ValidItem, 2, Used)')

    def test_generate_checkingbi_report(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/checkin/', data={"checkin": ""}, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkin created.')

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkin'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')],
            'itemizedOutput': ['itemized'], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(response.context['results'][0]['item'], 'ValidItem')
        self.assertEqual(response.context['results'][0]['is_new'], False)
        self.assertEqual(response.context['results'][0]['quantity'], 2)

    def test_generate_checkoutgbi_report(self):
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

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkout'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')],
            'itemizedOutput': ['itemized'],  
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(response.context['results'][0]['item'], 'ValidItem')
        self.assertEqual(response.context['results'][0]['is_new'], False)
        self.assertEqual(response.context['results'][0]['quantity'], 2)

    def test_export_checkin_report(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/checkin/', data={"checkin": ""}, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkin created.')

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkin'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            'export_table': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=Checkin Report ' + weekAgo.strftime('%Y-%m-%d') +  ' to ' + today.strftime('%Y-%m-%d') + '.csv')
        self.assertContains(response, 'id,user,datetime,notes,items,value')
        self.assertContains(response, 'testuser')
        self.assertContains(response, '"(ValidItem, 2, Used)",0')

    def test_export_checkout_report(self):
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

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkout'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            'export_table': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        # Check if valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=Checkout Report ' + weekAgo.strftime('%Y-%m-%d') +  ' to ' + today.strftime('%Y-%m-%d') + '.csv')
        self.assertContains(response, 'id,user,datetime,family,childName,ageRange,notes,items,value')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'ValidFamily,Big Chungus,3 - 5,,"(ValidItem, 2, Used)",0')

    def test_export_checkingbi_report(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-in'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/checkin/', data={"checkin": ""}, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)

        # Check if created
        self.assertEqual(Checkin.objects.filter().count(), 1)

        # Check for message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Checkin created.')

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkin'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'itemizedOutput': ['itemized'],
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            'export_table': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=Checkin Report By Item ' + weekAgo.strftime('%Y-%m-%d') +  ' to ' + today.strftime('%Y-%m-%d') + '.csv')
        self.assertContains(response, 'id,item,category,is_new,quantity,value,new/used price')
        self.assertContains(response, 'ValidItem,No category,False,2,0')

    def test_export_checkoutgbi_report(self):
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

        today = date.today()
        weekAgo = today - timedelta(days=7)
        dictionary = {
            'tx-type': ['Checkout'],
            'start-date': [weekAgo.strftime('%Y-%m-%d')], 
            'end-date': [today.strftime('%Y-%m-%d')], 
            'itemizedOutput': ['itemized'],
            'csrfmiddlewaretoken': ['gorIARWkwGHd78mWsRPmvQIGcaE6FGtCxmo0tWApqHWmxKN35j6zUeI5R8yysl5R'], 
            'export': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        response = self.client.post('/report/', qdict, follow=True)
        
        # Check if valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=Checkout Report By Item ' + weekAgo.strftime('%Y-%m-%d') +  ' to ' + today.strftime('%Y-%m-%d') + '.csv')
        self.assertContains(response, 'item,new/used,category,quantity,new/used price,total value')
        self.assertContains(response, 'ValidItem,Used,No category,2,0,0')
