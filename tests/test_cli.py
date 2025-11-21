from typer.testing import CliRunner
from gitminer.cli import app
from git import Repo

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

def test_cli_invalid_repo():
    result = runner.invoke(app, ["analyze", "caminho/que/nao/existe"])

    output = (result.stdout or "") + (result.stderr or "")

    assert result.exit_code != 0
    assert (
        "Repositório inválido" in output
        or "Error" in output
        or "Invalid value" in output
    )


def test_cli_no_args_shows_help():
    result = runner.invoke(app, [])

    output = (result.stdout or "") + (result.stderr or "")

    assert "Usage" in output or "uso" in output.lower()

def test_cli_no_arguments():
    result = runner.invoke(app, ["analyze"])

    output = (result.stdout or "") + (result.stderr or "")

    assert result.exit_code != 0
    assert "Missing argument" in output or "Error" in output



