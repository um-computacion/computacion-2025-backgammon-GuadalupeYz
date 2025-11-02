import os, re, shutil

root = "tests"
backup_dir = "backups_tests_guada"
os.makedirs(backup_dir, exist_ok=True)

print("🧩 Corrigiendo nombres de atributos en tests...")

# copia de seguridad de los tests
for filename in os.listdir(root):
    if filename.endswith(".py"):
        src = os.path.join(root, filename)
        dst = os.path.join(backup_dir, filename)
        shutil.copy2(src, dst)

# patrones de atributos antiguos
patron_privado = re.compile(r"(_[A-Za-z]+\_\_)([a-zA-Z_]+)(?!_)")
cambios = 0

for filename in os.listdir(root):
    if not filename.endswith(".py"):
        continue
    filepath = os.path.join(root, filename)
    with open(filepath, encoding="utf-8") as f:
        contenido = f.read()

    # convierte _Clase__atributo → _Clase__atributo__
    nuevo = patron_privado.sub(lambda m: f"{m.group(1)}{m.group(2)}__", contenido)

    if nuevo != contenido:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(nuevo)
        print(f"✅ Arreglado: {filename}")
        cambios += 1

print(f"\n🎯 Arreglo completado: {cambios} archivos modificados.")
print("💾 Backup en:", backup_dir)
