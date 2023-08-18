from django.shortcuts import render, redirect
from django.http import Http404
import markdown2

from . import util


def index(request, query=None, titles=None, search=False):
    if titles is None:
        entries = util.list_entries()
    else:
        entries = titles
        
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "search": search,
        "query": query
    })

def page(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found")
    
    entry_html = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/page.html", {
        "entry": entry_html, 
        "title": title
    })

def search(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        titles, direct_link = util.search_entry(query)
        if direct_link:
            return page(request, titles)
        else: 
            return index(request, query, titles, True)
        
def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        if util.entry_existance(title):
            return render(request, "encyclopedia/create.html", {
                "entry_exist": True
            })
        util.save_entry(title, content)
        return redirect("page", title=title)
    else:
        return render(request, "encyclopedia/create.html")
        
        