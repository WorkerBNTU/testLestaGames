from django.contrib import admin
from .models import Document, Word, Tf

admin.site.register(Document)
admin.site.register(Word)
admin.site.register(Tf)
