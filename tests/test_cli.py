from typer.testing import CliRunner
from gitminer.cli import app, _validate_repo_path
from git import Repo
from pathlib import Path
import pytest

runner = CliRunner()


def test_cli_invalid_path():
    """Deve falhar quando o caminho não existe."""
    path = Path("caminho/invalido")
    result = runner.invoke(app, ["analyze", str(path)], mix_stderr=False)
    assert result.exit_code != 0
    assert f"O caminho '{path}' não é um diretório válido" in result.stderr


def test_cli_not_a_git_repo(tmp_path):
    """Deve falhar quando o diretório existe mas não é um repositório Git."""
    result = runner.invoke(app, ["analyze", str(tmp_path)], mix_stderr=False)
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_cli_security_invalid_repo(tmp_path):
    """Security deve falhar com diretório não-git."""
    result = runner.invoke(app, ["security", str(tmp_path)], mix_stderr=False)
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_cli_export_invalid_repo(tmp_path):
    """Export deve falhar com diretório não-git."""
    result = runner.invoke(app, ["export", str(tmp_path), "--output-dir", str(tmp_path)], mix_stderr=False)
    assert result.exit_code != 0
    assert f"O diretório '{tmp_path}' não é um repositório Git válido" in result.stderr


def test_validate_repo_path_invalid_directory():
    """Deve lançar erro quando o caminho não é diretório."""
    with pytest.raises(SystemExit):
        _validate_repo_path(Path("nao_existe"))


def test_validate_repo_path_not_git_repo(tmp_path):
    """Deve falhar quando o diretório não é Git."""
    with pytest.raises(SystemExit):
        _validate_repo_path(tmp_path)


def test_validate_repo_path_valid_repo(tmp_path):
    """Deve aceitar um repositório git válido."""
    Repo.init(tmp_path)
    _validate_repo_path(tmp_path)


def test_cli_analyze_command(test_repo):
    """Testa o comando 'analyze'."""
    result = runner.invoke(app, ["analyze", test_repo])
    assert result.exit_code == 0
    assert "Análise concluída" in result.stdout or "🚀 Iniciando análise completa" in result.stdout


def test_cli_security_command(test_repo):
    """Testa o comando de segurança."""
    result = runner.invoke(app, ["security", test_repo])
    assert result.exit_code == 0


def test_cli_export_command(test_repo, tmp_path):
    """Testa a exportação."""
    output = tmp_path / "out"
    result = runner.invoke(app, ["export", test_repo, "--output-dir", str(output)])
    assert result.exit_code == 0
    assert output.exists()


def test_cli_plot_command(test_repo, tmp_path):
    """Testa a geração de gráficos."""
    output = tmp_path / "plots"
    result = runner.invoke(app, ["plot", test_repo, "--output-dir", str(output)])
    assert result.exit_code == 0
    assert output.exists()
