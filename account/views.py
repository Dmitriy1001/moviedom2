from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('signin')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class SignIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'account/signin.html'
    redirect_authenticated_user = True
