import spacy
import os
import argparse
import spacy.util
import sys
from rich import print
from rich.tree import Tree
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()


def analyze_text(nlp, text, filename):
  console.print(Panel(f"📄 Analizando archivo: [bold]{filename}[/bold]", style="magenta"))

  doc = nlp(text)

  # Tabla de Tokens y POS
  table = Table(title="Tokens y Part-of-Speech", show_lines=True)
  table.add_column("Token", style="cyan")
  table.add_column("Lemma", style="red")
  table.add_column("POS (Part-of-Speech)", style="green")
  table.add_column("Dep (Dependency)", style="yellow")
  table.add_column("Head", style="magenta")
  table.add_column("Shape", style="blue")
  table.add_column("Alpha", style="red")
  table.add_column("Stop", style="green")

  for token in doc:
    table.add_row(
      token.text,
      token.lemma_, 
      token.pos_, 
      token.dep_, 
      token.head.text, 
      token.shape_, 
      str(token.is_alpha), 
      str(token.is_stop)
    )
  console.print(table)

  # Árbol de dependencias con Rich
  roots = [token for token in doc if token.head == token]
  if roots:
    console.print("\n[cyan]Árbol sintáctico (dependencias):[/cyan]")
    for root in roots:
        tree = build_dependency_tree(root)
        console.print(tree)

  # Entidades
  console.print("\n[green]Entidades reconocidas:[/green]")
  if doc.ents:
    for ent in doc.ents:
      console.print(f"[bold cyan]{ent.text}[/bold cyan] → [yellow]{ent.label_}[/yellow]")
  else:
    console.print("[dim]Ninguna entidad reconocida.[/dim]")

  console.print("\n[bold green]✅ Análisis completado.[/bold green]\n")


def build_dependency_tree(token):
  """Construye un árbol Rich de dependencias recursivo."""
  node_label = f"[cyan]{token.text}[/cyan] ([yellow]{token.dep_}[/yellow])"
  tree = Tree(node_label)
  for child in token.children:
    tree.add(build_dependency_tree(child))
  return tree


def list_models(installed_models):
  print("\n[bold magenta]Modelos spaCy instalados:[/bold magenta]")
  table = Table(show_lines=True)
  table.add_column("Nombre del modelo", style="cyan")
  for m in installed_models:
    table.add_row(m)
  console.print(table)


def main():
  parser = argparse.ArgumentParser(
    description="Analiza archivos .txt o .c con spaCy.",
    formatter_class=argparse.RawTextHelpFormatter
  )

  parser.add_argument("--model", type=str, help="Modelo spaCy a usar (debe estar instalado)")
  parser.add_argument("--folder", type=str, default="samples", help="Carpeta donde buscar archivos")
  parser.add_argument("--list-models", action="store_true", help="Lista los modelos spaCy instalados")

  args = parser.parse_args()
  installed_models = spacy.util.get_installed_models()

  # Listar modelos
  if args.list_models:
    list_models(installed_models)
    sys.exit(0)

  # Validación: --model obligatorio
  if not args.model:
    console.print("[red]El argumento --model es obligatorio si no usas --list-models[/red]")
    parser.print_help()
    sys.exit(1)

  # Verificar que el modelo esté instalado
  if args.model not in installed_models:
    console.print(f"[red]Error: modelo '{args.model}' no está instalado.[/red]")
    list_models(installed_models)
    console.print(f"[yellow]Puedes instalarlo con: python -m spacy download {args.model}[/yellow]")
    sys.exit(1)

  console.print(f"[green]Usando modelo spaCy: {args.model}[/green]")
  nlp = spacy.load(args.model)

  # Recorrer archivos
  for root, _, files in os.walk(args.folder):
    for filename in files:
      if filename.endswith((".txt", ".c")):
        filepath = os.path.join(root, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
          content = f.read()
        analyze_text(nlp, content, filepath)


if __name__ == "__main__":
    main()
