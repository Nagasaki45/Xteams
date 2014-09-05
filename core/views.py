from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import mail_admins
from django.contrib import messages

from .forms import RegistrationForm, ContactForm

User = get_user_model()


class Register(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        User.objects.create_user(username=username, password=password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(Register, self).form_valid(form)


class Contact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('teams:list')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        content = 'From: {}.\n\n{}'.format(email,
                                           form.cleaned_data['content'])
        mail_admins(subject, content)
        messages.success(self.request, 'Your message has been sent. Thanks!')
        return super(Contact, self).form_valid(form)
