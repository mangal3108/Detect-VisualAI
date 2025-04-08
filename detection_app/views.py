from django.shortcuts import render
from django.http import JsonResponse
import os
import cv2
import numpy as np
import pytesseract
import time
import logging
from pdf2image import convert_from_path

# Set up logger
logger = logging.getLogger(__name__)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLO model with correct paths
yolo_net = cv2.dnn.readNet("D:\desktop bg\AI DETECTION\models\yolov3.weights", 
                          "D:\desktop bg\AI DETECTION\models\yolov3.cfg")
layer_names = yolo_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

def home(request):
    return render(request, 'index.html')

def image_detection(request):
    return render(request, 'image-detection.html')

def pdf_detection(request):
    return render(request, 'pdf-detection.html')

def text_detection(request):
    return render(request, 'text-detection.html')

def scan_ai(request):
    return render(request, 'scan-ai.html')

def process_manual_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        return JsonResponse({
            'processed_text': text,
            'message': 'Text processed successfully'
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            upload_dir = 'static/uploads'
            
            # Create upload directory if it doesn't exist
            try:
                os.makedirs(upload_dir, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create upload directory: {str(e)}")
                return JsonResponse({
                    'error': 'Failed to create upload directory',
                    'details': str(e)
                }, status=500)
                
            file_name = f"{int(time.time())}_{file.name}"
            file_path = os.path.join(upload_dir, file_name)
            
            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                logger.info(f"Successfully uploaded file: {file_name}")

                if file.name.endswith(('.png', '.jpg', '.jpeg')):
                    result = detect_ai_image_content(file_path)
                    return JsonResponse(result)
                else:
                    return JsonResponse({'error': 'Unsupported file format'}, status=400)
                    
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
    return JsonResponse({'error': 'No file uploaded'}, status=400)

def upload_pdf(request):
    if request.method == 'POST':
        if 'pdf' in request.FILES:
            file = request.FILES['pdf']
            upload_dir = 'static/uploads'
            
            # Create upload directory if it doesn't exist
            try:
                os.makedirs(upload_dir, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create upload directory: {str(e)}")
                return JsonResponse({
                    'error': 'Failed to create upload directory',
                    'details': str(e)
                }, status=500)
                
            file_name = f"{int(time.time())}_{file.name}"
            file_path = os.path.join(upload_dir, file_name)
            
            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                logger.info(f"Successfully uploaded PDF: {file_name}")

                if file.name.endswith('.pdf'):
                    return detect_ai_pdf_content(file_path)
                else:
                    return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)
                    
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
    return JsonResponse({'error': 'No PDF file uploaded'}, status=400)

def detect_ai_pdf_content(pdf_path):
    def analyze_text_content(text):
        # Simple heuristic for text analysis
        human_words = ['the', 'and', 'is', 'in', 'to', 'of']  # Example human-like words
        ai_words = ['generated', 'model', 'algorithm', 'data', 'AI']  # Example AI-like words
        
        human_count = sum(text.lower().count(word) for word in human_words)
        ai_count = sum(text.lower().count(word) for word in ai_words)
        
        total_count = human_count + ai_count
        
        if total_count == 0:
            return {
                'human_percentage': 0.0,
                'ai_percentage': 0.0
            }
        
        return {
            'human_percentage': round((human_count / total_count) * 100, 2),
            'ai_percentage': round((ai_count / total_count) * 100, 2)
        }




    try:
        logger.info(f"Starting PDF processing for: {pdf_path}")
        
        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return JsonResponse({'error': 'PDF file not found'}, status=400)
            
        # Verify poppler path exists
        poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
        if not os.path.exists(poppler_path):
            logger.error(f"Poppler path not found: {poppler_path}")
            return JsonResponse({'error': 'PDF processing tools not configured properly'}, status=500)
            
        # Convert PDF to images with error handling
        try:
            logger.info("Converting PDF to images...")
            images = convert_from_path(
                pdf_path, 
                poppler_path=poppler_path,
                fmt='jpeg',
                thread_count=4
            )
        except Exception as e:
            logger.error(f"PDF conversion failed: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': 'PDF conversion failed',
                'details': str(e)
            }, status=400)
            
        if not images:
            logger.error("No pages found in PDF")
            return JsonResponse({'error': 'No pages found in PDF'}, status=400)

        results = []
        text_analysis_results = []


        logger.info(f"Processing {len(images)} pages...")
        for idx, image in enumerate(images):
            image_path = f"static/uploads/temp_{int(time.time())}_{idx}.jpg"
            try:
                logger.info(f"Processing page {idx + 1}")
                image.save(image_path, 'JPEG')
                result = detect_ai_image_content(image_path)
                extracted_text = pytesseract.image_to_string(image)  # Extract text from the image
                text_analysis = analyze_text_content(extracted_text)  # Analyze the extracted text
                text_analysis_results.append(text_analysis)  # Store the analysis results


                results.append(result)
                logger.info(f"Successfully processed page {idx + 1}")
            except Exception as e:
                error_msg = f'Page {idx + 1} processing failed: {str(e)}'
                logger.error(error_msg)
                results.append({
                    'error': error_msg,
                    'page': idx + 1
                })
                continue

        # Check if any page has AI detected content
        successful_results = [r for r in results if isinstance(r, dict) and 'ai_detected' in r]
        ai_detected = any(r['ai_detected'] for r in successful_results)
        
        logger.info(f"PDF processing completed. Successful pages: {len(successful_results)}, Failed pages: {len(results) - len(successful_results)}")
        
        return JsonResponse({
            'results': results,
            'ai_detected': ai_detected,
            'message': f"Processed {len(results)} pages",
            'successful_pages': len(successful_results),
            'text_analysis_results': text_analysis_results,  # Include text analysis results
            'human_accuracy': sum(result['human_percentage'] for result in text_analysis_results) / len(text_analysis_results) if text_analysis_results else 0,
            'ai_accuracy': sum(result['ai_percentage'] for result in text_analysis_results) / len(text_analysis_results) if text_analysis_results else 0,



            'failed_pages': len(results) - len(successful_results)
        })
        
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'PDF processing failed',
            'details': str(e)
        }, status=500)

def llm_text_detection(request):
    if request.method == 'POST':
        if 'llm_file' in request.FILES:
            file = request.FILES['llm_file']
            try:
                text = file.read().decode('utf-8')
                result = {'text': text, 'ai_probability': 0.75}
                return JsonResponse(result)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        elif 'llm_text' in request.POST:
            text = request.POST.get('llm_text', '')
            if text:
                result = {'text': text, 'ai_probability': 0.75}
                return JsonResponse(result)
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def detect_ai_image_content(image_path):
    def analyze_image_content(detections):
        # Simple heuristic for image analysis
        human_count = sum(1 for d in detections if d['class_id'] in [0, 1])  # Example human-like classes
        ai_count = sum(1 for d in detections if d['class_id'] in [2, 3])  # Example AI-like classes
        
        total_count = human_count + ai_count
        
        if total_count == 0:
            return {
                'human_percentage': 0.0,
                'ai_percentage': 0.0
            }
        
        return {
            'human_percentage': round((human_count / total_count) * 100, 2),
            'ai_percentage': round((ai_count / total_count) * 100, 2)
        }


    image = cv2.imread(image_path)
    height, width, channels = image.shape

    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    yolo_net.setInput(blob)
    layer_outputs = yolo_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    detections = []
    if len(indices) > 0:
        for i in indices.flatten():
            detection = {
                'box': boxes[i],
                'confidence': confidences[i],
                'class_id': int(class_ids[i])
            }
            detections.append(detection)

    output_image = image.copy()
    for detection in detections:
        x, y, w, h = detection['box']
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    output_path = image_path.replace('.', '_detected.')
    cv2.imwrite(output_path, output_image)

    analysis_results = analyze_image_content(detections)  # Analyze the detections for accuracy
    ai_detected = len(detections) > 0 and any(d['confidence'] > 0.8 for d in detections)

    
    return {
        'human_accuracy': analysis_results['human_percentage'],  # Include human accuracy
        'ai_accuracy': analysis_results['ai_percentage'],  # Include AI accuracy

        'detections': detections,
        'output_image': output_path,
        'ai_detected': ai_detected,
        'message': f"Detected {len(detections)} objects"
    }
