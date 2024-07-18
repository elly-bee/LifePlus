# forms.py
from django import forms
from .models import MyUser,Orders
from .models import Products


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','password','first_name', 'last_name', 'dateofbirth','email', 'marital_status', 'gender', 'address', 'phone_number_1', 'phone_number_2','parent']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dateofbirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'phone_number_1': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control', 'id': 'parent-select'}),
        }

class keyBonusUpdate(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['keyBonus']  
        widgets = {
            'keyBonus': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyBonus'].queryset = MyUser.objects.all()
       
        





class CreateProducts(forms.ModelForm):
    package_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]*'}))
    class Meta:
        model = Products
        fields = ['package_name','package_price','bonus']
        widgets = {
            'package_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bonus': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'