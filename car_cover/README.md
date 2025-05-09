# OLX Car Cover Scraper

A Python script that scrapes car cover listings from OLX India and saves the results in multiple formats.

## Description

This scraper uses Selenium to extract car cover listings from OLX India. It navigates to the car cover search page, loads multiple pages of results, and extracts key information from each listing including:

- Title
- Price
- Location
- Posted date
- URL link
- Image URL

## Requirements

- Python 3.10+
- Chrome browser
- ChromeDriver (automatically installed by webdriver-manager)

## Installation

1. Clone this repository or download the script files
2. Install the required Python packages:

```bash
pip install selenium webdriver-manager
```

## Usage

Run the script with Python:

```bash
python scraper.py
```

The script will:
1. Open a headless Chrome browser
2. Navigate to the OLX car cover search page
3. Scrape up to 3 pages of listings (configurable)
4. Save the results in multiple file formats (json, text, csv)

## Output Files

The script generates three output files:

1. **CSV File (`olx_car_covers.csv`)**: Tabular data format, good for importing into spreadsheet applications like Excel
2. **Text File (`olx_car_covers.txt`)**: Human-readable format with each listing clearly separated
3. **JSON File (`olx_car_covers.json`)**: Structured data format, ideal for programmatic use or API consumption

## Customization

You can modify the following parameters in the `main()` function:

- `search_url`: Change to search for different items
- `num_pages`: Adjust the number of pages to scrape

## Troubleshooting

If you encounter any issues:

1. Make sure Chrome is installed on your system
2. Check if you have a working internet connection
3. Verify that you can access the OLX website normally in your browser
4. Try running without headless mode for debugging (remove the `--headless` option in the code)