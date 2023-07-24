# app/forms.py

from django import forms


number_of_click_choice = [
    ('1', '3'),
    ('2', '4'),
    ('3', '5'),
]


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    number_of_click = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=number_of_click_choice,
        label='Number Of Click'
    )
    image = forms.FileField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        image = cleaned_data.get('image')
        number_of_click = cleaned_data.get('number_of_click')

        if not username and not email and not image and not number_of_click:
            raise forms.ValidationError('You have to write something!')


# class RegisterStepTwoForm(forms.Form):
#     email = forms.EmailField()
