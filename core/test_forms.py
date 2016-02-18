from unittest import TestCase

from . import forms


class ContactFormTest(TestCase):

    def test_clean_content(self):
        data = {'subject': 'test', 'email': 'moshe@gmail.com',
                'content': 'This is a test'}
        form = forms.ContactForm(data)
        form.full_clean()
        expected_content_lines = ['From: moshe@gmail.com', 'Subject: test',
                                  '', 'This is a test']
        expected_content = '\n'.join(expected_content_lines)
        self.assertEqual(form.cleaned_data['content'], expected_content)
