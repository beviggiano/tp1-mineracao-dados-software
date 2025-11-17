import pandas as pd
from pydriller import Repository
from typing import Dict, List, Any
from collections import defaultdict

def analyze_commits(repo_path: str) -> pd.DataFrame:
    """
    Analisa o histórico de commits de um repositório para calcular o churn.

    Args:
        repo_path (str): O caminho para o repositório Git local.

    Returns:
        pd.DataFrame: DataFrame com dados de churn por arquivo.
                      Colunas: ['file_path', 'churn'].
    """
    churn_by_file: Dict[str, int] = defaultdict(int)

    try:
        repo = Repository(repo_path)
        for commit in repo.traverse_commits():
            for modification in commit.modified_files:
                # Pydriller pode retornar None para path
                if modification.new_path:
                    churn = modification.added_lines + modification.deleted_lines
                    churn_by_file[modification.new_path] += churn
    except Exception as e:
        print(f"Aviso: Não foi possível analisar os commits. Erro: {e}")
        return pd.DataFrame(columns=['file_path', 'churn'])

    if not churn_by_file:
        return pd.DataFrame(columns=['file_path', 'churn'])

    data: List[Dict[str, Any]] = [
        {"file_path": path, "churn": churn}
        for path, churn in churn_by_file.items()
    ]

    df = pd.DataFrame(data)
    return df
