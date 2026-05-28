"""
Generación de datos sintéticos para la validación de una metodología de
captura, centralización, análisis y visualización de datos biomédicos quirúrgicos.

El script genera:
- data/datos_biomedicos_quirurgicos_sinteticos.csv
- data/eventos_quirurgicos_sinteticos.csv
- data/diccionario_variables_dataset.csv

Los datos son completamente sintéticos y no corresponden a pacientes reales.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def clamp(value, low, high):
    return max(low, min(high, value))


def generate_dataset(output_dir="data", n_episodes=10, seed=42):
    random.seed(seed)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    main_csv = output_path / "datos_biomedicos_quirurgicos_sinteticos.csv"
    events_csv = output_path / "eventos_quirurgicos_sinteticos.csv"
    dict_csv = output_path / "diccionario_variables_dataset.csv"

    main_rows = []
    event_rows = []

    surgery_types = [
        "Colecistectomia laparoscopica",
        "Apendicectomia",
        "Hernia inguinal",
        "Artroscopia rodilla",
        "Cirugia ginecologica",
    ]

    start_base = datetime(2026, 5, 20, 8, 0, 0)

    for i in range(1, n_episodes + 1):
        id_paciente = f"P{i:03d}"
        id_episodio = f"EQ{i:03d}"
        start = start_base + timedelta(hours=i - 1)
        surgery = random.choice(surgery_types)

        pre_minutes = 20
        intra_minutes = random.choice([60, 70, 80, 90, 100])
        post_minutes = 30

        hr_base = random.randint(68, 86)
        sys_base = random.randint(118, 138)
        dia_base = random.randint(70, 84)
        spo2_base = random.randint(97, 99)
        temp_base = round(random.uniform(36.2, 36.8), 1)
        rr_base = random.randint(13, 18)

        event_times = {
            start + timedelta(minutes=pre_minutes): "inicio_anestesia",
            start + timedelta(minutes=pre_minutes + 5): "intubacion",
            start + timedelta(minutes=pre_minutes + 15): "incision",
            start + timedelta(minutes=pre_minutes + random.choice([25, 30, 35])): "administracion_farmaco",
            start + timedelta(minutes=pre_minutes + intra_minutes - 10): "cierre",
            start + timedelta(minutes=pre_minutes + intra_minutes): "traslado_recuperacion",
        }

        hypotension_time = None
        if i in [2, 5, 8]:
            hypotension_time = start + timedelta(minutes=pre_minutes + random.choice([35, 45, 55]))
            event_times[hypotension_time] = "hipotension"

        for ts, event_name in sorted(event_times.items()):
            event_rows.append({
                "id_paciente": id_paciente,
                "id_episodio": id_episodio,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "fase_asistencial": (
                    "preoperatoria" if ts < start + timedelta(minutes=pre_minutes)
                    else "intraoperatoria" if ts < start + timedelta(minutes=pre_minutes + intra_minutes)
                    else "postoperatoria"
                ),
                "evento_clinico": event_name,
                "tipo_cirugia": surgery
            })

        total_minutes = pre_minutes + intra_minutes + post_minutes

        for minute in range(0, total_minutes + 1, 5):
            ts = start + timedelta(minutes=minute)

            if minute < pre_minutes:
                phase = "preoperatoria"
                hr = hr_base + random.randint(-5, 6)
                sys = sys_base + random.randint(-8, 8)
                dia = dia_base + random.randint(-5, 5)
                spo2 = spo2_base + random.randint(-1, 1)
                temp = temp_base + random.uniform(-0.1, 0.1)
                rr = rr_base + random.randint(-2, 2)
            elif minute < pre_minutes + intra_minutes:
                phase = "intraoperatoria"
                hr = hr_base - random.randint(3, 12) + random.randint(-4, 4)
                sys = sys_base - random.randint(10, 25) + random.randint(-6, 6)
                dia = dia_base - random.randint(6, 14) + random.randint(-4, 4)
                spo2 = spo2_base + random.choice([-1, 0, 0, 1])
                temp = temp_base - random.uniform(0.2, 0.7)
                rr = random.randint(10, 16)

                if hypotension_time and abs((ts - hypotension_time).total_seconds()) <= 5 * 60:
                    sys = random.randint(78, 92)
                    dia = random.randint(45, 58)
                    hr += random.randint(6, 14)
            else:
                phase = "postoperatoria"
                hr = hr_base + random.randint(-2, 10)
                sys = sys_base - random.randint(0, 12) + random.randint(-5, 5)
                dia = dia_base - random.randint(0, 8) + random.randint(-3, 4)
                spo2 = spo2_base + random.choice([-2, -1, 0, 0, 1])
                temp = temp_base - random.uniform(0.1, 0.5)
                rr = rr_base + random.randint(-1, 4)

            event_name = event_times.get(ts, "")

            main_rows.append({
                "id_paciente": id_paciente,
                "id_episodio": id_episodio,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "fase_asistencial": phase,
                "frecuencia_cardiaca": int(clamp(round(hr), 45, 130)),
                "presion_sistolica": int(clamp(round(sys), 70, 180)),
                "presion_diastolica": int(clamp(round(dia), 40, 110)),
                "spo2": int(clamp(round(spo2), 88, 100)),
                "temperatura": round(clamp(temp, 35.0, 38.5), 1),
                "frecuencia_respiratoria": int(clamp(round(rr), 8, 28)),
                "evento_clinico": event_name,
            })

    main_fields = [
        "id_paciente", "id_episodio", "timestamp", "fase_asistencial",
        "frecuencia_cardiaca", "presion_sistolica", "presion_diastolica",
        "spo2", "temperatura", "frecuencia_respiratoria", "evento_clinico"
    ]

    with open(main_csv, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=main_fields)
        writer.writeheader()
        writer.writerows(main_rows)

    event_fields = [
        "id_paciente", "id_episodio", "timestamp",
        "fase_asistencial", "evento_clinico", "tipo_cirugia"
    ]

    with open(events_csv, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=event_fields)
        writer.writeheader()
        writer.writerows(event_rows)

    dictionary_rows = [
        {"Campo": "id_paciente", "Descripción": "Identificador sintético del paciente"},
        {"Campo": "id_episodio", "Descripción": "Identificador del episodio quirúrgico"},
        {"Campo": "timestamp", "Descripción": "Fecha y hora simulada del registro"},
        {"Campo": "fase_asistencial", "Descripción": "Fase del proceso: preoperatoria, intraoperatoria o postoperatoria"},
        {"Campo": "frecuencia_cardiaca", "Descripción": "Frecuencia cardíaca simulada"},
        {"Campo": "presion_sistolica", "Descripción": "Presión arterial sistólica simulada"},
        {"Campo": "presion_diastolica", "Descripción": "Presión arterial diastólica simulada"},
        {"Campo": "spo2", "Descripción": "Saturación de oxígeno simulada"},
        {"Campo": "temperatura", "Descripción": "Temperatura corporal simulada"},
        {"Campo": "frecuencia_respiratoria", "Descripción": "Frecuencia respiratoria simulada"},
        {"Campo": "evento_clinico", "Descripción": "Evento asociado al episodio, cuando aplica"},
    ]

    with open(dict_csv, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["Campo", "Descripción"])
        writer.writeheader()
        writer.writerows(dictionary_rows)

    print(f"Datos biomédicos generados: {main_csv} ({len(main_rows)} filas)")
    print(f"Eventos generados: {events_csv} ({len(event_rows)} filas)")
    print(f"Diccionario generado: {dict_csv}")


if __name__ == "__main__":
    generate_dataset()
