from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView


class Base:
    def get(self, request, *args, **kwargs):
        if not request.session.keys():
            return HttpResponseRedirect(reverse('auth'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.session.keys():
            return HttpResponseRedirect(reverse('auth'))
        return super().post(request, *args, **kwargs)


class BaseTemplateView(Base, TemplateView):
    allowed_methods = ['GET']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BaseFormView(Base, FormView):
    allowed_methods = ['GET', 'POST']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseCreateView(Base, CreateView):
    allowed_methods = ['GET', 'POST']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
