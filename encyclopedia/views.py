import random
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util #from the current directory import util.py

class CreateNewPage(forms.Form):
    article_title = forms.CharField(label="Article Title", widget=forms.TextInput(attrs={
        "placeholder": "Article Title",
        "class" : "form-control col-md-8 col-lg-8",

    }))
    article_content = forms.CharField(label = "Article Content", widget=forms.Textarea(attrs={
        "class" : "form-control col-md-8 col-lg-8"
    
    }))

    editable = forms.BooleanField(initial=False,required=False,widget=forms.HiddenInput())


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
            "entry_content": markdown.convert(entry_title),
            "entry_title" : entry_content
        })

def search(request):
    search_entry = request.GET.get("q","")
    if(util.get_entry(search_entry) is not None):
        return HttpResponseRedirect(reverse("entry",kwargs={"entry_content":search_entry}))
    else:
        wiki_substring = []
        for entry in util.list_entries():
            if search_entry.upper() in entry.upper():
                wiki_substring.append(entry)
        
        return render(request,"encyclopedia/search.html",{
            "entries" : wiki_substring,
            "search_entry" : search_entry
        })


def random_function(request):
    list_of_entries = util.list_entries()
    chosen_list = random.choice(list_of_entries)

    return HttpResponseRedirect(reverse("entry",kwargs={"entry_content":chosen_list}))


def create(request):

    if request.method == "POST":
        form = CreateNewPage(request.POST)
        

        if form.is_valid():
            article_title = form.cleaned_data["article_title"]
            article_content = form.cleaned_data["article_content"]
        
            
            if util.get_entry(article_title) is None or form.cleaned_data["editable"] is True:
                util.save_entry(article_title, article_content)
                return HttpResponseRedirect(reverse("entry",kwargs={"entry_content":article_title}))
            else:
                return render(request,"encyclopedia/create.html",{
                "form" : form,
                "entry_title" : article_title,
                "page_exists" : True
            })            


    return render(request, "encyclopedia/create.html", {
        "form" : CreateNewPage()
    }) 

def edit(request,entry):
    entry_content = util.get_entry(entry)
    if entry_content is None:
        return render(request,"encyclopedia/error.html",{
            "entry_title" : entry
        })

    else:
        form = CreateNewPage()
        form.fields["article_title"].initial = entry
        form.fields["article_title"].widget = forms.HiddenInput()
        form.fields["article_content"].initial = entry_content
        form.fields["editable"].initial = True
       
        return render(request,"encyclopedia/create.html",{
            "form" : form,
            "edit" : form.fields["editable"].initial,
            "entry_title" : form.fields["article_title"].initial
        })
