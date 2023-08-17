from django.shortcuts import render
from django.http import Http404
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found")
    
    # Convert Markdown to HTML
    entry_html = markdown2.markdown(entry_content)

    return render(request, "encyclopedia/page.html", {
        "entry": entry_html, 
        "title": title.upper()
    })