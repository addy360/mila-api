from django.urls import path

from api.views import contact, index, show
urlpatterns = [
    path('', index, name="all_posts"),
    path('admin/contact', contact, name='contact'),
    path('<str:url>/', show, name="post_details")
]
