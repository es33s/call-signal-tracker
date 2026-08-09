#!/usr/bin/env python3
"""
CALL & SIGNAL TRACKER
Educational tool for analyzing user-provided call logs
and mobile network signal data.

This tool does NOT intercept calls, access telecom networks,
or track devices. It only analyzes data supplied by the user.
"""

from pathlib import Path
import os
import pandas as pd

APP_NAME = "CALL & SIGNAL TRACKER"
APP_VERSION = "1.1"
DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")

DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

REQUIRED_COLUMNS = {
    "timestamp",
    "call_type",
    "phone_number",
    "cell_id",
    "radio_type",
    "rsrp",
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    clear_screen()
    print("=" * 60)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print("1. Import Data (CSV / JSON)")
    print("2. View Call Logs")
    print("3. View All Records")
    print("4. Search by Phone Number")
    print("5. Filter by Date Range")
    print("6. Analyze Signal Strength")
    print("7. Analyze Network Types")
    print("8. Top Cells by Signal Strength")
    print("9. Show Summary")
    print("10. Export Report (CSV)")
    print("11. Exit")
    print("=" * 60)


def validate_columns(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        print("\n[!] Missing required columns:")
        for column in sorted(missing):
            print(f"    - {column}")
        return False
    return True


def load_data(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"[!] File not found: {file_path}")
        return pd.DataFrame()

    try:
        ext = path.suffix.lower()

        if ext == ".csv":
            df = pd.read_csv(path)
        elif ext == ".json":
            df = pd.read_json(path)
        else:
            print("[!] Unsupported format. Please use CSV or JSON.")
            return pd.DataFrame()

        if df.empty:
            print("[!] The file contains no records.")
            return pd.DataFrame()

        if not validate_columns(df):
            return pd.DataFrame()

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["rsrp"] = pd.to_numeric(df["rsrp"], errors="coerce")

        print(f"[+] Data loaded successfully: {len(df)} records")
        return df

    except Exception as exc:
        print(f"[!] Error loading data: {exc}")
        return pd.DataFrame()


def import_data():
    print("\n[1] Import CSV file")
    print("[2] Import JSON file")
    choice = input("Select option (1-2): ").strip()

    if choice not in {"1", "2"}:
        print("[!] Invalid option.")
        return pd.DataFrame()

    file_path = input("Enter file path: ").strip().strip('"').strip("'")
    expected = ".csv" if choice == "1" else ".json"

    if not file_path.lower().endswith(expected):
        print(f"[!] Please select a {expected} file.")
        return pd.DataFrame()

    return load_data(file_path)


def print_table(df):
    if df.empty:
        print("[!] No records to display.")
        return

    display_df = df.copy()
    if "timestamp" in display_df.columns:
        display_df["timestamp"] = display_df["timestamp"].astype(str)

    print(display_df.to_string(index=False))


def view_all_records(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    print("\n================ ALL RECORDS ================")
    print_table(df.sort_values("timestamp", ascending=False))


def view_call_logs(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    calls = df[
        df["call_type"]
        .astype(str)
        .str.upper()
        .isin(["INCOMING", "OUTGOING", "MISSED"])
    ]

    if calls.empty:
        print("[!] No call logs found.")
        return

    print("\n================ CALL LOGS ================")
    print_table(calls.sort_values("timestamp", ascending=False))


def search_by_number(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    number = input("Enter phone number to search: ").strip()
    result = df[
        df["phone_number"].astype(str).str.contains(number, case=False, na=False)
    ]

    if result.empty:
        print("[!] No records found.")
    else:
        print("\n================ SEARCH RESULTS ================")
        print_table(result.sort_values("timestamp", ascending=False))


def filter_by_date(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    start_text = input("Start date (YYYY-MM-DD HH:MM:SS): ").strip()
    end_text = input("End date (YYYY-MM-DD HH:MM:SS): ").strip()

    start = pd.to_datetime(start_text, errors="coerce")
    end = pd.to_datetime(end_text, errors="coerce")

    if pd.isna(start) or pd.isna(end):
        print("[!] Invalid date format.")
        return

    if start > end:
        print("[!] Start date must be before end date.")
        return

    result = df[
        (df["timestamp"] >= start) &
        (df["timestamp"] <= end)
    ]

    if result.empty:
        print("[!] No records found in this range.")
    else:
        print("\n================ DATE FILTER RESULTS ================")
        print_table(result.sort_values("timestamp", ascending=False))


def analyze_signal_strength(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    valid = df.dropna(subset=["rsrp"]).copy()

    if valid.empty:
        print("[!] No valid RSRP values found.")
        return

    strongest = valid.loc[valid["rsrp"].idxmax()]
    weakest = valid.loc[valid["rsrp"].idxmin()]
    average = valid["rsrp"].mean()

    print("\n============= SIGNAL STRENGTH ANALYSIS =============")
    print(f"Valid RSRP records : {len(valid)}")
    print(f"Average RSRP       : {average:.2f} dBm")
    print(f"Strongest signal   : {strongest['rsrp']:.2f} dBm")
    print(f"Strongest Cell ID  : {strongest['cell_id']}")
    print(f"Weakest signal     : {weakest['rsrp']:.2f} dBm")
    print(f"Weakest Cell ID    : {weakest['cell_id']}")


def analyze_network_types(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    distribution = df["radio_type"].fillna("Unknown").value_counts()

    print("\n============= NETWORK TYPE DISTRIBUTION =============")
    for network, count in distribution.items():
        print(f"{str(network):<15} : {count}")


def top_cells_by_signal(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    valid = df.dropna(subset=["rsrp", "cell_id"])

    if valid.empty:
        print("[!] No valid cell/RSRP data found.")
        return

    top_cells = (
        valid.groupby("cell_id")["rsrp"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    print("\n============= TOP 5 CELLS BY AVERAGE RSRP =============")
    for cell_id, average in top_cells.items():
        print(f"Cell ID: {cell_id:<15} Avg RSRP: {average:.2f} dBm")


def show_summary(df):
    if df.empty:
        print("[!] No data loaded.")
        return

    valid_rsrp = df["rsrp"].dropna()

    print("\n================ SUMMARY ================")
    print(f"Total records : {len(df)}")

    if valid_rsrp.empty:
        print("Average RSRP  : N/A")
        print("Strongest     : N/A")
        print("Weakest       : N/A")
        return

    strongest = df.loc[df["rsrp"].idxmax()]
    weakest = df.loc[df["rsrp"].idxmin()]

    print(f"Average RSRP  : {valid_rsrp.mean():.2f} dBm")
    print(
        f"Strongest     : {strongest['rsrp']:.2f} dBm "
        f"(Cell ID: {strongest['cell_id']})"
    )
    print(
        f"Weakest       : {weakest['rsrp']:.2f} dBm "
        f"(Cell ID: {weakest['cell_id']})"
    )

    print("\nCall types:")
    for call_type, count in df["call_type"].fillna("Unknown").value_counts().items():
        print(f"  {call_type}: {count}")


def export_report(df):
    if df.empty:
        print("[!] No data to export.")
        return

    filename = input(
        "Enter report filename (default: report.csv): "
    ).strip()

    if not filename:
        filename = "report.csv"

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    output = REPORTS_DIR / Path(filename).name

    try:
        df.to_csv(output, index=False)
        print(f"[+] Report exported successfully: {output}")
    except Exception as exc:
        print(f"[!] Error exporting report: {exc}")


def main():
    df = pd.DataFrame()

    while True:
        show_menu()
        choice = input("Select an option (1-11): ").strip()

        if choice == "1":
            df = import_data()

        elif choice == "2":
            view_call_logs(df)

        elif choice == "3":
            view_all_records(df)

        elif choice == "4":
            search_by_number(df)

        elif choice == "5":
            filter_by_date(df)

        elif choice == "6":
            analyze_signal_strength(df)

        elif choice == "7":
            analyze_network_types(df)

        elif choice == "8":
            top_cells_by_signal(df)

        elif choice == "9":
            show_summary(df)

        elif choice == "10":
            export_report(df)

        elif choice == "11":
            print("[+] Exiting. Stay safe!")
            break

        else:
            print("[!] Invalid option. Please choose 1-11.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
