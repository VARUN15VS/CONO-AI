import customtkinter as ctk
import time
import threading
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MovingDots(ctk.CTkFrame):
    def __init__(self, parent, height = 250, width = 250):
        super().__init__(master = parent, height = height, width = width)
        self.canvas = ctk.CTkCanvas(self, width=250, height=250, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.canvas.create_text(125, 125, text="CONO", fill="#8B5DFF", font=("Arial", 24, "bold"))

        self.create_arcs()

        self.dots = []
        self.create_dots()
        self.animate_dots()
        
        self.pack(side = 'top', expand = True, fill = 'both')

    def create_arcs(self):
        """Create 4 disconnected arcs to form a circle."""
        radius = 120
        center_x = 125
        center_y = 125

        arc_extent = 90
        self.canvas.create_arc(center_x - radius, center_y - radius,
                               center_x + radius, center_y + radius,
                               start=0, extent=arc_extent, style="arc", outline="#8B5DFF", width=3)
        
        self.canvas.create_arc(center_x - radius, center_y - radius,
                               center_x + radius, center_y + radius,
                               start=120, extent=arc_extent, style="arc", outline="#8B5DFF", width=3)
        
        self.canvas.create_arc(center_x - radius, center_y - radius,
                               center_x + radius, center_y + radius,
                               start=240, extent=arc_extent, style="arc", outline="#8B5DFF", width=3)

        self.canvas.create_arc(center_x - radius, center_y - radius,
                               center_x + radius, center_y + radius,
                               start=360, extent=arc_extent, style="arc", outline="#8B5DFF", width=3)

    def create_dots(self):
        radius = 100
        center_x = 125
        center_y = 125
        num_dots = 30

        for i in range(num_dots):
            angle = (i / num_dots) * 2 * math.pi
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            dot = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#8B5DFF", outline="")
            self.dots.append(dot)

    def animate_dots(self):
        def move_dots():
            for i in range(len(self.dots)):
                angle = (i / len(self.dots)) * 2 * math.pi
                speed = 0.02 + 0.01 * i
                x = 125 + 100 * math.cos(angle + speed * time.time())
                y = 125 + 100 * math.sin(angle + speed * time.time())
                self.canvas.moveto(self.dots[i], x - 3, y - 3)
            self.after(10, move_dots)

        move_dots()