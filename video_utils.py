# video_utils.py, Video editor backend

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


def convert_to_ass_with_effects(subtitlefile, output_ass, font_name, font_size):
    """Convierte cualquier subtítulo a formato ASS con efecto de zoom incorporado."""
    try:
        with open(subtitlefile, 'r', encoding='utf-8') as f_in, \
             open(output_ass, 'w', encoding='utf-8') as f_out:

            # Cabecera ASS con parámetros dinámicos
            f_out.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, Bold, Italic, Outline
Style: Default,{font_name},{font_size},&H00FFFFFF,0,0,1

[Events]
Format: Layer, Start, End, Style, Text
""")

            if subtitlefile.endswith('.srt'):
                # Procesar SRT
                lines = f_in.readlines()
                current_text = []
                start_time = end_time = None
                for line in lines:
                    line = line.strip()
                    if '-->' in line:
                        if current_text:
                            # Escribir entrada anterior
                            write_ass_entry(f_out, start_time, end_time, current_text)
                            current_text = []
                        start_str, end_str = line.split('-->')
                        start_time = convert_time_srt(start_str.strip())
                        end_time = convert_time_srt(end_str.strip())
                    elif line.isdigit() or not line:
                        continue
                    else:
                        current_text.append(line)
                if current_text:
                    write_ass_entry(f_out, start_time, end_time, current_text)

            elif subtitlefile.endswith('.lrc'):
                # Procesar LRC
                for line in f_in:
                    line = line.strip()
                    if line.startswith('['):
                        end_bracket = line.find(']')
                        if end_bracket != -1:
                            time_str = line[1:end_bracket]
                            text = line[end_bracket+1:]
                            start_time = convert_time_lrc(time_str)
                            # Asumir duración fija de 3 segundos para LRC
                            end_time = start_time + 3.0
                            write_ass_entry(f_out, start_time, end_time, [text])

    except Exception as e:
        print(f"Error converting subtitles: {e}")
        raise

def write_ass_entry(f_out, start, end, text_lines):
    """Escribe una línea de subtítulo ASS con efecto de zoom aplicado siempre."""
    effect = r"\t(\fscx100\fscy100,\fscx120\fscy120)"  # Efecto siempre activo
    text = r"\N".join(text_lines).replace(r"\N\N", r"\N")  # Unir líneas
    
    f_out.write(
        f"Dialogue: 0,{format_time_ass(start)},{format_time_ass(end)},Default,"
        f"{{{effect}}}{text}\n"
    )

def convert_time_srt(time_str):
    """Convierte tiempo SRT (00:00:00,000) a segundos."""
    h, m, s = time_str.split(':')
    s, ms = s.replace(',', '.').split('.')
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def convert_time_lrc(time_str):
    """Convierte tiempo LRC ([mm:ss.xx]) a segundos."""
    m, s = time_str.split(':')
    s = s.replace('.', '')
    return int(m)*60 + int(s)/100

def format_time_ass(seconds):
    """Formatea segundos a tiempo ASS (H:MM:SS.XX)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

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
        os.remove(temp_ass)  # Limpiar archivo temporal
    except Exception as e:
        print(f"Error: {e}")
        raise
    
    return output_path
