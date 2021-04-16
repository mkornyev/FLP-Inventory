from django import forms
from django.db.models import Q

from inventory.models import Item, Family, Category

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())
    required_css_class = 'required'

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
    required_css_class = 'required'

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

class CreateFamilyForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'type':'tel'}), required=False)
    required_css_class = 'required'

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class CreateItemForm(forms.Form):
    category   = forms.ModelChoiceField(queryset=Category.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-select'}))
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    required_css_class = 'required' 
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the name field.
    def clean_name(self):
        # Confirms that the username is already present in the
        # Item model database.
        name = self.cleaned_data.get('name')
        if Item.objects.filter(name__exact=name):
            raise forms.ValidationError("Item already exists.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return name 

    # Customizes form validation for the quantity field.
    def clean_quantity(self):
        # Confirms the quantity is above zero
        quantity = self.cleaned_data.get('quantity')

        if quantity < 0:
            raise forms.ValidationError("Quantity must be zero or above.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return quantity

    # Customizes form validation for the quantity field.
    def clean_price(self):
        # Confirms the quantity is above zero
        price = self.cleaned_data.get('price')

        if price and price < 0:
            raise forms.ValidationError("Price must be above zero.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return price

class AddItemForm(forms.Form):
    # category   = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                     widget=forms.Select(attrs={'class': 'form-select'}))
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    required_css_class = 'required'

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the name field.
    def clean_name(self):
        # Confirms that the username is already present in the
        # Item model database.
        name = self.cleaned_data.get('name')
        if not Item.objects.filter(name__exact=name):
            raise forms.ValidationError("Item does not exist.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return name 

    def clean_quantity(self):
        # Confirms the quantity is above zero
        quantity = self.cleaned_data.get('quantity')

        if quantity <= 0:
            raise forms.ValidationError("Quantity must be above zero.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return quantity

class CheckOutForm(forms.Form):
    family = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    required_css_class = 'required'

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_family(self):
        # Confirms the family exists
        family = self.cleaned_data.get('family').strip()

        if ',' in family: 
            comma = family.index(',')
            lname = family[0:comma]
            fname = family[comma+2:]

            if not Family.objects.filter(
                Q(fname__exact=fname) and Q(lname__exact=lname)
            ):
                raise forms.ValidationError("Family does not exist.")
        
        else: 
            if not Family.objects.filter(lname__exact=family):
                raise forms.ValidationError("Family does not exist.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return family
