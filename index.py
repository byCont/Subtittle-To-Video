#index.py, Video Editor Backend

from flask import Flask
from flask import request
from flask import send_file
from flask_cors import CORS

from video_utils import generateVideoFromAudioAndSubtitles
from config import config
import os

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
        font_name = request.form.get('font_name', 'Product Sans')
        font_size = int(request.form.get('font_size', 30))
        text_case = request.form.get('text_case', 'lower')
        text_color = request.form.get('text_color', '#00000000')

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
						image_path=image_path
        )

        return {
            "status": "success",
            "message": "Video generated successfully",
            "generated_videopath": generated_video_path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to generate video: " + str(e)
        }
