from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)
