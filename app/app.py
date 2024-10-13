import customtkinter as ctk
import os
from matplotlib import pyplot as plt
from tkinter import messagebox  

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Select Languages")
        self.geometry("400x400")

        checkbox_frame = ctk.CTkFrame(self)
        checkbox_frame.pack(pady=20)

        self.cpp_var = ctk.BooleanVar()
        self.python_var = ctk.BooleanVar()
        self.java_var = ctk.BooleanVar()

        self.cpp_checkbox = ctk.CTkCheckBox(checkbox_frame, text="C++", variable=self.cpp_var)
        self.python_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Python", variable=self.python_var)
        self.java_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Java", variable=self.java_var)

        self.cpp_checkbox.grid(row=0, column=0, padx=10)
        self.python_checkbox.grid(row=0, column=1, padx=10)
        self.java_checkbox.grid(row=0, column=2, padx=10)

        self.slider_label = ctk.CTkLabel(self, text="Iterations (2^x): 1024")
        self.slider_label.pack(pady=10)

        self.iterations_slider = ctk.CTkSlider(self, from_=6, to=13, number_of_steps=10, command=self.update_slider_label)
        self.iterations_slider.set(10)  
        self.iterations_slider.pack(pady=10)

        self.matrices_label = ctk.CTkLabel(self, text="Number of Matrices:")
        self.matrices_label.pack(pady=5)

        self.matrices_entry = ctk.CTkEntry(self, placeholder_text="Enter number of matrices")
        self.matrices_entry.pack(pady=5)

        self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.on_calculate)
        self.calculate_button.pack(pady=10)

        self.plot_button = ctk.CTkButton(self, text="Plot", command=self.on_plot)
        self.plot_button.pack(pady=10)

    def update_slider_label(self, value):
        self.slider_label.configure(text=f"Iterations (2^{int(value)}): {2**int(value)}")

    def on_calculate(self):
        size = 2
        iterations = int(self.iterations_slider.get()) 
        
        number_of_matrices = self.matrices_entry.get()
        if not number_of_matrices.isdigit():
            print("Please enter a valid number of matrices")
            return
        number_of_matrices = int(number_of_matrices)
        
        print(f"Starting calculation with {iterations} iterations and {number_of_matrices} matrices...")

        if self.cpp_var.get():
            for conf in range(6):
                for i in range(iterations):
                    print(f"Running C++ script for {number_of_matrices} matrices of size {size}")
                    self.execute_command(f"../scripts/main -s {size} -i {number_of_matrices} -c {conf}")
                    size *= 2
                size = 2

        if self.java_var.get():
            for conf in range(6):
                for i in range(iterations):
                    print(f"Running Java script for {number_of_matrices} matrices of size {size}")
                    self.execute_command(f"java ../scripts/main.java -s {size} -i {number_of_matrices} -c {conf}")
                    size *= 2
                size = 2

        if self.python_var.get():
            for conf in range(6):
                for i in range(iterations):
                    print(f"Running Python script for {number_of_matrices} matrices of size {size}")
                    self.execute_command(f"python3 ../scripts/main.py -s {size} -i {number_of_matrices} -c {conf}")
                    size *= 2
                size = 2

    def execute_command(self, command):
        os.system(command) 

    def on_plot(self):
        output_file = "../data/output.txt"

        if not os.path.exists(output_file):
            messagebox.showinfo("Info", "Please run the Calculate command first.")
            return

        with open(output_file, 'r') as f:
            content = f.readlines()

        config_map = {
            0: "ijk",
            1: "ikj",
            2: "jik",
            3: "kij",
            4: "jki",
            5: "kji",
        }

        data = {i: {'C++': ([], []), 'Python': ([], []), 'Java': ([], [])} for i in range(6)}

        max_size = 2 ** int(self.iterations_slider.get())  

        for line in content:
            language, x_value, y_value, _, config = line.split(',')
            x_value = int(x_value)
            y_value = float(y_value)
            config = int(config)

            if x_value <= max_size:
                if language == "C++":
                    data[config]['C++'][0].append(x_value)
                    data[config]['C++'][1].append(y_value)
                elif language == "python":
                    data[config]['Python'][0].append(x_value)
                    data[config]['Python'][1].append(y_value)
                elif language == "Java":
                    data[config]['Java'][0].append(x_value)
                    data[config]['Java'][1].append(y_value)

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for config in range(6):
            ax = axes[config]

            if self.cpp_var.get():
                cx, cy = data[config]['C++']
                ax.plot(cx, cy, label='C++', marker='o')

            if self.python_var.get():
                px, py = data[config]['Python']
                ax.plot(px, py, label='Python', marker='o')

            if self.java_var.get():
                jx, jy = data[config]['Java']
                ax.plot(jx, jy, label='Java', marker='o')

            ax.set_title(f'Configuration: {config_map[config]}')
            ax.set_xlabel('Matrix Size')
            ax.set_ylabel('Execution Time')
            ax.legend()
            ax.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
