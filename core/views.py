from django.conf import settings
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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
