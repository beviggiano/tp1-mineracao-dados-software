# Arquivo: gitminer-cli/gitminer/cli.py

import typer
from pathlib import Path
import git
from typing_extensions import Annotated

from gitminer.analyzers import commits, complexity, hotspots, security as security_analyzer, maintainability
from gitminer.reports import exporter, plots, summary

app = typer.Typer(help="GitMiner: Uma ferramenta CLI para mineração de repositórios Git.")

def _validate_repo_path(repo_path: Path) -> None:
    """Verifica se o caminho é um repositório Git válido."""
    if not repo_path.is_dir():
        print(f"❌ Erro: O caminho '{repo_path}' não é um diretório válido.")
        raise typer.Exit(code=1)
    try:
        _ = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        print(f"❌ Erro: O diretório '{repo_path}' não é um repositório Git válido.")
        raise typer.Exit(code=1)

@app.command()
def analyze(
    repo_path: Annotated[Path, typer.Argument(exists=True, file_okay=False, help="Caminho para o repositório Git local.")]
):
    """Roda todas as análises e exibe um relatório resumido."""
    _validate_repo_path(repo_path)
    print(f"🚀 Iniciando análise completa para: {repo_path}")
    
    with typer.progressbar(length=4, label="Analisando") as progress:
        commits_df = commits.analyze_commits(str(repo_path))
        progress.update(1)
        
        complexity_df = complexity.analyze_complexity(str(repo_path))
        progress.update(1)
        
        hotspots_df = hotspots.find_hotspots(commits_df, complexity_df)
        progress.update(1)

        maintainability_df = maintainability.analyze_maintainability(str(repo_path), complexity_df)
        progress.update(1)
        
    summary.print_summary_report(hotspots_df, complexity_df, commits_df, maintainability_df)

@app.command()
def security(
    repo_path: Annotated[Path, typer.Argument(exists=True, file_okay=False, help="Caminho para o repositório Git local.")]
):
    """Roda a análise de segurança com o Bandit."""
    _validate_repo_path(repo_path)
    issues = security_analyzer.analyze_security(str(repo_path))
    summary.print_security_report(issues)

@app.command()
def export(
    repo_path: Annotated[Path, typer.Argument(exists=True, file_okay=False, help="Caminho para o repositório Git local.")],
    format: Annotated[str, typer.Option("--format", help="Formato de saída: 'csv' ou 'json'.")] = "csv",
    output_dir: Annotated[Path, typer.Option("--output-dir", help="Diretório para salvar os resultados.")] = Path("results"),
):
    """Exporta os resultados da análise para CSV ou JSON."""
    _validate_repo_path(repo_path)
    print(f"📦 Exportando dados para o formato '{format}' no diretório '{output_dir}'...")

    commits_df = commits.analyze_commits(str(repo_path))
    complexity_df = complexity.analyze_complexity(str(repo_path))
    hotspots_df = hotspots.find_hotspots(commits_df, complexity_df)
    maintainability_df = maintainability.analyze_maintainability(str(repo_path), complexity_df)

    if not commits_df.empty:
        exporter.export_data(commits_df, format, output_dir, "commits_analysis")
    if not complexity_df.empty:
        exporter.export_data(complexity_df, format, output_dir, "complexity_analysis")
    if not hotspots_df.empty:
        exporter.export_data(hotspots_df, format, output_dir, "hotspots_analysis")
    if not maintainability_df.empty:
        exporter.export_data(maintainability_df, format, output_dir, "maintainability_analysis")

@app.command()
def plot(
    repo_path: Annotated[Path, typer.Argument(exists=True, file_okay=False, help="Caminho para o repositório Git local.")],
    metric: Annotated[str, typer.Option("--metric", help="Métrica para plotar: 'complexity', 'churn', 'hotspots', ou 'maintainability'.")] = "hotspots",
    output_dir: Annotated[Path, typer.Option("--output-dir", help="Diretório para salvar os gráficos.")] = Path("plots"),
):
    """Gera gráficos para as métricas de análise."""
    _validate_repo_path(repo_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📊 Gerando gráfico para a métrica '{metric}'...")
    
    commits_df = commits.analyze_commits(str(repo_path))
    complexity_df = complexity.analyze_complexity(str(repo_path))

    if metric == "hotspots":
        hotspots_df = hotspots.find_hotspots(commits_df, complexity_df)
        plots.plot_hotspots(hotspots_df, output_dir)
    elif metric == "complexity":
        plots.plot_complexity(complexity_df, output_dir)
    elif metric == "churn":
        plots.plot_churn(commits_df, output_dir)
    elif metric == "maintainability":
        maintainability_df = maintainability.analyze_maintainability(str(repo_path), complexity_df)
        plots.plot_maintainability(maintainability_df, output_dir)
    else:
        print(f"❌ Erro: Métrica '{metric}' não suportada.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()