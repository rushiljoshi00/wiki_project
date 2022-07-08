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
    search_entry = request.GET.get('q','')
    if(util.get_entry(search_entry) is not None):
        return HttpResponseRedirect(reverse("entry",kwargs={'entry_content':search_entry}))
    else:
        wiki_substring = []
        for entry in util.list_entries():
            if search_entry.upper() in entry.upper():
                wiki_substring.append(entry)
        
        return render(request,"encyclopedia/index.html",{
            "entries" : wiki_substring,
            "search_entry" : search_entry,
            "search_result" : True
        })


def random(request):
    None

def edit(request):
    None

def create(reqeust):
    None 

