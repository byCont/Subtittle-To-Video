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

def generateVideoFromAudioAndSubtitles(
    audiofile: str,
    subtitlefile: str,
    font_name: str = "Product Sans",
    font_size: int = 30
):
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])
    
    # Obtener duración del audio
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()

    # Calcular márgenes para los subtítulos
    first_margin_v = 150  # Margen original
    second_margin_v = first_margin_v - 45  # Segundo subtítulo arriba del primero
    second_font = font_size - 10  # Segundo subtítulo más abajo
    # Generar video directamente con ffmpeg
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    command = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-t", str(audio_duration),
        "-i", background_video_path,
        "-i", audiofile,
        "-vf", (
            f"scale=1920:1080,fps=24,"
            f"subtitles={subtitlefile}:force_style="
            f"'FontName={font_name},FontSize={font_size},Alignment=2,MarginV={first_margin_v},"
            "OutlineColour=&H80000000&,BorderStyle=1',"
            f"subtitles={subtitlefile}:force_style="
            f"'FontName={font_name},FontSize={second_font},Alignment=2,MarginV={second_margin_v},"
            "OutlineColour=&H80000000&,BorderStyle=1'"
        ),
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
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el video: {e}")
        raise
    
    return output_path