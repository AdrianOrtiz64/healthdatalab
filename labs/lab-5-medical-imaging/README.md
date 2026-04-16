# Lab 5 — Exploración de Imágenes Médicas con DICOM

En los labs anteriores trabajamos exclusivamente con datos **tabulares**: tablas de pacientes, diagnósticos codificados, signos vitales numéricos. Pero en la práctica clínica, una parte enorme de los datos son **no estructurados**: imágenes, texto libre, señales fisiológicas.

Ahora damos el salto:

> Un archivo DICOM no es "solo una imagen". Es un contenedor que empaqueta la imagen junto con cientos de campos de metadata clínica: quién es el paciente, qué equipo se usó, cómo interpretar los píxeles.

---

## Objetivo del laboratorio

Explorar el estándar **DICOM** como formato nativo de imágenes médicas para:

- Entender la estructura de un archivo DICOM: imagen + metadata clínica
- Extraer y comparar metadata entre modalidades (CT, MR, radiografía)
- Aplicar **windowing** para revelar diferentes estructuras anatómicas en la misma imagen
- Construir un volumen 3D a partir de múltiples cortes DICOM
- Realizar **segmentación por umbral** usando unidades Hounsfield

---

## Qué aprenderás

- Por qué DICOM existe y qué información se pierde al exportar a PNG/JPEG
- Cómo las unidades Hounsfield (HU) codifican densidad de tejidos en CT
- Cómo el windowing transforma el mismo dato crudo en visualizaciones completamente diferentes
- Por qué la representación importa antes de cualquier paso de modelado

---

## Dataset

Este lab **no requiere descargas externas**. Todos los datos provienen de archivos de prueba incluidos en la librería `pydicom`:

| Archivo | Modalidad | Tamaño | Uso |
|---------|-----------|--------|-----|
| `CT_small.dcm` | CT | 128x128 | Windowing, HU, segmentación |
| `MR_small.dcm` | MR | 64x64 | Comparar modalidades |
| `MR-SIEMENS-DICOM-WithOverlays.dcm` | MR | 484x484 | Metadata rica, dual window |
| `RG1_UNCI.dcm` | CR (radiografía) | 1955x1841 | Comparar modalidades |
| Serie CT5N (5 cortes) | CT | 16x16 | Concepto de volumen 3D |

---

## Flujo de trabajo

Sigue el flujo definido en `COURSE_SETUP.md`.

1. Actualiza `main`
2. Crea tu branch:

```bash
git checkout -b lab05-medical-imaging/grupo-N
```

3. Trabaja únicamente en ese branch
4. Haz commits durante el proceso (hay 4 checkpoints)
5. Entrega con Pull Request

---

## Importante

Este laboratorio se guía completamente desde el notebook:

```
notebooks/Lab05_Imagenes_Medicas_DICOM.ipynb
```

No necesitas descargar datos ni instalar software adicional más allá de Docker.

---

## Antes de empezar

Verifica:

```bash
git branch
git remote -v
docker compose up -d
```

- No estás en `main`
- Tienes `origin` y `upstream`
- Docker está corriendo (jupyter)

---

## Resultado esperado

Al final deberías poder:

- Extraer metadata clínica de cualquier archivo DICOM
- Explicar por qué la misma imagen CT se ve diferente con distintas ventanas
- Construir un volumen 3D a partir de cortes individuales
- Segmentar tejidos usando umbrales de unidades Hounsfield
- Reflexionar sobre las implicaciones de privacidad de los archivos DICOM
