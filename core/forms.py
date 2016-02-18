from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        lines = ['From: {}'.format(self.cleaned_data['email']),
                 'Subject: {}'.format(self.cleaned_data['subject']),
                 '',
                 self.cleaned_data['content']]
        self.cleaned_data['content'] = '\n'.join(lines)
