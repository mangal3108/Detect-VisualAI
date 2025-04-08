

## 🧠 AI-Based Image, PDF, and Text Detection System

An intelligent web application that detects AI-generated content in **images**, **PDFs**, and **text** using deep learning techniques like YOLOv3 and Tesseract OCR. Built with Django and a user-friendly frontend.

---

### 🚀 Features

- 🔍 Detect AI-generated images using YOLOv3
- 📄 Analyze PDFs (image + text extraction)
- 📝 Detect AI-generated text via keyword-based heuristics
- 📷 Optional: Real-time camera input for surveillance
- 📊 Displays AI vs Human content accuracy
- 🌐 Simple web interface

---

### 🧰 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django (Python)
- **AI Models:** YOLOv3, Tesseract OCR
- **Libraries:** OpenCV, NumPy, pytesseract, pdf2image, Pillow
- **Deployment Ready:** Localhost / Cloud (Heroku, AWS, etc.)

---

### 📁 Project Structure

```
📦 ai-detector/
├── 📁 static/               # CSS, JS, images
├── 📁 templates/            # HTML templates
├── 📁 uploads/              # Uploaded files
├── 📄 views.py              # Main logic (YOLO + Tesseract)
├── 📄 urls.py
├── 📄 settings.py
├── 📄 manage.py
└── 📄 requirements.txt
```

---

### ⚙️ Installation & How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-detector.git
   cd ai-detector
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Required Tools Are Installed:**
   - **Tesseract OCR:**  
     Download and install from [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)  
     Add the path to `pytesseract.pytesseract.tesseract_cmd` in `views.py`.

   - **Poppler for Windows (PDF to image):**  
     Download from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)

   - **YOLOv3 Files (Place in `/models/` directory):**
     - `yolov3.cfg`
     - `yolov3.weights`

5. **Run the server**
   ```bash
   python manage.py runserver
   ```

6. **Open in Browser**  
   Go to `http://127.0.0.1:8000/`

---

### 🧪 How It Works

- **Images:** Analyzed using YOLOv3 model
- **PDFs:** Converted to images → OCR text → AI vs Human probability
- **Text:** Pattern matching and keyword scoring for AI-likeness

---

### 📌 Future Enhancements

- Transformer-based AI content detection
- Integration with OpenAI/Gemini API (optional)
- Enhanced UI with result graphs
- Voice & audio analysis (upcoming)

---

### 📬 Contact

Created by **Mangal Krishna Singh Bhadouriya**  
📧 [mangalkrishnabhadouriya@gmail.com](mailto:mangalkrishnabhadouriya@gmail.com)  
🎓 ITM University, Gwalior


### ⚙️ How to Run

1. **Navigate to the project directory:**
   ```bash
   cd ai_detection_project
   ```

2. **Run the Django development server:**
   ```bash
   python manage.py runserver
   ```

3. **Open your browser and go to:**
   ```
   http://127.0.0.1:8000/
   ```

Your AI Detection Web App should now be running locally! 🚀


