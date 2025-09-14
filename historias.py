import click
import requests
import json
from datetime import datetime
from pathlib import Path

def generate_with_ollama(prompt: str, ollama_url: str, model: str) -> str:
    """Envía un prompt al modelo de Ollama y devuelve la respuesta generada."""
    response = requests.post(
        ollama_url,
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()


@click.command()
@click.option("--rol", prompt="¿Quién es el usuario? (Como...)", help="Ej: administrador, cliente, etc.")
@click.option("--funcionalidad", prompt="¿Qué desea hacer? (Quiero...)", help="La acción que el usuario quiere realizar.")
@click.option("--beneficio", prompt="¿Para qué lo quiere? (Para...)", help="El beneficio esperado.")
@click.option("--output", type=click.Choice(["console", "markdown", "json"]), default="markdown",
              show_default=True, help="Formato de salida en consola (console, markdown o json).")
@click.option("--save", is_flag=True, help="Guardar también el resultado en archivo.")
@click.option("--outdir", default="historias", help="Directorio donde guardar archivos si se usa --save.")
@click.option("--ollama-url", default="http://localhost:11434/api/generate", show_default=True, help="URL de la API de Ollama.")
@click.option("--model", default="llama3.1", show_default=True, help="Modelo de Ollama a utilizar.")
def generar_historia(rol, funcionalidad, beneficio, output, save, outdir, ollama_url, model):
    """Genera una historia de usuario enriquecida con ayuda de un modelo LLM (en Ollama)."""

    historia_base = f"Como {rol}, quiero {funcionalidad}, para {beneficio}."

    prompt = f"""
Genera una historia de usuario siguiendo metodologías ágiles a partir de la siguiente base:

{historia_base}

Responde en formato **JSON válido** con la siguiente estructura exacta:

{{
  "historia": "Como..., quiero..., para...",
  "notas_tecnicas": [
    "nota 1",
    "nota 2"
  ],
  "criterios_aceptacion": [
    "criterio 1",
    "criterio 2",
    "criterio 3"
  ]
}}

Asegúrate de devolver solo el JSON y que sea válido.
"""

    resultado = generate_with_ollama(prompt, ollama_url, model)

    try:
        data = json.loads(resultado)
    except json.JSONDecodeError:
        click.echo("⚠️ El modelo no devolvió un JSON válido. Respuesta cruda:")
        click.echo(resultado)
        return

    # 📌 Mostrar en consola según formato elegido
    if output == "console":
        click.echo("\n📌 Historia de Usuario Generada:\n")
        click.echo(f"Historia: {data['historia']}\n")
        click.echo("➡ Notas Técnicas")
        for nota in data["notas_tecnicas"]:
            click.echo(f"- {nota}")
        click.echo("\n➡ Criterios de Aceptación")
        for criterio in data["criterios_aceptacion"]:
            click.echo(f"- {criterio}")

    elif output == "markdown":
        md_output = "# Historia de Usuario\n\n"
        md_output += f"**Historia**: {data['historia']}\n\n"
        md_output += "## Notas Técnicas\n"
        for nota in data["notas_tecnicas"]:
            md_output += f"- {nota}\n"
        md_output += "\n## Criterios de Aceptación\n"
        for criterio in data["criterios_aceptacion"]:
            md_output += f"- {criterio}\n"
        click.echo(md_output)

    elif output == "json":
        json_output = json.dumps(data, indent=4, ensure_ascii=False)
        click.echo(json_output)

    # 📌 Guardar archivo solo si se pide explícitamente
    if save:
        Path(outdir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output == "markdown":
            filename = Path(outdir) / f"historia_{timestamp}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(md_output)
            click.echo(f"\n✅ Historia guardada en: {filename}")

        elif output == "json":
            filename = Path(outdir) / f"historia_{timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(json_output)
            click.echo(f"\n✅ Historia guardada en: {filename}")

        else:  # console → guardar como .txt
            filename = Path(outdir) / f"historia_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(data["historia"] + "\n\n")
                f.write("## Notas Técnicas\n")
                for nota in data["notas_tecnicas"]:
                    f.write(f"- {nota}\n")
                f.write("\n## Criterios de Aceptación\n")
                for criterio in data["criterios_aceptacion"]:
                    f.write(f"- {criterio}\n")
            click.echo(f"\n✅ Historia guardada en: {filename}")


if __name__ == "__main__":
    generar_historia()
