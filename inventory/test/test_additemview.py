from django.test import TestCase
from django.contrib.auth.models import User

from inventory.models import Item

class AddItemTestCase(TestCase):
    def setUp(self):
        item = Item.objects.create(name="ValidItem", quantity=5)
        item.save()

        user = User.objects.create_superuser(username='testuser', password='12345')
        user.save()

    def test_post_success(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post(
            "/checkin/", data={"additem": "",
                               "item": "ValidItem",
                               "new_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/checkout/", data={"additem": "",
                                "item": "ValidItem",
                                "used_quantity": 1}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        session = self.client.session

        self.assertEqual(session['transactions-in'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": true}}]'])
        self.assertEqual(session['transactions-out'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 1, "is_new": false}}]'])

    def test_post_error(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post(
            "/checkin/", data={"additem": "",
                               "item": "InvalidItem",
                               "quantity": 1}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item does not exist.")

    def test_post_new_item_only_success(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post(
            "/checkin/", data={"additem": "",
                               "item": "ValidItem",
                               "new_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/checkout/", data={"additem": "",
                               "item": "ValidItem",
                               "new_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        session = self.client.session

        self.assertEqual(session['transactions-in'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": true}}]'])
        
        self.assertEqual(session['transactions-out'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": true}}]'])

    def test_post_used_item_only_success(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post(
            "/checkin/", data={"additem": "",
                               "item": "ValidItem",
                               "used_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/checkout/", data={"additem": "",
                               "item": "ValidItem",
                               "used_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        session = self.client.session

        self.assertEqual(session['transactions-in'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": false}}]'])

        self.assertEqual(session['transactions-out'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": false}}]'])

    def test_post_used_and_new_item_success(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.post(
            "/checkin/", data={"additem": "",
                               "item": "ValidItem",
                               "used_quantity": 1,
                               "new_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/checkout/", data={"additem": "",
                               "item": "ValidItem",
                               "used_quantity": 1,
                               "new_quantity": 2}, follow=True
        )

        self.assertEqual(response.status_code, 200)

        session = self.client.session

        #print(session['transactions-in'])

        self.assertEqual(session['transactions-in'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 1, "is_new": false}}]', '[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": true}}]'])

        self.assertEqual(session['transactions-out'],
                         ['[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 1, "is_new": false}}]', '[{"model": "inventory.itemtransaction", "pk": null, "fields": {"item": 1, "quantity": 2, "is_new": true}}]'])
