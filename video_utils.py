# video_utils.py, Video editor backend

# video_utils.py
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from config import config
import time
import subprocess
import os

def trimVideo(videofile: str, start_time: int, end_time: int):
    clip = VideoFileClip(videofile)
    videofile = videofile.replace(config['video_savepath'], "")
    trimpath = config['video_savepath'] + "edited_" + str(int(time.time())) + videofile
    trimmed_clip = clip.subclip(start_time, end_time)
    trimmed_clip.write_videofile(trimpath)
    return trimpath

def mergeVideos(videoclip_filenames):
    videoclips = []
    for filename in videoclip_filenames:
        videoclips.append(VideoFileClip(filename))
    final_clip = concatenate_videoclips(videoclips, method="compose")
    finalpath = "clips/finalrender_" + str(int(time.time())) + ".mp4"
    final_clip.write_videofile(finalpath)
    return finalpath

def generateVideoFromAudioAndSubtitles(audiofile: str, subtitlefile: str):
    
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[4])
    
    # Cargar el video de fondo
    video = VideoFileClip(background_video_path)
    
    # Cargar el audio
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    
    # Repetir el video de fondo para igualar la duración del audio
    looped_video = video.loop(duration=audio_duration)
    
    # Agregar el audio al video repetido
    looped_video = looped_video.set_audio(audio)
    
    # Guardar el video sin subtítulos temporalmente
    temp_video_path = config['video_savepath'] + "temp_video_" + str(int(time.time())) + ".mp4"
    looped_video.write_videofile(temp_video_path, codec="libx264", audio_codec="aac")
    
    # Generar el video final con subtítulos utilizando ffmpeg
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    command = [
        
        "ffmpeg",
        "-i", temp_video_path,  # Cambiado para usar el video temporal con audio
        "-vf", (
            f"scale=1280:720,subtitles={subtitlefile}:force_style="
            "'FontName=Product Sans,FontSize=40,Alignment=2,MarginV=140,"
            "OutlineColour=&H80FFFFFF&,BorderStyle=1'"
        ),
        "-c:v", "libx264",
        "-preset", "medium",  # Balance entre calidad y velocidad de codificación
        "-crf", "27",  # Factor de calidad constante (18-28 es un buen rango, menor = mejor calidad)
        "-c:a", "aac",
        "-b:a", "199k",
        "-y",  # Sobrescribir archivo de salida si existe
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el video: {e}")
        raise
    finally:
        # Eliminar el video temporal
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
    
    return output_path
