import os
import uuid
import zipfile
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.views import View

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.values()
        if not files:
            return JsonResponse({'error': 'No files were uploaded.'}, status=400)

        # Create a unique folder name for this upload
        folder_name = str(uuid.uuid4())
        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads', folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Save uploaded files to the folder
        file_paths = []
        for file in files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            file_paths.append(file_path)

        # Ensure the 'uploads' and 'zips' directories exist
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'zips'), exist_ok=True)

        # Create a zip file
        zip_filename = f'{folder_name}.zip'
        zip_path = os.path.join(settings.MEDIA_ROOT, 'zips', zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for file_path in file_paths:
                zip_file.write(file_path, os.path.basename(file_path))

        # Clean up the original files
        for file_path in file_paths:
            os.remove(file_path)
        os.rmdir(folder_path)

        # Generate the download URL
        download_url = request.build_absolute_uri(f'/download/{zip_filename}/')

        return JsonResponse({'download_url': download_url})

class DownloadView(View):
    def get(self, request, filename):
        file_path = os.path.join(settings.MEDIA_ROOT, 'zips', filename)
        if os.path.exists(file_path):
            download_url = request.build_absolute_uri(f'/media/zips/{filename}')
            return render(request, 'download.html', {'download_url': download_url})
        else:
            return HttpResponse("File not found", status=404)

def serve_zip_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'zips', filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("File not found", status=404)

