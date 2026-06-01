from PIL import Image, ImageDraw, ImageFont
import textwrap, os, shutil

OUT = r"E:\20_UNI\Html proyects\prospectiva_de_la_tecnologia\assets\images\practica-1"
IMG_SRC = r"E:\20_UNI\Html proyects\prospectiva_de_la_tecnologia\assets\img"

BG      = (12, 12, 12)
PROMPT  = (15, 198, 116)
CMD     = (255, 215, 100)
OUT_CLR = (204, 204, 204)
DIM     = (110, 110, 110)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 14
PAD   = 22
LINE_H = 20
WIDTH = 1100

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except:
    font = ImageFont.load_default()

CHAR_W = 8  # aprox chars que caben por pixel

def wrap(text, max_chars=128):
    """Devuelve lista de (color, linea) respetando el color original."""
    return textwrap.wrap(text, width=max_chars) or [""]

def render(lines, filename):
    """lines: lista de (color, texto). Soporta lineas largas con wrap."""
    expanded = []
    for color, text in lines:
        chunks = wrap(text)
        expanded.append((color, chunks[0]))
        for c in chunks[1:]:
            expanded.append((color, "    " + c))   # indent continuation

    h = PAD * 2 + LINE_H * len(expanded)
    img = Image.new("RGB", (WIDTH, max(h, 60)), BG)
    d   = ImageDraw.Draw(img)
    y   = PAD
    for color, text in expanded:
        d.text((PAD, y), text, font=font, fill=color)
        y += LINE_H
    img.save(os.path.join(OUT, filename))
    print(f"  OK  {filename}")

# ─────────────────────────────────────────────────────────────────────────────
# 01 · Comandos iniciales: version + pull + ls  (de tu captura)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama --version"),
    (OUT_CLR, "ollama version is 0.24.0"),
    (PROMPT,  "PS C:\\Users\\sebas> ollama pull llama3.2:3b"),
    (OUT_CLR, "pulling manifest"),
    (OUT_CLR, "pulling dde5aa3fc5ff: 100%   2.0 GB"),
    (OUT_CLR, "pulling 966de95ca8a6: 100%   1.4 KB"),
    (OUT_CLR, "pulling fcc5a6bec9da: 100%   7.7 KB"),
    (OUT_CLR, "pulling a70ff7e570d9: 100%   6.0 KB"),
    (OUT_CLR, "pulling 56bb8bd477a5: 100%  96 B"),
    (OUT_CLR, "pulling 34bb5ab01051: 100%  561 B"),
    (OUT_CLR, "verifying sha256 digest"),
    (OUT_CLR, "writing manifest"),
    (OUT_CLR, "success"),
    (PROMPT,  "PS C:\\Users\\sebas> ollama ls"),
    (DIM,     "NAME                           ID              SIZE      MODIFIED"),
    (OUT_CLR, "llama3.2:3b                    a80c4f17acd5    2.0 GB    29 seconds ago"),
    (OUT_CLR, "qwen3:8b                       500a1f067a9f    5.2 GB    2 months ago"),
    (OUT_CLR, "gemma3:12b                     f4031aab637d    8.1 GB    4 months ago"),
    (OUT_CLR, "nomic-embed-text:latest        0a109f422b47    274 MB    4 months ago"),
    (OUT_CLR, "gemma3:4b                      a2af6cc3eb7f    3.3 GB    4 months ago"),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "01-ollama-version-pull-ls.png")

# ─────────────────────────────────────────────────────────────────────────────
# 02 · ollama ls final con todos los modelos
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama ls"),
    (DIM,     "NAME                           ID              SIZE      MODIFIED"),
    (OUT_CLR, "tinyllama:1.1b-chat-v1-q8_0    3746473cdb1e    1.2 GB    About a minute ago"),
    (OUT_CLR, "phi4-mini:latest               78fad5d182a7    2.5 GB    3 minutes ago"),
    (OUT_CLR, "llama3.2:3b                    a80c4f17acd5    2.0 GB    12 minutes ago"),
    (OUT_CLR, "qwen3:8b                       500a1f067a9f    5.2 GB    2 months ago"),
    (OUT_CLR, "gemma3:12b                     f4031aab637d    8.1 GB    4 months ago"),
    (OUT_CLR, "gemma3:4b                      a2af6cc3eb7f    3.3 GB    4 months ago"),
    (OUT_CLR, "nomic-embed-text:latest        0a109f422b47    274 MB    4 months ago"),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "02-ollama-ls.png")

# ─────────────────────────────────────────────────────────────────────────────
# 03 · nomic-embed-text: salida de embedding  (de tu captura)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  'PS C:\\Users\\sebas> ollama run nomic-embed-text:latest "Explica la revolucion francesa en 10 palabras."'),
    (OUT_CLR, "[0.033415258, 0.07893758, -0.17154904, -0.009049314, 0.042240504, -0.07398131,"),
    (OUT_CLR, "-0.036301084, -0.013867525, -0.039575953, -0.02154797, -0.047059923, -0.009520072..."),
    (OUT_CLR, " 0.013161, -0.003363353, 0.02070440, -0.03478075, 0.02604252, -0.016564058,"),
    (OUT_CLR, "-0.049684443, 0.043986878, -0.002653683, 0.01906796, -0.084100490, -0.052825153..."),
    (OUT_CLR, " 0.077338144, -0.003385451, 0.07832809, -0.09086652, -0.055078615, -0.035006290..."),
    (DIM,     " ... (vector de 768 dimensiones — salida de un modelo de embeddings, no texto)"),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "03-nomic-embed-text.png")

# ─────────────────────────────────────────────────────────────────────────────
# 04 · Phi4-mini P1  (respuesta correcta)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama run phi4-mini:latest"),
    (CMD,     '>>> "Explica la diferencia entre inteligencia artificial, aprendizaje automatico,'),
    (CMD,     '     IA generativa y LLM para estudiantes universitarios. Responde en espanol,'),
    (CMD,     '     con tono academico y maximo 200 palabras."'),
    (DIM,     ""),
    (OUT_CLR, "La Inteligencia Artificial (IA) es el termino general que abarca sistemas"),
    (OUT_CLR, "capaces de realizar tareas tipicas de seres humanos como pensar, razonar y aprender."),
    (DIM,     ""),
    (OUT_CLR, "El Aprendizaje Automatico (ML), una rama especifica de IA, involucra algoritmos"),
    (OUT_CLR, "disenados para mejorar su desempeno en funcion a la experiencia previa."),
    (DIM,     ""),
    (OUT_CLR, "La IA Generativa se refiere a sistemas que pueden crear contenido nuevo: imagenes,"),
    (OUT_CLR, "textos o musica, imitando estilos especificos del entrenamiento dado."),
    (DIM,     ""),
    (OUT_CLR, "Los LLM son un tipo especifico de modelo generativo. Son redes neuronales con"),
    (OUT_CLR, "gran cantidad de parametros para entender y generar lenguaje natural."),
    (DIM,     ""),
    (OUT_CLR, "Los LLMs representan uno de sus desarrollos mas innovadores hasta la fecha."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "04-phi4mini-p1.png")

# ─────────────────────────────────────────────────────────────────────────────
# 05 · TinyLlama P3 español  (alucinacion — confunde LLM con LL.M.)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama run tinyllama:1.1b-chat-v1-q8_0"),
    (CMD,     '>>> "Menciona tres riesgos academicos de usar LLM sin verificar fuentes.'),
    (CMD,     '     Incluye un ejemplo breve para cada riesgo."'),
    (DIM,     ""),
    (OUT_CLR, "1. Riesgo de falta de estatus en la prestigiosa universidad de su preferencia:"),
    (OUT_CLR, "   Aunque el programa LLM puede ser exitoso, a menudo los alumnos no han pasado"),
    (OUT_CLR, "   examenes de admision y no reciben reconocimiento de la universidad."),
    (DIM,     ""),
    (OUT_CLR, "2. Riesgo de confianza: Al asistir al LLM, los alumnos deberan ser capacitados"),
    (OUT_CLR, "   en un campo especifico y prepararse para competir con otros alumnos con"),
    (OUT_CLR, "   mayores recursos fiscales."),
    (DIM,     ""),
    (OUT_CLR, "3. Riesgo de expectativas bajas: El precio de acceder al LLM depende de la"),
    (OUT_CLR, "   universidad. Si el programa LLM tiene un precio bajo, los alumnos podrian"),
    (OUT_CLR, "   pensar que las expectativas son demasiado bajas y rechazar el programa."),
    (DIM,     ""),
    (OUT_CLR, "Ejemplos breves:"),
    (OUT_CLR, "1. Estudio de un tema de derecho publico en el caso del LL.M. de Harvard..."),
    (OUT_CLR, "2. Un estudiante de LL.M. de Oxford empezo a trabajar como cocinero en una tienda."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "05-tinyllama-es-alucinacion.png")

# ─────────────────────────────────────────────────────────────────────────────
# 06 · TinyLlama P3 inglés  (sigue alucinando — de tu captura)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama run tinyllama:1.1b-chat-v1-q8_0"),
    (CMD,     '>>> "Mention three academic risks of using LLMs without verifying sources.'),
    (CMD,     '     Include a brief example for each risk."'),
    (DIM,     ""),
    (OUT_CLR, "1. False Accusations: Inaccurate statements made by legal professionals to the"),
    (OUT_CLR, "   media can lead to lawsuits and negative publicity for LLM programs. For"),
    (OUT_CLR, "   example, a LLM student who claims to have represented a client in a high-profile"),
    (OUT_CLR, "   case may later be sued for misrepresentation and falsified evidence."),
    (DIM,     ""),
    (OUT_CLR, "   Example: In 2019, a law school admitted to giving false information about its"),
    (OUT_CLR, "   LLM program to the media. The university settled legal disputes with students."),
    (DIM,     ""),
    (OUT_CLR, "2. Conflicts of Interest: LLM programs affiliated with law firms can create"),
    (OUT_CLR, "   conflicts of interest. Example: In 2017, a LLM program was criticized for"),
    (OUT_CLR, "   allowing its faculty member's firm to sponsor the annual LLM conference."),
    (DIM,     ""),
    (OUT_CLR, "3. Improper Academic Conduct: Faculty members taking positions without disclosing"),
    (OUT_CLR, "   conflicts of interest. Example: In 2018, professors at the University of Toronto"),
    (OUT_CLR, "   were found employed by law firms while holding academic positions, leading"),
    (OUT_CLR, "   to their resignations from the LLM program."),
    (DIM,     ""),
    (OUT_CLR, "In conclusion, legal professionals should verify sources before using them,"),
    (OUT_CLR, "including in law schools pursuing an LLM program."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "06-tinyllama-en-alucinacion.png")

# ─────────────────────────────────────────────────────────────────────────────
# 07 · Gemma3 12B P3  (contraste correcto)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama run gemma3:12b"),
    (CMD,     '>>> "Menciona tres riesgos academicos de usar LLM sin verificar fuentes.'),
    (CMD,     '     Incluye un ejemplo breve para cada riesgo."'),
    (DIM,     ""),
    (OUT_CLR, "1. Fabricacion de informacion (Alucinaciones): Los LLM pueden inventar informacion"),
    (OUT_CLR, "   o citas que parecen plausibles pero son completamente falsas. Ejemplo: inventa"),
    (OUT_CLR, "   el nombre de un economista y una publicacion academica que nunca existieron."),
    (DIM,     ""),
    (OUT_CLR, "2. Plagio involuntario: La redaccion generada puede ser muy similar al material"),
    (OUT_CLR, "   existente sin citar las fuentes originales. Ejemplo: texto similar a un"),
    (OUT_CLR, "   capitulo de un libro de historia popular presentado sin cita."),
    (DIM,     ""),
    (OUT_CLR, "3. Sesgo y perspectivas limitadas: Los LLM reflejan sesgos de sus datos de"),
    (OUT_CLR, "   entrenamiento, perpetuando estereotipos. Ejemplo: descripcion sesgada de un"),
    (OUT_CLR, "   lider politico exagerando ciertos aspectos por datos desequilibrados."),
    (DIM,     ""),
    (OUT_CLR, "Siempre verifica la informacion generada por LLM con fuentes fiables."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "07-gemma3-12b-p3.png")

# ─────────────────────────────────────────────────────────────────────────────
# 08 · Qwen3 8B P4  (ESP32)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  "PS C:\\Users\\sebas> ollama run qwen3:8b"),
    (CMD,     '>>> "Dame un ejemplo de como un estudiante de ingenieria podria usar un LLM'),
    (CMD,     '     para apoyar desarrollo con ESP32, sin sustituir su aprendizaje."'),
    (DIM,     ""),
    (OUT_CLR, "Escenario: sistema de monitoreo de temperatura con ESP32 + sensor DHT11."),
    (DIM,     ""),
    (OUT_CLR, "1. Generacion de codigo inicial — el LLM provee un esqueleto de partida:"),
    (CMD,     "   #include <WiFi.h>"),
    (CMD,     "   #include <DHT.h>"),
    (CMD,     "   DHT dht(14, DHT11);"),
    (CMD,     "   WiFiServer server(80);"),
    (DIM,     ""),
    (OUT_CLR, "2. Explicacion de conceptos — el LLM explica DHT11 y protocolo I2C."),
    (OUT_CLR, "3. Debugging — el LLM sugiere causas; el estudiante verifica con hardware real."),
    (OUT_CLR, "4. Recursos — el LLM recomienda tutoriales; el estudiante aplica y prueba."),
    (DIM,     ""),
    (OUT_CLR, "El LLM actua como asistente, no como reemplazo del aprendizaje practico."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "08-qwen3-p4-esp32.png")

# ─────────────────────────────────────────────────────────────────────────────
# 09 · Gemma3 12B multimodal  (de tu captura)
# ─────────────────────────────────────────────────────────────────────────────
render([
    (PROMPT,  'PS C:\\Users\\sebas> ollama run gemma3:12b "Describe esta imagen: C:\\Users\\sebas\\Pictures\\Screenshots\\gear.png"'),
    (OUT_CLR, "Added image 'C:\\Users\\sebas\\Pictures\\Screenshots\\gear.png'"),
    (OUT_CLR, "Claro, aqui tienes una descripcion de la imagen:"),
    (DIM,     ""),
    (OUT_CLR, "**Descripcion general:**"),
    (DIM,     ""),
    (OUT_CLR, "La imagen muestra dos engranajes dibujados en rojo sobre un fondo de cuadricula"),
    (OUT_CLR, "clara. Los engranajes parecen ser dibujos esquematicos, posiblemente realizados"),
    (OUT_CLR, "en un software CAD o similar."),
    (DIM,     ""),
    (OUT_CLR, "**Detalles:**"),
    (DIM,     ""),
    (OUT_CLR, "*  Engranaje grande: Es un engranaje grande con gran cantidad de dientes."),
    (OUT_CLR, "   Tiene un orificio circular en el centro."),
    (OUT_CLR, "*  Engranaje pequeno: Situado cerca del engranaje grande. Tambien tiene"),
    (OUT_CLR, "   un orificio circular en el centro."),
    (OUT_CLR, "*  Dibujo: Delineados con una linea roja audaz y limpia — representacion"),
    (OUT_CLR, "   clara y simplificada."),
    (DIM,     ""),
    (OUT_CLR, "**Contexto:**"),
    (DIM,     ""),
    (OUT_CLR, "Estos elementos sugieren ingenieria mecanica, transmision de potencia,"),
    (OUT_CLR, "o sistemas de maquinaria."),
    (PROMPT,  "PS C:\\Users\\sebas>"),
], "09-gemma3-12b-multimodal.png")

# ─────────────────────────────────────────────────────────────────────────────
# 10 · Copiar imagen original del engranaje analizado
# ─────────────────────────────────────────────────────────────────────────────
src = os.path.join(IMG_SRC, "Imagen analizada.png")
dst = os.path.join(OUT, "10-imagen-analizada.png")
shutil.copy2(src, dst)
print(f"  OK  10-imagen-analizada.png  (copiada del original)")

print("\nTodas las imagenes generadas.")
