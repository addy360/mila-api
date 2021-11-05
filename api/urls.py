from django.urls import path

from api.views import index, show
urlpatterns = [
    path('', index, name="all_posts"),
    path('<str:url>/', show, name="post_details")
]
