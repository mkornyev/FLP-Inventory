from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item, Checkout, Checkin, Family, AgeRange
from django.http.request import QueryDict, MultiValueDict
from datetime import date, timedelta
from unittest.mock import patch

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive, GoogleDriveFile

class GenerateReportDriveTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        family = Family.objects.create(lname="ValidFamily")
        family.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

        ageRange = AgeRange.objects.create(low=3, high=5) # will have value 1
        ageRange.save()

    def test_export_drive_checkin_report(self):
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
            'export_drive_table': ['']
        }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))
        csvFile = GoogleDriveFile({'title': 'Checkin Report ' + today.strftime('%Y-%m-%d') + ' to ' + weekAgo.strftime('%Y-%m-%d') + '.csv', 'mimeType': 'text/csv'})

        with patch.object(GoogleAuth, 'LocalWebserverAuth') as patch_auth:
            with patch.object(GoogleDrive, 'CreateFile', return_value=csvFile) as patch_createfile:
                with patch.object(GoogleDriveFile, 'SetContentString') as patch_setcontentstring:
                    with patch.object(GoogleDriveFile, 'Upload') as patch_upload:
                        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        patch_auth.assert_called()
        patch_createfile.assert_called()
        self.assertEqual(patch_createfile.return_value, csvFile)
        patch_setcontentstring.assert_called()
        patch_upload.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(len(response.context['results']), 1)
    
    def test_export_drive_checkout_report(self):
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
            'export_drive_table': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))
        csvFile = GoogleDriveFile({'title': 'Checkout Report ' + today.strftime('%Y-%m-%d') + ' to ' + weekAgo.strftime('%Y-%m-%d') + '.csv', 'mimeType': 'text/csv'})

        with patch.object(GoogleAuth, 'LocalWebserverAuth') as patch_auth:
            with patch.object(GoogleDrive, 'CreateFile', return_value=csvFile) as patch_createfile:
                with patch.object(GoogleDriveFile, 'SetContentString') as patch_setcontentstring:
                    with patch.object(GoogleDriveFile, 'Upload') as patch_upload:
                        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        patch_auth.assert_called()
        patch_createfile.assert_called()
        self.assertEqual(patch_createfile.return_value, csvFile)
        patch_setcontentstring.assert_called()
        patch_upload.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(len(response.context['results']), 1)
    
    def test_export_drive_checkingbi_report(self):
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
            'export_drive_table': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))
        csvFile = GoogleDriveFile({'title': 'Checkin Report By Item ' + today.strftime('%Y-%m-%d') + ' to ' + weekAgo.strftime('%Y-%m-%d') + '.csv', 'mimeType': 'text/csv'})

        with patch.object(GoogleAuth, 'LocalWebserverAuth') as patch_auth:
            with patch.object(GoogleDrive, 'CreateFile', return_value=csvFile) as patch_createfile:
                with patch.object(GoogleDriveFile, 'SetContentString') as patch_setcontentstring:
                    with patch.object(GoogleDriveFile, 'Upload') as patch_upload:
                        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        patch_auth.assert_called()
        patch_createfile.assert_called()
        self.assertEqual(patch_createfile.return_value, csvFile)
        patch_setcontentstring.assert_called()
        patch_upload.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(len(response.context['results']), 1)

    def test_export_drive_checkoutgbi_report(self):
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
            'export_drive': ['']
            }

        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))
        csvFile = GoogleDriveFile({'title': 'Checkout Report By Item ' + today.strftime('%Y-%m-%d') + ' to ' + weekAgo.strftime('%Y-%m-%d') + '.csv', 'mimeType': 'text/csv'})

        with patch.object(GoogleAuth, 'LocalWebserverAuth') as patch_auth:
            with patch.object(GoogleDrive, 'CreateFile', return_value=csvFile) as patch_createfile:
                with patch.object(GoogleDriveFile, 'SetContentString') as patch_setcontentstring:
                    with patch.object(GoogleDriveFile, 'Upload') as patch_upload:
                        response = self.client.post('/report/', qdict, follow=True)

        # Check if valid
        patch_auth.assert_called()
        patch_createfile.assert_called()
        self.assertEqual(patch_createfile.return_value, csvFile)
        patch_setcontentstring.assert_called()
        patch_upload.assert_called()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reports/generate_report.html')
        self.assertEqual(len(response.context['results']), 1)
