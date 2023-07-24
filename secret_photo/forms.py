# app/forms.py

from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    image = forms.FileField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        image = cleaned_data.get('image')

        if not username and not email and not image:
            raise forms.ValidationError('You have to write something!')


# class RegisterStepTwoForm(forms.Form):
#     email = forms.EmailField()
