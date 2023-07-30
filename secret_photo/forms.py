# app/forms.py

from django import forms


number_of_click_choice = [
    ('4', '4'),
    ('6', '6'),
    ('8', '8'),
    ('10', '10'),
]


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email'}))
    number_of_click = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=number_of_click_choice,
        label='Number Of Click'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        number_of_click = cleaned_data.get('number_of_click')

        if not email and not number_of_click:
            raise forms.ValidationError('Invalid Form')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email address'}))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email address'}))


class ResetPasswordConfirmForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'readonly': 'readonly'},
    ))
    number_of_click = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=number_of_click_choice,
        label='Number Of Click'
    )


class PhotoUploadForm(forms.Form):
    photo = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
