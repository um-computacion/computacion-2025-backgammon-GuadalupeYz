import os
import re
import shutil

# === CONFIGURACIÓN ===
CARPETAS = ["codigo", "cli", "pygame_ui"]  # podés agregar más si querés
BACKUP_DIR = "backups_backgammon"

# === CREAR BACKUP ===
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

print(f"\n🧰 Creando backup en '{BACKUP_DIR}' antes de hacer cambios...\n")

for carpeta in CARPETAS:
    if os.path.exists(carpeta):
        shutil.copytree(carpeta, os.path.join(BACKUP_DIR, carpeta), dirs_exist_ok=True)

# === EXPRESIÓN REGULAR: busca self.__atributo (sin __ final) ===
patron = re.compile(r"(self\.__[a-zA-Z_][a-zA-Z0-9_]*)(?!_)")

# === PROCESAR ARCHIVOS .py ===
for carpeta in CARPETAS:
    for root, _, files in os.walk(carpeta):
        for file in files:
            if file.endswith(".py"):
                ruta = os.path.join(root, file)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()

                # aplicar reemplazo
                nuevo_contenido = patron.sub(lambda m: m.group(1) + "__", contenido)

                if nuevo_contenido != contenido:
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(nuevo_contenido)
                    print(f"✅ Modificado: {ruta}")

print("\n🎯 Refactor finalizado con éxito.")
print("💾 Todos los archivos originales están en la carpeta 'backups_backgammon/'.")
