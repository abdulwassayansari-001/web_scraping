from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "legislative"

urlpatterns = [
    # path("", views., name="legislative"),
    path("success/", views.success_page, name="success_page"),
    path("data_json/", views.data_json, name="data_json"),
    path("combine_data_json/", views.combine_data_json, name="combine_data_json"),
    path("combine_data/", views.combine_data, name="combine_data"),
    path("", views.data, name="data"),
    path('upload_member_csv/', views.upload_member_csv, name='upload_member_csv'),
    path('upload_combine_data_csv/', views.upload_combine_data_csv, name='upload_combine_data_csv'),
    path('upload_committee_csv/', views.upload_committee_csv, name='upload_committee_csv'),
    path('upload_subcommittee_csv/', views.upload_subcommittee_csv, name='upload_subcommittee_csv'),
    path('upload_title_csv/', views.upload_title_csv, name='upload_title_csv'),
    path('upload_hierarchy_csv/', views.upload_hierarchy_csv, name='upload_hierarchy_csv'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('delete_data/<int:id>', views.delete_data, name='delete_data'),
]