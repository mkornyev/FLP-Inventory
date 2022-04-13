from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item
import json

class EditActionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

    def test_edit_quantity_positive(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/editquantity/0/out/5/', follow=True)
        
        #verify it returns to checkout
        self.assertRedirects(response, '/checkout/')
        
        session = session.load()
        saved_list = session['transactions-out']
        curr_item = json.loads(saved_list[0])

        #verify the correct value is saved
        assert(curr_item[0]['fields']['quantity'] == 5)


    def test_edit_quantity_zero(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/editquantity/0/out/0/', follow=True)
        
        #verify it returns to checkout
        self.assertRedirects(response, '/checkout/')
        
        session = session.load()
        saved_list = session['transactions-out']
        curr_item = json.loads(saved_list[0])

        #verify the correct value is moved to 1 since qty 0 is not possible
        assert(curr_item[0]['fields']['quantity'] == 1)

    def test_edit_quantity_negative(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/editquantity/0/out/-1/', follow=True)
        
        # negative nums cant be inputted into int urls so 404 should return (handled in JS function)
        self.assertEqual(response.status_code, 404)
    
    def test_edit_quantity_decimal(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2}}]']
        session.save()

        response = self.client.post('/editquantity/0/out/2.5/', follow=True)
        
        # decimal  nums cant be inputted into int urls so 404 should return (handled in input text HTML)
        self.assertEqual(response.status_code, 404)


    def test_edit_isnew_used(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": 1}}]']
        session.save()

        response = self.client.post('/editisnew/0/out/0/', follow=True)

        self.assertRedirects(response, '/checkout/')
        
        session = session.load()
        saved_list = session['transactions-out']
        curr_item = json.loads(saved_list[0])

        # #verify the is_new is moved to 0
        assert(not curr_item[0]['fields']['is_new'])
    
    def test_edit_isnew_new(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": 0}}]']
        session.save()

        response = self.client.post('/editisnew/0/out/1/', follow=True)

        self.assertRedirects(response, '/checkout/')
        
        session = session.load()
        saved_list = session['transactions-out']
        curr_item = json.loads(saved_list[0])

        # #verify the is_new is moved to 0
        assert(curr_item[0]['fields']['is_new'])
    
    def test_edit_isnew_not0or1(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": 0}}]']
        session.save()

        response = self.client.post('/editisnew/0/out/5/', follow=True)

        self.assertRedirects(response, '/checkout/')
        
        session = session.load()
        saved_list = session['transactions-out']
        curr_item = json.loads(saved_list[0])

        # #verify the is_new is moved to 0
        assert(not curr_item[0]['fields']['is_new'])

    def test_edit_isnew_negative(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": 0}}]']
        session.save()

        response = self.client.post('/editisnew/0/out/-5/', follow=True)  

        # negative nums cant be inputted into int urls so 404 should return (handled w/ dropdown)
        self.assertEqual(response.status_code, 404)
    
    def test_edit_isnew_decimal(self):
        self.client.login(username='testuser', password='12345')

        # Add item transaction
        session = self.client.session
        session['transactions-out'] = ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": 0}}]']
        session.save()

        response = self.client.post('/editisnew/0/out/2.5/', follow=True)  

        # decimal nums cant be inputted into int urls so 404 should return (handled w/ dropdown)
        self.assertEqual(response.status_code, 404)
