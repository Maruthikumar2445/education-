from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import os
import speech_recognition as sr
import soundfile as sf
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json
import uuid
import logging
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
class Config:
    UPLOAD_FOLDER = 'uploads'
    REPORTS_FOLDER = 'reports'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
    CLEANUP_THRESHOLD = 100 * 1024 * 1024  # 100MB
    API_KEY = "AIzaSyACd3jcYie92qktM_Gbc78O6ykgwJvPjNU"
  # Get API key from environment variable

app.config.from_object(Config)

# Ensure required folders exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['REPORTS_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Configure Gemini API
if not Config.API_KEY:
    raise ValueError("Gemini API key not found in environment variables")
    
genai.configure(api_key=Config.API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_VIDEO_EXTENSIONS

def cleanup_old_files():
    """Clean up old files when storage exceeds threshold"""
    try:
        total_size = 0
        for folder in [app.config['UPLOAD_FOLDER'], app.config['REPORTS_FOLDER']]:
            for root, _, files in os.walk(folder):
                for file in files:
                    total_size += os.path.getsize(os.path.join(root, file))

        if total_size > Config.CLEANUP_THRESHOLD:
            logger.info("Starting cleanup of old files")
            for folder in [app.config['UPLOAD_FOLDER'], app.config['REPORTS_FOLDER']]:
                for root, _, files in os.walk(folder):
                    for file in files:
                        filepath = os.path.join(root, file)
                        # Remove files older than 24 hours
                        if (datetime.now() - datetime.fromtimestamp(os.path.getctime(filepath))).days >= 1:
                            os.remove(filepath)
                            logger.info(f"Removed old file: {filepath}")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

class VideoConverter:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.output_folder = os.path.join(upload_folder, 'output_audio')
        os.makedirs(self.output_folder, exist_ok=True)

    def convert_to_audio(self, video_file):
        """Convert video to audio with enhanced error handling and quality settings"""
        try:
            video_path = os.path.join(self.upload_folder, video_file)
            output_path = os.path.join(self.output_folder, f"{uuid.uuid4()}.wav")
            
            # Enhanced FFmpeg command with better quality settings
            command = (
                f'ffmpeg -y -i "{video_path}" '
                f'-vn -acodec pcm_s16le -ar 44100 -ac 2 "{output_path}" '
                f'-loglevel error'
            )
            
            result = os.system(command)
            if result != 0:
                raise Exception("FFmpeg conversion failed")

            return output_path

        except Exception as e:
            logger.error(f"Error converting video to audio: {str(e)}")
            raise

    def convert_audio_to_text(self, audio_path):
        """Convert audio to text with improved accuracy and error handling"""
        r = sr.Recognizer()
        full_text = []

        try:
            with sf.SoundFile(audio_path) as audio_file:
                total_duration = len(audio_file) / audio_file.samplerate

            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                r.adjust_for_ambient_noise(source)
                
                # Process audio in chunks of 30 seconds
                chunk_duration = 30
                for offset in range(0, int(total_duration), chunk_duration):
                    audio = r.record(source, duration=min(chunk_duration, total_duration - offset))
                    try:
                        text = r.recognize_google(audio, language='en-US')
                        full_text.append(text)
                    except sr.UnknownValueError:
                        logger.warning(f"Could not understand audio at offset {offset}")
                    except sr.RequestError as e:
                        logger.error(f"Error with speech recognition service: {str(e)}")
                        raise

            return " ".join(full_text)

        except Exception as e:
            logger.error(f"Error in audio to text conversion: {str(e)}")
            raise

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        cleanup_old_files()  # Clean up old files before new upload

        if 'video' not in request.files:
            return jsonify({'error': 'No video file uploaded'}), 400

        video = request.files['video']
        if video.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(video.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        filename = secure_filename(f"{uuid.uuid4()}_{video.filename}")
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        video.save(video_path)
        logger.info(f"Video saved: {filename}")

        converter = VideoConverter(app.config['UPLOAD_FOLDER'])
        audio_path = converter.convert_to_audio(filename)
        extracted_text = converter.convert_audio_to_text(audio_path)

        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)

        return jsonify({'text': extracted_text})

    except Exception as e:
        logger.error(f"Error in upload_video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()

        if not question or not answer:
            return jsonify({'error': 'Missing or empty question or answer'}), 400

        # Enhanced prompt with better structure and guidelines
        prompt = f"""Question: {question}
Answer: {answer}

Please provide a comprehensive evaluation of the answer based on the following criteria:

1. Relevance (0-10 points):
- Direct address of the question
- Completeness of response
- Depth of understanding

2. Accuracy (0-10 points):
- Factual correctness
- Proper use of concepts
- Logical consistency

3. Structure (0-10 points):
- Organization
- Clarity
- Flow of ideas

4. Language (0-10 points):
- Grammar
- Vocabulary
- Style

Please provide:
1. A score for each criterion
2. Brief justification for each score
3. Overall score (average of all criteria)
4. Specific suggestions for improvement

Format the response clearly with headers and bullet points."""

        response = model.generate_content(prompt)
        if not response.text:
            raise ValueError("Empty response from AI model")

        return jsonify({'evaluation': response.text})

    except Exception as e:
        logger.error(f"Error in evaluate: {str(e)}")
        return jsonify({'error': f'Evaluation error: {str(e)}'}), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        required_fields = ['question', 'answer', 'evaluation']
        
        if not all(data.get(field, '').strip() for field in required_fields):
            return jsonify({'error': 'Missing required data'}), 400

        report_id = str(uuid.uuid4())
        filename = f'report_{report_id}.pdf'
        filepath = os.path.join(app.config['REPORTS_FOLDER'], filename)

        # Generate PDF with improved formatting and error handling
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            styles = getSampleStyleSheet()
            story = []

            # Add timestamp and report ID
            story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph(f"Report ID: {report_id}", styles['Normal']))
            story.append(Spacer(1, 12))

            # Add content with improved formatting
            for section, content in [
                ("Question", data['question']),
                ("Answer", data['answer']),
                ("Evaluation", data['evaluation'])
            ]:
                story.append(Paragraph(section, styles['Heading1']))
                story.append(Paragraph(content, styles['Normal']))
                story.append(Spacer(1, 12))

            doc.build(story)
            logger.info(f"Report generated: {filename}")
            
            return jsonify({'filename': filename})

        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
            raise

    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_report/<filename>')
def download_report(filename):
    try:
        file_path = os.path.join(app.config['REPORTS_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Report not found'}), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'evaluation_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        )

    except Exception as e:
        logger.error(f"Error in download_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

if __name__ == '__main__':
    app.run(debug=True,port=5055)  # Set debug=False for production