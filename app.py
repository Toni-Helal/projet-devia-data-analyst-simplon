from __future__ import annotations

from pathlib import Path

from sales_dashboard.analysis import DataValidationError, load_sales_data
from sales_dashboard.reporting import export_html_reports, write_summary_markdown

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ventes.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
SUMMARY_PATH = BASE_DIR / "docs" / "fiche_synthese.md"


def main() -> int:
    try:
        dataframe = load_sales_data(DATA_PATH)
    except DataValidationError as error:
        print(error)
        return 1

    export_html_reports(dataframe, OUTPUT_DIR)
    write_summary_markdown(dataframe, SUMMARY_PATH)

    print("Artifacts updated:")
    print(f"- Summary: {SUMMARY_PATH}")
    print(f"- HTML reports: {OUTPUT_DIR}")
    print("Primary interface: streamlit run dashboard.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
