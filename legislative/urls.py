from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "legislative"

urlpatterns = [
    # path("", views., name="legislative"),
    path("member/", views.create_member, name="member"),
    path("committee/", views.create_committee, name="committee"),
    path("subcommittee/", views.create_subcommittee, name="subcommittee"),
    path("success/", views.success_page, name="success_page"),
    path("data_json/", views.data_json, name="data_json"),
    path("data/", views.data, name="data"),
    path('upload_member_csv/', views.upload_member_csv, name='upload_member_csv'),
    path('upload_committee_csv/', views.upload_committee_csv, name='upload_committee_csv'),
    path('upload_title_csv/', views.upload_title_csv, name='upload_title_csv'),
    path('upload_data/', views.upload_data, name='upload_data'),
]