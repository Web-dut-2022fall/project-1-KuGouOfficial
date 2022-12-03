import random

import markdown as md
from django.shortcuts import render, redirect

from .util import get_entry, save_entry, list_entries


def index(request):
    enties = list_entries()
    enties = [{'link': each.replace(' ', '+'), 'text': each} for each in enties]
    if request.method == 'GET':
        query = request.GET.get('q')
        if query == None:
            return render(request, "encyclopedia/index.html", {
                "entries": enties
            })
        else:
            for i in enties:
                i = i['text']
                if i == query:
                    content = get_entry(i)
                    content = md.markdown(content,
                                          extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',
                                                      'markdown.extensions.toc'])
                    return render(request, "encyclopedia/content.html", {'markdown': content,
                                                                         'Title': i})
            return render(request, 'encyclopedia/not_found.html', {'item': query, 'entries': enties})
    if request.GET.get('random') == '1':
        rani = random.randint(0, len(enties) - 1)
        return redirect(f"/?q={enties[rani]['link']}")


def create_md(req):
    if req.method == "GET":
        if req.GET.get('q') != None:
            return index(req)
        return render(req, "encyclopedia/create_md.html")
    else:
        hint = {}
        title = req.POST.get('title')
        content = req.POST.get('content')
        content = '#' + title + '\n' + content
        if title in list_entries():
            hint['error'] = '成功覆盖原文件'
        else:
            hint['success'] = '提交成功'
        save_entry(title, content)
        return render(req, "encyclopedia/create_md.html", hint)
