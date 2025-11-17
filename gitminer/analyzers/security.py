import sys
from io import StringIO
from typing import List, Dict, Any
from bandit.core import config, manager

def analyze_security(repo_path: str) -> List[Dict[str, Any]]:
    """
    Executa a análise de segurança do Bandit em um diretório.

    Args:
        repo_path (str): O caminho para o repositório.

    Returns:
        List[Dict[str, Any]]: Uma lista de dicionários, cada um representando uma vulnerabilidade.
    """
    # Usar 'capture_output' é uma forma mais limpa de lidar com a saída do Bandit
    b_conf = config.BanditConfig()
    b_mgr = manager.BanditManager(b_conf, "custom", quiet=True)
    
    # Redireciona a saída para evitar que o Bandit imprima diretamente no console
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        b_mgr.discover_files([repo_path], recursive=True)
        b_mgr.run_tests()
    finally:
        sys.stdout = original_stdout # Restaura a saída padrão

    results: List[Dict[str, Any]] = []
    for issue in b_mgr.get_issue_list():
        results.append({
            "test_id": issue.test_id,
            "test_name": issue.test,
            "severity": issue.severity,
            "confidence": issue.confidence,
            "filename": issue.fname,
            "line_number": issue.lineno,
            "issue_text": issue.text,
        })
    return results
