from typer.testing import CliRunner
from gitminer.cli import app, _validate_repo_path
from git import Repo
import typer
import pytest
from pathlib import Path

runner = CliRunner()

# ---------------------------
# Testes Positivos
# ---------------------------

def test_cli_analyze_command(test_repo):
    result = runner.invoke(app, ["analyze", test_repo])
    assert result.exit_code == 0
    assert "Iniciando análise completa" in result.stdout
    assert "Top 5 Hotspots" in result.stdout
    assert "main.py" in result.stdout


def test_cli_security_command(test_repo):
    result = runner.invoke(app, ["security", test_repo])
    assert result.exit_code == 0
    assert "Nenhum problema de segurança encontrado" in result.stdout


def test_cli_export_command(tmp_path, test_repo):
    output_dir = tmp_path / "output"
    result = runner.invoke(app, ["export", test_repo, "--output-dir", str(output_dir)])
    assert result.exit_code == 0
    assert "Exportando dados" in result.stdout
    assert (output_dir / "commits_analysis.csv").exists()


# ---------------------------
# Testes Negativos
# ---------------------------

def test_cli_invalid_path():
    path = Path("caminho/invalido")
    result = runner.invoke(app, ["analyze", str(path)])
    assert result.exit_code != 0
    assert f"O caminho '{path}' não é um diretório válido" in result.stderr


def test_cli_not_a_git_repo(tmp_path):
    result = runner.invoke(app, ["analyze", str(tmp_path)])
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_cli_security_invalid_repo(tmp_path):
    result = runner.invoke(app, ["security", str(tmp_path)])
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_cli_export_invalid_repo(tmp_path):
    result = runner.invoke(app, ["export", str(tmp_path), "--output-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_cli_plot_invalid_metric(test_repo, tmp_path):
    result = runner.invoke(app, [
        "plot",
        test_repo,
        "--metric", "banana",
        "--output-dir", str(tmp_path)
    ])
    
    assert result.exit_code != 0
    assert "Métrica 'banana' não suportada" in result.stdout or result.stderr


# ---------------------------
# Testes Diretos do validador
# ---------------------------

def test_validate_repo_path_invalid_directory(tmp_path):
    fake = tmp_path / "nao_existe"
    with pytest.raises(typer.Exit):
        _validate_repo_path(fake)


def test_validate_repo_path_not_git_repo(tmp_path):
    with pytest.raises(typer.Exit):
        _validate_repo_path(tmp_path)


def test_validate_repo_path_valid_repo(tmp_path):
    Repo.init(tmp_path)
    _validate_repo_path(tmp_path)
