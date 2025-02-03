# convert_to_ass.py, Functions for convert sub to .ass

import re
import tkinter as tk
from tkinter import messagebox


def convert_to_ass_with_effects(subtitlefile, output_ass, font_name, font_size, text_case, text_color):
    try:
        with open(subtitlefile, 'r', encoding='utf-8') as f_in, \
             open(output_ass, 'w', encoding='utf-8') as f_out:

            # Cabecera ASS con parámetros dinámicos
            f_out.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,1,1,4,2,0,0,50,0,1
Style: Secondary,{font_name},{font_size},&H00000000,&HFFFFFFFF,&H00FFFFFF,&HFFFFFFFF,0,0,1,5,4,2,0,0,50,0,1

[Events]
Format: Layer, Start, End, Style, Text
TextCase: {text_case}
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
                            write_ass_entry(f_out, start_time, end_time, current_text, index, font_size, text_case, text_color)
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
                    write_ass_entry(f_out, start_time, end_time, current_text, index, font_size, text_case, text_color)
                    index += 1

            elif subtitlefile.endswith('.lrc'):
              entries = []  # Almacenar todos los subtítulos temporalmente
              index = 0

              # Primera pasada: recolectar subtítulos válidos
              for line in f_in:
                  line = line.strip()
                  if line.startswith('['):
                      end_bracket = line.find(']')
                      if end_bracket != -1:
                          # Extraer tiempo y texto
                          time_str = line[1:end_bracket]
                          text = line[end_bracket+1:].lstrip()  # Eliminar espacios solo al inicio del texto

                          # Validar si el tiempo tiene formato correcto (ej: mm:ss.xx)
                          if ":" in time_str and "." in time_str:  # Filtra solo tiempos válidos
                              try:
                                  start_time = convert_time_lrc(time_str)
                                  # Aplicar delay de 1 segundo
                                  start_time -= 1
                                  entries.append((start_time, text))
                              except:
                                  print(f"Formato de tiempo inválido en línea: {line}")  # Debug opcional

              # Segunda pasada: calcular end_time dinámico
              for i in range(len(entries)):
                  start_time, text = entries[i]

                  if i < len(entries) - 1:
                      next_start = entries[i + 1][0]
                      time_diff = next_start - start_time
                      end_time = next_start if time_diff < 7 else start_time + 5
                  else:
                      end_time = start_time + 8

                  end_time +=1
                  write_ass_entry(f_out, start_time, end_time, [text], index, font_size, text_case, text_color)
                  index += 1

    except Exception as e:
        print(f"Error converting subtitles: {e}")
        raise

def convert_color(color):
    # Asegurarse de que el color sea una cadena
    if not isinstance(color, str):
        raise ValueError("El color debe ser una cadena en formato #RRGGBBAA")
    
    # Eliminar el carácter '#' si está presente
    if color.startswith('#'):
        color = color[1:]
    # Convertir de #RRGGBBAA a &HBBGGRR&
    bb = color[4:6]
    gg = color[2:4]
    rr = color[0:2]
    return f"{bb}{gg}{rr}"

# Función auxiliar para capitalizar ignorando los signos ¿ y ¡
def custom_capitalize(text_with_parens):
    """
    Recibe una cadena que comienza con '(' y termina con ')'.
    Si el contenido (excluyendo los paréntesis) empieza por '¡' o '¿',
    se mantiene ese signo y se capitaliza el resto, es decir, se
    convierte la primera letra posterior a ese signo a mayúscula.
    """
    # Extraer el contenido interno
    content = text_with_parens[1:-1]
    if not content:
        return text_with_parens  # Si está vacío, se devuelve tal cual.
    
    # Si el primer carácter es uno de los signos especiales
    if content[0] in ('¡', '¿'):
        signo = content[0]
        # Capitalizar el resto del contenido (si existe algo tras el signo)
        if len(content) > 1:
            nuevo_contenido = signo + content[1:].capitalize()
        else:
            nuevo_contenido = content
    else:
        nuevo_contenido = content.capitalize()
    
    return "(" + nuevo_contenido + ")"
    
def write_ass_entry(f_out, start, end, text_lines, index, font_size,  text_case, text_color):
    effect = r"\t(\fscx115\fscy115,\fscx110\fscy110,\fscx100\fscy100)" # 0. ZOOM
    #effect = r"\t(0,1000,\frx5\fry-5\fscx103\blur0.8)\t(1000,2000,\frx-5\fry5\fscx97)\t(2000,3000,\frx0\fry0\fscx100)"#*8. "FLUIDO"
    text = r"\N".join(text_lines).replace(r"\N\N", r"\N")
    if text_case == 'upper':
        text = text.upper()
    elif text_case == 'lower':
        text = text.capitalize()

   
    
    #Texto entre parentesis, Chorus
    text = re.sub(
      r'(\([^)]+\))',
      lambda match: (r'{\3c&HFFFFFF&\c&H00000&\4c&HFFFFFF&\shad3\bord2}\N'
                      + custom_capitalize(match.group(1))
                      + r'{\r}'),
      text
    )
    # Expresiones no cantadas, a resaltar
    text = re.sub(
      r'("([^"]+)")',
      r'{\\3c&HFFFFFF&\\c&HB1B7F5&\\4c&H00000&\\shad3\\bord2}\\N\1{\\r}',
      text
    )
    # entre * Titles
    text = re.sub(
        r'\*([^*]+)\*',
        lambda match: r'{\\3c&FFFFFF&\c&C0C0C0&\4c&H00000&\shad3\bord2}\N' + match.group(1).upper() + r'{\\r}',
        text
    )

    # enfasis %
    text = re.sub(
        r'\%([^%]+)\%',
        lambda match: r'{\\3c&H736556&\c&HB1EDF5&\4c&H00000&\shad3\bord2}\N' + match.group(1).capitalize() + r'{\\r}',
        text
    )

    if index % 2 == 0:
        # Posición superior personalizada: centro horizontal + margen vertical
        style_override = r"\an8\pos(960,200)\a6"  # Combinación an8 + pos + centrado horizontal
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
