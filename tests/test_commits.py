import pandas as pd
from gitminer.analyzers.commits import analyze_commits
import os

def test_analyze_commits(test_repo):
    """Testa se a análise de churn funciona corretamente."""
    df = analyze_commits(test_repo)
    
    assert not df.empty
    assert "file_path" in df.columns
    assert "churn" in df.columns
    
    # Normaliza o caminho do arquivo para ser independente do SO
    main_py_path = os.path.join('', 'main.py').replace('\\', '/')
    utils_py_path = os.path.join('', 'utils.py').replace('\\', '/')
    
    # Verifica o churn do 'main.py'
    # Commit 1: 2 linhas add
    # Commit 2: 2 linhas add, 1 del
    # Total churn = 2 + 3 = 5
    main_py_churn = df[df["file_path"] == main_py_path]["churn"].iloc[0]
    assert main_py_churn == 5

    # Verifica o churn do 'utils.py'
    # Commit 2: 2 linhas add
    utils_py_churn = df[df["file_path"] == utils_py_path]["churn"].iloc[0]
    assert utils_py_churn == 2