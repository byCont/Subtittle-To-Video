# video_utils.py, Video editor backend

from moviepy.editor import AudioFileClip
from config import config
import time
import subprocess
from convert_to_ass import convert_to_ass_with_effects
import os

def generateVideoFromAudioAndSubtitles(
    audiofile: str, 
    subtitlefile: str, 
    font_name: str = "Product Sans",
    font_size: int = 30
):
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])
    
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()
    
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    # Convertir subtítulos a ASS con efectos
    temp_ass = "temp_subtitles.ass"
    convert_to_ass_with_effects(subtitlefile, temp_ass, font_name, font_size)
    
    # Cadena de filtros simplificada
    vf_chain = [
      "scale=1920:1080",
      "fps=24",
      f"subtitles={temp_ass}:force_style="
      f"'FontName={font_name},FontSize={font_size},"
      "Alignment=10,Outline=2,Blur=15'"
    ]

    command = [
      "ffmpeg",
      "-stream_loop", "-1",
      "-t", str(audio_duration),
      "-i", background_video_path,
      "-i", audiofile,
      "-vf", ",".join(vf_chain),
      "-c:v", "libx265",
      "-preset", "medium",
      "-crf", "30",
      "-c:a", "aac",
      "-b:a", "299k",
      "-map", "0:v:0",
      "-map", "1:a:0",
      "-shortest",
      "-y",
      output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        # os.remove(temp_ass)  # Limpiar archivo temporal
    except Exception as e:
        print(f"Error: {e}")
        raise
    
    return output_path
