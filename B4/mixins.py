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
