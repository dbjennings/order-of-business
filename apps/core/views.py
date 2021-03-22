from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CoreAuthenticationForm, CoreUserAddForm

class CoreLoginView(LoginView):

    template_name = 'core/login.html'
    form_class = CoreAuthenticationForm
    redirect_authenticated_user = True

class CoreRegisterView(CreateView):

    template_name = 'core/register.html'
    form_class = CoreUserAddForm
    success_url = reverse_lazy('landing')
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        '''Redirects to User's Home if already authenticated'''

        # Check for redirect and authenticated user
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            
            # Redirect to the user's home page
            redirect_to = reverse_lazy('landing')
            return HttpResponseRedirect(redirect_to)

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        '''Automatically authenticates and logs in new users'''

        # Pass the form to CreateView.form_valid() to save the new user
        super().form_valid(form)

        # Authenticate the user using POST data
        new_user = authenticate(username=self.request.POST['email'],
                                password=self.request.POST['password1'])

        # Login the authenticated user
        login(self.request, new_user)

        return HttpResponseRedirect(self.get_success_url())
