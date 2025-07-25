# chatPDFMovil

chatPDFMovil es una aplicación móvil compuesta por dos grandes módulos principales:

1. **El Frontend móvil:** la app que los usuarios usan en sus teléfonos para interactuar.
2. **El servicio de ChatPDF:** el backend que procesa los PDFs y responde a las preguntas realizadas por los usuarios.

Este README describe ambos componentes y sus responsabilidades dentro del proyecto.

---

## 1. Frontend móvil

El frontend es una aplicación móvil (por ejemplo, en React Native o Flutter) que permite a los usuarios:

- **Subir archivos PDF** desde su dispositivo móvil.
- **Interactuar mediante un chat** con el PDF cargado, enviando preguntas y recibiendo respuestas.
- **Ver el historial de preguntas y respuestas** relacionadas a cada documento.

El frontend se encarga de la experiencia de usuario, la navegación, el manejo de archivos locales y la comunicación segura con el servicio de backend (ChatPDF).

### Flujo general del usuario

1. **Carga un PDF** desde su dispositivo.
2. **Envía una pregunta** sobre el contenido del PDF mediante la interfaz de chat.
3. **Recibe la respuesta** generada por el backend y la ve en el chat.
4. **Puede consultar el historial** de interacción para ese documento.

---

## 2. Servicio ChatPDF (Backend)

El backend es responsable de:

- **Recibir el PDF** y almacenarlo temporalmente, si es necesario.
- **Procesar el contenido** del PDF, extrayendo el texto y preparándolo para responder preguntas.
- **Recibir preguntas** del frontend y emplear algoritmos de procesamiento de lenguaje natural (NLP) para localizar y generar respuestas relevantes usando el contenido del PDF.
- **Enviar la respuesta** al frontend para que el usuario la vea en la app.

El backend puede estar construido en cualquier stack que soporte procesamiento de PDFs y NLP (por ejemplo, Node.js, Python, etc.), y puede integrarse con APIs de inteligencia artificial si es necesario.

---

## Resumen de la arquitectura

```
[Usuario móvil]
      |
      v
[App móvil (Frontend)]
      |
      v
[API ChatPDF (Backend)]
      |
      v
[Procesamiento PDF + IA]
```

---

## Instalación y ejecución

Consulta los README específicos de cada subcarpeta (`/frontend` y `/chatpdf` o equivalente) para instrucciones detalladas sobre instalación y ejecución de cada módulo.

