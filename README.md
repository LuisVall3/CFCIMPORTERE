# ⚡ NovaSource Power | Carbon Free Importer

> **Manual de Usuario y Guía de Operación**  
> *Sistema de Procesamiento y Carga del Daily Operator Log (Carbon Free Chile)*  
> **Desarrollado por:** LuisVall3  
> **Versión:** 1.0.0

---

## 📋 Descripción General

**Carbon Free Importer** es una herramienta de escritorio desarrollada para automatizar la lectura, validación y consolidación del informe diario de operaciones (*Daily Operator Log*) de las plantas fotovoltaicas administradas por **NovaSource Power Services** bajo el contrato de Carbon Free Chile.

El sistema evita la duplicidad de información, procesa archivos Excel oficiales enviados por el equipo de flota y consolida los datos en un **Excel Maestro** centralizado sin dejar huecos o celdas vacías tras eliminaciones manuales.

---

## 🛠️ Requisitos del Sistema

* **Sistema Operativo:** Windows 10 / 11 (64-bits) o macOS Big Sur / Sonoma (Apple Silicon & Intel).
* **Software Adicional:** Microsoft Excel o compatible (.xlsx).
* **Conexión a Red:** No requerida (funciona de forma 100% local).

---

## 📥 Descarga e Instalación

1. Dirígete a la sección de **[Releases / Lanzamientos]** en el repositorio de GitHub.
2. Descarga el paquete comprimido oficial: **`CarbonFreeImporter.zip`**.
3. Extrae el contenido del archivo `.zip` en una carpeta local de tu equipo (por ejemplo, en `C:\NovaSource\` o en tu Escritorio).

> ⚠️ **Aviso de descarga (Navegadores / Windows SmartScreen):**  
> Al abrir una aplicación ejecutable descargada directamente de internet, es posible que Chrome o Windows muestren la advertencia: *"Archivo poco habitual / No se puede verificar"*.
> * **En Google Chrome:** Haz clic en los tres puntos **`...`** o en la flecha del archivo en descargas $\rightarrow$ selecciona **Guardar de todos modos**.
> * **En Windows:** Haz clic en **Más información** $\rightarrow$ selecciona **Ejecutar de todos modos**.

---

## ⚙️ Configuración Inicial (Primera Ejecución)

La primera vez que ejecutes el programa (`CarbonFreeImporter.exe`), el sistema te solicitará configurar las **rutas fijas de trabajo**:

1. **Archivo Excel Maestro (`.xlsx`):** Selecciona o define la ubicación de la planilla principal donde se consolidan todos los registros históricos.
2. **Carpeta de Registros (Logs):** Selecciona la carpeta donde el sistema guardará las bitácoras técnicas de auditoría de cada importación.
3. Haz clic en **`GUARDAR Y CONTINUAR`**.

> 💡 **Nota:** Esta configuración se guarda de forma permanente en tu sistema (`AppData` en Windows / `Application Support` en macOS). No tendrás que volver a seleccionar estas rutas en futuras ejecuciones.

---

## 🚀 Guía de Uso Paso a Paso

### Paso 1: Iniciar la Aplicación
Abre el archivo ejecutable de la aplicación. Verás la pantalla principal con el distintivo corporativo de **NovaSource Power** y la consola de estado en verde con el mensaje `● SISTEMA LISTO`.

### Paso 2: Importar un Reporte
1. Haz clic en el botón principal **`⚡ IMPORTAR REPORTE`**.
2. Se abrirá la ventana del explorador de archivos. Busca y selecciona el archivo Excel con el reporte del día que deseas procesar.
3. El botón cambiará automáticamente a estado `● PROCESANDO...` mientras el hilo en segundo plano analiza el archivo.

### Paso 3: Validación y Consolidación Automática
El motor interno ejecutará los siguientes controles:
* **Filtro de Duplicados:** Compara los registros del archivo nuevo contra el Excel Maestro. Si un registro ya existe, lo ignorará automáticamente para prevenir duplicidad.
* **Compactación Inteligente:** Inserta las filas nuevas inmediatamente después del último registro real, asegurando que no queden huecos o celdas vacías intermedias aunque hayas borrado filas manualmente en Excel.
* **Registro de Auditoría:** Escribe una bitácora detallada en la consola con la cantidad exacta de registros agregados o ignorados.

### Paso 4: Finalización
Al concluir el proceso, el indicador cambiará a **`● IMPORTACIÓN COMPLETADA`** y se mostrará un mensaje confirmando que la base de datos se ha actualizado exitosamente.

---

## 📑 Estructura de Archivos y Persistencia

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| `config.json` | Almacena las rutas del Excel Maestro y Logs configuradas por el usuario. |
| `Maestro.xlsx` | Planilla consolidada acumulativa con el historial operacional. |
| `data/Logs/` | Carpeta contenedora de los archivos `.log` generados por fecha. |

---

## ❓ Preguntas Frecuentes y Solución de Problemas

#### 1. ¿Qué sucede si el archivo que intento cargar no tiene registros nuevos?
El programa informará en la consola que no hay registros nuevos para agregar (`0 registros agregados`) y no alterará la estructura del Excel Maestro.

#### 2. Borré filas manualmente en el Excel Maestro, ¿el programa dejará un espacio en blanco?
**No.** El sistema recalcula la última fila real con datos antes de cada inserción mediante concatenación continua, asegurando que los registros nuevos queden pegados consecutivamente.

#### 3. ¿Cómo puedo cambiar las rutas del Maestro o de los Logs si cambié de carpeta?
Puedes editar directamente el archivo de configuración `config.json` ubicado en tu carpeta de usuario de Windows (`%APPDATA%\NovaSource\config.json`) o borrar las rutas dentro de las comillas para que el programa te vuelva a solicitar la ventana emergente al iniciar.

---

## 👨‍💻 Soporte Técnico y Autoría

* **Desarrollador:** LuisVall3
* **Organización:** NovaSource Power Services
* **Proyecto:** Carbon Free Importer