# convert_to_ass.py, Functions for convert sub to .ass

def convert_to_ass_with_effects(subtitlefile, output_ass, font_name, font_size):
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
                lines = f_in.readlines()
                current_text = []
                start_time = end_time = None
                index = 0
                for line in lines:
                    line = line.strip()
                    if '-->' in line:
                        if current_text:
                            if start_time is None or end_time is None:  # Validación
                                raise ValueError("Timestamp faltante")
                            end_time +=1  # Añadir 2 segundos de margen
                            write_ass_entry(f_out, start_time, end_time, current_text, index, font_size)
                            index += 1
                            current_text = []
                        start_str, end_str = line.split('-->')
                        start_time = convert_time_srt(start_str.strip())
                        end_time = convert_time_srt(end_str.strip())
                    elif line.isdigit() or not line:
                        continue
                    else:
                        current_text.append(line)
                # Bloque final
                if current_text:
                    if start_time is None or end_time is None:  # Validación
                        raise ValueError("Timestamp faltante en último subtítulo")
                    end_time += 1 # Añadir dos segundos de margen
                    write_ass_entry(f_out, start_time, end_time, current_text, index, font_size)
                    index += 1

            elif subtitlefile.endswith('.lrc'):
                entries = []  # Almacenar todos los subtítulos temporalmente
                index = 0
                
                # Primera pasada: recolectar todos los tiempos y textos
                for line in f_in:
                    line = line.strip()
                    if line.startswith('['):
                        end_bracket = line.find(']')
                        if end_bracket != -1:
                            time_str = line[1:end_bracket]
                            text = line[end_bracket+1:]
                            start_time = convert_time_lrc(time_str)
                            entries.append((start_time, text))
                
                # Segunda pasada: calcular end_time dinámico
                for i in range(len(entries)):
                    start_time, text = entries[i]
                    
                    # Calcular end_time según criterio
                    if i < len(entries) - 1:
                        next_start = entries[i + 1][0]
                        time_diff = next_start - start_time
                        end_time = next_start if time_diff < 7 else start_time + 5
                    else:
                        end_time = start_time + 8  # Último subtítulo
                    end_time +=1  # Añadir 2 segundos de margen
                    write_ass_entry(f_out, start_time, end_time, [text], index, font_size)
                    index += 1

    except Exception as e:
        print(f"Error converting subtitles: {e}")
        raise
    
def write_ass_entry(f_out, start, end, text_lines, index, font_size):
    #effect = r"\t(\fscx100\fscy100,\fscx105\fscy105,\fscx110\fscy110)" # 0. ZOOM     
    #effect = r"\t(0,500,\fscx105\fscy105\1a&H20&\3a&H40&)\t(500,1000,\fscx100\fscy100\1a&H00&\3a&H00&)" #1. "RESPIRACIÓN LUMÍNICA"  
    #effect = r"\t(0,1000,\frx5\fry-5\fscx103\blur0.8)\t(1000,2000,\frx-5\fry5\fscx97)\t(2000,3000,\frx0\fry0\fscx100)"#*8. "FLUIDO
    # 11. "AURORA BOREALIS" (Degradado dinámico con brillo polar)
    #effect = r"\t(0,2000,\1c&H6CFFEC&\3c&H002A3C&\blur3\be2\fscx105)\t(2000,4000,\1c&HFFB86C&\3c&H3C1A00&)"

    # 12. "KINETIC TYPOGRAPHY" (Movimiento sincronizado con ritmo)
    #effect = r"\t(0,250,\frz-2\pos($x+10,$y))\t(250,500,\frz2\pos($x-10,$y))\t(500,750,\frz0\pos($x,$y))"

    # 13. "HOLOGRAPHIC GLOW" (Efecto holograma con sombra 3D)
    #effect = r"\t(0,150,\fscx130\fscy70)\t(150,300,\fscx70\fscy130)\t(300,450,\fscx100\fscy100)"

    # 14. "MAGNETIC PULSE" (Atracción/repulsión de caracteres)
    #effect = r"\t(0,300,\fax-0.1\fay0.1)\t(300,600,\fax0.05\fay-0.05)\t(600,900,\fax0\fay0)"

    # 15. "CELESTIAL ORBIT" (Rotación orbital alrededor de un punto)
    #effect = r"\t(0,5000,\frx360\fry-360\fscx90\fscy90\pos(960,540))"

    # 16. "LIQUID MORPH" (Transición fluida entre escalados)
    effect = r"\t(0,800,\fscx115\fscy85\blur1)\t(800,1600,\fscx85\fscy115)\t(1600,2400,\fscx100\fscy100)"

    # 17. "NEON GLITCH" (Distorsión retro con parpadeo RGB)
    #effect = r"\t(0,150,\c&HFF0000&\bord3)\t(150,300,\c&H00FF00&\bord0)\t(300,450,\c&H0000FF&\bord3)\t(450,600,\c&HFFFFFF&\bord1)"

    # 18. "GRAVITY DROP" (Caída con rebote realista)
    #effect = r"\t(0,200,\pos($x,$y-80)\frx-15)\t(200,400,\pos($x,$y+30)\frx10)\t(400,600,\pos($x,$y)\frx0)"

    # 19. "PRISMATIC WAVE" (Onda de color horizontal)
    #effect = r"\t(0,1000,\1c&HFF0000&\clip(0,0,960,1080))\t(0,1000,\1c&H0000FF&\clip(960,0,1920,1080))"

    # 20. "QUANTUM FADE" (Desintegración en partículas)
    #effect = r"\t(0,500,\alpha&H00&\fscx130\blur10)\t(500,1000,\alpha&HFF&\fscx100\blur0)"
    text = r"\N".join(text_lines).replace(r"\N\N", r"\N")
    
    if index % 2 == 0:
        # Posición superior personalizada: centro horizontal + margen vertical
        style_override = r"\an8\pos(960,220)\a6"  # Combinación an8 + pos + centrado horizontal
    else:
        # Centro absoluto con margen dinámico
        style_override = r"\an5\mv50"  # Centro-central con margen inferior
    
    f_out.write(
        f"Dialogue: 0,{format_time_ass(start)},{format_time_ass(end)},Default,"
        f"{{{effect}{style_override}}}{text}\n"
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