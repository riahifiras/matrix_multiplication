# Matrix Multiplication Performance Analysis

This project is a school assignment designed to introduce parallel programming concepts by measuring execution time and memory consumption for matrix multiplication across three different programming languages: **C++**, **Python**, and **Java**.

The project currently focuses on comparing execution times for different matrix multiplication loop orderings (ijk, ikj, jik, etc.) under various matrix sizes.

## Features
- Matrix multiplication using different loop configurations (ijk, ikj, jik, etc.)
- Execution time analysis for C++, Java, and Python implementations
- User-friendly desktop interface for selecting matrix sizes and configurations
- Performance comparisons to observe the impact of cache locality and loop order on execution time

## Future Work
- Implement memory consumption measurement
- Add parallel programming algorithms to leverage multi-core CPU architectures

## Usage

### Step 1: Compile the C++ Script
Before running the application, compile the C++ script:

```cpp
g++ -o main main.cpp
```

### Step 2: Run the Python Application
Start the desktop application using the following command:

```python
python3 app.py
```

### Step 3: Use the Application
In the desktop UI, you can:
1. Select the programming languages (**C++**, **Python**, **Java**) for matrix multiplication.
2. Set the maximum matrix size for multiplication.
3. Define the number of iterations for matrix multiplication. For example, if you choose 10, the program will multiply two matrices 10 times and calculate the total execution time for those 10 operations.

The application will then run the selected configurations and display the execution times for analysis.
