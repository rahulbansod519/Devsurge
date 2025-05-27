import os
import subprocess
from git import Repo
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def clone_repo(repo_url, clone_dir="cloned_repo"):
    if os.path.exists(clone_dir):
        subprocess.run(["rm", "-rf", clone_dir])
    Repo.clone_from(repo_url, clone_dir)
    console.print(f"[green]Cloned {repo_url} into {clone_dir}[/green]")
    return clone_dir

def analyze_python_files(clone_dir):
    table = Table(title="Python File Analysis")
    table.add_column("File", style="cyan")
    table.add_column("Size (KB)", justify="right")
    table.add_column("Lines", justify="right")
    table.add_column("Last Modified", justify="right")

    for path in Path(clone_dir).rglob("*.py"):
        size_kb = round(path.stat().st_size / 1024, 2)
        lines = sum(1 for _ in open(path))
        last_modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
        table.add_row(str(path), str(size_kb), str(lines), last_modified)

    console.print(table)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")
    repo_path = clone_repo(repo_url)
    analyze_python_files(repo_path)
