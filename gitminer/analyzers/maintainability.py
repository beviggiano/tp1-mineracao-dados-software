import ast
import math
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

class HalsteadMetricsVisitor(ast.NodeVisitor):
    """
    Um NodeVisitor para percorrer uma AST e coletar métricas de Halstead.
    """
    def __init__(self):
        self.operators = set()
        self.operands = set()
        self.total_operators = 0
        self.total_operands = 0

    def visit(self, node):
        # Mapeia tipos de nós AST para operadores
        # Esta lista pode ser expandida para ser mais precisa
        operator_nodes = (
            ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp,
            ast.Assign, ast.AugAssign, ast.Attribute, ast.Subscript,
            ast.Call, ast.keyword
        )
        if isinstance(node, operator_nodes):
            self.operators.add(type(node).__name__)
            self.total_operators += 1
        
        # Mapeia tipos de nós AST para operandos
        elif isinstance(node, (ast.Name, ast.Constant)):
            self.operands.add(str(node))
            self.total_operands += 1
        
        super().visit(node)

def calculate_halstead_volume(code: str) -> float:
    """Calcula o Volume Halstead para um trecho de código."""
    try:
        tree = ast.parse(code)
        visitor = HalsteadMetricsVisitor()
        visitor.visit(tree)

        n1 = len(visitor.operators)  # Número de operadores distintos
        n2 = len(visitor.operands)   # Número de operandos distintos
        N1 = visitor.total_operators # Número total de operadores
        N2 = visitor.total_operands  # Número total de operandos

        # Vocabulário e Comprimento do programa
        vocabulary = n1 + n2
        length = N1 + N2
        
        if vocabulary == 0:
            return 0.0

        # Volume Halstead
        volume = length * math.log2(vocabulary)
        return volume
    except (SyntaxError, ValueError):
        # Retorna 0 se o código não puder ser parseado
        return 0.0

def analyze_maintainability(repo_path: str, complexity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o Índice de Manutenibilidade para os arquivos Python em um repositório.

    Args:
        repo_path (str): O caminho para o repositório.
        complexity_df (pd.DataFrame): DataFrame da análise de complexidade do Lizard.

    Returns:
        pd.DataFrame com o Índice de Manutenibilidade por arquivo.
    """
    path = Path(repo_path)
    python_files = list(path.rglob("*.py"))

    if not python_files or complexity_df.empty:
        return pd.DataFrame()

    mi_data: List[Dict[str, Any]] = []

    for py_file in python_files:
        try:
            relative_path = str(py_file.relative_to(path)).replace('\\', '/')
            
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            lines_of_code = len([line for line in code.splitlines() if line.strip() and not line.strip().startswith('#')])
            if lines_of_code == 0:
                continue

            # Pega a complexidade ciclomática do DataFrame do Lizard
            complexity_row = complexity_df[complexity_df['file_path'] == relative_path]
            if complexity_row.empty:
                continue
            
            cyclomatic_complexity = complexity_row['total_complexity'].iloc[0]
            if cyclomatic_complexity == 0:
                # Evita divisão por zero ou log de zero, assume complexidade mínima de 1
                cyclomatic_complexity = 1


            # Calcula o Volume Halstead (nossa nova métrica)
            halstead_volume = calculate_halstead_volume(code)
            if halstead_volume <= 0: # Evita log de zero ou negativo
                continue

            # Calcula o Índice de Manutenibilidade
            # Usando logaritmo natural (ln) como na fórmula original
            mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * math.log(lines_of_code)
            
            # Normaliza para uma escala de 0 a 100
            mi_scaled = max(0, (mi * 100) / 171)

            mi_data.append({
                "file_path": relative_path,
                "maintainability_index": round(mi_scaled, 2),
                "halstead_volume": round(halstead_volume, 2)
            })
        except Exception:
            # Ignora arquivos que não podem ser lidos ou analisados
            continue
            
    return pd.DataFrame(mi_data)
