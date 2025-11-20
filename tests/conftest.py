import pytest
from git import Repo
from pathlib import Path

@pytest.fixture(scope="session")
def test_repo(tmp_path_factory):
    """Cria um repositório Git temporário para os testes."""
    repo_dir = tmp_path_factory.mktemp("test_repo")
    repo = Repo.init(repo_dir)

    # Criação do primeiro commit
    (repo_dir / "main.py").write_text("def hello():\n    print('hello')\n", encoding='utf-8')
    repo.index.add(["main.py"])
    repo.index.commit("Initial commit")

    # Criação do segundo commit com alterações
    (repo_dir / "main.py").write_text("def hello():\n    # A simple function\n    print('hello world')\n", encoding='utf-8')
    (repo_dir / "utils.py").write_text("def utility_func():\n    pass\n", encoding='utf-8')
    repo.index.add(["main.py", "utils.py"])
    repo.index.commit("Add feature and utility")

    return str(repo_dir)