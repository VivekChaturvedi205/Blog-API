
from django.urls import path
from .views import BlogView,PublicView

urlpatterns = [
    path('blog/', BlogView.as_view(), name='blog'),
    path('publicview/', PublicView.as_view(), name='publicview')
]
