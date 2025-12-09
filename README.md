## Benchmark

I ran `benchmark.py` on a dataset with 10,000 rows and 5 columns.

### Results

**Writer**

- CustomCsvWriter: **0.0491 seconds**
- csv.writer: **0.0171 seconds**

**Reader**

- CustomCsvReader: **0.2071 seconds**
- csv.reader: **0.0217 seconds**

### Analysis

- The **built-in csv module is faster** for both reading and writing.
- The custom writer is roughly **3× slower** than `csv.writer`.
- The custom reader is roughly **10× slower** than `csv.reader`.

This is expected because:

- Python’s `csv` module is implemented in **highly optimized C code**.
- My custom implementation is written in **pure Python** and reads the file
  **character by character**, which adds overhead.
  
Even though it is slower, the custom reader and writer:

- Correctly handle **quoted fields**, **escaped quotes (`""`)**, and **newlines inside fields**.
- Work in a **streaming way**, returning one row at a time instead of loading the whole file into memory.

The benchmark shows the performance trade-off between a simple, educational
implementation and the optimized standard library.
