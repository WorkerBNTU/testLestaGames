from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import Log
from .forms import LestaForm
from collections import Counter
from .models import Word, Document, Tf


def index(request):
    words = []
    if request.method == 'POST':
        form = LestaForm(request.POST, request.FILES)
        if 'file' in request.FILES:
            file = request.FILES['file']
            """"
            предполагаю, что текст не нужно предварительно преобразовывать
            например, работать со знаками препинания, пробелами, регистром и т.п
            """
            if file.name.endswith('.txt'):
                doc = Document.objects.create(name=file.name)
                list_words = file.read().decode('utf-8').split()
                word_counts = Counter(list_words)
                for word, count in word_counts.items():
                    word_obj, created = Word.objects.get_or_create(word=word)
                    Tf.objects.create(word=word_obj, document=doc, count=count/len(list_words))
            else:
                form.add_error('file', 'Только txt файлы.')
        elif 'deleteAll' in request.POST:
            Document.objects.all().delete()
            try:
                del request.session['doc_id']
            except KeyError:
                pass
            return redirect(index)
        else:
            return HttpResponse('Какая-то ошибка')
    else:
        form = LestaForm()
        if 'docSelect' in request.GET:
            doc_id = request.GET['docSelect']
            doc = Document.objects.get(id=doc_id)
            if 'fileSelect' in request.GET:
                request.session['doc_id'] = doc_id
            elif 'deleteSelect' in request.GET:
                doc.delete()
                try:
                    if doc_id == request.session['doc_id']:
                        del request.session['doc_id']
                except KeyError:
                    pass

    docs = Document.objects.all()
    doc_id = request.session.get('doc_id')
    if doc_id and docs:
        doc = Document.objects.get(id=doc_id)
        words_list = Tf.objects.filter(document=doc).annotate(IDF=Log(10, float(len(docs))/Count('word__document'))).order_by('-IDF')
        paginator = Paginator(words_list, 10)
        page_number = request.GET.get('page')
        words = paginator.get_page(page_number)
    return render(request, 'words/index.html', {'my_form': form, 'docs': docs, 'words': words})
