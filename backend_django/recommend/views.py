# from ..backend import wsgi

from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import BookSerializer, DeweyDecimalLink, BooksDisplayedSerlizer
from .models import Book, BooksDisplayed
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import xml.etree.ElementTree as ET
import xmltodict, json
from urllib.request import urlopen
from urllib.parse import urlencode
from json2table import convert
import json
import os


# Create your views here.


# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})


    
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()






# isbn to Dewey decimal
def deweyDecimalLink(request):


    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'isbn'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})

    
    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContent = json.loads(jsonDumps)

    # items = jsonContent.get("classify").get('works').get('work')
    base = jsonContent.get("classify").get('editions').get('edition')[0]
    # deweyNumber = base.get('classifications').get('class')[0].get('@sfa')

    # pets_data = open("data.json", "w")
    # json.dump(xmlDict, pets_data)
    # pets_data.close()



def owiToDDC(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = None
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # http://classify.oclc.org/classify2/Classify?owi=263706&summary=true



def showStaticMock(request):

    # if request.method == 'GET':
    queryset = BooksDisplayed.objects.all()
    serializer = BooksDisplayedSerlizer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)



def saveFileUpload(upload, savePath):

    with open(savePath, "wb+") as outputFile:
        uploadedFile = upload.FILES["file-upload-name"]
        for chunk in uploadedFile.chunks():
            outputFile.write(chunk)


class BooksDisplayedList(generics.ListCreateAPIView):
    queryset = BooksDisplayed.objects.all()
    serializer_class = BooksDisplayedSerlizer

    


'''

# Search by title
# take user's book title input and attach to the base url to display search result link
base = 'http://classify.oclc.org/classify2/Classify?'
parmType = 'title'
parmValue = request.GET.get('q')
searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
# http://classify.oclc.org/classify2/Classify?title=into+the+wild
# http://127.0.0.1:8000/bookclassify/?q=into+the+wild

# ------------------------------------------------------------
jsonData = 'bookMockData.json'
def showStaticMock(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, jsonData)

    with open(my_file) as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)
'''