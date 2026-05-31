import os
import sys
import subprocess
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def clonar_repo(url):
    repo_name = url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", url, repo_name], check=True)
    return repo_name

def analizar_vulnerabilidades(codigo, archivo):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Analizá este código buscando vulnerabilidades de seguridad.
Buscá: SQL injection, hardcoded secrets, race conditions, command injection, path traversal.
Si encontrás algo, indicá: vulnerabilidad, severidad (CRITICAL/HIGH/MEDIUM/LOW) y línea aproximada.
Si no hay nada, respondé solo: CLEAN

Archivo: {archivo}
Código:
{codigo}"""
        }]
    )
    return response.choices[0].message.content

def escanear_repo(path):
    reporte = []
    archivos = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".go")):
                archivos.append(os.path.join(root, file))

    print(f"🔍 Escaneando {len(archivos)} archivos...\n")

    for archivo in archivos:
        with open(archivo, "r", errors="ignore") as f:
            codigo = f.read()
        
        if len(codigo.strip()) < 50:
            continue

        resultado = analizar_vulnerabilidades(codigo, archivo)
        
        if "CLEAN" not in resultado:
            print(f"⚠️  {archivo}")
            print(resultado)
            reporte.append(f"## {archivo}\n{resultado}\n")
            print("-" * 50)

    return reporte

url = sys.argv[1] if len(sys.argv) > 1 else input("URL del repo: ")
print(f"📥 Clonando {url}...\n")
repo = clonar_repo(url)
reporte = escanear_repo(repo)

with open("reporte.md", "w") as f:
    f.write("# Bug Bounty Report\n\n")
    f.writelines(reporte)

print(f"\n✅ Reporte generado en reporte.md")
