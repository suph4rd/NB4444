from django.shortcuts import redirect
from django.urls import reverse_lazy

from B4 import forms, models


class NoteViewMixin:
    form_class = forms.NoteModelForm
    model = models.Note
    queryset = None
    success_url = reverse_lazy("b4:note")

    def get_initial(self):
        self.initial = {"user": self.request.user}
        return super().get_initial()


class AdminQsManagerMixin:
    def get_queryset(self, request):
        manager = self.model._default_manager
        if hasattr(self.model, "get_admin_manager"):
            manager = self.model.get_admin_manager()
        qs = manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class UserRecordMixin:
    model = None
    queryset = None

    def dispatch(self, request, *args, **kwargs):
        if self.model and not self.queryset:
            self.queryset = self.model.objects.all()
        if self.queryset and hasattr(self.model, 'user') \
                and request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class IsCurrentUserMixin:
    redirect_url: str = None

    def dispatch(self, request, *args, **kwargs):
        answer = self._check_user(request)
        if answer:
            return answer
        return super().dispatch(request, *args, **kwargs)

    def _check_user(self, request):
        obj = self.get_object()
        if obj.user_id != request.user.id:
            return redirect(self.redirect_url)

