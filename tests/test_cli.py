from typer.testing import CliRunner
from gitminer.cli import app, _validate_repo_path
from git import Repo
import pytest

runner = CliRunner()

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
    Repo.init(tmp_path)   # cria repo git vazio

    # Não deve lançar erro
    _validate_repo_path(tmp_path)