from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import reverse

from utils.index import MillardAyo


ma = MillardAyo()


@api_view()
def index(request: Request):
    next_url = request.query_params.get('next')
    if not next_url:
        ma.run()
    else:
        ma.parse_next_page(next_url)
    data = {
        "data": {
            "posts": ma.posts,
            "next": f"/?next={ma.next_page_url}",

        }
    }
    return Response(data=data)


@api_view()
def show(request, url):
    # ma.parse_next_page(url)
    return Response(url)
