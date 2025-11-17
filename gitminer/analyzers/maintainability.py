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
