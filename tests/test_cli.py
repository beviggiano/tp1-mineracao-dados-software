from typer.testing import CliRunner
from gitminer.cli import app, _validate_repo_path
from git import Repo
from pathlib import Path
import pytest
import click

runner = CliRunner()


def test_cli_invalid_path():
    path = Path("caminho/invalido")
    result = runner.invoke(app, ["analyze", str(path)])
    assert result.exit_code != 0
    assert "não é um diretório válido" in result.stdout


def test_cli_not_a_git_repo(tmp_path):
    result = runner.invoke(app, ["analyze", str(tmp_path)])
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_cli_security_invalid_repo(tmp_path):
    result = runner.invoke(app, ["security", str(tmp_path)])
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_cli_export_invalid_repo(tmp_path):
    result = runner.invoke(app, ["export", str(tmp_path), "--output-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert "não é um repositório Git válido" in result.stdout


def test_validate_repo_path_invalid_directory():
    with pytest.raises(click.exceptions.Exit):
        _validate_repo_path(Path("/isso/nao/existe/mesmo"))


def test_validate_repo_path_not_git_repo(tmp_path):
    with pytest.raises(click.exceptions.Exit):
        _validate_repo_path(tmp_path)


def test_validate_repo_path_valid_repo(tmp_path):
    Repo.init(tmp_path)
    _validate_repo_path(tmp_path)


def test_cli_analyze_command(test_repo):
    result = runner.invoke(app, ["analyze", test_repo])
    assert result.exit_code == 0
    assert "Análise" in result.stdout or "Iniciando análise" in result.stdout


def test_cli_security_command(test_repo):
    result = runner.invoke(app, ["security", test_repo])
    assert result.exit_code == 0


def test_cli_export_command(test_repo, tmp_path):
    out = tmp_path / "out"
    result = runner.invoke(app, ["export", test_repo, "--output-dir", str(out)])
    assert result.exit_code == 0
    assert out.exists()


def test_cli_plot_command(test_repo, tmp_path):
    out = tmp_path / "plots"
    result = runner.invoke(app, ["plot", test_repo, "--output-dir", str(out)])
    assert result.exit_code == 0
    assert out.exists()
