from django.urls import path

from . import views

app_name = "data"

urlpatterns = [
    path("products/", views.products, name="products"),
    path("products_page/", views.products_page, name="products"),
    path("data/", views.data, name="data"),
    path("leadership_data/", views.get_leadership_data, name="leadership_data"),
    path("get_data/", views.get_data, name="leadership_data"),
    path("accepted_data/", views.accepted_data, name='accepted_data'),
    path("rejected_data/", views.rejected_data, name='reject_data'),
    path("accepted/", views.accepted, name='accepted'),
    path("rejected/", views.rejected, name='rejected'),


]