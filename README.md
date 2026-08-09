# Call & Signal Tracker

A Python-based educational tool for analyzing **user-provided** call-log
and mobile-network signal data from CSV or JSON files.

> **Important:** This project does not intercept calls, access telecom
> networks, locate devices, or collect data from other people's phones.
> It only analyzes data that the user already has permission to analyze.

## Features

- Import CSV and JSON datasets
- View all records
- View incoming, outgoing, and missed calls
- Search records by phone number
- Filter records by date range
- Analyze RSRP signal strength
- Find strongest and weakest cells
- Analyze network/radio-type distribution
- Show summary statistics
- Export analyzed data to CSV

## Installation

Python 3.8+ is recommended.

```bash
git clone https://github.com/es33s/call-signal-tracker.git
cd call-signal-tracker
pip install -r requirements.txt
```

## Run

```bash
python call_signal_tracker.py
```

On some systems:

```bash
python3 call_signal_tracker.py
```

## Try the included sample data

Start the program:

```bash
python call_signal_tracker.py
```

Choose:

```text
1. Import Data
```

Then enter:

```text
data/sample_data.csv
```

The sample dataset contains fictional/test values only.

## Expected CSV columns

The analyzer expects these columns:

```text
timestamp
call_type
phone_number
duration
cell_id
lac
mcc
mnc
radio_type
rsrp
```

### RSRP

RSRP is a common LTE/5G signal-strength measurement expressed in dBm.
Because the values are normally negative, a value closer to zero generally
represents a stronger signal.

For example:

```text
-70 dBm  → stronger
-100 dBm → weaker
```

## Responsible Use

Use this project only with data you own or are explicitly authorized to
analyze. Do not upload real phone numbers, private call logs, or sensitive
telecom information to a public repository.

The included sample data is fictional.

## License

MIT License. See `LICENSE`.
