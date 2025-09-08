#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador automático de noticias
"""

import random
from datetime import datetime

# Listas para generar noticias
temas = ["tecnología", "deportes", "política", "economía", "salud"]
verbos = ["anuncia", "lanza", "reveala", "presenta", "descubre"]
sustantivos = ["nuevo producto", "investigación", "estudio", "proyecto"]

def generar_noticia():
    """Genera una noticia aleatoria"""
    tema = random.choice(temas)
    verbo = random.choice(verbos)
    sustantivo = random.choice(sustantivos)
    
    noticia = f"{tema.capitalize()}: {random.choice(['Empresa', 'Gobierno', 'Científicos'])} {verbo} {sustantivo} revolucionario"
    
    return noticia

def main():
    print("🎯 GENERADOR DE NOTICIAS AUTOMÁTICO")
    print("=" * 40)
    
    # Generar 5 noticias
    for i in range(5):
        print(f"{i+1}. {generar_noticia()}")
    
    print(f"\n📅 Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
