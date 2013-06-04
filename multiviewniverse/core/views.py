from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.base import ContextMixin, TemplateView
import re


_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')


class MultiModelCreateFormView(TemplateView, ContextMixin):
    model_form_classes = []
    initial = {}
    success_url = None

    def _format_model_name(self, model):
        name = _underscorer1.sub(r'\1_\2', model.__name__).lower()
        return name

    def _get_model_form_name(self, model):
        return '%s_form' % self._format_model_name(model)

    def get(self, request, *args, **kwargs):
        return super(MultiModelCreateFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        if all([forms[f].is_valid() for f in forms]):
            o = {forms[f].model_class_name:forms[f].save(commit=False) for f in forms}
            for f in forms:
                forms[f].initial.update(o)
            o = [forms[f].save(commit=True) for f in forms]
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

    def get_context_data(self, **kwargs):
        context = super(MultiModelCreateFormView, self).get_context_data(**kwargs)
        context.update(self.get_forms())
        return context

    def get_forms(self):
        forms = {}
        for m in self.model_form_classes:
            form_class = m[0]
            model_class = m[1]
            form_name = self._get_model_form_name(model_class)
            forms[form_name] = form_class(prefix=form_name, **self.get_form_kwargs(model_class))
            forms[form_name].model_class_name = self._format_model_name(model_class)
        return forms

    def get_form_kwargs(self, model):
        initials = self.get_initial()
        kwargs = {'initial': initials}

        initials_method_name = 'get_%s_initials' % (self._format_model_name(model))
        if hasattr(self, initials_method_name) and callable(getattr(self, initials_method_name)):
            initials_method = getattr(self, initials_method_name)
            initials.update(initials_method())

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        if self.success_url:
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def get_initial(self):
        return self.initial.copy()

    def forms_valid(self, forms):
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(**forms))


class MultiModelUpdateFormView(MultiModelCreateFormView):
    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        if all([forms[f].is_valid() for f in forms]):
            o = [forms[f].save() for f in forms]
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

    def get_form_kwargs(self, model):
        kwargs = super(MultiModelUpdateFormView, self).get_form_kwargs(model)
        get_instance_method_name = 'get_%s_object' % (self._format_model_name(model))
        if hasattr(self, get_instance_method_name) and callable(getattr(self, get_instance_method_name)):
            instance_method = getattr(self, get_instance_method_name)
            instance = instance_method()
            kwargs.update({'instance': instance})
        else:
            raise Exception('Implement "%s" to be able to get the object instance' % get_instance_method_name)
        return kwargs

    def get_success_url(self):
        if self.success_url:
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def get_initial(self):
        return self.initial.copy()

    def forms_valid(self, forms):
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(**forms))
