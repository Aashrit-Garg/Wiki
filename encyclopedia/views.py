from markdown2 import Markdown
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random


class NewTaskForm(forms.Form):
    title = forms.CharField(label="New Page Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": False,
    })

def content(request, title):

    entry = util.get_entry(title)
    if entry != None:
        return render(request, "encyclopedia/content.html", {
            "entry": Markdown().convert(entry),
            "title": title,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": ("Entry: \"" + title + "\" Not Found!"),
            "title": title.capitalize(),
        })

def search(request):
    value = request.GET.get('q','')
    entry = util.get_entry(value)
    if entry != None:
        return HttpResponseRedirect(reverse("content", kwargs={'title': value }))
    else:
        results = []
        for name in util.list_entries():
            if value in name:
                results.append(name)
        
        return render(request, "encyclopedia/index.html", {
            "title": value,
            "search": True,
            "entries": results
        })

def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in util.list_entries() or form.cleaned_data["edit"] == True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("content", kwargs={'title': title }))
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "existing": True,
                })
                
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "existing": False,
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm(),
            "existing": False,
        })

def edit(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "message": ("Entry: \"" + title + "\" Not Found!"),
            "title": title.capitalize(),
        })
    else:
        form = NewTaskForm()
        form.fields["title"].initial = title     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entry
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "existing": False,
            "edit": True,
            "title": title
        })

def randomPage(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("content", kwargs={'title': title }))