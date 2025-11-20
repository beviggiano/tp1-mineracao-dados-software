# Arquivo: gitminer-cli/gitminer/reports/plots.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_hotspots(hotspots_df: pd.DataFrame, output_dir: Path):
    """Gera um gráfico de dispersão para hotspots."""
    if hotspots_df.empty:
        print("⚠️ Nenhum dado de hotspot para plotar.")
        return

    plt.figure(figsize=(12, 8))
    plt.scatter(hotspots_df['total_complexity'], hotspots_df['churn'], c=hotspots_df['hotspot_score'], cmap='viridis', s=100, alpha=0.7)
    plt.colorbar(label='Hotspot Score')
    plt.xlabel('Complexidade Ciclomática Total')
    plt.ylabel('Churn (Linhas Adicionadas + Removidas)')
    plt.title('Análise de Hotspots: Complexidade vs. Churn')
    plt.grid(True)
    
    filepath = output_dir / "hotspots_report.png"
    plt.savefig(filepath)
    print(f"✅ Gráfico de hotspots salvo em: {filepath}")
    plt.close()

def plot_complexity(complexity_df: pd.DataFrame, output_dir: Path, top_n: int = 10):
    """Gera um gráfico de barras para a complexidade."""
    if complexity_df.empty:
        print("⚠️ Nenhum dado de complexidade para plotar.")
        return
        
    top_files = complexity_df.nlargest(top_n, 'total_complexity')
    
    plt.figure(figsize=(12, 8))
    plt.barh(top_files['file_path'], top_files['total_complexity'], color='skyblue')
    plt.xlabel('Complexidade Ciclomática Total')
    plt.ylabel('Arquivo')
    plt.title(f'Top {top_n} Arquivos por Complexidade Ciclomática')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    filepath = output_dir / "complexity_report.png"
    plt.savefig(filepath)
    print(f"✅ Gráfico de complexidade salvo em: {filepath}")
    plt.close()


def plot_churn(commits_df: pd.DataFrame, output_dir: Path, top_n: int = 10):
    """Gera um gráfico de barras para o churn."""
    if commits_df.empty:
        print("⚠️ Nenhum dado de churn para plotar.")
        return
        
    top_files = commits_df.nlargest(top_n, 'churn')
    
    plt.figure(figsize=(12, 8))
    plt.barh(top_files['file_path'], top_files['churn'], color='salmon')
    plt.xlabel('Churn (Linhas Adicionadas + Removidas)')
    plt.ylabel('Arquivo')
    plt.title(f'Top {top_n} Arquivos por Churn')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    filepath = output_dir / "churn_report.png"
    plt.savefig(filepath)
    print(f"✅ Gráfico de churn salvo em: {filepath}")
    plt.close()

def plot_maintainability(maintainability_df: pd.DataFrame, output_dir: Path, top_n: int = 10):
    """Gera um gráfico de barras para o Índice de Manutenibilidade."""
    if maintainability_df.empty:
        print("⚠️ Nenhum dado de manutenibilidade para plotar.")
        return
        
    # Pegamos os arquivos com o *menor* MI, pois são os mais problemáticos
    worst_files = maintainability_df.nsmallest(top_n, 'maintainability_index')
    
    plt.figure(figsize=(12, 8))
    # Barras em vermelho para indicar perigo/alerta
    plt.barh(worst_files['file_path'], worst_files['maintainability_index'], color='firebrick')
    plt.xlabel('Índice de Manutenibilidade (0-100, menor é pior)')
    plt.ylabel('Arquivo')
    plt.title(f'Top {top_n} Piores Arquivos por Manutenibilidade')
    plt.xlim(0, 100) # O índice vai de 0 a 100
    plt.gca().invert_yaxis()
    plt.tight_layout()

    filepath = output_dir / "maintainability_report.png"
    plt.savefig(filepath)
    print(f"✅ Gráfico de manutenibilidade salvo em: {filepath}")
    plt.close()