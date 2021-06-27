from django import forms

class AuthenticationForm(forms.Form):
    username = forms.EmailField(label='Your name', max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Password'}))