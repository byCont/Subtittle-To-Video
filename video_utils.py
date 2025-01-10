# video_utils.py
# Video editor backend

from moviepy.editor import VideoFileClip, concatenate_videoclips
from config import config
import time
import subprocess

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

# Add Subtitles
def addSubtitles(videofile: str, subtitlefile: str):
    videofile_name = videofile.replace(config['video_savepath'], "")
    output_path = config['video_savepath'] + "subtitled_" + str(int(time.time())) + videofile_name

    command = [
        "ffmpeg",
        "-i", videofile,
        "-vf", (
            f"subtitles={subtitlefile}:force_style="
            "'FontName=Product Sans,FontSize=40,Alignment=2,MarginV=140,"
            "OutlineColour=&H80FFFFFF&,BorderStyle=1'"
        ),
        "-c:a", "aac",
        "-b:a", "299k",
        output_path
    ]

    subprocess.run(command, check=True)
    return output_path
