import os
import subprocess
from git import Repo
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table

from collections import defaultdict
# DevSurge: A Python GitHub Repo Analyzer
# This script clones a GitHub repository, analyzes Python files, and generates a heatmap of git activity.

console = Console()

def clone_repo(repo_url, clone_dir="cloned_repo"):
    """
    Clone a GitHub repository to a specified directory.
    :param repo_url: URL of the GitHub repository to clone
    :param clone_dir: Directory where the repository will be cloned
    :return: Path to the cloned repository
    """
    
    if os.path.exists(clone_dir):
        subprocess.run(["rm", "-rf", clone_dir])
    Repo.clone_from(repo_url, clone_dir)
    console.print(f"[green]Cloned {repo_url} into {clone_dir}[/green]")
    return clone_dir

def analyze_python_files(clone_dir):
    """
    Analyze Python files in the cloned repository and generate a summary table.
    :param clone_dir: Directory where the repository is cloned
    """
    if not os.path.exists(clone_dir):
        console.print(f"[red]Directory {clone_dir} does not exist. Please clone a repository first.[/red]")
        return
    console.print(f"[blue]Analyzing Python files in {clone_dir}...[/blue]")
    # Create a table to display Python file analysis
    console.clear()
    console.print(f"[blue]Generating Python file analysis table...[/blue]")     
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

def analyze_git_activity(clone_dir):
    repo = Repo(clone_dir)
    file_stats = defaultdict(lambda: {"commits": 0, "authors": set(), "last_commit": None})

    for commit in repo.iter_commits(paths=".", max_count=500):
        for file in commit.stats.files:
            if file.endswith(".py"):
                file_stats[file]["commits"] += 1
                file_stats[file]["authors"].add(commit.author.email)
                if not file_stats[file]["last_commit"]:
                    file_stats[file]["last_commit"] = datetime.fromtimestamp(commit.committed_date).strftime("%Y-%m-%d")

    table = Table(title="🔥 DevSurge Git Activity Heatmap")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Commits", justify="right")
    table.add_column("Contributors", justify="right")
    table.add_column("Last Commit", justify="right")
    table.add_column("🔥 Volatility Score", justify="right", style="red")

    for file, stats in sorted(file_stats.items(), key=lambda x: x[1]["commits"] * len(x[1]["authors"]), reverse=True):
        score = stats["commits"] * len(stats["authors"])
        table.add_row(file, str(stats["commits"]), str(len(stats["authors"])), stats["last_commit"], str(score))

    console.print(table)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")
    repo_path = clone_repo(repo_url)
    analyze_python_files(repo_path)
    analyze_git_activity(repo_path)