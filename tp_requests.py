import os
import csv
import json
from collections import defaultdict, Counter

def extract_sld_har(url):
    parts = url.split('.')
    return parts[1]

def extract_sld_csv(url):
    parts = url.split('.')
    return parts[0]

def parse_file_number(row):
    return int(row[0])

# Function to find the corresponding HAR file for a given number
def find_har_file(har_directory, number):
    har_file_name = f"{number}.har"
    har_file_path = os.path.join(har_directory, har_file_name)
    if os.path.exists(har_file_path):
        return har_file_path

# Function to count the number of third-party requests for a given site
def count_third_party_requests(har_file_path, base_domain):
    third_party_count = 0
    third_party_domains = set()
    with open(har_file_path, 'r', encoding='utf-8') as har_file:
        har_data = json.load(har_file)
        entries = har_data['log']['entries']
        for entry in entries:
            url = entry['request']['url']
            entry_sld = extract_sld_har(url)
            if entry_sld != base_domain:
                third_party_domains.add(entry_sld)
                third_party_count += 1
    return third_party_count, third_party_domains

# Dictionary to store the number of third-party requests for each site
third_party_counts = defaultdict(int)
# Dictionary to store third-party domains for each site
third_party_domains_dict = defaultdict(set)
# List to store all third-party domains
all_third_party_domains = []

with open("top-1m.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        file_number = parse_file_number(row)
        base_domain = extract_sld_csv(row[1])
        har_file_path = find_har_file("Har Files", file_number)

        if har_file_path:
            third_party_count, third_party_domains = count_third_party_requests(har_file_path, base_domain)
            all_third_party_domains.extend(third_party_domains)
            third_party_domains_dict[base_domain] = third_party_domains
            third_party_counts[base_domain] = third_party_count

third_party_counter = Counter(all_third_party_domains)
top_10_third_parties = third_party_counter.most_common(10)

with open("tp_requests.txt", 'w') as output:
    output.write("Number of third-party requests for each site:\n")
    for domain, count in third_party_counts.items():
        output.write(f"Site {domain}: {count} third-party requests\n")
        output.write(f"Third-party domains: {', '.join(third_party_domains_dict[domain])}\n")

    output.write("\nTop 10 most common third parties across all sites:\n")
    for domain, count in top_10_third_parties:
        output.write(f"{domain}: {count} occurrences\n")