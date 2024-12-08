import os
import time
from django.conf import settings

class CleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timestamp_file = os.path.join(settings.BASE_DIR, 'last_cleanup.txt')
        if os.path.exists(self.timestamp_file):
            with open(self.timestamp_file, 'r') as f:
                self.last_cleanup = float(f.read().strip())
        else:
            self.last_cleanup = 0

    def __call__(self, request):
        current_time = time.time()
        if current_time - self.last_cleanup > 3 * 3600:  # 12 hours in seconds
        # if current_time - self.last_cleanup > 60:  # 12 hours in seconds
            self.cleanup_zip_files()
            self.last_cleanup = current_time
            with open(self.timestamp_file, 'w') as f:
                f.write(str(self.last_cleanup))
        return self.get_response(request)

    def cleanup_zip_files(self):
        zip_folder = os.path.join(settings.MEDIA_ROOT, 'zips')
        deleted_count = 0

        for filename in os.listdir(zip_folder):
            file_path = os.path.join(zip_folder, filename)
            try:
                if os.path.isfile(file_path) and file_path.endswith('.zip'):
                    os.unlink(file_path)
                    deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        print(f"Deleted {deleted_count} zip files from filesystem.")