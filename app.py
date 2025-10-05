from flask import Flask, render_template, send_file, request, after_this_request
from utils import get_file_size, get_file_extension, allowed_file, get_file_type, images, videos, music
import os
import time
import threading
from converter import convert_image, convert_video, convert_audio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_FILE_AGE'] = 600  # 10 minutes for original files
app.config['CONVERTED_FILE_AGE'] = 60  # 1 minute for converted files

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Track original uploaded files vs converted files
original_files = set()
file_lock = threading.Lock()

# Note cleanup setup is vibe coded by claude 4.5 sonnet 
def cleanup_old_files():
    """Background task to clean up abandoned files"""
    while True:
        try:
            current_time = time.time()
            upload_folder = app.config['UPLOAD_FOLDER']
            
            for filename in os.listdir(upload_folder):
                filepath = os.path.join(upload_folder, filename)
                
                # Check if it's a file
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    
                    # Different age thresholds for original vs converted files
                    with file_lock:
                        is_original = filename in original_files
                    
                    max_age = app.config['MAX_FILE_AGE'] if is_original else app.config['CONVERTED_FILE_AGE']
                    
                    if file_age > max_age:
                        try:
                            os.remove(filepath)
                            with file_lock:
                                original_files.discard(filename)
                            app.logger.info(f"Cleaned up old file: {filename}")
                        except Exception as e:
                            app.logger.error(f"Error removing {filename}: {e}")
                            
        except Exception as e:
            app.logger.error(f"Error in cleanup task: {e}")
        
        # Run cleanup every 2 minutes
        time.sleep(120)

# Start background cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/converter', methods=['POST'])
def converter():
    file = request.files['file']
    filename = file.filename
    
    if not allowed_file(filename, images + videos + music):
        return "Unsupported file type.", 400
    
    # Generate unique filename to avoid conflicts
    timestamp = str(int(time.time() * 1000))
    base_name, ext = os.path.splitext(filename)
    unique_filename = f"{base_name}_{timestamp}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # Save the file
    file.save(filepath)
    
    # Mark as original file (will be kept longer)
    with file_lock:
        original_files.add(unique_filename)
    
    # Check file size
    file_size = get_file_size(filepath)
    if file_size > 100 * 1024 * 1024:  # 100 MB limit
        # Clean up the uploaded file if it's too large
        if os.path.exists(filepath):
            os.remove(filepath)
        with file_lock:
            original_files.discard(unique_filename)
        return "File size exceeds the 100 MB limit.", 400
    
    file_extension = get_file_extension(unique_filename)
    return render_template('converterPage.html', filename=unique_filename, file_extension=file_extension)

@app.route('/convert/<filename>', methods=['POST'])
def convert_file(filename):
    target_format = request.form['output_format']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if original file still exists
    if not os.path.exists(filepath):
        return "Original file not found. Please upload again.", 404
    
    file_extension = get_file_extension(filename)
    file_type = get_file_type(file_extension)
    output_file = None

    try:
        if file_type == "image" and target_format in images:
            output_file = convert_image(filepath, target_format)
        elif file_type == "video" and target_format in videos:
            output_file = convert_video(filepath, target_format)
        elif file_type == "audio" and target_format in music:
            output_file = convert_audio(filepath, target_format)
        else:
            # Clean up original file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            with file_lock:
                original_files.discard(filename)
            return "Unsupported conversion.", 400

        # Only clean up the CONVERTED file after sending
        # Keep the ORIGINAL file for potential re-conversions
        @after_this_request
        def cleanup(response):
            try:
                # Only remove converted file, keep original
                if output_file and os.path.exists(output_file):
                    os.remove(output_file)
            except Exception as e:
                app.logger.error(f"Error during cleanup: {e}")
            return response

        return send_file(output_file, as_attachment=True)
        
    except Exception as e:
        # Clean up files on conversion error
        if os.path.exists(filepath):
            os.remove(filepath)
        with file_lock:
            original_files.discard(filename)
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
        return f"Error during conversion: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)