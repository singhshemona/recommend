# from ..backend import wsgi

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer, DeweyDecimalLink
from .models import Book
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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



# class DeweyView(viewsets.ModelViewSet):
#     serializer_class = DeweyDecimalLink
#     queryset = DeweyDecimalLink.objects.all()


# take user's book title input and attach to the base url to display search result link
def deweyDecimalLink(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # http://classify.oclc.org/classify2/Classify?title=into+the+wild
    # http://127.0.0.1:8000/bookclassify/?q=into+the+wild


    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContent = json.loads(jsonDumps)

    items = jsonContent.get("classify").get('works').get('work')

    # pets_data = open("data.json", "w")
    # json.dump(xmlDict, pets_data)
    # pets_data.close()



    # jsonDict = {}
    # jsonDict["works"] = jsonContent.get('classify')

    # result = []
    # for item in jsonContent:
    #     my_dict = {}
    #     my_dict['owi']=item.get("classify").get
    #     result.append(my_dict)
    # back_json=json.dumps(jsonDict)

    # books = jsonContent['work']

    '''
    Need to searlize the data! Then return JSON
    '''

    return JsonResponse(items, safe=False)





def owiToDDC(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = None
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # http://classify.oclc.org/classify2/Classify?owi=263706&summary=true





    # --------------------------------------------
    # print(jsonContent, file='output.txt')

    # json_object = {"key" : "value"}
    # build_direction = "TOP_TO_BOTTOM"
    # table_attributes = {"style" : "width:100%"}
    # html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    # return HttpResponse(html)
    # return HttpResponse(jsonContent)