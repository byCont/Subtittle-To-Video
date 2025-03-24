from subt_process.write_entry import write_ass_entry

def convert_to_ass_with_effects(subtitlefile, output_ass, font_name, font_size, text_case, text_color):
    try:
        with open(subtitlefile, 'r', encoding='utf-8') as f_in, \
             open(output_ass, 'w', encoding='utf-8') as f_out:

            # Escribir la cabecera ASS solo con "Default"
            f_out.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,1,1,0,2,0,0,50,0,1

[Events]
Format: Layer, Start, End, Style, Text
TextCase: {text_case}
""")

            # Lista para almacenar todos los subtítulos procesados
            all_subtitles = []
            title_artist = None

            # Procesamiento de .srt
            if subtitlefile.endswith('.srt'):
                content = f_in.read().strip()
                blocks = content.split('\n\n')
                for i, block in enumerate(blocks):
                    lines = block.splitlines()
                    if len(lines) < 3:
                        continue
                    timestamp_line = lines[1]
                    try:
                        start_str, end_str = timestamp_line.split('-->')
                    except ValueError:
                        raise ValueError(f"Error en el formato de tiempo en el bloque:\n{block}")
                    start_time = convert_time_srt(start_str.strip())
                    end_time = convert_time_srt(end_str.strip()) + 2
                    text_lines = lines[2:]
                    all_subtitles.append({
                        'start': start_time,
                        'end': end_time,
                        'text_lines': text_lines
                    })
                    if i == 0:
                        title_artist = {'text_lines': text_lines}

            # Procesamiento de .lrc
            elif subtitlefile.endswith('.lrc'):
                entries = []
                current_entry = None
                for line in f_in:
                    line = line.rstrip("\n")
                    if line.startswith('['):
                        if current_entry:
                            entries.append(current_entry)
                        end_bracket = line.find(']')
                        if end_bracket != -1:
                            time_str = line[1:end_bracket]
                            raw_text = line[end_bracket+1:].lstrip()
                            text = raw_text.replace("\\n", "\n")
                            try:
                                start_time = convert_time_lrc(time_str) - 1
                                text_lines = [line.strip() for line in text.split('\n') if line.strip()]
                                current_entry = {
                                    'start': start_time,
                                    'text_lines': text_lines
                                }
                            except Exception as e:
                                print(f"Error en tiempo: {line} ({e})")
                                current_entry = None
                    else:
                        if current_entry is not None and line.strip():
                            current_entry['text_lines'].append(line.strip())
                if current_entry:
                    entries.append(current_entry)
                for i, entry in enumerate(entries):
                    start_time = entry['start']
                    if i < len(entries) - 1:
                        next_start = entries[i + 1]['start']
                        time_diff = next_start - start_time
                        end_time = next_start if time_diff < 8 else start_time + 7
                    else:
                        end_time = start_time + 8
                    all_subtitles.append({
                        'start': start_time + 0.5,
                        'end': end_time + 1.5,
                        'text_lines': entry['text_lines']
                    })
                    if i == 0:
                        title_artist = {'text_lines': entry['text_lines']}

            all_subtitles.sort(key=lambda x: x['start'])

            # Identificar gaps (espacios en blanco)
            gaps = []
            video_start = 0
            for i in range(len(all_subtitles)):
                current_sub = all_subtitles[i]
                if i == 0 and current_sub['start'] > 0:
                    gaps.append({
                        'start': video_start,
                        'end': max(0, current_sub['start'] - 2)
                    })
                if i < len(all_subtitles) - 1:
                    next_sub = all_subtitles[i + 1]
                    if next_sub['start'] - current_sub['end'] > 2:
                        gaps.append({
                            'start': current_sub['end'],
                            'end': max(current_sub['end'], next_sub['start'] - 2)
                        })

            # Escribir subtítulos normales con "Default" y title_mode=False
            for i, subtitle in enumerate(all_subtitles):
                write_ass_entry(
                    f_out,
                    subtitle['start'],
                    subtitle['end'],
                    subtitle['text_lines'],
                    i,
                    font_size,
                    text_case,
                    text_color,
                    font_name,
                    style="Default",
                    title_mode=False  # Por defecto, se omite ya que es False
                )

            # Escribir título/artista en huecos con "Default" y title_mode=True (centrado)
            if title_artist and gaps:
                for i, gap in enumerate(gaps):
                    if gap['end'] - gap['start'] >= 1:
                        write_ass_entry(
                            f_out,
                            gap['start'],
                            gap['end'],
                            title_artist['text_lines'],
                            10000 + i,
                            font_size,
                            text_case,
                            text_color,
                            font_name,
                            style="Default",
                            title_mode=True  # Centrado para título/artista
                        )

    except Exception as e:
        print(f"Error converting subtitles: {e}")
        raise

def convert_time_srt(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.replace(',', '.').split('.')
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def convert_time_lrc(time_str):
    m, s = time_str.split(':')
    s = s.replace('.', '')
    return int(m)*60 + int(s)/100