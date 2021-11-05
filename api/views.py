from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import reverse

from utils.index import MillardAyo, get_base_server_addr


@api_view()
def index(request: Request):
    ma = MillardAyo()
    next_url = request.query_params.get('next')
    print(next_url)
    if not next_url:
        ma.run()
    else:
        ma.parse_next_page(next_url)
    data = {
        "data": {
            "base_url": get_base_server_addr(request),
            "posts": ma.posts,
            "next": f"{get_base_server_addr(request)}/?next={ma.next_page_url}",
        }
    }
    return Response(data=data)


@api_view()
def show(request, url):
    ma = MillardAyo()
    res = ma.get_post_details(url)
    data = {
        "data": {
            "post": res,
        }
    }
    return Response(data=data)
