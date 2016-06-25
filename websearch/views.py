from django.core.validators import URLValidator, ValidationError
from django.shortcuts import render, render_to_response
from backend.htmlparser import HtmlParser
from models import *

# Create your views here.
from django.template import RequestContext


def home(request):
    return render_to_response('home.html')


def indexation(request):
    if request.method == "POST":
        indexing_urls = []
        url_validator = URLValidator(schemes=['http', 'https'])
        urls = request.POST.get('url')
        if urls:
            u_list = urls.split(", ")
            for url in u_list:
                try:
                    url_validator(url)
                except ValidationError:
                    continue
                indexing_urls.append(url)

        if len(indexing_urls):
            h = HtmlParser(indexing_urls)
            h.multiproc()
            result = 'Crawler successfully end working!'
        else:
            result = 'No valid URLs'

    else:
        result = ''

    c = RequestContext(request)
    return render_to_response('indexation.html', {'result': result}, c)


def urls(request):
    pages = WebPage.objects.all()
    id_list = []
    for page in pages:
        id_list.append(page.id)
    if not request.method == "POST" or request.POST.get('id') == '':
        return render_to_response('urls.html', {'pages': pages})
    if int(request.POST.get('id')) in id_list:
        WebPage.objects.get(id=request.POST.get('id')).delete()
    return render_to_response('urls.html', {'pages': pages})
