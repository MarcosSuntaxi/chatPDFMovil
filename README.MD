# chatPDFMovil

chatPDFMovil es una aplicación móvil que permite a los usuarios cargar archivos PDF y chatear con ellos utilizando tecnologías de inteligencia artificial. El proyecto está diseñado para ofrecer una experiencia intuitiva y eficiente, facilitando la interacción, consulta y extracción de información de documentos PDF directamente desde dispositivos móviles.

## Características principales

- **Carga de PDFs:** Permite a los usuarios subir archivos PDF desde su dispositivo móvil.
- **Chat Inteligente:** Interfaz de chat donde los usuarios pueden hacer preguntas sobre el contenido del PDF y obtener respuestas automáticas.
- **Procesamiento de Lenguaje Natural:** Utiliza modelos de IA para interpretar las preguntas y extraer información relevante del documento.
- **Interfaz Amigable:** Diseño adaptado para dispositivos móviles, con navegación sencilla y rápida.
- **Historial de Conversaciones:** Guarda el historial de interacciones para cada documento PDF.
- **Soporte Multiplataforma:** Compatible con Android y iOS (según la configuración del proyecto).

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/MarcosSuntaxi/chatPDFMovil.git
   ```
2. **Instala dependencias:**
   - Si el proyecto está basado en React Native:
     ```bash
     npm install
     ```
   - Si utiliza otro framework, sigue las instrucciones específicas en la documentación del subdirectorio correspondiente.

3. **Configura las variables de entorno:**
   - Renombra el archivo `.env.example` a `.env` y completa los datos necesarios (API keys, endpoints, etc.).

4. **Ejecuta la app:**
   - Para Android:
     ```bash
     npx react-native run-android
     ```
   - Para iOS:
     ```bash
     npx react-native run-ios
     ```

## Estructura del Proyecto

```
chatPDFMovil/
├── android/            # Archivos nativos para Android
├── ios/                # Archivos nativos para iOS
├── src/                # Código fuente principal de la app
│   ├── components/     # Componentes reutilizables
│   ├── screens/        # Pantallas principales de la app
│   ├── services/       # Servicios (API, manejo de PDF, IA, etc.)
│   └── utils/          # Utilidades y helpers
├── assets/             # Imágenes, fuentes y recursos estáticos
├── App.js              # Punto de entrada de la aplicación
├── package.json        # Dependencias y scripts
└── README.md           # Este archivo
```

## Uso

1. Abre la aplicación en tu dispositivo móvil.
2. Carga un archivo PDF desde tu dispositivo.
3. Utiliza la interfaz de chat para interactuar con el documento, haciendo preguntas específicas sobre su contenido.
4. Consulta el historial de conversaciones para revisar preguntas y respuestas anteriores.

## Tecnologías utilizadas

- **React Native** (o el framework móvil correspondiente)
- **Node.js** (para backend si aplica)
- **Librerías de IA / NLP** (por ejemplo, OpenAI o similares)
- **Manejo de archivos PDF**
- **Redux / Context API** para manejo de estado (si aplica)

## Contribución

¡Las contribuciones son bienvenidas! Si deseas colaborar:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Si tienes dudas, sugerencias o necesitas soporte, puedes abrir un issue en el repositorio o contactar al mantenedor principal.

---
Desarrollado con ❤️ por MarcosSuntaxi y colaboradores.