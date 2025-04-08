from django.urls import path
from .views import home, image_detection, pdf_detection, text_detection, scan_ai, upload_file, upload_pdf, process_manual_text, llm_text_detection


urlpatterns = [
    path('', home, name='home'),
    path('image-detection/', image_detection, name='image_detection'),
    path('pdf-detection/', pdf_detection, name='pdf_detection'),
    path('text-detection/', text_detection, name='text_detection'),
    path('scan-ai/', scan_ai, name='scan_ai'),
    path('upload-file/', upload_file, name='upload_file'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('process-manual-text/', process_manual_text, name='process_manual_text'),
    path('llm-text-detection/', llm_text_detection, name='llm_text_detection'),
]
