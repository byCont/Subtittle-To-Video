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
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])
    
    # Obtener duración del audio
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()

    # Generar video directamente con ffmpeg
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    command = [
        "ffmpeg",
        "-stream_loop", "-1",  # Loop infinito para fondos cortos
        "-t", str(audio_duration),  # Cortar a la duración del audio
        "-i", background_video_path,
        "-i", audiofile,
        "-vf", (
            f"scale=1920:1080,fps=24,subtitles={subtitlefile}:force_style="
            "'FontName=Product Sans,FontSize=40,Alignment=2,MarginV=140,"
            "OutlineColour=&H80FFFFFF&,BorderStyle=1'"
        ),
        "-c:v", "libx265",
        "-preset", "medium",
        "-crf", "30",
        "-c:a", "aac",
        "-b:a", "299k",
        "-map", "0:v:0",  # Video del fondo
        "-map", "1:a:0",  # Audio del input
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