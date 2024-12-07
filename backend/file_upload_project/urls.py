"""
URL configuration for file_upload_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from file_upload.views import FileUploadView, DownloadView ,serve_zip_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<str:filename>/', DownloadView.as_view(), name='download'),
    path('media/zips/<str:filename>', serve_zip_file, name='serve-zip-file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
