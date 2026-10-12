import csv
from pathlib import Path

from faker import Faker

Faker.seed(42)

RUTA_ALU = Path(__file__).parent.parent / "data" / "alumnos.csv"
fake = Faker()
with open(RUTA_ALU, mode="w", newline="", encoding="utf-8") as data:
    writer = csv.writer(data)
    writer.writerow(["id", "nombre", "apellido", "email", "es_menor", "grupo_id"])
    for i in range(1, 41):
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = f"{nombre.lower()}.{apellido.lower()}.{i}@example.com"
        es_menor = fake.boolean(chance_of_getting_true=70)
        grupo_id = fake.random_int(min=1, max=7)
        writer.writerow([i, nombre, apellido, email, es_menor, grupo_id])

Faker.seed(43)
RUTA_GRU = Path(__file__).parent.parent / "data" / "grupos.csv"
fake = Faker()
with open(RUTA_GRU, mode="w", newline="", encoding="utf-8") as data:
    writer = csv.writer(data)
    writer.writerow(["id", "nombre", "dias_semana"])
    for i in range(1, 8):
        nombre = fake.random_element(
            elements=[
                f"Elefantes {i}",
                f"Tigres {i}",
                f"Leones {i}",
                f"Jirafas {i}",
                f"Cebras {i}",
                f"Rinocerontes {i}",
                f"Hipopótamos {i}",
                f"Cocodrilos {i}",
                f"Serpientes {i}",
                f"Avestruz {i}",
            ],
        )

        dias_semana = fake.random_elements(
            elements=[0, 1, 2, 3, 4],
            length=fake.random_int(min=1, max=3),
            unique=True,
        )
        writer.writerow([i, nombre, sorted(dias_semana)])
