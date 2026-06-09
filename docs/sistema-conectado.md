---
title: Cómo funciona el sistema conectado
layout: default
nav_order: 4
---

# Cómo funciona todo el sistema conectado

**Arquitectura:** GitHub Pages · FastAPI · Groq API · Render
{: .label .label-blue }

---

## Visión general

El sistema integra tres capas independientes que se comunican entre sí: un **frontend estático** servido desde GitHub Pages, un **backend Python** ejecutado en Render, y la **API de Groq** como motor de procesamiento de voz e inteligencia artificial.

```mermaid
flowchart LR
    subgraph Cliente["🌐 Cliente (Navegador)"]
        UI["HTML / CSS / JS\nGitHub Pages"]
    end
    subgraph Servidor["⚙️ Servidor (Render)"]
        API["FastAPI\napp.py"]
    end
    subgraph IA["🤖 IA (Groq API)"]
        W["Whisper\nSTT"]
        L["LLM\nLlama / Mixtral"]
    end

    UI -- "POST /voz-a-ladder\n(audio blob)" --> API
    API -- "audio" --> W
    W -- "texto transcrito" --> API
    API -- "texto + contexto PDF" --> L
    L -- "JSON Ladder" --> API
    API -- "VozLadderResponse" --> UI
```

> **Regla de oro:** El frontend nunca procesa — solo captura y muestra. Todo el procesamiento vive en el backend.

---

## 1. El Frontend (GitHub Pages)

El frontend es una aplicación **completamente estática**: no hay servidor Python ni Node.js ejecutándose. GitHub Pages sirve archivos HTML, CSS y JavaScript directamente desde el repositorio.

### ¿Qué hace el frontend?

```
Usuario habla → micrófono → audio blob → fetch POST /voz-a-ladder
```

```mermaid
flowchart LR
    A[🎤 Micrófono\ndel usuario] -->|MediaRecorder API| B[Audio Blob\nen memoria]
    B -->|fetch con FormData| C[POST /voz-a-ladder\nRender Backend]
    C -->|JSON de respuesta| D[Renderiza resultado\nen pantalla]
```

### Fragmento representativo del cliente

```javascript
// Captura de audio en el navegador
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const recorder = new MediaRecorder(stream);
let chunks = [];

recorder.ondataavailable = e => chunks.push(e.data);
recorder.onstop = async () => {
    const blob = new Blob(chunks, { type: 'audio/webm' });

    // Envío al backend
    const form = new FormData();
    form.append('audio', blob, 'grabacion.webm');

    const res = await fetch('https://tu-app.onrender.com/voz-a-ladder', {
        method: 'POST',
        body: form
    });
    const data = await res.json();  // VozLadderResponse
    mostrarResultado(data);
};
recorder.start();
```

| Responsabilidad | ¿Quién la hace? |
|----------------|-----------------|
| Capturar audio del micrófono | Browser (`MediaRecorder API`) |
| Convertir audio a blob | Browser (JavaScript) |
| Enviar al backend | `fetch()` en el cliente |
| Mostrar el resultado | Manipulación del DOM |
| Procesar el audio / llamar a IA | ❌ **No — lo hace el backend** |

---

## 2. El Backend (Render)

El backend es un servidor Python real ejecutado en Render. Al recibir una petición de audio, orquesta dos llamadas secuenciales a la API de Groq.

### Flujo interno

```
Recibe audio → Groq Whisper (STT) → texto → Groq LLM → JSON Ladder → respuesta
```

```mermaid
flowchart TD
    A[📥 Recibe audio\nPOST /voz-a-ladder] --> B[Groq Whisper\nSpeech-to-Text]
    B --> C[Texto transcrito\nen español]
    C --> D[Groq LLM\n+ contexto de PDFs]
    D --> E{¿Respuesta válida?}
    E -->|Sí| F[JSON Ladder\nstructurado]
    E -->|No| G[Error 422\nUnprocessable]
    F --> H[📤 VozLadderResponse\nal frontend]
```

### Estructura simplificada de `app.py`

```python
from fastapi import FastAPI, UploadFile
from groq import Groq

app = FastAPI()
client = Groq()

# Al arrancar el servidor, se cargan los PDFs con Vision
contexto_pdf = cargar_pdfs_con_vision()

@app.post("/voz-a-ladder")
async def voz_a_ladder(audio: UploadFile):
    # Paso 1 — Transcribir audio con Whisper
    transcripcion = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=(audio.filename, await audio.read()),
        language="es"
    )

    # Paso 2 — LLM genera estructura Ladder
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": contexto_pdf},
            {"role": "user",   "content": transcripcion.text}
        ],
        response_format={"type": "json_object"}
    )

    return VozLadderResponse.model_validate_json(
        respuesta.choices[0].message.content
    )
```

> **Nota sobre el contexto:** `contexto_pdf` se carga **una sola vez** cuando el servidor arranca. Cada reinicio recarga todos los PDFs, lo que consume tokens de Groq Vision.

---

## 3. Render como hosting

Render actúa como un servidor gestionado: toma el repositorio de GitHub, instala dependencias y mantiene el proceso activo.

### Ciclo de vida de un despliegue

```
GitHub push → Render detecta cambio → rebuild → reinicia servidor → carga PDFs de nuevo
```

```mermaid
flowchart TD
    A[🔀 git push a GitHub] --> B[Render detecta\nel webhook]
    B --> C[pip install -r requirements.txt]
    C --> D[uvicorn app:app --host 0.0.0.0 --port 10000]
    D --> E[Lifespan: carga PDFs\ncon Groq Vision]
    E --> F[✅ Servidor listo\naceptando peticiones]

    style E fill:#fff3cd,stroke:#ffc107
```

### Configuración clave en Render

| Parámetro | Valor típico | Descripción |
|-----------|-------------|-------------|
| **Build Command** | `pip install -r requirements.txt` | Instala dependencias en cada deploy |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` | Inicia el servidor ASGI |
| **Environment Variables** | `GROQ_API_KEY`, etc. | Se configuran en el dashboard de Render |
| **Plan** | Free / Starter | El plan gratuito "hiberna" tras 15 min de inactividad |

> **Problema conocido:** Cada reinicio recarga los PDFs desde cero, gastando tokens de Groq Vision. Una solución es cachear el contexto serializado en disco o en una variable de entorno.

---

## 4. El flujo completo de una petición de voz

Este diagrama muestra toda la cadena de eventos desde que el usuario habla hasta que ve el resultado.

```mermaid
sequenceDiagram
    actor U as 👤 Usuario
    participant B as Browser<br/>(GitHub Pages)
    participant R as Render<br/>(FastAPI)
    participant G as Groq API

    U->>B: Pulsa "Grabar" y habla
    B->>B: MediaRecorder captura audio
    U->>B: Pulsa "Detener"
    B->>R: POST /voz-a-ladder<br/>(audio blob, multipart/form-data)
    R->>G: Whisper STT<br/>(audio → texto)
    G-->>R: Texto transcrito
    Note over R: Combina texto + contexto PDF
    R->>G: LLM Completions<br/>(texto + system prompt)
    G-->>R: JSON Ladder (estructura)
    R-->>B: VozLadderResponse (JSON)
    B->>U: Muestra resultado en pantalla
```

### Resumen de responsabilidades por capa

| Capa | Tecnología | Responsabilidad principal |
|------|-----------|--------------------------|
| **Frontend** | HTML/JS (GitHub Pages) | Capturar audio · Enviar al backend · Mostrar resultado |
| **Backend** | FastAPI (Render) | Orquestar llamadas a Groq · Validar respuesta |
| **STT** | Groq Whisper | Convertir audio a texto |
| **LLM** | Groq (Llama / Mixtral) | Generar estructura Ladder desde el texto |
| **Contexto** | PDFs + Groq Vision | Proveer información del dominio al LLM |

---

## ¿Por qué esta arquitectura?

```mermaid
flowchart LR
    subgraph Gratis["Gratis / Low-cost"]
        GHP["GitHub Pages\n(frontend estático)"]
        GR["Render Free\n(backend Python)"]
        GQ["Groq API\n(free tier)"]
    end

    GHP -- "sin servidor\nsin costo" --- GHP
    GR -- "sleep tras\n15 min idle" --- GR
    GQ -- "rate limits\npero gratis" --- GQ
```

| Decisión | Alternativa descartada | Razón |
|----------|----------------------|-------|
| GitHub Pages para frontend | Netlify, Vercel | Integración nativa con el repo |
| Render para backend | Railway, Fly.io | Plan gratuito, deploy desde GitHub |
| Groq para STT + LLM | OpenAI, Ollama | Velocidad (LPU) y capa gratuita generosa |
| FastAPI | Flask, Django | Validación de tipos con Pydantic, soporte async nativo |
