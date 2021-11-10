
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import reverse
from api.serializer import ContactSerializer
from datetime import datetime


from utils.index import MillardAyo, get_base_server_addr, send_email_to_admin


@api_view()
def index(request: Request):
    ma = MillardAyo()
    next_url = request.query_params.get('next')
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


@api_view(http_method_names=['POST'])
def contact(request):
    contactS = ContactSerializer(data=request.POST)
    if not contactS.is_valid():
        data = {
            "data": {
                "errors": contactS.errors,
            }
        }
        return Response(data, 422)

    message = contactS.data['message']
    email = contactS.data['email']
    fullname = contactS.data['fullname']

    send_email_to_admin(f"Email from MilaApi Contact {datetime.now()}",
                        message=f"{fullname} - {email} \n\n {message}", from_email=email)

    data = {
        "data": {
            "message": "Thank you!",
        }
    }

    return Response(data)
