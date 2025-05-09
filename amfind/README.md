# AMFI NAV Data Extractor

A shell script to extract Scheme Name and Asset Value data from AMFI (Association of Mutual Funds in India) NAV files.

## Description

This utility downloads NAV (Net Asset Value) data from the AMFI website and extracts the following information:
- Scheme Code
- Scheme Name
- NAV (Net Asset Value)
- NAV Date

The data is processed and saved in both TSV (Tab-Separated Values) and JSON formats for easy integration with other tools and systems.

## Requirements

- Bash shell
- curl (for downloading data)
- awk (for data processing)
- sed (for JSON formatting)

These tools are available by default on most Linux and macOS systems.

## Usage

1. Make the script executable (one-time setup):

```bash
chmod +x extract_nav.sh
```

2. Run the script:

```bash
./extract_nav.sh
```

## Output Files

The script generates two files with timestamps in their names:

1. `amfi_nav_data_YYYYMMDD.tsv` - Tab-separated values file
2. `amfi_nav_data_YYYYMMDD.json` - JSON format file

## How It Works

1. The script downloads NAV data from `https://www.amfiindia.com/spages/NAVAll.txt`
2. It processes the semicolon-delimited data to extract relevant fields
3. The data is cleaned and formatted for both TSV and JSON outputs
4. Temporary files are cleaned up automatically