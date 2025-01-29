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
    font_size: int = 90,
    text_case: str = 'lower',
    text_color: str = "#0000FF80"
):
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])
    
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()
    
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    # Convertir subtítulos a ASS con efectos
    temp_ass = "temp_subtitles.ass"
    convert_to_ass_with_effects(subtitlefile, temp_ass, font_name, font_size, text_case)
    
    # Cadena de filtros compleja para añadir el cuadro con el color recibido
    complex_filter = (
        "[0:v]scale=1920:1080[scaled]; "  # Escalar el video de fondo
        f"color=c={text_color}:s=1920x1080,format=rgba[color_layer]; "  # Generar capa con color personalizado
        "[scaled][color_layer]overlay=format=auto[overlaid]; "  # Combinar capas
        "[overlaid]fps=24[withfps]; "  # Ajustar FPS
        f"[withfps]subtitles={temp_ass}:force_style="  # Añadir subtítulos
        f"'FontName={font_name},FontSize={font_size},Outline=2,Blur=15'[final]" 
    )

    command = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-t", str(audio_duration),
        "-i", background_video_path,
        "-i", audiofile,
        "-filter_complex", complex_filter,
        "-map", "[final]",  # Mapear salida del filtro
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "30",
        "-c:a", "aac",
        "-b:a", "299k",
        "-shortest",
        "-y",
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        os.remove(temp_ass)  # Limpiar archivo temporal
    except Exception as e:
        print(f"Error: {e}")
        raise
    
    return output_path
