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

# ---------------------------
# Testes Diretos do Validador
# ---------------------------

def test_validate_repo_path_invalid_directory(tmp_path):
    """Deve falhar quando o caminho não é diretório."""
    fake_path = tmp_path / "nao_existe"
    with pytest.raises(SystemExit):
        _validate_repo_path(fake_path)


def test_validate_repo_path_not_git_repo(tmp_path):
    """Deve falhar quando o diretório existe mas não é repositório Git."""
    with pytest.raises(SystemExit):
        _validate_repo_path(tmp_path)


def test_validate_repo_path_valid_repo(tmp_path):
    """Deve passar quando o diretório é um repositório Git válido."""
    Repo.init(tmp_path)
    _validate_repo_path(tmp_path)
