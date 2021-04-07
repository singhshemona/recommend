from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Book
from django.http import HttpResponse

from urllib.parse import urlencode
# from backend import deweyDecimalScript

# Create your views here.

# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

# def bookClassifyView(request):
#     # linkPrefix = 'http://classify.oclc.org/classify2/Classify?title='
#     # linkPostfix = 'the%20essential%20rumi&summary=true'
#     userTitleInput = 'the essential Rumi'
    
#     linkToBooks = deweyDecimalScript("hello") > 'text.txt'
#     return HttpResponse(linkToBooks)



def deweyDecimalLink(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = request.GET.get('q') #'the essential Rumi'
    # summaryBase = '&summary=true'

    # def getText(nodelist):
    #     rc = ""
    #     for node in nodelist:
    #         if node.nodeType == node.TEXT_NODE:
    #             rc = rc + node.data
    #     return rc

    # xdoc = ''
    # try:
    nextURL = base + urlencode({parmType:parmValue.encode('utf-8')}) # + summaryBase
    # else: nextURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # print(nextURL) # XML: send this to front end
    return HttpResponse(nextURL)


# def get_queryset(self): # new
#         query = self.request.GET.get('q')
#         object_list = City.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
#         return object_list