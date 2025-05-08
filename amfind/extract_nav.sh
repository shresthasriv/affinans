TSV_FILE="amfi_nav_data_$(date +%Y%m%d).tsv"
JSON_FILE="amfi_nav_data_$(date +%Y%m%d).json"

echo "Downloading AMFI NAV data..."
curl -s https://www.amfiindia.com/spages/NAVAll.txt > nav_data_raw.txt

if [ ! -s nav_data_raw.txt ]; then
    echo "Error: Failed to download data or received empty file"
    exit 1
fi

echo "Extracting Scheme Name and NAV data..."

echo -e "Scheme_Code\tScheme_Name\tNAV\tNAV_Date" > "$TSV_FILE"

awk -F';' '
    # Skip header lines and empty lines
    NF >= 5 && $1 ~ /^[0-9]+$/ {
        scheme_code = $1;
        scheme_name = $4;
        nav = $5;
        nav_date = $6;
        
        # Remove any extra quotes and spaces
        gsub(/^[ \t]+|[ \t]+$/, "", scheme_name);
        gsub(/^[ \t]+|[ \t]+$/, "", nav);
        gsub(/^[ \t]+|[ \t]+$/, "", nav_date);
        
        # Print to TSV, handling fields with quotes properly
        printf "%s\t%s\t%s\t%s\n", scheme_code, scheme_name, nav, nav_date;
    }
' nav_data_raw.txt >> "$TSV_FILE"

echo "TSV file created: $TSV_FILE"

echo "Creating JSON file..."
echo "[" > "$JSON_FILE"
awk -F'\t' 'NR>1 {
    printf "  {\n    \"scheme_code\": \"%s\",\n    \"scheme_name\": \"%s\",\n    \"nav\": \"%s\",\n    \"nav_date\": \"%s\"\n  }%s\n", 
    $1, $2, $3, $4, (NR==EOF)?"":",";
}' "$TSV_FILE" >> "$JSON_FILE"
# Fix the last comma issue
sed -i '$ s/},/}/' "$JSON_FILE"
echo "]" >> "$JSON_FILE"

echo "JSON file created: $JSON_FILE"
echo "Cleaning up temporary files..."
rm nav_data_raw.txt

echo "Processing complete!"
echo "Notes:"
echo "- TSV format is more efficient for large datasets and easier to process with command-line tools"
echo "- JSON format is better for web applications, API responses, and when data structure flexibility is needed"
echo "- Choose based on your specific use case - TSV for simplicity, JSON for interoperability" 