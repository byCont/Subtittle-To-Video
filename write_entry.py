# write_entry.py

import re

def write_ass_entry(f_out, start, end, text_lines, index, font_size, text_case, text_color):
    
    # Definir el efecto y override general que incluya blur, posición y colores por defecto
    effect = r"\t(\fscx115\fscy115,\fscx110\fscy110,\fscx105\fscy105)"
   
    # Procesar y limpiar las líneas del texto
    clean_lines = [line for line in text_lines if line]
    # Unir las líneas usando el separador ASS de salto de línea
    text = r"\N".join(clean_lines)
    # Asegurarse de que no queden dobles secuencias de salto
    text = r"\N".join(clean_lines) if len(clean_lines) > 1 else clean_lines[0] if clean_lines else ""

    # Mantener espacios en líneas vacías intencionales
    text = text.replace(r"\N\N", r"\N")  # Prevenir dobles saltos
    # Aplicar capitalización según corresponda
    
    if text_case == 'upper':
        text = text.upper()
    elif text_case == 'capitalize':
        # Capitalizar cada línea por separado, preservando el literal "\N"
        text = r"\N".join([
            line[:1].upper() + line[1:].lower() if line else ''
            for line in text.split(r"\N")
        ])
    
    # Determinar colores según el valor de text_color
    if text_color == 'dark':
        default_c = '&H000000'
        chorus_c  = '&H5B5B5B'
        quote_c   = '&H909090'
        title_c = '&H303030'
        highlight_c = '&H454545'
        shadow_3c = '&HFFFFFF'
    # Blue
    elif text_color == 'blue':
        default_c = '&H503E2C'
        chorus_c  = '&HA67428'
        quote_c   = '&HC79954'
        title_c = '&H604315'
        highlight_c = '&H76521A'
        shadow_3c = '&HFFFFFF'

    elif text_color == 'coffee':
        default_c   = '&H2C3E50'   
        chorus_c    = '&H2874A6'   
        quote_c     = '&H5499C7'
        title_c     = '&H154360'
        highlight_c = '&H1A5276'
        shadow_3c   = '&HFFFFFF'

    elif text_color == 'green':
        default_c   = '&H2C503E'
        chorus_c    = '&H28A674'
        quote_c     = '&H54C799'
        title_c     = '&H156043'
        highlight_c = '&H1A7652'
        shadow_3c   = '&HFFFFFF'

    elif text_color == 'red':
        default_c   = '&H161E64'
        chorus_c    = '&H3B417C'
        quote_c     = '&H182C8A'
        title_c     = '&H102240'
        highlight_c = '&1E1E9A'
        shadow_3c   = '&HFFFFFF'
        
    else: # light
        default_c = '&HFFFFFF'
        chorus_c  = '&H8BFFFF'
        quote_c   = '&HD8FDFF'
        title_c = '&HF3F3F3'
        highlight_c = '&DCD0BD'
        shadow_3c = '&H000000'

    # Definir el override de estilo por defecto (con blur, posición y demás)
    style_override = r"\blur15"
    if index % 2 == 0:
        style_override += r"\an8\pos(960,100)\a6"
    else:
        style_override += r"\an8\pos(960,400)\a6"
    
    # Combinar en un solo bloque el efecto y override general
    override_tags = fr'{{{effect}{style_override}\\c{default_c}\\3c{shadow_3c}\\4c{shadow_3c}\\shad3\\bord2}}'
    
    # --- Aplicar estilos especiales en línea y luego reinsertar el override por defecto ---
    # Nota: se añade al final de cada segmento estilizado: {\\r} + override_tags,
    # para que el resto del texto siga usando el override que incluye blur.
    
    text = re.sub(  # Estilo para coros (entre paréntesis)
        r'(\([^)]+\))', 
        lambda match: fr'{{\fnDancing Script Bold\\fs{font_size + 20}\\3c{shadow_3c}&\\c{chorus_c}&\\4c{shadow_3c}&\\shad3\\bord2}}'
                       + custom_capitalize(match.group(1), 'capitalize')
                       + r'{\\r}' + override_tags,
        text
    )
    text = re.sub(  # Estilo para citas (entre comillas)
        r'("([^"]+)")', 
        lambda match: fr'{{\fnDancing Script Bold\\fs{font_size + 20}\\3c{shadow_3c}&\\c{quote_c}&\\4c{shadow_3c}&\\shad3\\bord2}}' 
                      + custom_capitalize(match.group(1), 'capitalize')
                      + r'{\\r}' + override_tags,
        text
    )
    text = re.sub(  # Estilo para asteriscos Titles
        r'\*([^*]+)\*', 
        lambda match: r'\N' + fr'{{\fs{font_size + 80}\\3c{shadow_3c}&\\c{title_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N'
                      + match.group(1).upper()
                      + r'{\\r}' + override_tags,
        text
    )
    text = re.sub(  # Estilo para porcentajes
        r'\%([^%]+)\%', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{ highlight_c}&\\4c{shadow_3c}&\\shad3\\bord2}}' 
                      + custom_capitalize(f'%{match.group(1)}%', text_case)
                      + r'{\\r}' + override_tags,
        text
    )

    # Escribir la línea final combinando el bloque de override general y el texto procesado
    f_out.write(
        f"Dialogue: 0,{format_time_ass(start)},{format_time_ass(end)},Default,"
        f"{override_tags}{text}\n"
    )

def format_time_ass(seconds):
    """Formatea segundos a tiempo ASS (H:MM:SS.XX)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# Función auxiliar para capitalizar ignorando signos como ¿ y ¡
def custom_capitalize(text, text_case):
    delimiter = None
    if text.startswith('(') and text.endswith(')'):
        delimiter = '()'
    elif text.startswith('"') and text.endswith('"'):
        delimiter = '""'
    elif text.startswith('%') and text.endswith('%'):
        delimiter = '%%'
    else:
        return text  # No es un delimitador válido

    content = text[1:-1]
    
    # Proteger la secuencia \N usando un marcador
    marker = '__NL__'
    protected_content = content.replace(r'\N', marker)

    if text_case == 'upper':
        nuevo_contenido = protected_content.upper()
    elif text_case == 'capitalize':
        if protected_content and protected_content[0] in ('¡', '¿'):
            signo = protected_content[0]
            resto = protected_content[1:]
            nuevo_contenido = signo + (resto[0].upper() + resto[1:].lower() if resto else "")
        else:
            nuevo_contenido = protected_content[0].upper() + protected_content[1:].lower()
    else:
        nuevo_contenido = protected_content  # Sin cambios

    # Restaurar el marcador; como lower() puede haberlo convertido a minúsculas,
    # reemplazamos ambas versiones
    nuevo_contenido = nuevo_contenido.replace(marker, r'\N').replace(marker.lower(), r'\N')

    if delimiter == '%%':
        return nuevo_contenido  # Para porcentajes, se eliminan los delimitadores
    elif delimiter == '()':
        return f"({nuevo_contenido})"
    elif delimiter == '""':
        return f'"{nuevo_contenido}"'