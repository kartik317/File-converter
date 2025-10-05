import os
images = ["png", "jpg", "jpeg", "webp"]
videos = ["mp4", "mkv", "avi", "mov", "mp3"] # mp3 is included because some users might want to extract audio from video files
music = ["mp3", "wav", "ogg", "m4a"]

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def get_file_type(extension):
    if extension in images:
        return "image"
    elif extension in music:
        return "audio"
    elif extension in videos:
        return "video"
    else:
        return "other"

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_size(filepath):
    return os.path.getsize(filepath)