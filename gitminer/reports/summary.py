# Arquivo: gitminer-cli/gitminer/reports/summary.py

import pandas as pd
from typing import List, Dict, Any

def print_summary_report(hotspots_df: pd.DataFrame, complexity_df: pd.DataFrame, commits_df: pd.DataFrame, maintainability_df: pd.DataFrame):
    """Exibe um relatório resumido no terminal."""
    print("\n✅ Análise concluída.")
    
    print("\n📊 Resumo do Repositório")
    print("------------------------")
    print(f"Total de Arquivos com Churn: {len(commits_df)}")
    print(f"Total de Arquivos com Complexidade Analisada: {len(complexity_df)}")
    
    if not hotspots_df.empty:
        print("\n🔥 Top 5 Hotspots (Complexidade vs. Churn)")
        print("--------------------------------------------")
        print(hotspots_df[['file_path', 'total_complexity', 'churn', 'hotspot_score']].head(5).to_string(index=False))

    if not complexity_df.empty:
        print("\n🧠 Top 5 Arquivos por Complexidade Ciclomática")
        print("-------------------------------------------------")
        print(complexity_df.nlargest(5, 'total_complexity')[['file_path', 'total_complexity']].to_string(index=False))

    if not commits_df.empty:
        print("\n📈 Top 5 Arquivos por Churn (Linhas Alteradas)")
        print("------------------------------------------------")
        print(commits_df.nlargest(5, 'churn')[['file_path', 'churn']].to_string(index=False))
    
    if not maintainability_df.empty:
        print("\n📉 Top 5 Arquivos com Menor Índice de Manutenibilidade (Pior para Manter)")
        print("----------------------------------------------------------------------")
        print(maintainability_df.nsmallest(5, 'maintainability_index').to_string(index=False))


def print_security_report(issues: List[Dict[str, Any]]):
    """Exibe o relatório de segurança do Bandit no terminal."""
    print("\n🔒 Executando análise de segurança com Bandit...")
    
    if not issues:
        print("\n✅ Nenhum problema de segurança encontrado.")
        return

    print("\n[!] Problemas de segurança encontrados:")
    for issue in issues:
        print(f"\n- [{issue['test_id']}] {issue['issue_text']}")
        print(f"  - Severidade: {issue['severity']}")
        print(f"  - Confiança: {issue['confidence']}")
        print(f"  - Arquivo: {issue['filename']}")
        print(f"  - Linha: {issue['line_number']}")