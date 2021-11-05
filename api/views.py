from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.index import MillardAyo


@api_view()
def index(request):
    ma = MillardAyo()
    ma.run()
    data = {
        "data": {
            "posts": ma.posts,
            "next": ma.next_page_url
        }
    }
    return Response(data=data)
