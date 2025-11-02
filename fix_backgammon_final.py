import os, re, shutil

# Carpetas a corregir
carpetas = ["codigo", "cli", "tests"]
backup_dir = "backups_fix_final"
os.makedirs(backup_dir, exist_ok=True)

print("🧩 Corrigiendo nombres internos en código y tests...\n")

# --- Crear backup completo ---
for carpeta in carpetas:
    if not os.path.exists(carpeta):
        continue
    dst = os.path.join(backup_dir, carpeta)
    shutil.copytree(carpeta, dst, dirs_exist_ok=True)

# --- Patrones ---
# Atributos internos: _Clase__atributo  →  _Clase__atributo__
patron_interno = re.compile(r"(_[A-Za-z]+\_\_)([a-zA-Z_]+)(?!_)")
# self.__atributo → self.__atributo__
patron_self = re.compile(r"(self\.\_\_)([a-zA-Z_]+)(?!_)")

archivos_modificados = 0
cambios_totales = 0

# --- Aplicar cambios ---
for carpeta in carpetas:
    for root, _, files in os.walk(carpeta):
        for file in files:
            if not file.endswith(".py"):
                continue
            ruta = os.path.join(root, file)
            with open(ruta, encoding="utf-8") as f:
                texto = f.read()
            nuevo = patron_interno.sub(lambda m: f"{m.group(1)}{m.group(2)}__", texto)
            nuevo = patron_self.sub(lambda m: f"{m.group(1)}{m.group(2)}__", nuevo)
            if nuevo != texto:
                archivos_modificados += 1
                cambios_totales += texto.count("__") - nuevo.count("__")  # estimativo
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(nuevo)
                print(f"✅ Corregido: {ruta}")

print(f"\n🎯 Arreglo completado: {archivos_modificados} archivos actualizados.")
print("💾 Backup guardado en:", backup_dir)
print("Ahora corré:")
print("   python3 -m unittest")
