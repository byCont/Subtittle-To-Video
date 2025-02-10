# write_entry.py

import re
    
def write_ass_entry(f_out, start, end, text_lines, index, font_size, text_case, text_color):
    effect = r"\t(\fscx115\fscy115,\fscx110\fscy110,\fscx105\fscy105)"
    text = r"\N".join(text_lines).replace(r"\N\N", r"\N")
    
    if text_case == 'upper':
        text = text.upper()
        
    elif text_case == 'capitalize':
         text = text.capitalize()
    
    
    # Determinar colores según text_color
    if text_color == 'dark':
        chorus_c = '&H734000'
        quote_c = '&H749574'        
        asterisk_c = '&H1D1D45'        
        percent_c = '&H347BD0'
        shadow_3c = '&HFFFFFF'
    else:
        chorus_c = '&H8BFFFF'
        quote_c = '&HB0C1EE'
        asterisk_c = '&HEEEEFF'
        percent_c = '&HFFE5C9'
        shadow_3c = '&H000000'

    # Aplicar estilos dinámicos
    text = re.sub( # Estilo para coros
        r'(\([^)]+\))', 
        lambda match: fr'{{\3c{shadow_3c}&\c{chorus_c}&\4c{shadow_3c}&\shad3\bord2}}\N' +  custom_capitalize(match.group(1), text_case),
        text
    )
    text = re.sub( # Estilo para citas
        r'("([^"]+)")', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{quote_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' +  custom_capitalize(match.group(1), text_case),
        text
    )
    text = re.sub( # Estilo para asteriscos
        r'\*([^*]+)\*', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{asterisk_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' + match.group(1).upper() + r'{\\r}',
        text
    )
    text = re.sub(
        r'\%([^%]+)\%', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{percent_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' + custom_capitalize(f'%{match.group(1)}%', text_case) + r'{\\r}',
        text
    )

    style_override = r"\blur15"
    if index % 2 == 0:
        style_override += r"\an8\pos(960,100)\a6"
    else:
        style_override += r"\an8\pos(960,400)\a6"

    f_out.write(
        f"Dialogue: 0,{format_time_ass(start)},{format_time_ass(end)},Default,"
        f"{{{effect}{style_override}}}{text}\n"
    )

def format_time_ass(seconds):
    """Formatea segundos a tiempo ASS (H:MM:SS.XX)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# Función auxiliar para capitalizar ignorando los signos ¿ y ¡
def custom_capitalize(text, text_case):
    """
    Capitaliza el texto dentro de delimitadores ()/""/%% según text_case.
    - Elimina los delimitadores % si están presentes.
    - Respetar signos iniciales como ¡/¿.
    """
    # Validar formato de entrada y extraer delimitador
    delimiter = None
    if text.startswith('(') and text.endswith(')'):
        delimiter = '()'
    elif text.startswith('"') and text.endswith('"'):
        delimiter = '""'
    elif text.startswith('%') and text.endswith('%'):
        delimiter = '%%'
    else:
        return text  # No es un delimitador válido
    
    # Extraer contenido interno (eliminando delimitadores y espacios)
    content = text[1:-1].strip()
    if not content:
        return text  # Contenido vacío
    
    # Aplicar transformación según text_case
    if text_case == 'upper':
        nuevo_contenido = content.upper()
    elif text_case == 'capitalize':
        # Manejar signos iniciales (¡/¿)
        if content[0] in ('¡', '¿'):
            signo = content[0]
            resto = content[1:].lstrip()
            nuevo_contenido = signo + (resto[0].upper() + resto[1:] if resto else "")
        else:
            nuevo_contenido = content[0].upper() + content[1:]
    else:
        nuevo_contenido = content  # Sin cambios
    
    # Reconstruir según el delimitador
    if delimiter == '%%':
        return nuevo_contenido  # Eliminar %%
    elif delimiter == '()':
        return f"({nuevo_contenido})"
    elif delimiter == '""':
        return f'"{nuevo_contenido}"'