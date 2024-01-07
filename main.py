import customtkinter as ctk
import ttkbootstrap as ttk

class App(ctk.CTk):
    def __init__(self):

        #window
        super().__init__(fg_color = "#20B2AA")
        self.geometry("600x400")
        self.title("BMI Calculator")
        self.resizable(False, False)
        self.iconbitmap("bmi.ico")
        
        #data
        self.metric_bool = ctk.BooleanVar(value = True)
        self.height_int = ctk.IntVar(value = 170)
        self.weight_float = ctk.DoubleVar(value = 65)
        self.bmi_string = ctk.StringVar()
        self.bmi_update()

        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        BMI(self, self.bmi_string)
        UnitSwitcher(self, self.metric_bool)

        #tracing
        self.height_int.trace_add("write", self.bmi_update)
        self.weight_float.trace_add("write", self.bmi_update)
        self.metric_bool.trace_add("write", self.change_units)

        #mainloop
        self.mainloop()

        #update func
    def bmi_update(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg/ height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)

    def change_units(self, *args):
         self.height_input.update_text(self.height_int.get())
         self.weight_input.weight_update()

class BMI(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        super().__init__(parent, text = "0.0",
                           font=("Fira Code Retina", 70, "bold"),
                           textvariable = bmi_string)
        self.place(relx = 0.5, rely = 0.3, anchor = "center")

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        self.weight_float = weight_float
        self.metric_bool = metric_bool
        super().__init__(parent, fg_color = "#D7DBDD",
                         corner_radius = 10,
                          width = 400,
                          height = 90)
        self.place(relx = 0.5, rely = 0.6, anchor = "center",)

        self.plus_button = ctk.CTkButton(self, text = "+",
                      width = 50,
                      font = (("Fira Code Retina", 30)),
                      height = 25,
                      fg_color = "#E5E7E9",
                      hover_color = "#F2F3F4",
                      text_color = "black",
                      command = lambda: self.weight_update(("plus","small"))).place(relx = 0.65, rely = 0.25 )
        
        self.minus_button = ctk.CTkButton(self, text = "-",
                      width = 50,
                      font = (("Fira Code Retina", 30)),
                      height = 25,
                      fg_color = "#E5E7E9",
                      hover_color = "#F2F3F4",
                      text_color = "black",
                      command = lambda: self.weight_update(("minus","small"))).place(relx = 0.23, rely = 0.25 )
        
        self.plus_button2 = ctk.CTkButton(self, text = "+",
                      width = 75,
                      font = (("Fira Code Retina", 30)),
                      height = 60,
                      fg_color = "#E5E7E9",
                      hover_color = "#F2F3F4",
                      text_color = "black",
                      command = lambda: self.weight_update(("plus","large"))).place(relx = 0.8, rely = 0.15 )
        
        self.minus_button2 = ctk.CTkButton(self, text = "-",
                      width = 75,
                      font = (("Fira Code Retina", 30)),
                      height = 60,
                      fg_color = "#E5E7E9",
                      hover_color = "#F2F3F4",
                      text_color = "black",
                      command = lambda: self.weight_update(("minus","large"))).place(relx = 0.02, rely = 0.15 )

        self.output_string = ctk.StringVar()
        self.weight_update()

        self.weight_text = ctk.CTkLabel(self,
                        font=("Fira Code Retina", 20),
                        text_color = "black",
                        textvariable = self.output_string
                        ).place(relx = 0.5, rely = 0.5,
                                 anchor = "center")

    def weight_update(self, info = None):
        if info:

            if self.metric_bool.get() == True:
                amount = 1 if info[1] == "large" else 0.1
            else:
                 amount = 0.453592 if info[1] == "large" else 0.453592/16
            if info[0] == "plus":
                    self.weight_float.set(round(self.weight_float.get() + amount, 2))
            else:
                    self.weight_float.set(round(self.weight_float.get() - amount, 2))
        if self.metric_bool.get() == True:
            self.output_string.set(f"{self.weight_float.get()}Kg")
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f"{int(pounds)}lb {int(ounces)}oz")

class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        self.metric_bool = metric_bool
        super().__init__(parent, fg_color = "#D7DBDD",
                         corner_radius = 10,
                          width = 470,
                          height = 60)
        self.place(relx = 0.5, rely = 0.85, anchor = "center")

        self.slider = ctk.CTkSlider(self, 
                               from_ = 100,
                               to = 300,
                               width = 350,
                               height = 25,
                               orientation = "horizontal",
                               progress_color = "#6082B6",
                               fg_color = "#36454F",
                               variable = height_int,
                               command = self.update_text)
        self.slider.place(relx = 0.4, rely = 0.5, anchor = "center")

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        height_text  = ctk.CTkLabel(self, text = "100",
                                    text_color = "black",
                                    font = ("Fira Code Retina", 25, "bold"),
                                    textvariable = self.output_string)
        height_text.place(relx = 0.87, rely = 0.5, anchor = "center")
    def update_text(self, amount):
        if self.metric_bool.get() == True:
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f"{meter}.{cm}m")
        else:
             feet, inches = divmod(amount/2.54, 12)
             self.output_string.set(f"{int(feet)}\'{int(inches)}\"")
             
class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
          self.metric_bool = metric_bool
          super().__init__(parent, text = "Metric",
                               font = ("Fira Code Retina", 25, "bold"),
                               text_color = "#F1C40F")
          self.place(relx = 0.97, rely = 0.02, anchor = "ne")
          self.bind("<Button-1>", self.change_units)
    def change_units(self, event):
         if self.metric_bool.get() == True:
              self.metric_bool.set(False) 
              self.configure(text = "Imperial")
         else:
              self.metric_bool.set("True")
              self.configure(text = "Metric")

App()