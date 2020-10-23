from django.shortcuts import render,redirect
import markdown2
from . import util
import re
import random


pagelist = util.list_entries()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    pagelist = util.list_entries()
    if request.method == "POST":
        term = request.POST
        term =term['q']
        searchlist = []

        for page in pagelist:

            if re.search(term.lower(), page.lower()):
                searchlist.append(page)
        if len(searchlist) == 0:
            return render(request, "encyclopedia/error.html", {
                'error_message': f'No results found for \'{term}\' '
            })

    return render(request, "encyclopedia/search.html", {
        'entries': searchlist
    })

def add_page(request):
    if request.method == "POST":
      title = request.POST.get('title')
      content = request.POST.get('content')
      if title in pagelist:
          return render(request,"encyclopedia/add_page.html", {
          'available' : True
          })
      else:

            util.save_entry(title, content)
            return redirect(entry, title=title)
    return render(request,"encyclopedia/add_page.html", {
     'available' : False
     })

def random_page(request):

    r = random.randint(0, len(pagelist)-1)
    title = pagelist[r]

    return redirect(entry, title=title)

def edit(request,title):
    content = util.get_entry(title)
    if request.method == "GET":
        pagelist = util.list_entries()
        if title in pagelist:
            content = util.get_entry(title)
            return render(request,"encyclopedia/edit.html", {
            "title":title,
            "content": content
            })
    if request.method == "POST":
        content = request.POST.get('newcontent')
        util.save_entry(title,content)
        return redirect(entry,title=title)


def entry(request,title):
    pagelist = util.list_entries()
    if title in pagelist:
            content = util.get_entry(title)

            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": markdown2.markdown(content)
                # send title and content to HTML
            })
    else:
            return render(request, "encyclopedia/error.html", {
                'error_message': 'Page not found'
            })
