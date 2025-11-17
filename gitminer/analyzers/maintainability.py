# Arquivo: gitminer-cli/gitminer/analyzers/maintainability.py

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
