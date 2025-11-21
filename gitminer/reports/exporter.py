import pandas as pd
from pathlib import Path
from typing import Literal

def export_data(
    data: pd.DataFrame,
    format: Literal["csv", "json"],
    output_dir: Path,
    filename: str
):
    """
    Exporta um DataFrame para CSV ou JSON.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if format == "csv":
        filepath = output_dir / f"{filename}.csv"
        data.to_csv(filepath, index=False)
        print(f"✅ Dados exportados para: {filepath}")
    elif format == "json":
        filepath = output_dir / f"{filename}.json"
        data.to_json(filepath, orient="records", indent=4)
        print(f"✅ Dados exportados para: {filepath}")
    else:
        print(f"❌ Formato de exportação '{format}' não suportado.")