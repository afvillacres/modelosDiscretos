import spacy
from pymongo import MongoClient

# Cargar el modelo de SpaCy en lenguaje español
nlp = spacy.load('es_core_news_lg')

# Conexión a MongoDB
client = MongoClient('mongodb+srv://avillacres:1234AZ@cluster0.ppg8sv5.mongodb.net/')

db = client.PythonConexio
sustantivos_en_bd = db.Sustantivos
verbos_en_bd = db.Verbos
oraciones_en_bd = db.Oraciones

def detectarSustantivosVerbos(oracion):
    doc = nlp(oracion)
    
    sustantivos = []
    verbos = []
    
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"}:
            sustantivos.append(token.text.lower())
        elif token.pos_ == "VERB":
            verbos.append(token.text.lower())
    
    return sustantivos, verbos

def comprobarBaseDatos(sustantivos, verbos):
    sustantivos_encontrados = []
    verbos_encontrados = []
    
    for sustantivo in sustantivos:
        if sustantivos_en_bd.find_one({"palabra": sustantivo}):
            sustantivos_encontrados.append(sustantivo)
    
    for verbo in verbos:
        if verbos_en_bd.find_one({"palabra": verbo}):
            verbos_encontrados.append(verbo)
    
    return sustantivos_encontrados, verbos_encontrados

def solicitarEtiquetas(tipo, palabra):
    if tipo == "sustantivo":
        while True:
            es_persona = input(f"¿{palabra} es una persona? (si/no): ").strip().lower()
            if es_persona == "si":
                categoria = "persona"
                break
            else:
                es_animal = input(f"Mmm, ¿quizás {palabra} es un animal? (si/no): ").strip().lower()
                if es_animal == "si":
                    categoria = "animal"
                    break
                else:
                    es_objeto = input(f"Entonces, ¿{palabra} es un objeto? (si/no): ").strip().lower()
                    if es_objeto == "si":
                        categoria = "objeto"
                        break
                    else:
                        print(f"No puedo determinar la categoría de {palabra}. Intentemos con otra palabra.")
        numero = input(f"¿{palabra} está en singular o plural? (singular/plural): ").strip().lower()
        return [categoria, numero]
    
    elif tipo == "verbo":
        while True:
            es_humano = input(f"¿Este {palabra} lo puede hacer una persona? (si/no): ").strip().lower()
            if es_humano == "si":
                categoria = "humano"
                numero = input(f"¿Una persona o varias personas pueden hacer {palabra}? (una/varias): ").strip().lower()
                break
            else:
                es_animal = input(f"¿Este {palabra} lo puede hacer un animal? (si/no): ").strip().lower()
                if es_animal == "si":
                    categoria = "animal"
                    numero = input(f"¿Un animal o varios animales pueden hacer {palabra}? (uno/varios): ").strip().lower()
                    break
                else:
                    categoria = "general"
                    numero = input(f"¿{palabra} está en singular o plural? (singular/plural): ").strip().lower()
                    break
        return [categoria, numero]

def insertarEnBaseDatos(palabra, tipo):
    etiquetas = solicitarEtiquetas(tipo, palabra)
    if tipo == "sustantivo":
        sustantivos_en_bd.insert_one({"palabra": palabra, "etiquetas": etiquetas})
    elif tipo == "verbo":
        verbos_en_bd.insert_one({"palabra": palabra, "etiquetas": etiquetas})

def convertir_negacion(frase):
    frase = frase.replace("no ", " ¬ ")
    frase = frase.replace("nunca ", " ¬ ")
    frase = frase.replace("nadie ", " ¬ ")
    return frase

def convertir_conjuncion(frase):
    frase = frase.replace(" y ", " ∧ ")
    frase = frase.replace(" e ", " ∧ ")
    return frase

def convertir_disyuncion(frase):
    frase = frase.replace(" o ", " ∨ ")
    return frase

def convertir_bicondicional(frase):
    frase = frase.replace(" si y solo si ", " ↔ ")
    return frase

def convertir_implicacion(frase):
    frase = frase.replace(" si ", " → ")
    frase = frase.replace(" entonces ", " → ")
    return frase

def convertir_cuantificadores(frase):
    frase = frase.replace("existe ", "∃ ")
    frase = frase.replace("algún ", "∃ ")
    frase = frase.replace("hay ", "∃ ")
    frase = frase.replace("todos ", "∀ ")
    frase = frase.replace("nosotros ", "∀ ")
    frase = frase.replace("para todo ", "∀ ")
    frase = frase.replace("para nosotros ", "∀ ")
    frase = frase.replace("Existe ", "∃ ")
    frase = frase.replace("Algún ", "∃ ")
    frase = frase.replace("Hay ", "∃ ")
    frase = frase.replace("Todos ", "∀ ")
    frase = frase.replace("Nosotros ", "∀ ")
    frase = frase.replace("Para todo ", "∀ ")
    frase = frase.replace("Para nosotros ", "∀ ")
    return frase

def limpiar_frase(frase):
    frase = frase.strip()
    frase = ' '.join(frase.split())
    return frase

def convertir_a_proposiciones(oracion):
    oracion = convertir_cuantificadores(oracion)
    oracion = convertir_negacion(oracion)
    oracion = convertir_conjuncion(oracion)
    oracion = convertir_disyuncion(oracion)
    oracion = convertir_implicacion(oracion)
    oracion = convertir_bicondicional(oracion)
    oracion = limpiar_frase(oracion)
    return oracion

def almacenar_oracion(oracion, proposicion):
    oraciones_en_bd.insert_one({"oracion": oracion, "proposicion": proposicion})

def obtener_proposicion(oracion):
    registro = oraciones_en_bd.find_one({"oracion": oracion})
    if registro:
        return registro["proposicion"]
    return None

# Ejecuta lo "principal"
while True:
    print(f"")
    print(f"------------------------------------------------------------------------------------------------")
    print(f"")
    oracion = input("Ingrese una oración: ")
    
    proposicion_existente = obtener_proposicion(oracion)
    if proposicion_existente:
        print("Sentencia en lenguaje natural:", oracion)
        print("Proposiciones lógicas (recuperadas):", proposicion_existente)
    else:
        sustantivos, verbos = detectarSustantivosVerbos(oracion)
        print(f"")
        print(f"------------------------------------------------------------------------------------------------")
        print(f"")
        print(f"Sustantivos: {', '.join(sustantivos)}")
        print(f"Verbos: {', '.join(verbos)}")

        sustantivos_encontrados, verbos_encontrados = comprobarBaseDatos(sustantivos, verbos)
        
        print(f"Sustantivos en la base de datos: {', '.join(sustantivos_encontrados)}")
        print(f"Verbos en la base de datos: {', '.join(verbos_encontrados)}")
        
        print(f"")
        print(f"------------------------------------------------------------------------------------------------")
        print(f"")

        for sustantivo in sustantivos:
            if sustantivo not in sustantivos_encontrados:
                print(f"Disculpa, esta palabra '{sustantivo}' es nueva para mí. ¿Me ayudas a saber qué es?")
                insertarEnBaseDatos(sustantivo, "sustantivo")

        for verbo in verbos:
            if verbo not in verbos_encontrados:
                print(f"Disculpa, esta palabra '{verbo}' es nueva para mí. ¿Me ayudas a saber qué es?")
                insertarEnBaseDatos(verbo, "verbo")
        
        print(f"")
        print(f"------------------------------------------------------------------------------------------------")
        print(f"")

        proposiciones = convertir_a_proposiciones(oracion)
        print("Sentencia en lenguaje natural:", oracion)
        print("Proposiciones lógicas:", proposiciones)

        almacenar_oracion(oracion, proposiciones)
    
    print(f"")
    print(f"------------------------------------------------------------------------------------------------")
    print(f"")
    continuar = input("¿Desea ingresar otra oración? (si/no): ").strip().lower()
    if continuar != "si":
        break

print("¡Gracias por usar el traductor de oraciones a proposiciones lógicas!")
