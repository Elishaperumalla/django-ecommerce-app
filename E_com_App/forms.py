# from django import forms
# from django.contrib.auth import get_user_model


# UserModel = get_user_model()

# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     full_name = forms.CharField(max_length=100, required=False)
#     phone = forms.CharField(max_length=15, required=False)

#     class Meta:
#         model = UserModel
#         fields = ['username', 'email', 'full_name', 'phone', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)

# class CheckoutForm(forms.Form):
#     street = forms.CharField(max_length=100)
#     city = forms.CharField(max_length=50)
#     state = forms.CharField(max_length=50)
#     zip = forms.CharField(max_length=10)