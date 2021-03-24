from django import forms

from inventory.models import Category, Family, Item

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class AddItemForm(forms.Form):
    category   = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField(max_length=50)
    price =  forms.DecimalField(max_digits=6, decimal_places=2)
    quantity = forms.IntegerField()

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class AddItemOutForm(forms.Form):
    category   = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField(max_length=50)
    quantity = forms.IntegerField()

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        item_name = cleaned_data.get('name')
        item = Item.objects.get(name__exact=item_name)

        quantity = cleaned_data.get('quantity')

        if item.quantity < quantity:
            raise forms.ValidationError("Not enough stock of item.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the name field.
    def clean_name(self):
        # Confirms that the username is already present in the
        # Item model database.
        name = self.cleaned_data.get('name')
        if Item.objects.filter(name__exact=name) == None:
            raise forms.ValidationError("Item does not exist.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return name 


class CheckOutForm(forms.Form):
    family = forms.ModelChoiceField(queryset=Family.objects.all())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data