from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "data"

urlpatterns = [
    path("", views.data, name="data"),
    path("get_scrap_data/", views.get_scrap_data, name="get_scrap_data"),
    path("get_data/", views.get_data, name="get_data"),
    path("accepted_data/", views.accepted_data, name='accepted_data'),
    path("accepted_modification/", views.accepted_modification, name='accepted_modification'),
    path("rejected_data/", views.rejected_data, name='reject_data'),
    path("accepted/", views.accepted, name='accepted'),
    path("rejected/", views.rejected, name='rejected'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('success/', views.success_page, name='success_page'),
    path('feedback_data/<int:data_id>/', views.feedback_data, name='feedback_data'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)