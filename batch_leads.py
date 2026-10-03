import sys
import os
import glob
import subprocess
import pandas as pd

# List of queries (Yahan apne keywords aur areas add karein)
queries = [
    # Example: Bettiah & nearby areas
    "Schools in Bettiah",
    "Coaching institutes in Bettiah",
    "Computer institutes in Bettiah",
    "Schools in Motihari",
    "Coaching in Motihari",
    "Colleges in West Champaran"
]

depth = "3"  # Depth 3 = har query se ~60 leads

print(f"Total queries to scrape: {len(queries)}\n")

for i, query in enumerate(queries, 1):
    print(f"[{i}/{len(queries)}] Scraping: {query} ...")
    # run.py ko call karega
    subprocess.run(["python3", "run.py", query, depth])

# Saari CSV files ko ek saath merge karna
print("\nMerging all results into a single file...")
all_files = glob.glob("results-*.csv")

if all_files:
    df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            pass

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        # Duplicate businesses/phone numbers remove karein
        combined_df.drop_duplicates(subset=["phone"], keep="first", inplace=True)
        
        output_file = "All_Leads_Combined.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"SUCCESS: Total {len(combined_df)} unique leads saved to '{output_file}'!")
else:
    print("No CSV files found.")
