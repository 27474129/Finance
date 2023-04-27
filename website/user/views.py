from django.views.generic import CreateView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView

from user.forms import CreateUserForm, AuthUserForm, UserProfileCommentForm
from user.models import User
from user.services import Auth
from base.base import BaseFormView


class UserRegView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user/reg.html'
    allowed_methods = ['GET', 'POST']

    success_url = reverse_lazy('auth')

    def get(self, request, *args, **kwargs):
        if request.session.keys():
            return HttpResponseRedirect(reverse('root'))
        return super().get(request, *args, **kwargs)


class UserAuthView(FormView):
    form_class = AuthUserForm
    template_name = 'user/auth.html'
    allowed_methods = ['GET', 'POST']

    def post(self, request, *args, **kwargs):
        auth = Auth()
        user_data = auth.authenticate(request.POST)
        if user_data:
            auth.authorize(request, uid=user_data[0], email=user_data[1])
            return HttpResponseRedirect(reverse('root'))
        return HttpResponse(False)


class UserLogoutView(LogoutView):
    allowed_methods = ['GET']
    next_page = reverse_lazy('auth')


class UserProfileView(BaseFormView):
    template_name = 'user/profile.html'
    form_class = UserProfileCommentForm

    def get(self, request, user_id, *args, **kwargs):
        # TODO: Добавить отображение комментариев
        self.uid = user_id
        return super().get(request, user_id)

    def post(self, request, user_id, *args, **kwargs):
        # TODO: Добавить создание комментариев к профилю
        return super().post(request, user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.get_user(self.uid)
        return context

    def get_success_url(self):
        return self.request.path


class RootView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('root')
