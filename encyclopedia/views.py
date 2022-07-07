from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util #from the current directory import util.py


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
   
    })

def entry(request,entry_content):
    markdown = Markdown()
    entry_title = util.get_entry(entry_content)

    if entry_title is None:
        return render(request,"encyclopedia/error.html",{
            "entry_title" : entry_content

        })
    else:
        return render(request,"encyclopedia/entry.html",{
           "entry_content": markdown.convert(entry_title)
        })

def search(request):
    search_entry = request.GET.get("q","")
    if util.list_entries(search_entry) is not None:
        return HttpResponseRedirect(reverse("entry",kwargs={"entry":search_entry}))

def edit(request):
    None

def error(request):
    None

def create(reqeust):
    None 

def random(request):
    None