import os
import csv
import json
from collections import defaultdict, Counter

def extract_sld_har(url):
    parts = url.split('.')
    return parts[1]

def parse_csv_row(row):
    return int(row[0]), row[1]

def find_har_file(har_directory, number):
    har_file_name = f"{number}.har"
    har_file_path = os.path.join(har_directory, har_file_name)
    if os.path.isfile(har_file_path):
        return har_file_path
    return None

def extract_cookies_from_request_or_response(har_entry):
    request = har_entry.get('request', {})
    response = har_entry.get('response', {})
    request_cookies = extract_cookies_from_headers(request.get('headers', []), request.get('url', ''))    
    response_cookies = extract_cookies_from_headers(response.get('headers', []))
    
    return request_cookies, response_cookies

def extract_cookies_from_headers(headers, url=''):
    cookies = []
    
    domain_start = url.find('://') + 3
    domain_end = url.find('/', domain_start) if '/' in url[domain_start:] else len(url)
    domain = url[domain_start:domain_end]
    
    for header in headers:
        if header['name'].lower() == 'cookie':
            cookies.extend(header['value'].split(';'))
    
    third_party_cookies = [cookie.strip() for cookie in cookies if not cookie.startswith(f"{domain}=")]
    
    return third_party_cookies

# Dictionary to store unique third-party cookies for each site
third_party_cookies_dict = defaultdict(set)

# List to store all third-party cookies
all_third_party_cookies = []

# Read CSV file and iterate through lines
with open("top-1m.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    for csv_row in csv_reader:
        # Parse the number and base domain from the CSV row
        file_number, base_domain_csv = parse_csv_row(csv_row)

        # Find the corresponding HAR file
        har_file_path = find_har_file("Har Files", file_number)

        if har_file_path:
            # Load HAR data
            with open(har_file_path, 'r', encoding='utf-8') as har_file:
                har_data = json.load(har_file)
                entries = har_data['log']['entries']

                # Iterate through HAR entries and extract cookies
                for entry in entries:
                    request_cookies, response_cookies = extract_cookies_from_request_or_response(entry)
                    all_third_party_cookies.extend(request_cookies)
                    all_third_party_cookies.extend(response_cookies)
                    third_party_cookies_dict[file_number].update(request_cookies)
                    third_party_cookies_dict[file_number].update(response_cookies)

# Count the occurrences of each third-party cookie
third_party_cookie_counter = Counter(all_third_party_cookies)

# Calculate the top 10 most common third-party cookies
top_10_third_party_cookies = third_party_cookie_counter.most_common(10)

# Write the results to the output file
with open("tp_cookies.txt", 'w') as output_file:
    output_file.write("Unique third-party cookies for each site:\n")
    for file_number, cookies in third_party_cookies_dict.items():
        output_file.write(f"Site {file_number}: {cookies}\n")

    output_file.write("\nTop 10 most common third-party cookies across all sites:\n")
    for cookie, count in top_10_third_party_cookies:
        output_file.write(f"{cookie}: {count} occurrences\n")