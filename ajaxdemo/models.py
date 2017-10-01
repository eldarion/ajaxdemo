from django.db import models


class Notebook(models.Model):
    name = models.CharField(max_length=100)
    note_order = models.TextField(blank=True)

    @property
    def notes(self):
        order_by = "pk"
        if self.note_order:
            pks = self.note_order.split("|")
            order_by = models.Case(*[
                models.When(pk=pk, then=pos)
                for pos, pk in enumerate(pks)
            ])
        return self.note_set.all().order_by(order_by)


class Note(models.Model):
    notebook = models.ForeignKey(Notebook)
    title = models.CharField(max_length=200)
    note = models.TextField()
    date = models.DateField()
