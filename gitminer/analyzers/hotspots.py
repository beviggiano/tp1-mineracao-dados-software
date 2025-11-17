import pandas as pd
import os

def find_hotspots(commits_df: pd.DataFrame, complexity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica hotspots combinando dados de churn de commits e complexidade.

    Args:
        commits_df (pd.DataFrame): DataFrame da análise de commits.
        complexity_df (pd.DataFrame): DataFrame da análise de complexidade.

    Returns:
        pd.DataFrame: DataFrame com arquivos classificados como hotspots.
    """
    if commits_df.empty or complexity_df.empty:
        return pd.DataFrame()

    # Normaliza os separadores de caminho para garantir a junção correta (Windows/Linux)
    commits_df['file_path'] = commits_df['file_path'].apply(lambda x: x.replace(os.sep, '/'))
    complexity_df['file_path'] = complexity_df['file_path'].apply(lambda x: x.replace(os.sep, '/'))

    merged_df = pd.merge(commits_df, complexity_df, on="file_path", how="inner")
    
    if merged_df.empty:
        return pd.DataFrame()

    # Calcula um score de hotspot
    merged_df["hotspot_score"] = merged_df["churn"] * merged_df["total_complexity"]

    hotspots_df = merged_df.sort_values(by="hotspot_score", ascending=False).reset_index(drop=True)

    return hotspots_df
