# Validación de metodología para datos biomédicos quirúrgicos

Repositorio asociado al Trabajo Fin de Máster: **Diseño de una metodología para la captura, centralización, análisis y visualización de datos biomédicos en entornos quirúrgicos**.

## Objetivo

Este repositorio contiene los archivos utilizados para la validación conceptual de la metodología propuesta. La validación se realiza mediante datos sintéticos representativos de episodios quirúrgicos simulados.

## Contenido

```text
data/
  datos_biomedicos_quirurgicos_sinteticos.csv
  eventos_quirurgicos_sinteticos.csv
  diccionario_variables_dataset.csv
  dataset_quirurgico_sintetico_tfm.xlsx

scripts/
  generar_datos_sinteticos.py

powerbi/
  espacio reservado para el archivo .pbix o capturas del dashboard

docs/
  documentación auxiliar
```

## Datos

Los datos incluidos son sintéticos y no corresponden a pacientes reales. El dataset principal incluye variables fisiológicas y temporales asociadas a episodios quirúrgicos simulados:

- frecuencia cardíaca
- presión arterial sistólica y diastólica
- saturación de oxígeno
- temperatura
- frecuencia respiratoria
- fase asistencial
- evento clínico asociado, cuando aplica

## Ejecución del script

Para regenerar los datos:

```bash
python scripts/generar_datos_sinteticos.py
```

El script generará los CSV dentro de la carpeta `data/`.

## Uso previsto

Los datos se utilizan para comprobar la aplicabilidad de la metodología propuesta: identificación de fuentes, captura, centralización, limpieza, análisis y visualización clínica mediante un dashboard de prueba.

## Consideraciones

La validación no tiene finalidad clínica ni diagnóstica. Su objetivo es verificar la coherencia del flujo metodológico sobre un escenario controlado.
