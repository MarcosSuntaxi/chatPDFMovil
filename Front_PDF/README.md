# Bienvenido a tu app Expo 👋

Este es un proyecto de [Expo](https://expo.dev) creado con [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Primeros pasos

### 1. Crea y activa un entorno virtual de Python

Antes de instalar las dependencias, configura y activa un entorno virtual de Python:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Mac/Linux
source venv/bin/activate
```

### 2. Instala las dependencias

```bash
npm install
```

### 3. Inicia la aplicación

```bash
npx expo start
```

En la salida, encontrarás opciones para abrir la app en un:

- [build de desarrollo](https://docs.expo.dev/develop/development-builds/introduction/)
- [emulador de Android](https://docs.expo.dev/workflow/android-studio-emulator/)
- [simulador de iOS](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), una sandbox limitada para probar el desarrollo de apps con Expo

Puedes comenzar a desarrollar editando los archivos dentro del directorio **app**. Este proyecto utiliza [ruteo basado en archivos](https://docs.expo.dev/router/introduction).

---

## Importante: Configuración de la URL del backend

En el archivo `app/(tabs)/explore.tsx`, **debes** cambiar la URL del backend por la dirección IP local de tu computadora. Modifica la siguiente línea:

```typescript
const BACKEND_URL = 'http://192.168.100.23:5000'; // Cambia por tu IP local
```

Reemplaza `192.168.100.23` por la IP local real de tu computadora para que la app pueda conectarse correctamente al servidor backend desde tu dispositivo.

---

## Obtener un proyecto limpio

Cuando estés listo, ejecuta:

```bash
npm run reset-project
```

Este comando moverá el código de inicio al directorio **app-example** y creará un nuevo directorio **app** donde podrás comenzar a desarrollar desde cero.

## Aprende más

Para aprender más sobre cómo desarrollar tu proyecto con Expo, revisa los siguientes recursos:

- [Documentación de Expo](https://docs.expo.dev/): Aprende lo básico o explora temas avanzados con nuestras [guías](https://docs.expo.dev/guides).
- [Tutorial de Expo](https://docs.expo.dev/tutorial/introduction/): Sigue este tutorial paso a paso para crear un proyecto que funcione en Android, iOS y web.

## Únete a la comunidad

Únete a nuestra comunidad de desarrolladores creando apps universales.

- [Expo en GitHub](https://github.com/expo/expo): Explora nuestra plataforma open source y contribuye.
- [Comunidad en Discord](https://chat.expo.dev): Chatea con otros usuarios de Expo y haz preguntas.
