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
              # Leer todo el contenido y separar por bloques (cada bloque corresponde a un subtítulo)
              content = f_in.read().strip()
              blocks = content.split('\n\n')
              index = 0
              for block in blocks:
                  # Separar las líneas de cada bloque sin eliminar los saltos de línea internos
                  lines = block.splitlines()
                  if len(lines) < 3:
                      continue  # Se espera al menos: índice, timestamp y una línea de texto
                  # La primera línea es el número del subtítulo (se ignora)
                  # La segunda línea contiene el timestamp
                  timestamp_line = lines[1]
                  try:
                      start_str, end_str = timestamp_line.split('-->')
                  except ValueError:
                      raise ValueError(f"Error en el formato de tiempo en el bloque:\n{block}")
                  start_time = convert_time_srt(start_str.strip())
                  end_time = convert_time_srt(end_str.strip())
                  # El resto de las líneas son el texto del subtítulo (se conserva cada línea)
                  text_lines = lines[2:]
                  # Opcional: añadir un margen (por ejemplo, 1 segundo) al tiempo de finalización
                  end_time += 1
                  write_ass_entry(f_out, start_time, end_time, text_lines, index, font_size, text_case, text_color)
                  index += 1

            elif subtitlefile.endswith('.lrc'):
              entries = []
              index = 0
              current_entry = None
              
              for line in f_in:
                  line = line.rstrip("\n")  # Quitar salto de línea final
                  
                  if line.startswith('['):
                      # 1. Guardar entrada anterior si existe
                      if current_entry:
                          entries.append(current_entry)
                      
                      end_bracket = line.find(']')
                      if end_bracket != -1:
                          time_str = line[1:end_bracket]
                          # 2. Extraer texto y procesar escapes
                          raw_text = line[end_bracket+1:].lstrip()
                          text = raw_text.replace("\\n", "\n")  # Convertir \\n a saltos reales
                          
                          try:
                              start_time = convert_time_lrc(time_str) - 1  # Aplicar delay
                              # 3. Dividir en líneas usando saltos reales
                              text_lines = [line.strip() for line in text.split('\n') if line.strip()]
                              current_entry = {
                                  'start': start_time,
                                  'text_lines': text_lines  # Lista de líneas procesadas
                              }
                          except Exception as e:
                              print(f"Error en tiempo: {line} ({e})")
                              current_entry = None
                  else:
                      # 4. Líneas subsiguientes sin timestamp
                      if current_entry is not None and line.strip():
                          # Agregar como línea adicional preservando espacios
                          current_entry['text_lines'].append(line.strip())
              
              # 5. Agregar última entrada después del loop
              if current_entry:
                  entries.append(current_entry)
              
              # Procesar todas las entradas para tiempos finales
              for i, entry in enumerate(entries):
                  start_time = entry['start']
                  
                  # 6. Calcular end_time dinámicamente
                  if i < len(entries) - 1:
                      next_start = entries[i + 1]['start']
                      time_diff = next_start - start_time
                      end_time = next_start if time_diff < 7 else start_time + 5
                  else:
                      end_time = start_time + 8
                  
                  # 7. Escribir entrada .ASS con todas las líneas
                  write_ass_entry(
                      f_out, 
                      start_time + 1, 
                      end_time + 2,  # Offset adicional
                      entry['text_lines'],  # Lista de líneas originales
                      index,
                      font_size,
                      text_case,
                      text_color
                  )
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
