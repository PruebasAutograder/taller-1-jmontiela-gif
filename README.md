[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/GMiPfv5D)
# Taller 1 - Sistemas Expertos con Experta

## Instrucciones para el Estudiante

### 📋 Objetivo
Completar el sistema experto para diagnóstico de vehículos usando la librería `experta` en Python.

### 🚀 Cómo empezar

1. **Clona este repositorio template** (ya lo hiciste si estás leyendo esto)
2. **Abre el archivo `Ejercicio_1_Taller_1.ipynb`** en Google Colab o Jupyter
3. **Completa las partes marcadas con `**`** (asteriscos)
4. **Sube tu notebook completado a este repositorio**
5. **Haz push para activar la autocalificación**

### ✅ Qué debes completar

El notebook tiene varias secciones incompletas marcadas con `**`. Debes:

1. **Completar la regla de frenos** (`@Rule` para `ruido_metalico`)
2. **Completar la regla de refrigerante** (usando `AND`)
3. **Completar las reglas de revisión general** (usando `NOT`)
4. **Completar todas las declaraciones `self.declare()`**
5. **Completar las declaraciones `self.retract()`**
6. **Completar la sección de ejecución** (`engine = VehicleDiagnosis()`, etc.)
7. **Agregar declaraciones de síntomas** para probar el sistema

### 🎯 Criterios de Evaluación

Tu ejercicio será calificado automáticamente en base a:

- **Sintaxis correcta** (10 pts): El código debe compilar sin errores
- **Ejecución exitosa** (10 pts): El código debe ejecutarse sin fallar
- **Reglas completadas** (40 pts): Las reglas deben estar sintácticamente correctas
- **Declaraciones correctas** (25 pts): `declare()` y `retract()` implementados
- **Sección de ejecución** (20 pts): Instanciación y uso del motor
- **Output del sistema** (5 pts): El sistema debe generar diagnósticos

**Puntaje mínimo para aprobar: 70%**

### 🔍 Cómo verificar tu trabajo

Después de hacer `push` a tu repositorio:

1. Ve a la pestaña **"Actions"** en tu repositorio GitHub
2. Verás el workflow **"Autocalificación Ejercicios IA"** ejecutándose
3. Haz clic en la ejecución más reciente para ver los detalles
4. En la sección de resultados verás tu puntuación y retroalimentación detallada

### ✨ Consejos

- **Lee cuidadosamente** los comentarios en el código para entender qué completar
- **Mantén la estructura** de las clases y decoradores `@Rule`
- **Usa los nombres correctos** para tipos de síntomas y estados
- **Prueba tu código** en Colab antes de subirlo
- **No cambies** la estructura general del archivo, solo completa lo que falta

### 🆘 Resolución de Problemas

**Mi código no compila:**
- Revisa la sintaxis de Python
- Asegúrate de cerrar todos los paréntesis y comillas
- Verifica la indentación

**Mi puntuación es baja:**
- Lee los detalles en la pestaña Actions
- Verifica que completaste TODAS las partes marcadas con `**`
- Asegúrate de que tu código genere output al ejecutarse

**El autograder no se ejecuta:**
- Verifica que subiste el archivo `.ipynb` correctamente
- Asegúrate de hacer `push` a la rama `main` o `master`

### 📞 Contacto
Si tienes problemas técnicos con GitHub Classroom, contacta a tus profesores.

---
**¡Buena suerte! 🎓**
