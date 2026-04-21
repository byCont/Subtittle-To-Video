#index.py, Video Editor Backend

from flask import Flask
from flask import request
from flask import send_file
from flask_cors import CORS

from video_utils import generateVideoFromAudioAndSubtitles
from config import config
import os
import uuid
import json

app = Flask(__name__,static_folder="./frontend/dist/assets",template_folder="./frontend/dist")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return {
		"status": "success",
		"message": "Video editor backend"
	}

@app.route('/clips/<filename>')
def render_clip(filename):
	return send_file(config['video_savepath'] + filename)

# Uploads a video file to server and returns filename
@app.route('/upload_video',methods=['POST'])
def upload_video():
	# check if video savepath exists
	if  not os.path.isdir("./clips"):
		os.mkdir("./clips")
	try:
		videofile = request.files['videofile']
		filepath = config['video_savepath'] + videofile.filename
		videofile.save(filepath)
	except FileNotFoundError:
		return "ERROR"

	return str(filepath)


@app.route('/generate_video', methods=['POST'])
def generate_video():
    task_id = request.form.get('task_id', str(uuid.uuid4()))
    # check if video savepath exists
    if not os.path.isdir("./clips"):
        os.mkdir("./clips")
    try:
        audiofile = request.files['audiofile']
        subtitlefile = request.files['subtitlefile']
        imagefile = request.files.get('imagefile')
        
        # Guardar imagen si está presente
        image_path = None
        if imagefile:
            image_path = config['video_savepath'] + imagefile.filename
            imagefile.save(image_path)
						
        # Obtener parámetros de estilo
        font_name = request.form.get('font_name', 'Lexend Bold')
        font_size = int(request.form.get('font_size', 30))
        text_case = request.form.get('text_case', 'capitalize')
        text_color = request.form.get('text_color', 'light')
        bg_color = request.form.get('bg_color', '#00000000')

        audio_path = config['video_savepath'] + audiofile.filename
        subtitle_path = config['video_savepath'] + subtitlefile.filename

        audiofile.save(audio_path)
        subtitlefile.save(subtitle_path)

        # Pasar parámetros a la función
        generated_video_path = generateVideoFromAudioAndSubtitles(
            audio_path, 
            subtitle_path,
            font_name=font_name,
            font_size=font_size,
            text_case=text_case,
            text_color=text_color,
            bg_color=bg_color,
            image_path=image_path,
            task_id=task_id
        )

        return {
            "status": "success",
            "message": "Video generated successfully",
            "generated_videopath": generated_video_path,
            "task_id": task_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to generate video: " + str(e)
        }

@app.route('/progress/<task_id>', methods=['GET'])
def get_progress(task_id):
    progress_file = os.path.join(config['video_savepath'], f"progress_{task_id}.txt")
    meta_file = os.path.join(config['video_savepath'], f"progress_{task_id}_meta.json")
    
    if not os.path.exists(meta_file):
        return {"status": "pending", "percentage": 0}
        
    try:
        with open(meta_file, 'r') as f:
            meta = json.load(f)
    except Exception:
        return {"status": "pending", "percentage": 0}
        
    duration = meta.get("duration", 1.0)
    
    if not os.path.exists(progress_file):
        return {"status": "processing", "percentage": 0, "speed": "0x", "time": "00:00:00", "duration": duration}
        
    out_time_us = 0
    speed = "N/A"
    out_time = "00:00:00"
    try:
        with open(progress_file, 'r') as f:
            lines = f.readlines()
            for line in reversed(lines):
                if line.startswith("out_time_us="):
                    val = line.split("=")[1].strip()
                    if val.isdigit() or val.startswith("-"):
                        out_time_us = int(val)
                elif line.startswith("speed="):
                    speed = line.split("=")[1].strip()
                elif line.startswith("out_time="):
                    out_time = line.split("=")[1].strip()
                if out_time_us and speed != "N/A" and out_time != "00:00:00":
                    break
    except Exception:
        pass
        
    if duration > 0:
        percentage = (max(0, out_time_us) / 1000000) / duration * 100
    else:
        percentage = 0
    percentage = min(100.0, max(0.0, percentage))
    
    return {
        "status": "processing",
        "percentage": round(percentage, 2),
        "speed": speed,
        "time": out_time,
        "duration": duration
    }
