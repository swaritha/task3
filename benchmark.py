import time
import random
import csv

from custom_csv import CustomCsvReader, CustomCsvWriter


def generate_data(num_rows=10000, num_cols=5):
    rows = []
    for _ in range(num_rows):
        row = []
        for _ in range(num_cols):
            choice = random.randint(0, 3)
            if choice == 0:
                value = "simpletext"
            elif choice == 1:
                value = "text,with,comma"
            elif choice == 2:
                value = 'He said "Hello"'
            else:
                value = "multi\nline"
            row.append(value)
        rows.append(row)
    return rows


def benchmark_writer(rows, filename_custom="custom_out.csv", filename_std="std_out.csv"):
    # Custom writer
    start = time.perf_counter()
    with open(filename_custom, "w", encoding="utf-8", newline="") as f:
        writer = CustomCsvWriter(f)
        writer.writerows(rows)
    custom_time = time.perf_counter() - start

    # Standard csv.writer
    start = time.perf_counter()
    with open(filename_std, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    std_time = time.perf_counter() - start

    return custom_time, std_time


def benchmark_reader(filename_custom="custom_out.csv", filename_std="std_out.csv"):
    # Read with our reader
    start = time.perf_counter()
    with open(filename_custom, "r", encoding="utf-8") as f:
        reader = CustomCsvReader(f)
        for _ in reader:
            pass
    custom_time = time.perf_counter() - start

    # Read with standard csv.reader
    start = time.perf_counter()
    with open(filename_std, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for _ in reader:
            pass
    std_time = time.perf_counter() - start

    return custom_time, std_time


def main():
    print("Generating data...")
    rows = generate_data()

    print("Benchmarking writer...")
    c_w, s_w = benchmark_writer(rows)
    print(f"Custom writer: {c_w:.4f} seconds")
    print(f"csv.writer   : {s_w:.4f} seconds")

    print("Benchmarking reader...")
    c_r, s_r = benchmark_reader()
    print(f"Custom reader: {c_r:.4f} seconds")
    print(f"csv.reader   : {s_r:.4f} seconds")


if __name__ == "__main__":
    main()
