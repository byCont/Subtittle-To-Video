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
        chorus_c  = '&H734000'
        quote_c   = '&H749574'
        asterisk_c= '&H1D1D45'
        percent_c = '&H347BD0'
        shadow_3c = '&HFFFFFF'
    else:
        default_c = '&HFFFFFF'
        chorus_c  = '&H8BFFFF'
        quote_c   = '&HB0C1EE'
        asterisk_c= '&HEEEEFF'
        percent_c = '&HFFE5C9'
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
        lambda match: fr'{{\fnDancing Script Bold\\fs{font_size + 20}\\3c{shadow_3c}&\\c{chorus_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N'
                       + custom_capitalize(match.group(1), 'capitalize')
                       + r'{\\r}' + override_tags,
        text
)
    text = re.sub(  # Estilo para citas (entre comillas)
        r'("([^"]+)")', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{quote_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' 
                      + custom_capitalize(match.group(1), text_case)
                      + r'{\\r}' + override_tags,
        text
    )
    text = re.sub(  # Estilo para asteriscos
        r'\*([^*]+)\*', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{asterisk_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' 
                      + match.group(1).upper()
                      + r'{\\r}' + override_tags,
        text
    )
    text = re.sub(  # Estilo para porcentajes
        r'\%([^%]+)\%', 
        lambda match: fr'{{\\3c{shadow_3c}&\\c{percent_c}&\\4c{shadow_3c}&\\shad3\\bord2}}\N' 
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
    """
    Capitaliza el texto dentro de delimitadores ()/""/%% según text_case.
    - Elimina los delimitadores % si están presentes.
    - Respeta signos iniciales como ¡/¿.
    """
    delimiter = None
    if text.startswith('(') and text.endswith(')'):
        delimiter = '()'
    elif text.startswith('"') and text.endswith('"'):
        delimiter = '""'
    elif text.startswith('%') and text.endswith('%'):
        delimiter = '%%'
    else:
        return text  # No es un delimitador válido
    
    content = text[1:-1].strip()
    if not content:
        return text  # Contenido vacío
    
    if text_case == 'upper':
        nuevo_contenido = content.upper()
    elif text_case == 'capitalize':
        if content[0] in ('¡', '¿'):
            signo = content[0]
            resto = content[1:].lstrip()
            nuevo_contenido = signo + (resto[0].upper() + resto[1:] if resto else "")
        else:
            nuevo_contenido = content[0].upper() + content[1:].lower()
    else:
        nuevo_contenido = content  # Sin cambios
    
    if delimiter == '%%':
        return nuevo_contenido  # Eliminar %%
    elif delimiter == '()':
        return f"({nuevo_contenido})"
    elif delimiter == '""':
        return f'"{nuevo_contenido}"'
