from django.contrib import messages
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


class AdminDeleteActionMixin:
    actions = ("set_delete_status",)

    def set_delete_status(self, request, queryset):
        queryset.update(is_delete=True)

    set_delete_status.short_description = "Пометить как удалённые"


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


class CKEditorErrorShowMixin:
    check_ck_field: str = None

    def form_invalid(self, form):
        if self.check_ck_field in form.errors:
            messages.error(self.request, f"{self.check_ck_field}: {form.errors[self.check_ck_field]}")
        return redirect(reverse_lazy('b4:note'))
