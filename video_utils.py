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
    text_color: str = "#0000FF80",
    image_path: str = None
):
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])
    
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()
    
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    # Convertir subtítulos a ASS con efectos
    temp_ass = "temp_subtitles.ass"
    convert_to_ass_with_effects(subtitlefile, temp_ass, font_name, font_size, text_case, text_color)
    
    # Cadena de filtros compleja para añadir el cuadro con el color recibido
    command = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-t", str(audio_duration),
        "-i", background_video_path,
        "-i", audiofile,
    ]

    # Añadir imagen si existe
    has_image = image_path is not None
    if has_image:
        command.extend(["-i", image_path])

    # Construir filtro complejo
    complex_filter = [
        "[0:v]scale=1920:1080[scaled];",
        f"color=c={text_color}:s=1920x1080,format=yuva420p[color_layer];",
        "[scaled][color_layer]overlay=format=auto[overlaid];",
        "[overlaid]fps=24[withfps];"
    ]

    if has_image:
        complex_filter.extend([
          f"[2:v]loop=loop=-1:start=0:size=1,trim=duration={audio_duration},scale=-1:1080[img];",  # Escalar al alto del video
          "[withfps][img]overlay=W-w:0:format=auto[with_image];",  # Posición derecha sin margen
          f"[with_image]subtitles={temp_ass}[final];"
        ])
    else:
        complex_filter.append(f"[withfps]subtitles={temp_ass}[final];")

    # Unir con ; y sin reemplazar espacios
    complex_filter_str = "; ".join(complex_filter).replace(";;", ";")

    command.extend([
        "-filter_complex", complex_filter_str,
        "-map", "[final]",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "30",
        "-c:a", "aac",
        "-b:a", "299k",
        "-shortest",
        "-y",
        output_path
    ])
    
    try:
      subprocess.run(command, check=True)
        # os.remove(temp_ass)  # Limpiar archivo temporal
    except Exception as e:
        print(f"Error: {e}")
        raise
    
    return output_path
