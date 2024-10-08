import java.io.*;
import java.util.*;

public class MatrixMultiplication {
    public static int configuration = 0; 

    public static void print3DVector(List<List<List<Integer>>> vec) {
        for (int i = 0; i < vec.size(); i++) {
            System.out.println("Layer " + i + ":");
            for (int j = 0; j < vec.get(i).size(); j++) {
                System.out.print(" Row " + j + ": ");
                for (int k = 0; k < vec.get(i).get(j).size(); k++) {
                    System.out.print(vec.get(i).get(j).get(k) + " ");
                }
                System.out.println();
            }
        }
    }

    public static List<List<List<Integer>>> parseFile(int size, int totalMatrices) {
        List<Integer> numbers = new ArrayList<>();
        String line;

        try (BufferedReader inputFile = new BufferedReader(new FileReader("data.txt"))) {
            while ((line = inputFile.readLine()) != null) {
                String[] tokens = line.trim().split("\\s+");
                for (String token : tokens) {
                    numbers.add(Integer.parseInt(token));
                }
            }
        } catch (IOException e) {
            System.err.println("Unable to open file data.txt");
            e.printStackTrace();
        }

        List<List<List<Integer>>> matrices = new ArrayList<>();

        for (int i = 0; i < totalMatrices; i++) {
            List<List<Integer>> matrix = new ArrayList<>();
            for (int j = 0; j < Math.pow(size, 2); j += size) {
                List<Integer> v = new ArrayList<>();
                for (int k = 0; k < size; k++) {
                    v.add(numbers.get(j + k));
                }
                matrix.add(v);
            }
            matrices.add(matrix);
        }

        return matrices;
    }


    public static long calculateMemoryUsage(List<List<List<Integer>>> matrices) {
        long totalSize = 0;
        totalSize += 16 * matrices.size(); 
        for (List<List<Integer>> matrix : matrices) {
            totalSize += 16 * matrix.size();
            for (List<Integer> row : matrix) {
                totalSize += 16 * row.size();
                totalSize += 4 * row.size(); 
            }
        }
        return totalSize;
    }

    public static long[][] multiply(List<List<Integer>> a, List<List<Integer>> b, int size) {
        long[][] result = new long[size][size];

        switch (configuration) {
            case 0: // ijk
                for (int i = 0; i < size; i++) {
                    for (int j = 0; j < size; j++) {
                        long sum = 0;
                        for (int k = 0; k < size; k++) {
                            sum += a.get(i).get(k) * b.get(k).get(j);
                        }
                        result[i][j] = sum;
                    }
                }
                break;

            case 1: // ikj
                for (int i = 0; i < size; i++) {
                    for (int k = 0; k < size; k++) {
                        long a_ik = a.get(i).get(k); // cache `a[i][k]`
                        for (int j = 0; j < size; j++) {
                            result[i][j] += a_ik * b.get(k).get(j);
                        }
                    }
                }
                break;

            case 2: // jik
                for (int j = 0; j < size; j++) {
                    for (int i = 0; i < size; i++) {
                        long sum = 0;
                        for (int k = 0; k < size; k++) {
                            sum += a.get(i).get(k) * b.get(k).get(j);
                        }
                        result[i][j] = sum;
                    }
                }
                break;

            case 3: // kij
                for (int k = 0; k < size; k++) {
                    for (int i = 0; i < size; i++) {
                        long a_ik = a.get(i).get(k); // cache `a[i][k]`
                        for (int j = 0; j < size; j++) {
                            result[i][j] += a_ik * b.get(k).get(j);
                        }
                    }
                }
                break;

            case 4: // jki
                for (int j = 0; j < size; j++) {
                    for (int k = 0; k < size; k++) {
                        long b_kj = b.get(k).get(j); // cache `b[k][j]`
                        for (int i = 0; i < size; i++) {
                            result[i][j] += a.get(i).get(k) * b_kj;
                        }
                    }
                }
                break;

            case 5: // kji
                for (int k = 0; k < size; k++) {
                    for (int j = 0; j < size; j++) {
                        long b_kj = b.get(k).get(j); // cache `b[k][j]`
                        for (int i = 0; i < size; i++) {
                            result[i][j] += a.get(i).get(k) * b_kj;
                        }
                    }
                }
                break;

            default: // default ijk
                for (int i = 0; i < size; i++) {
                    for (int j = 0; j < size; j++) {
                        long sum = 0;
                        for (int k = 0; k < size; k++) {
                            sum += a.get(i).get(k) * b.get(k).get(j);
                        }
                        result[i][j] = sum;
                    }
                }
                break;
        }
        return result;
    }

    public static void multiplication(List<List<List<Integer>>> matrices, int size) {
        try (PrintWriter outputFile = new PrintWriter(new FileWriter("output.txt", true))) {
            long startTime = System.nanoTime();

            long initialMemory = calculateMemoryUsage(matrices);
            
            for (int i = 0; i < matrices.size() / 2; i++) {
                multiply(matrices.get(i), matrices.get(i + matrices.size() / 2), size);
            }
            long endTime = System.nanoTime();
            double duration = (endTime - startTime) / 1e9; 
            
            long finalMemory = calculateMemoryUsage(matrices);
            
            outputFile.println("Java," + size + "," + duration + "," + (finalMemory - initialMemory) + "," + configuration);
            System.out.println("Multiplication took " + duration + " seconds.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        if (args.length != 6) {
            System.err.println("Usage: java MatrixMultiplication -s <size> -i <total_matrices> -c <configuration>");
            System.exit(1);
        }

        int size = 0;
        int totalMatrices = 0;

        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("-s")) {
                size = Integer.parseInt(args[++i]);
            } else if (args[i].equals("-i")) {
                totalMatrices = Integer.parseInt(args[++i]);
            } else if (args[i].equals("-c")) {
                configuration = Integer.parseInt(args[++i]);
            }
        }

        if (size <= 0 || totalMatrices <= 0 || configuration < 0 || configuration > 5) {
            System.err.println("Size and total matrices must be positive integers, and configuration must be between 0 and 5.");
            System.exit(1);
        }

        List<List<List<Integer>>> matrices = parseFile(size, totalMatrices);
        multiplication(matrices, size);
    }
}
