#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;

int configuration = 0;

void print3DVector(const vector<vector<vector<int>>> &vec)
{
    for (size_t i = 0; i < vec.size(); ++i)
    {
        cout << "Layer " << i << ":" << endl;
        for (size_t j = 0; j < vec[i].size(); ++j)
        {
            cout << " Row " << j << ": ";
            for (size_t k = 0; k < vec[i][j].size(); ++k)
            {
                cout << vec[i][j][k] << " ";
            }
            cout << endl;
        }
    }
}

vector<vector<vector<int>>> parse_file(int size, int total_matrices)
{
    ifstream inputFile("data.txt");

    if (!inputFile)
    {
        cerr << "Unable to open file data.txt";
        return {};
    }

    vector<int> numbers;
    string line;

    while (getline(inputFile, line))
    {
        stringstream ss(line);
        int number;

        while (ss >> number)
        {
            numbers.push_back(number);
        }
    }

    vector<vector<vector<int>>> matrices;

    for (int i = 0; i < total_matrices; i++)
    {
        vector<vector<int>> matrix;
        for (int j = 0; j < pow(size, 2); j += size)
        {
            vector<int> v;
            for (int k = 0; k < size; k++)
            {
                v.push_back(numbers[j + k]);
            }
            matrix.push_back(v);
        }
        matrices.push_back(matrix);
    }

    inputFile.close();
    return matrices;
}

long calculateMemoryUsage(const vector<vector<vector<int>>> &matrices)
{
    long totalSize = sizeof(matrices);          
    totalSize += sizeof(int) * matrices.size(); 
    for (const auto &matrix : matrices)
    {
        totalSize += sizeof(matrix);             
        totalSize += sizeof(int) * matrix.size(); 
        for (const auto &row : matrix)
        {
            totalSize += sizeof(row);              
            totalSize += sizeof(int) * row.size(); 
        }
    }
    return totalSize;
}

vector<vector<long>> multiplyy(const vector<vector<int>> &a, const vector<vector<int>> &b, int size)
{
    vector<vector<long>> result(size, vector<long>(size, 0));

    switch (configuration)
    {
    // ijk
    case 0:
        for (int i = 0; i < size; i++)
        {
            for (int j = 0; j < size; j++)
            {
                long sum = 0;
                for (int k = 0; k < size; k++)
                {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        break;
    // ikj
    case 1:
        for (int i = 0; i < size; i++)
        {
            for (int k = 0; k < size; k++)
            {
                long a_ik = a[i][k]; // cache `a[i][k]` since it's reused
                for (int j = 0; j < size; j++)
                {
                    result[i][j] += a_ik * b[k][j];
                }
            }
        }
        break;
    // jik
    case 2:
        for (int j = 0; j < size; j++)
        {
            for (int i = 0; i < size; i++)
            {
                long sum = 0;
                for (int k = 0; k < size; k++)
                {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        break;
    // kij
    case 3:
        for (int k = 0; k < size; k++)
        {
            for (int i = 0; i < size; i++)
            {
                long a_ik = a[i][k];
                for (int j = 0; j < size; j++)
                {
                    result[i][j] += a_ik * b[k][j];
                }
            }
        }
        break;
    // jki
    case 4:
        for (int j = 0; j < size; j++)
        {
            for (int k = 0; k < size; k++)
            {
                long b_kj = b[k][j]; // cache b[k][j] since it's reused
                for (int i = 0; i < size; i++)
                {
                    result[i][j] += a[i][k] * b_kj;
                }
            }
        }
        break;
    // kji
    case 5:
        for (int k = 0; k < size; k++)
        {
            for (int j = 0; j < size; j++)
            {
                long b_kj = b[k][j]; // cache b[k][j] since it's reused
                for (int i = 0; i < size; i++)
                {
                    result[i][j] += a[i][k] * b_kj;
                }
            }
        }
        break;
    // default ijk
    default:
        for (int i = 0; i < size; i++)
        {
            for (int j = 0; j < size; j++)
            {
                long sum = 0;
                for (int k = 0; k < size; k++)
                {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        break;
    }
    return result;
}

void multiplication(const vector<vector<vector<int>>> &matrices, int size)
{
    ofstream outputFile("output.txt", ios::app);

    auto start = chrono::high_resolution_clock::now();

    size_t initial_memory = calculateMemoryUsage(matrices);

    for (int i = 0; i < matrices.size() / 2; i++)
    {
        multiplyy(matrices[i], matrices[i + matrices.size() / 2], size);
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;

    size_t final_memory = calculateMemoryUsage(matrices);

    outputFile << "C++," << to_string(matrices[0][0].size()) << ","
               << to_string(duration.count()) << ","
               << to_string(final_memory - initial_memory) << "," 
               << to_string(configuration) << endl;

    cout << "Multiplication took " << duration.count() << " seconds." << endl;
    outputFile.close();
}

int main(int argc, char *argv[])
{
    if (argc != 7) 
    {
        cerr << "Usage: " << argv[0] << " -s <size> -i <total_matrices> -c <configuration>" << endl;
        return 1;
    }

    int size = 0;
    int total_matrices = 0;

    for (int i = 1; i < argc; i++)
    {
        if (string(argv[i]) == "-s")
        {
            size = atoi(argv[++i]);
        }
        else if (string(argv[i]) == "-i")
        {
            total_matrices = atoi(argv[++i]);
        }
        else if (string(argv[i]) == "-c") 
        {
            configuration = atoi(argv[++i]);
        }
    }

    if (size <= 0 || total_matrices <= 0 || configuration < 0 || configuration > 5)
    {
        cerr << "Size and total matrices must be positive integers, and configuration must be between 0 and 5." << endl;
        return 1;
    }

    vector<vector<vector<int>>> matrices = parse_file(size, total_matrices);
    multiplication(matrices, size);
    return 0;
}
