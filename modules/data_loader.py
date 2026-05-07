"""Carga y limpieza de las seis hojas Excel con series de turismo del ICT."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import numpy as np
import pandas as pd


class DataLoader:
    """Utilidades estáticas para cargar las hojas del archivo ICT."""

    FILE_NAME: ClassVar[str] = "Series_sitio_web_ICT_2025.xlsx"
    ROOT_DIR: ClassVar[Path] = Path(__file__).resolve().parents[1]
    DEFAULT_PATH: ClassVar[Path] = ROOT_DIR / "data" / FILE_NAME
    FALLBACK_PATH: ClassVar[Path] = ROOT_DIR / FILE_NAME
    ZONE_COLUMNS: ClassVar[list[str]] = [
        "América del Norte",
        "Europa",
        "América del Sur",
        "América Central",
        "Caribe",
        "Otras zonas",
    ]

    @staticmethod
    def _resolve_file() -> Path:
        if DataLoader.DEFAULT_PATH.exists():
            return DataLoader.DEFAULT_PATH
        if DataLoader.FALLBACK_PATH.exists():
            return DataLoader.FALLBACK_PATH
        raise FileNotFoundError(
            f"No se encontró {DataLoader.FILE_NAME}. Colóquelo en "
            f"{DataLoader.DEFAULT_PATH}."
        )

    @staticmethod
    def _to_float(value: object) -> float:
        if pd.isna(value):
            return np.nan
        if isinstance(value, (int, float, np.integer, np.floating)):
            return float(value)
        cleaned = str(value).strip()
        if cleaned == "" or cleaned.lower() in {"nan", "año", "ano"}:
            return np.nan
        cleaned = (
            cleaned.replace("\u00a0", "")
            .replace(" ", "")
            .replace(",", "")
            .replace("%", "")
        )
        return float(cleaned)

    @staticmethod
    def _detect_data_start(raw_df: pd.DataFrame) -> int:
        for index, row in raw_df.iterrows():
            numeric_row = pd.to_numeric(row, errors="coerce")
            if numeric_row.between(1900, 2100).any():
                return int(index)
        raise ValueError("No se pudo detectar la fila inicial de datos numéricos.")

    @staticmethod
    def _sheet_names() -> list[str]:
        file_path = DataLoader._resolve_file()
        return pd.ExcelFile(file_path, engine="openpyxl").sheet_names

    @staticmethod
    def _find_sheet(preferred: str, aliases: list[str] | None = None) -> str | None:
        available = DataLoader._sheet_names()
        candidates = [preferred, *(aliases or [])]
        for candidate in candidates:
            if candidate in available:
                return candidate
        return None

    @staticmethod
    def _read_year_value_sheet(sheet_name: str, value_column: str) -> pd.DataFrame:
        file_path = DataLoader._resolve_file()
        raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine="openpyxl")
        rows: list[dict[str, float | int]] = []
        for _, row in raw_df.iterrows():
            numeric_row = pd.to_numeric(row, errors="coerce")
            year_positions = [
                position
                for position, value in enumerate(numeric_row)
                if pd.notna(value) and 1900 <= float(value) <= 2100 and float(value).is_integer()
            ]
            for position in year_positions:
                if position + 1 >= len(row):
                    continue
                value = DataLoader._to_float(row.iloc[position + 1])
                if pd.notna(value):
                    rows.append({"Año": int(numeric_row.iloc[position]), value_column: value})
                    break
        if not rows:
            raise ValueError(f"No se encontraron datos anuales en la hoja {sheet_name}.")
        df = pd.DataFrame(rows).drop_duplicates(subset=["Año"], keep="last").sort_values("Año")
        df.index = pd.Index(df["Año"], name="Año")
        return df[["Año", value_column]]

    @staticmethod
    def _read_clean_sheet(sheet_name: str, columns: list[str]) -> pd.DataFrame:
        file_path = DataLoader._resolve_file()
        raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine="openpyxl")
        start_row = DataLoader._detect_data_start(raw_df)
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=None,
            skiprows=start_row,
            engine="openpyxl",
        )
        df = df.iloc[:, : len(columns)].copy()
        df.columns = columns
        df["Año"] = pd.to_numeric(df["Año"], errors="coerce")
        df = df.dropna(subset=["Año"])
        df = df[df["Año"].between(1900, 2100)]
        df["Año"] = df["Año"].astype(int)

        for column in columns:
            if column != "Año":
                df[column] = df[column].map(DataLoader._to_float)

        df = df.dropna(how="all", subset=[column for column in columns if column != "Año"])
        df = df.drop_duplicates(subset=["Año"], keep="last")
        df = df.sort_values("Año").reset_index(drop=True)
        df.index = pd.Index(df["Año"], name="Año")
        return df[columns]

    @staticmethod
    def _read_zone_matrix(sheet_name: str) -> pd.DataFrame:
        file_path = DataLoader._resolve_file()
        raw_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine="openpyxl")
        year_row_index: int | None = None
        year_positions: list[int] = []
        years: list[int] = []

        for index, row in raw_df.iterrows():
            numeric_row = pd.to_numeric(row, errors="coerce")
            positions = [
                position
                for position, value in enumerate(numeric_row)
                if pd.notna(value) and 2010 <= float(value) <= 2030 and float(value).is_integer()
            ]
            if len(positions) >= 3:
                year_row_index = int(index)
                year_positions = positions
                years = [int(numeric_row.iloc[position]) for position in positions]
                break

        if year_row_index is None:
            raise ValueError(f"No se encontraron encabezados de años en la hoja {sheet_name}.")

        zone_aliases = {
            "AMÉRICA DEL NORTE": "América del Norte",
            "AMERICA DEL NORTE": "América del Norte",
            "EUROPA": "Europa",
            "AMÉRICA DEL SUR": "América del Sur",
            "AMERICA DEL SUR": "América del Sur",
            "AMÉRICA CENTRAL": "América Central",
            "AMERICA CENTRAL": "América Central",
            "CARIBE": "Caribe",
            "OTRAS ZONAS": "Otras zonas",
            "OTRAS ZONAS2": "Otras zonas",
        }

        records: dict[str, list[float]] = {}
        for _, row in raw_df.iloc[year_row_index + 1 :].iterrows():
            label_values = [str(value).strip().upper() for value in row.iloc[:4] if pd.notna(value) and str(value).strip()]
            label = next((zone_aliases[value] for value in label_values if value in zone_aliases), None)
            if label is None:
                continue
            records[label] = [DataLoader._to_float(row.iloc[position]) for position in year_positions]

        missing = [zone for zone in DataLoader.ZONE_COLUMNS if zone not in records]
        if missing:
            raise ValueError(f"Faltan zonas en {sheet_name}: {', '.join(missing)}.")

        df = pd.DataFrame({"Año": years})
        for zone in DataLoader.ZONE_COLUMNS:
            df[zone] = records[zone]
        df = df.dropna(subset=DataLoader.ZONE_COLUMNS, how="all").sort_values("Año")
        df.index = pd.Index(df["Año"], name="Año")
        return df[["Año", *DataLoader.ZONE_COLUMNS]]

    @staticmethod
    def load_total_arrivals() -> pd.DataFrame:
        """Devuelve llegadas totales anuales con columnas ['Año', 'Total']."""
        sheet_name = DataLoader._find_sheet("TV_1951-2025")
        if sheet_name is None:
            raise ValueError("No se encontró la hoja TV_1951-2025.")
        return DataLoader._read_year_value_sheet(sheet_name, "Total")

    @staticmethod
    def load_air_arrivals() -> pd.DataFrame:
        """Devuelve llegadas por vía aérea con columnas ['Año', 'Vía aérea']."""
        sheet_name = DataLoader._find_sheet("VA_1976-2025")
        if sheet_name is None:
            raise ValueError("No se encontró la hoja VA_1976-2025.")
        return DataLoader._read_year_value_sheet(sheet_name, "Vía aérea")

    @staticmethod
    def load_by_zone(sheet_name: str) -> pd.DataFrame:
        """Devuelve llegadas o participación por zona desde 'Cuadro 3' o 'Cuadro 4'."""
        if sheet_name not in {"Cuadro 3", "Cuadro 4"}:
            raise ValueError("sheet_name debe ser 'Cuadro 3' o 'Cuadro 4'.")
        resolved_sheet = DataLoader._find_sheet(sheet_name, aliases=["Todas_vías"] if sheet_name == "Cuadro 3" else [])
        if resolved_sheet:
            try:
                df = DataLoader._read_clean_sheet(resolved_sheet, ["Año", *DataLoader.ZONE_COLUMNS])
                if not df.empty:
                    return df
            except ValueError:
                pass
            return DataLoader._read_zone_matrix(resolved_sheet)

        if sheet_name == "Cuadro 4":
            zone_df = DataLoader.load_by_zone("Cuadro 3").copy()
            for zone in DataLoader.ZONE_COLUMNS:
                zone_df[zone] = pd.to_numeric(zone_df[zone], errors="coerce")
            zone_totals = zone_df[DataLoader.ZONE_COLUMNS].sum(axis=1)
            for zone in DataLoader.ZONE_COLUMNS:
                zone_df[zone] = zone_df[zone] / zone_totals * 100
            return zone_df[["Año", *DataLoader.ZONE_COLUMNS]]

        raise ValueError(f"No se encontró la hoja {sheet_name}.")

    @staticmethod
    def load_annual_variation() -> pd.DataFrame:
        """Devuelve variación porcentual anual con columnas ['Año', 'Var %']."""
        sheet_name = DataLoader._find_sheet("Var % anual")
        if sheet_name:
            return DataLoader._read_clean_sheet(sheet_name, ["Año", "Var %"])
        total_df = DataLoader.load_total_arrivals()
        df = total_df[["Año", "Total"]].copy()
        df["Var %"] = df["Total"].pct_change() * 100
        df = df.dropna(subset=["Var %"])
        df.index = pd.Index(df["Año"], name="Año")
        return df[["Año", "Var %"]]

    @staticmethod
    def load_growth_rates() -> pd.DataFrame:
        """Devuelve tasas de crecimiento como fracciones con columnas ['Año', 'Crecimiento']."""
        sheet_name = DataLoader._find_sheet("Crecimientos")
        if sheet_name:
            df = DataLoader._read_clean_sheet(sheet_name, ["Año", "Crecimiento"])
        else:
            total_df = DataLoader.load_total_arrivals()
            df = total_df[["Año", "Total"]].copy()
            df["Crecimiento"] = df["Total"].pct_change()
            df = df[df["Año"].between(2022, 2025)].dropna(subset=["Crecimiento"])
            df.index = pd.Index(df["Año"], name="Año")
            df = df[["Año", "Crecimiento"]]
        if df["Crecimiento"].abs().max(skipna=True) > 1:
            df["Crecimiento"] = df["Crecimiento"] / 100.0
        return df
