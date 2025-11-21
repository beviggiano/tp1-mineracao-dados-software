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
