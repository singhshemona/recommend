# from ..backend import wsgi

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Book
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
import xml.etree.ElementTree as ET
import xmltodict, json
from urllib.request import urlopen
from urllib.parse import urlencode
from json2table import convert



# Create your views here.

# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()




# take user's book title input and attach to the base url to display search result link
def deweyDecimalLink(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    
    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonContent = json.dumps(xmlDict, indent=3, sort_keys=True)

    return HttpResponse(jsonContent)

    json_object = {"key" : "value"}
    build_direction = "TOP_TO_BOTTOM"
    table_attributes = {"style" : "width:100%"}
    html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)



    return HttpResponse(html)
    # return HttpResponse(jsonContent)


def owiToDDC(request):
    pass