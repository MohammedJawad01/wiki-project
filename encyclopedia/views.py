from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random

def convert_md_to_html(title):
    content=util.get_entry(title)
    markdown=Markdown()
    if content == None:
        return None
    else :
        return markdown.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request , title ):
    html_content=convert_md_to_html(title)
    if html_content == None :
        return render (request , "encyclopedia/error.html" ,{
            "message" : "This entry does not exist"
        })
    else :
        return render ( request , "encyclopedia/entry.html" , {
            "title":title ,
            "content":html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render ( request , "encyclopedia/entry.html" , {
            "title":entry_search ,
            "content":html_content
        })
        # making recommendation for search
        else :
            Entries = util.list_entries()
            recommendation = []
            for entry in Entries :
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render (request , "encyclopedia/search.html" , {
                "recommendation" : recommendation
            })

def new_page (request):
    if request.method == "GET":
        return render(request , "encyclopedia/new.html")
    else :
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render (request , "encyclopedia/error.html" , {
                "message" : "Entry page is already exists"
            } )
        else :
            util.save_entry(title , content)
            html_content = convert_md_to_html(title)
            return render (request , "encyclopedia/entry.html" , {
                "title" :title ,
                "content" : html_content     
            })
        
def edit (request):
    if request.method == 'POST' :
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render (request , "encyclopedia/edit.html", {
            "title" : title , 
            "content":content
        })
    
def save_edit (request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST ['content']
        util.save_entry(title , content)
        html_content = convert_md_to_html(title)
        return render (request , "encyclopedia/entry.html" , {
            "title" :title ,
            "content" : html_content     
        })
    

def random_entry (request):
    Entries = util.list_entries()
    random_ent = random.choice (Entries)
    html_content = convert_md_to_html(random_ent)
    return render (request , "encyclopedia/entry.html" ,{
        "title":random_ent,
        "content":html_content
    })