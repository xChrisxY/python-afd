import re

def detect_sql_injection(text):
    
    sql_patterns = [
        r"(\bor\b|\band\b)",  # Operadores lógicos
        r"('.*?'|\".*?\")",  # Cadenas entre comillas simples o dobles
        r"(--|#)",  # Comentarios SQL de una línea,
        r"(-|#)",  # Comentarios SQL de una línea
        r"/\*.*?\*/",  # Comentarios de múltiples líneas
        r"(select\b|insert\b|update\b|delete\b|drop\b|truncate\b|exec\b)",  # Palabras clave SQL
        r"(\bunion\b\s+select\b)",  # UNION SELECT
        r"(;.*?--)|(;.*?$)",  # Comandos terminados con punto y coma
        r"((\%27)|(\'))(\s+or\s+|\s+and\s+)?(\d=\d|\d=\d+|true|false)",  # Ejemplos como ' OR '1'='1
        r"((\%27)|(\'))\s+(drop|select|insert|delete)\s",  # DROP TABLE y similares
    ]
    sql_regex = re.compile('|'.join(sql_patterns), re.IGNORECASE)
    
    
    matches = sql_regex.findall(text)
    
    if matches:
        print(f"Posible inyección SQL detectada: {matches}")
        return True
    else:
        print("No se detectaron inyecciones SQL.")
        return False

#text = "Este es un ejemplo de inyección: ' OR '1'='1; DROP TABLE users; --"
text = "¿Por qué lo usamos? Es un hecho establecido hace demasiado tiempo que un lector ,se distraerá con el contenido del texto de un sitio mientras que mira su diseño,El punto de usar Lorem Ipsum es ' OR '1'='1 que tiene una distribución más o menos normal ,las letras, al contrario de usar textos como por ejemplo 'Contenido aquí, contenido aquí,'; DROP TABLE users; -- Estos textos hacen parecerlo un español que se puede leer."

detect_sql_injection(text)
