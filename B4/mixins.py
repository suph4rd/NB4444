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