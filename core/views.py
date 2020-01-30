from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins
from django.contrib import messages

from .forms import ContactForm


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password2'])
        login(self.request, user)
        return response


class Contact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('groups:list')

    def form_valid(self, form):
        mail_admins('New message from Xteams', form.cleaned_data['content'])
        messages.success(self.request, 'Your message has been sent. Thanks!')
        return super(Contact, self).form_valid(form)
