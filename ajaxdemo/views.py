from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView

from .forms import NoteForm
from .models import Notebook


class NotebookCreateView(CreateView):
    model = Notebook
    template_name = "notebook_form.html"
    fields = [
        "name"
    ]

    def get_success_url(self):
        return reverse("notebook_notes", kwargs=dict(pk=self.object.pk))


class NotebookNotesView(DetailView):

    template_name = "notes.html"
    model = Notebook

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["note_list"] = self.object.notes
        context["form"] = NoteForm()
        context["post_url"] = reverse("ajax_notes_create", kwargs=dict(notebook_pk=self.object.pk))
        return context


@require_POST
def ajax_notes_create(request, notebook_pk):
    notebook = get_object_or_404(Notebook, pk=notebook_pk)
    data = {}
    note = None
    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.notebook = notebook
        note.save()
        form = NoteForm()
        data["append-fragments"] = {
            "#note-list": render_to_string("_note.html", {"note": note})
        }
    data["html"] = render_to_string("_note_form.html", {
        "note": note,
        "form": form,
        "post_url": reverse("ajax_notes_create", kwargs=dict(notebook_pk=notebook_pk))
    }, request)
    return JsonResponse(data)


def ajax_notes_update(request, notebook_pk, pk):
    notebook = get_object_or_404(Notebook, pk=notebook_pk)
    data = {}
    note = get_object_or_404(notebook.note_set, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        post_url = reverse("ajax_notes_update", kwargs=dict(notebook_pk=notebook.pk, pk=pk))
        if form.is_valid():
            note = form.save()
            form = NoteForm()
            post_url = reverse("ajax_notes_create", kwargs=dict(notebook_pk=notebook.pk))
            data["fragments"] = {
                "#note-{}".format(note.pk): render_to_string("_note.html", {"note": note})
            }
    else:
        form = NoteForm(instance=note)
        post_url = reverse("ajax_notes_update", kwargs=dict(notebook_pk=notebook.pk, pk=pk))
    data["html"] = render_to_string("_note_form.html", {
        "note": note,
        "form": form,
        "post_url": post_url
    }, request)
    return JsonResponse(data)


@require_POST
def ajax_notes_update_order(request, notebook_pk):
    notebook = get_object_or_404(Notebook, pk=notebook_pk)
    notebook.note_order = request.POST.get("order")
    notebook.save()
    return JsonResponse({})
