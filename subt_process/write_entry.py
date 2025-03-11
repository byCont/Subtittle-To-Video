import re

def format_time_ass(seconds):
    """Convierte el tiempo en segundos a formato ASS (h:mm:ss.cs)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def custom_capitalize(text, text_case):
    """Aplica mayúsculas a los subtítulos según el formato requerido"""
    delimiter = None
    if text.startswith('(') and text.endswith(')'):
        delimiter = '()'
    elif text.startswith('"') and text.endswith('"'):
        delimiter = '""'
    elif text.startswith('%') and text.endswith('%'):
        delimiter = '%%'
    else:
        return text

    content = text[1:-1]
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
        nuevo_contenido = protected_content

    nuevo_contenido = nuevo_contenido.replace(marker, r'\N').replace(marker.lower(), r'\N')

    if delimiter == '%%':
        return nuevo_contenido
    elif delimiter == '()':
        return f"({nuevo_contenido})"
    elif delimiter == '""':
        return f'"{nuevo_contenido}"'

def write_ass_entry(f_out, start, end, text_lines, index, font_size, text_case, text_color, style="Default", title_mode=False):
    """
    Genera una línea de subtítulo en formato ASS con efecto de animación tipo 'cube'.
    El texto entra desde abajo hasta quedar centrado y, en los últimos 2000 ms,
    gira (simulando el giro de un cubo) y se desplaza hacia la izquierda y arriba sin desvanecerse.
    """
    if style == "Default":
        # Efectos de animación
        effect = r"\t(\fscx120\fscy120,\fscx100\fscy100)"  # Zoom dinámico
        style_override = r"\blur5\fade(200,0)"  # Fade-in con desenfoque
        
        # Movimiento y tracking dinámico
        # move_effect = r"\move(960,1200,960,600,0,1500)"  # Entrada desde abajo
        # tracking_effect = r"\t(\fsp10,\fsp0)"  # Ajuste de tracking de letras

        # Posición de los subtítulos (arriba o abajo)
        if title_mode:
            style_override += r"\an8\pos(960,100)"  # Posición superior para títulos
        else:
            if index % 2 == 0:
                style_override += r"\an8\pos(960,100)"  # Arriba
            else:
                style_override += r"\an8\pos(960,400)"  # Abajo

        # Configuración de colores
        color_map = {
            'dark':   ('&H000000', '&H5B5B5B', '&H909090', '&H303030', '&H454545', '&HFFFFFF'),
            'blue':   ('&H503E2C', '&HA67428', '&HC79954', '&H604315', '&H76521A', '&HFFFFFF'),
            'coffee': ('&H2C3E50', '&H2874A6', '&H5499C7', '&H154360', '&H1A5276', '&HFFFFFF'),
            'green':  ('&H2C503E', '&H28A674', '&H54C799', '&H156043', '&H1A7652', '&HFFFFFF'),
            'red':    ('&H161E64', '&H3B417C', '&H182C8A', '&H102240', '&H1E1E9A', '&HFFFFFF'),
            'light':  ('&HFFFFFF', '&H8BFFFF', '&HD8FDFF', '&HF3F3F3', '&HDCD0BD', '&H000000')
        }
        default_c, chorus_c, quote_c, title_c, highlight_c, shadow_3c = color_map.get(text_color, color_map['light'])

        # Duración total en ms y cálculo para la animación de "cube".
        duration_ms = int((end - start) * 1000)
        exit_start = max(0, duration_ms - 2000)  # La transformación se realiza durante los últimos 2000 ms

        # Animación de salida tipo 'cube':
        # Se simula una rotación lateral (por ejemplo, -90°) mientras el texto se desplaza a la izquierda y arriba.
        # Además, se reduce ligeramente el escalado (al 90%) para dar sensación de perspectiva.
        # exit_effect = fr"\t({exit_start},{duration_ms},\fscx90\fscy90\frz-90\move({initial_pos[0]},{initial_pos[1]},{initial_pos[0]-300},{initial_pos[1]-100}))"

        # Combinar todas las etiquetas override
        # override_tags = fr'{{{move_effect}{effect}{tracking_effect}{style_override}{exit_effect}\c{default_c}\3c{shadow_3c}\4c{shadow_3c}\shad3\bord2}}'
        override_tags = fr'{{{effect}{style_override}\c{default_c}\3c{shadow_3c}\4c{shadow_3c}\shad3\bord2}}'

        # Procesar y limpiar el texto
        clean_lines = [line for line in text_lines if line]
        text = r"\N".join(clean_lines) if len(clean_lines) > 1 else (clean_lines[0] if clean_lines else "")
        text = text.replace(r"\N\N", r"\N")

        # Aplicar capitalización
        if text_case == 'upper':
            text = text.upper()
        elif text_case == 'capitalize':
            text = r"\N".join([line[:1].upper() + line[1:].lower() if line else '' for line in text.split(r"\N")])

        # Aplicar estilos especiales (para textos entre paréntesis, comillas, asteriscos, etc.)
        text = re.sub(
            r'(\([^)]+\))',
            lambda match: fr'{{\fnDancing Script Bold\fs140\3c{shadow_3c}&\c{chorus_c}&\4c{shadow_3c}&\shad3\bord2}}'
                          + custom_capitalize(match.group(1), 'capitalize')
                          + r'{\r}' + override_tags,
            text
        )
        text = re.sub(
            r'("([^"]+)")',
            lambda match: fr'{{\fnDancing Script Bold\fs140\3c{shadow_3c}&\c{chorus_c}&\4c{shadow_3c}&\shad3\bord2}}'
                          + custom_capitalize(match.group(1), 'capitalize')
                          + r'{\r}' + override_tags,
            text
        )
        text = re.sub(
            r'\*([^*]+)\*',
            lambda match: fr'{{\fs180\3c{shadow_3c}&\c{title_c}&\4c{shadow_3c}&\shad3\bord2}}\N'
                          + match.group(1).upper()
                          + r'{\r}' + override_tags,
            text
        )
        text = re.sub(
            r'\+([^+]+)\+',
            lambda match: fr'{{\fs{font_size + 40}\3c{shadow_3c}&\c{highlight_c}&\4c{shadow_3c}&\shad3\bord2}}\N'
                          + match.group(1).upper()
                          + r'{\r}' + override_tags,
            text
        )
        text = re.sub(
            r'\%([^%]+)\%',
            lambda match: fr'{{\3c{shadow_3c}&\c{highlight_c}&\4c{shadow_3c}&\shad3\bord2}}'
                          + custom_capitalize(match.group(1), text_case)
                          + r'{\r}' + override_tags,
            text
        )

        # Opcional: si no se aplicaron estilos especiales, se puede ajustar el tamaño de fuente según el número de líneas
        styled_text = text
        lines = styled_text.split(r'\N')
        num_lines = len(lines)
        has_special_styles = any(marker in styled_text for marker in ['{\\fn', '{\\fs', '{\\3c', '{\\c'])
        if not has_special_styles:
            if num_lines >= 2:
                if len(lines[0]) >= len(lines[1]):
                    line1 = f'{{\\fs90}}{lines[0]}'
                    line2 = f'{{\\fs130}}{lines[1]}'
                else:
                    line1 = f'{{\\fs130}}{lines[0]}'
                    line2 = f'{{\\fs90}}{lines[1]}'
                text = line1 + '\\N' + line2
            elif num_lines == 1:
                text = f'{{\\fs140}}{lines[0]}'

    # Escribir la línea de diálogo en el archivo
    f_out.write(
        f"Dialogue: 0,{format_time_ass(start)},{format_time_ass(end)},{style},"
        f"{override_tags}{text}\n"
    )
