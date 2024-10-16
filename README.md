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

## Dependencies

Make sure you have the following installed before running the project:
- **Python 3.x**
- **g++** (for compiling C++ code)
- **Java JDK** (for Java execution)

## Usage

### Step 1: Compile the C++ Script
Before running the application, compile the C++ script:

```bash
cd scripts
g++ -o main main.cpp
```

### Step 2: Run the Python Application
Start the desktop application using the following commands:

#### 1. Navigate into the app directory and create a virtual environment

```bash
cd app
python3 -m venv venv
```

#### 2. Activate the virtual environment

```bash
source ./venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install matplotlib customtkinter
```

#### 4. Run the app

```bash
python3 app.py
```

### Step 3: Use the Application
In the desktop UI, you can:
1. Select the programming languages (**C++**, **Python**, **Java**) for matrix multiplication.
2. Set the maximum matrix size for multiplication.
3. Define the number of iterations for matrix multiplication. For example, if you choose 10, the program will multiply two matrices 10 times and calculate the total execution time for those 10 operations.

The application will then run the selected configurations and display the execution times for analysis.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
