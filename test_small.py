from custom_csv import CustomCsvReader, CustomCsvWriter

rows = [
    ["name", "age", "note"],
    ["Alice", "20", "Hello"],
    ["Bob, Jr.", "18", "Has, comma"],
    ["Charlie", "25", 'He said "Hi"'],
    ["Dana", "30", "multi\nline text"],
]

# 1. Write sample.csv
with open("sample.csv", "w", encoding="utf-8", newline="") as f:
    writer = CustomCsvWriter(f)
    writer.writerows(rows)

print("Finished writing sample.csv")

# 2. Read it back using our reader
with open("sample.csv", "r", encoding="utf-8") as f:
    reader = CustomCsvReader(f)
    print("Reading sample.csv with CustomCsvReader:")
    for row in reader:
        print(row)
