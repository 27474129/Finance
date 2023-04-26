from django.views.generic import CreateView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView

from user.forms import CreateUserForm, AuthUserForm
from user.models import User
from user.utils import Auth


class UserRegView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user/reg.html'
    success_url = reverse_lazy('auth')

    def get(self, request, *args, **kwargs):
        if request.session.keys():
            return HttpResponseRedirect(reverse_lazy('root'))
        return super().get(request, *args, **kwargs)


class UserAuthView(FormView):
    form_class = AuthUserForm
    template_name = 'user/auth.html'
    success_url = reverse_lazy('root')

    def post(self, request, *args, **kwargs):
        auth = Auth()
        user_data = auth.authenticate(request.POST)
        if user_data:
            auth.authorize(request, uid=user_data[0], email=user_data[1])
            return HttpResponse(request.session['token'])
        return HttpResponse(False)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth')


class RootView(View):
    def get(self, request, *args, **kwargs):
        auth = Auth()
        if auth.decode_token(request.session.get('token')):
            return HttpResponse('root')
        return HttpResponseRedirect(reverse_lazy('auth'))
