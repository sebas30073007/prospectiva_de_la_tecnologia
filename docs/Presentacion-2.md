---
title: ·Presentación LAVO  
layout: default
nav_order: 9
---

# Presentación: Ladder Voice — LAVO

**Tema:** Programación Ladder · Inteligencia Artificial · PLC · Voz a texto
{: .label .label-blue }

---

## Introducción

Esta presentación corresponde al proyecto **Ladder Voice**, también llamado **LAVO**. El proyecto propone una plataforma para asistir la programación de PLC mediante lenguaje natural, voz e inteligencia artificial.

La idea principal de LAVO es permitir que el usuario describa una lógica de control en lenguaje natural y que el sistema transforme esa instrucción en una representación estructurada que pueda visualizarse como un diagrama Ladder.

---

## ¿Qué es LAVO?

**LAVO** es un agente o plataforma de programación asistida para PLC. Su objetivo es facilitar la creación de lógica Ladder a partir de instrucciones escritas o habladas.

El flujo general del proyecto puede resumirse así:

```text
Voz o texto del usuario
        ↓
Reconocimiento de voz a texto
        ↓
Interpretación mediante IA
        ↓
Generación de JSON lógico
        ↓
Compilación a diagrama Ladder
        ↓
Validación visual
        ↓
Envío de configuración al PLC
```

Este enfoque busca que el usuario no tenga que escribir directamente toda la lógica Ladder desde cero, sino que pueda apoyarse en un asistente inteligente para construir, revisar y validar programas de control.

---

## Presentación en Canva

A continuación se muestra la presentación realizada en Canva sobre el proyecto **Ladder Voice — LAVO**.

<div style="position: relative; width: 100%; height: 0; padding-top: 56.25%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16);
 margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy"
    style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;"
    src="https://www.canva.com/design/DAHMB6OQad8/view?embed"
    allowfullscreen="allowfullscreen"
    allow="fullscreen">
  </iframe>
</div>

[Ver presentación directamente en Canva](https://canva.link/d53fyd83wf4tcpj){: .btn .btn-blue }

---

## Relación con el proyecto

La presentación explica el propósito de **LAVO** como una herramienta que conecta inteligencia artificial con automatización industrial. El proyecto integra tecnologías como:

| Componente | Función dentro del proyecto |
|---|---|
| Interfaz web | Permite al usuario escribir o grabar instrucciones |
| STT | Convierte la voz del usuario en texto |
| LLM | Interpreta la instrucción y genera lógica estructurada |
| JSON lógico | Representa la lógica de control de forma ordenada |
| Editor Ladder | Permite visualizar y validar el programa |
| Backend | Coordina la comunicación entre IA, frontend y PLC |
| PLC Horner / Cscape | Ejecuta la lógica de control mediante un programa maestro |

---

## Enfoque técnico

El proyecto no busca reprogramar completamente el PLC en cada instrucción. En cambio, plantea dejar un programa maestro cargado en el PLC y modificar registros o configuraciones desde el backend.

Este enfoque permite que:

- el PLC mantenga la ejecución segura de la lógica,
- el usuario pueda validar visualmente el programa antes de aplicarlo,
- la IA genere estructuras lógicas revisables,
- el sistema sea más flexible y escalable.

---

## Importancia del proyecto

LAVO representa una aplicación práctica de inteligencia artificial en el área de automatización. Su valor principal está en acercar la programación Ladder a usuarios que quieren construir lógica de control de forma más intuitiva.

Además, el proyecto permite explorar cómo los modelos de lenguaje pueden participar en tareas técnicas, siempre considerando validaciones, seguridad y supervisión antes de ejecutar acciones en hardware real.

---

## Reflexión

El desarrollo de LAVO muestra que la inteligencia artificial puede utilizarse como una capa de asistencia para procesos industriales y educativos. Sin embargo, también evidencia que los sistemas conectados a PLC requieren validación estricta, revisión humana y una arquitectura segura.

Por esta razón, LAVO no sustituye la lógica de control tradicional, sino que funciona como un puente entre el lenguaje natural del usuario y la programación Ladder utilizada en automatización.

---