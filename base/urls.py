from . import views
from django.conf import settings
from django.conf.urls.static import static  # new
from django.urls import path

urlpatterns = [
    path("home/", views.HomePage.as_view(), name="home"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #new

