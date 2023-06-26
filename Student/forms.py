from django import forms
from django.forms import widgets
from .models import Item,ReserveItem
from datetime import date, timedelta,datetime 
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
yr = (datetime.now().year)+1


CategoryChoices = [
    ('Book','Book'),
    ('CD','CD')
]
class ItemRegistration(forms.ModelForm): #form for item registration..only for admin
    Quantity = forms.IntegerField(min_value=1,max_value=50)
    YearOfPublished = forms.IntegerField(min_value=1980,max_value=datetime.now().year)
    class Meta:
        model = Item
        fields = '__all__'
        widgets={
            'Name': forms.TextInput(attrs={"placeholder": "Enter Item Name..",'id': 'Name','class': 'form-control form-control-lg'}),
            'AuthorName': forms.TextInput(attrs={"placeholder": "Enter Author Name..",'id': 'AuthorName','class': 'form-control form-control-lg'}),
            'Category': forms.Select(choices=CategoryChoices,attrs={"placeholder": "Select Category..",'id': 'Category','class': 'form-control form-control-lg'}), #for dropdown as Book or CD
            'Quantity': forms.NumberInput(attrs={"placeholder": "Select Quantity..",'id': 'Quantity','class': 'form-control form-control-lg'}),
            'YearOfPublished' : forms.NumberInput(attrs={"placeholder": "Select Year Of Published..",'id': 'YearOfPublished','class': 'form-control form-control-lg'}),
        }
        

class ItemUpdation(forms.ModelForm):  #form to update item only for admin
    Quantity = forms.IntegerField(min_value=1,max_value=50)
    YearOfPublished = forms.IntegerField(min_value=1980,max_value=datetime.now().year)
    class Meta:
        model = Item
        fields = '__all__'
        widgets={  #all the fields are reaonly except the quantity
            'Name': forms.TextInput(attrs={'readonly':True,'id': 'Name','class': 'form-control form-control-lg'}),
            'Category': forms.TextInput(attrs={'readonly':True,'id': 'Category','class': 'form-control form-control-lg'}),
            'AuthorName': forms.TextInput(attrs={'readonly':True,'id': 'AuthorName','class': 'form-control form-control-lg'}),
            'Quantity': forms.NumberInput(attrs={'id': 'Quantity','class': 'form-control form-control-lg'}),
            'YearOfPublished': forms.NumberInput(attrs={'readonly':True,'id': 'YearOfPublished','class': 'form-control form-control-lg'})
        }
        
class ReserveItemForm(forms.ModelForm):  #form for user to reserve item
    class Meta:
        model = ReserveItem
        fields = '__all__'
        widgets = {
            'ItemId':forms.TextInput(attrs={'readonly':True,'id': 'ItemId','class': 'form-control form-control-lg'}),
            'UserId':forms.TextInput(attrs={'readonly':True,'id': 'UserId','class': 'form-control form-control-lg'}),
            'Category': forms.TextInput(attrs={'readonly':True,'id': 'Category','class': 'form-control form-control-lg'}),
            'DateOfIssue': forms.DateInput(attrs={'type': 'date', 'value': date.today().strftime("%Y-%m-%d"),'readonly':True,'id': 'DateOfIssue','class': 'form-control form-control-lg'}),
            'DateOfReturn': forms.DateInput(attrs={'type': 'date', 'value': (date.today()+timedelta(days=7)).strftime("%Y-%m-%d"),'readonly':True,'id': 'DateOfReturn','class': 'form-control form-control-lg'}),
        }

class ReleaseItemForm(forms.ModelForm): #form for user to release item
    class Meta:
        model = ReserveItem
        fields = '__all__'
        widgets = {
            'ItemId':forms.TextInput(attrs={'readonly':True,'id': 'ItemId','class': 'form-control form-control-lg'}),
            'UserId':forms.TextInput(attrs={'readonly':True,'id': 'UserId','class': 'form-control form-control-lg'}),
            'Category': forms.TextInput(attrs={'readonly':True,'id': 'Category','class': 'form-control form-control-lg'}),
            'DateOfIssue': forms.DateInput(attrs={'readonly':True,'id': 'DateOfIssue','class': 'form-control form-control-lg'}),
            'DateOfReturn': forms.DateInput(attrs={'readonly':True,'id': 'DateOfReturn','class': 'form-control form-control-lg'}),
        }
        
class userUpdateForm(UserChangeForm):   #user updation form...
    password = None
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'first_name':forms.TextInput(attrs={'id': 'first_name','class': 'form-control form-control-lg'}),
            'last_name':forms.TextInput(attrs={'id': 'last_name','class': 'form-control form-control-lg'}),
            'email':forms.EmailInput(attrs={'id': 'email','class': 'form-control form-control-lg'})
        }

class PasswordChangeCustomForm(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control form-control-lg'})
        
