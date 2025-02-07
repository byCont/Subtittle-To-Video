# convert_to_ass.py, Functions for convert sub to .ass
from write_entry import write_ass_entry

def convert_to_ass_with_effects(subtitlefile, output_ass, font_name, font_size, text_case, text_color):
    try:
        with open(subtitlefile, 'r', encoding='utf-8') as f_in, \
             open(output_ass, 'w', encoding='utf-8') as f_out:

            # Determinar estilos según text_color
            if text_color == 'light':
                default_primary = "&H00FFFFFF"
                default_secondary_color = "&H000000FF"
                default_outline = "&H00000000"
                default_back = "&H00000000"
                secondary_primary = "&H00000000"
                secondary_secondary = "&HFFFFFFFF"
                secondary_outline = "&H00FFFFFF"
                secondary_back = "&HFFFFFFFF"
            else:  # dark
                default_primary = "&H00000000"
                default_secondary_color = "&H00FFFFFF"
                default_outline = "&H00FFFFFF"
                default_back = "&H00FFFFFF"
                secondary_primary = "&H00FFFFFF"
                secondary_secondary = "&HFF000000"
                secondary_outline = "&H00000000"
                secondary_back = "&H00000000"

            # Cabecera ASS con parámetros dinámicos
            f_out.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,{font_name},{font_size},{default_primary},{default_secondary_color},{default_outline},{default_back},0,0,1,1,4,2,0,0,50,0,1
Style: Secondary,{font_name},{font_size},{secondary_primary},{secondary_secondary},{secondary_outline},{secondary_back},0,0,1,5,4,2,0,0,50,0,1

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
