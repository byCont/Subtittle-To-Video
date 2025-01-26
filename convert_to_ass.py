# convert_to_ass.py, Functions for convert sub to .ass

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