from typer.testing import CliRunner
from gitminer.cli import app, _validate_repo_path
from git import Repo
import pytest

runner = CliRunner()

# ---------------------------
# Testes Positivos dos Comandos
# ---------------------------

def test_cli_analyze_command(test_repo):
    """Testa o comando 'analyze'."""
    result = runner.invoke(app, ["analyze", test_repo])
    assert result.exit_code == 0
    assert "Análise concluída" in result.stdout
    assert "Top 5 Hotspots" in result.stdout
    assert "main.py" in result.stdout


def test_cli_security_command(test_repo):
    """Testa o comando 'security'."""
    result = runner.invoke(app, ["security", test_repo])
    assert result.exit_code == 0
    assert "Nenhum problema de segurança encontrado" in result.stdout


def test_cli_export_command(tmp_path, test_repo):
    """Testa o comando 'export'."""
    output_dir = tmp_path / "output"
    result = runner.invoke(app, ["export", test_repo, "--output-dir", str(output_dir)])
    
    assert result.exit_code == 0
    assert "Exportando dados" in result.stdout
    assert (output_dir / "commits_analysis.csv").exists()

def test_cli_invalid_repo():
    result = runner.invoke(
        app,
        ["analyze", "caminho/que/nao/existe"]
    )
    
    # Use .output which contains both stdout and stderr
    output = result.output
    
    print(f"DEBUG Output: '{output}'")
    print(f"DEBUG Exit code: {result.exit_code}")
    
    assert result.exit_code != 0
    assert (
        "Erro" in output 
        or "repositório" in output.lower()
        or "inválido" in output.lower()
        or "caminho" in output
        or "error" in output.lower()
        or "invalid" in output.lower()
    )

# ---------------------------
# Testes Negativos do CLI
# ---------------------------

def test_cli_invalid_path():
    """Deve falhar quando o caminho não existe."""
    result = runner.invoke(app, ["analyze", "caminho/invalido"])
    
    assert result.exit_code != 0
    assert "não é um diretório válido" in result.stdout


def test_cli_not_a_git_repo(tmp_path):
    """Deve falhar quando o diretório existe mas não é um repositório Git."""
    result = runner.invoke(app, ["analyze", str(tmp_path)])
    
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_cli_security_invalid_repo(tmp_path):
    """Security deve falhar com diretório não-git."""
    result = runner.invoke(app, ["security", str(tmp_path)])
    
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_cli_export_invalid_repo(tmp_path):
    """Export deve falhar com diretório não-git."""
    result = runner.invoke(app, ["export", str(tmp_path), "--output-dir", str(tmp_path)])
    
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_cli_plot_invalid_metric(test_repo, tmp_path):
    """Plot deve falhar com métrica não suportada."""
    result = runner.invoke(app, [
        "plot",
        test_repo,
        "--metric", "banana",
        "--output-dir", str(tmp_path)
    ])
    
    assert result.exit_code != 0
    assert "Métrica 'banana' não suportada" in result.stdout


def test_cli_no_args_shows_help():
    result = runner.invoke(app, ["--help"])
    
    output = result.stdout
    
    print(f"DEBUG Help Output: '{output}'")
    
    help_indicators = ["Usage", "usage", "Commands", "Options", "Comandos", "Opções", "help", "ajuda"]
    assert any(indicator.lower() in output.lower() for indicator in help_indicators)

def test_cli_no_arguments():
    result = runner.invoke(app, ["analyze"])
    
    output = result.output
    
    print(f"DEBUG No Args Output: '{output}'")
    print(f"DEBUG No Args Exit code: {result.exit_code}")
    
    assert result.exit_code != 0
    assert any(phrase in output.lower() for phrase in [
        "missing argument", 
        "error", 
        "required",
        "faltando",
        "argumento",
        "missing",
        "argument"
    ])
