import customtkinter as ctk
import os
from matplotlib import pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("yes")
        self.geometry("300x200")

        self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.on_calculate)
        self.calculate_button.pack(pady=10)

        self.integer_input = ctk.CTkEntry(self, placeholder_text="Enter an integer")
        self.integer_input.pack(pady=10)

        self.plot_button = ctk.CTkButton(self, text="Plot", command=self.on_plot)
        self.plot_button.pack(pady=10)

    def on_calculate(self):
        size = 2
        number_of_matrices = 100
        print("Starting...")
        print("multiplication in progress...")
        
        for conf in range(6):
            for i in range(8):
                print(f"running C++ script for {number_of_matrices} matrices of size {size}")
                self.execute_command(f"./main -s {size} -i {number_of_matrices} -c {conf}")
                size *= 2
            size = 2
        
        for conf in range(6):
            for i in range(8):
                print(f"running java script for {number_of_matrices} matrices of size {size}")
                self.execute_command(f"java main.java -s {size} -i {number_of_matrices} -c {conf}")
                size *= 2
            size = 2
        
        for conf in range(6):
            for i in range(8):
                print(f"running python script for {number_of_matrices} matrices of size {size}")
                self.execute_command(f"python3 main.py -s {size} -i {number_of_matrices} -c {conf}")
                size *= 2
            size = 2
            
    def execute_command(self, command):
        os.system(command) 
        

    def on_plot(self):
        f = open("output.txt", 'r')
        content = f.readlines()
        meh = [line.split(',') for line in content]
        
        config_map = {
            0: "ijk",
            1: "ikj",
            2: "jik",
            3: "kij",
            4: "jki",
            5: "kji",
        }
        

        data = {i: {'C++': ([], []), 'Python': ([], []), 'Java': ([], [])} for i in range(6)}


        for i in meh:
            language = i[0]
            x_value = int(i[1])
            y_value = float(i[2])
            config = int(i[4])
            
            if language == "C++":
                data[config]['C++'][0].append(x_value)
                data[config]['C++'][1].append(y_value)
            elif language == "python":
                data[config]['Python'][0].append(x_value)
                data[config]['Python'][1].append(y_value)
            elif language == "Java":
                data[config]['Java'][0].append(x_value)
                data[config]['Java'][1].append(y_value)

        f.close()


        fig, axes = plt.subplots(2, 3, figsize=(15, 10)) 
        axes = axes.flatten() 


        for config in range(6):
            ax = axes[config]  
            cx, cy = data[config]['C++']
            px, py = data[config]['Python']
            jx, jy = data[config]['Java']
            
            ax.plot(cx, cy, label='C++', marker='o')
            ax.plot(px, py, label='Python', marker='o')
            ax.plot(jx, jy, label='Java', marker='o')
            
            ax.set_title(f'Configuration: {config_map[config]}')
            ax.set_xlabel('X Axis (Second Field)')
            ax.set_ylabel('Y Axis (Third Field)')
            ax.legend()
            ax.grid(True)

        plt.tight_layout()  
        plt.show()        

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
