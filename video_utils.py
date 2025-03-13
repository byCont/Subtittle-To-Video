# video_utils.py, Video editor backend 

def generateVideoFromAudioAndSubtitles(
    audiofile: str,
    subtitlefile: str,
    font_name: str = "Product Sans Bold",
    font_size: int = 110,
    text_case: str = 'capitalize',
    text_color: str = 'light',
    bg_color: str = "#00000000",
    image_path: str = None
):
    import os
    import time
    import subprocess
    from moviepy.editor import AudioFileClip
    from config import config
    from subt_process.convert_to_ass import convert_to_ass_with_effects

    # 1. Seleccionar video de fondo
    background_videos_folder = os.path.join(os.path.dirname(__file__), 'background_videos')
    background_video_path = os.path.join(background_videos_folder, os.listdir(background_videos_folder)[0])

    # 2. Seleccionar logo (input 2)
    # logo_folder = os.path.join(os.path.dirname(__file__), 'logo')
    # logo_image_path = os.path.join(logo_folder, os.listdir(logo_folder)[0])
    
    # 3. Obtener duración del audio
    audio = AudioFileClip(audiofile)
    audio_duration = audio.duration
    audio.close()
    
    output_path = config['video_savepath'] + "generated_" + str(int(time.time())) + ".mp4"
    
    # 4. Convertir subtítulos a ASS con efectos
    temp_ass = "temp_subtitles.ass"
    convert_to_ass_with_effects(subtitlefile, temp_ass, font_name, font_size, text_case, text_color)
    
    ## Construir comando base
    command = [
        "ffmpeg",
        "-stream_loop", "-1",          # Loop para el video de fondo
        "-t", str(audio_duration),
        "-i", background_video_path,   # Input 0: Video de fondo
        "-i", audiofile,               # Input 1: Audio
    ]

    # Si existe una imagen adicional, se añade como Input 2
    has_image = image_path is not None
    if has_image:
        command.extend(["-i", image_path])  # Input 2: Imagen adicional

    # Agregar video glitch como capa adicional
    glitch_video_path = os.path.join(background_videos_folder, "glitch.mp4")
    command.extend(["-stream_loop", "-1", "-i", glitch_video_path])  # Input 3 si has_image, Input 2 si no
    glitch_idx = 2 if not has_image else 3  # Corregir el índice del glitch

    # Construir filtro complejo dinámicamente
    complex_filter = []

    # Escalar el video de fondo
    complex_filter.append("[0:v]scale=1920:1080[scaled];")

    # Capa de color (si se requiere)
    has_color = bg_color != "#00000000"
    if has_color:
        complex_filter.extend([
            f"color=c={bg_color}:s=1920x1080,format=yuva420p[color_layer];",
            "[scaled][color_layer]overlay=format=auto[overlaid];",
            "[overlaid]fps=24[base];"
        ])
    else:
        complex_filter.append("[scaled]fps=24[base];")

    # Capa de imagen (opcional)
    if has_image:
        # Usamos Input 2 para la imagen adicional
        complex_filter.extend([
            f"[2:v]loop=loop=-1:start=0:size=1,trim=duration={audio_duration},scale=-1:1080[img];",
            "[base][img]overlay=W-w:0:format=auto[base];"
        ])

    # Superponer video glitch con opacidad del 70%
    complex_filter.extend([
        f"[{glitch_idx}:v]scale=1920:1080,format=yuva420p,colorchannelmixer=aa=0.3[glitch];",
        "[base][glitch]overlay=0:0:format=auto[base];"
    ])

    # Añadir subtítulos
    complex_filter.append(f"[base]subtitles={temp_ass}[final];")

    # Unir filtros en una sola cadena
    complex_filter_str = "".join(complex_filter)

    # Completar comando
    command.extend([
        "-filter_complex", complex_filter_str,
        "-map", "[final]",
        "-map", "1:a:0",
        "-c:v", "libx265",
        "-preset", "medium",
        "-crf", "29",
        "-c:a", "aac",
        "-b:a", "299k",
        "-shortest",
        "-y",
        output_path
    ])
    
    try:
        subprocess.run(command, check=True)
        # os.remove(temp_ass)  # Limpiar archivo temporal si lo deseas
    except Exception as e:
        print(f"Error: {e}")
        raise
    
    return output_path
