import lizard
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

def analyze_complexity(repo_path: str) -> pd.DataFrame:
    """
    Analisa a complexidade ciclomática dos arquivos de código em um repositório.

    Args:
        repo_path (str): O caminho para o repositório Git.

    Returns:
        pd.DataFrame: DataFrame com a complexidade agregada por arquivo.
                      Colunas: ['file_path', 'total_complexity'].
    """
    path = Path(repo_path)
    supported_extensions = [
        ".c", ".cpp", ".cc", ".h", ".hpp",
        ".java", ".js", ".jsx", ".ts", ".tsx",
        ".py", ".go", ".rb", ".php", ".swift",
        ".kt", ".scala", ".rs"
    ]

    files_to_analyze = [
        str(p) for p in path.rglob("*")
        if p.is_file() and p.suffix in supported_extensions
    ]
    
    if not files_to_analyze:
        return pd.DataFrame(columns=['file_path', 'total_complexity'])

    analysis_results = lizard.analyze(files_to_analyze)

    complexity_by_file: Dict[str, int] = {}
    for file_info in analysis_results:
        try:
            relative_path = str(Path(file_info.filename).relative_to(path))
            total_ccn = sum(func.cyclomatic_complexity for func in file_info.function_list)
            complexity_by_file[relative_path] = total_ccn
        except ValueError:
            # Ignora arquivos que não estão no caminho do repositório (raro)
            continue

    data: List[Dict[str, Any]] = [
        {"file_path": path, "total_complexity": complexity}
        for path, complexity in complexity_by_file.items()
    ]
    
    df = pd.DataFrame(data)
    return df
