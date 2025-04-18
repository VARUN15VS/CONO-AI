from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
import customtkinter as ctk
from home import *
from entertainment import *
from market import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\harsh\OneDrive\Desktop\CONO-AI\CONO-AI\side_panel_assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x680+50+0')
        self.title('CONO-AI')
        self.resizable(False, False)
        
        canvas = Canvas(self,bg = "#FFFFFF",height = 680,width = 243,bd = 0,highlightthickness = 0,relief = "ridge")

        canvas.place(x = 0, y = 0)
        side_canvas = canvas.create_rectangle(0.0,0.0,243.0,680.0,fill="#000000",outline="")
        
        frame = Frame(self, bg = '#000000', width = 957, height = 680)
        frame.place(x = 243, y = 0)
        
        Home(frame)

        image_image_1 = PhotoImage(
            file=relative_to_assets("blue_image_5.png"))
        image_1 = canvas.create_image(
            23.0,
            353.0,
            image=image_image_1
        )
         
        canvas.create_text(
            64.0,
            611.0,
            anchor="nw",
            text="Powered By",
            fill="#ffffff",
            font=("Inter", 14 * -1)
        )

        cono_text = canvas.create_text(
            49.0,
            632.0,
            anchor="nw",
            text="TEAM CONO",
            fill="#8B5DFF",
            font=("Tienne Regular", 20 * -1)
        )

        button1_frmae = Frame(canvas, bg = '#ffffff', width = 196.0, height = 60.0)
        canvas.create_window((47, 206), window = button1_frmae, anchor='nw')

        button2_frmae = Frame(canvas, bg = '#ffffff', width = 196.0, height = 60.0)
        canvas.create_window((47, 266), window = button2_frmae, anchor='nw')

        button3_frmae = Frame(canvas, bg = '#ffffff', width = 196.0, height = 60.0)
        canvas.create_window((47, 326), window = button3_frmae, anchor='nw')

        button4_frmae = Frame(canvas, bg = '#ffffff', width = 196.0, height = 60.0)
        canvas.create_window((47, 386.2), window = button4_frmae, anchor='nw')

        button1 = ctk.CTkButton(button1_frmae, corner_radius = 0, width = 196.0, height = 60.0, text = 'HOME', font = ("Helvetica", 16, "bold"),command = lambda : print("Button-1"), text_color = '#000000', fg_color = '#8B5DFF', hover_color = '#141414', state = 'normal')
        button1.pack(side = 'top', expand = True, fill = 'both')
        button2 = ctk.CTkButton(button2_frmae, corner_radius = 0, width = 196.0, height = 60.0, text = 'MARKET', font = ("Helvetica", 16, "bold"),command = lambda : print("Button-2"), text_color = '#8B5DFF', fg_color = '#000000', hover_color = '#141414', state = 'normal')
        button2.pack(side = 'top', expand = True, fill = 'both')
        button3 = ctk.CTkButton(button3_frmae, corner_radius = 0, width = 196.0, height = 60.0, text = 'ENTERTAINMENT', font = ("Helvetica", 16, "bold"),command = lambda : self.entertainment(frame), text_color = '#8B5DFF', fg_color = '#000000', hover_color = '#141414', state = 'normal')
        button3.pack(side = 'top', expand = True, fill = 'both')
        button4 = ctk.CTkButton(button4_frmae, corner_radius = 0, width = 196.0, height = 60.0, text = 'SETTINGS', font = ("Helvetica", 16, "bold"),command = lambda : print("Button-4"), text_color = '#8B5DFF', fg_color = '#000000', hover_color = '#141414', state = 'normal')
        button4.pack(side = 'top', expand = True, fill = 'both')

        image_image_2 = PhotoImage(
            file=relative_to_assets("cono logo2.png"))
        image_2 = canvas.create_image(
            122.0,
            90.0,
            image=image_image_2
        )

        image_image_3 = PhotoImage(
            file=relative_to_assets("blue_image_3.png"))
        image_3 = canvas.create_image(
            23.0,
            231.0,
            image=image_image_3
        )

        image_image_4 = PhotoImage(
            file=relative_to_assets("blue_image_4.png"))
        image_4 = canvas.create_image(
            23.0,
            292.0,
            image=image_image_4
        )

        image_image_5 = PhotoImage(
            file=relative_to_assets("blue_image_2.png"))
        image_5 = canvas.create_image(
            23.0,
            414.0,
            image=image_image_5
        )
        
        #Event Listners
        button1.bind('<Button-1>', lambda event : self.destroy_and_restore(frame, 'home'), add = '+')
        button1.bind('<Button-1>', lambda event : self.button_selected(button1, button2, button3, button4, 'yes1', canvas, side_canvas, cono_text, image_2, image_3, image_4, image_5, image_1))
        button2.bind('<Button-1>', lambda event : self.destroy_and_restore(frame, 'market'), add = '+')
        button2.bind('<Button-1>', lambda event : self.button_selected(button2, button1, button3, button4, 'yes', canvas, side_canvas, cono_text, image_2, image_3, image_4, image_5, image_1))
        button3.bind('<Button-1>', lambda event : self.destroy_and_restore(frame, 'entertainment'), add = '+')
        button3.bind('<Button-1>', lambda event : self.button_selected(button3, button2, button1, button4, 'no', canvas, side_canvas, cono_text, image_2, image_3, image_4, image_5, image_1))
        
        self.mainloop()
        
    def destroy_and_restore(self, frame, name):
        if frame is not None:
            frame.destroy()
        frame = Frame(self, bg='#000000', width=957, height=680)
        frame.place(x=243, y=0)
        if name == 'home':
            self.after(100, lambda: Home(parent=frame))  # Pass the frame as the parent
        elif name == 'entertainment':
            self.after(100, lambda: Entertainment(parent=frame))  # Pass the frame as the parent
        elif name == 'market':
            self.after(10, lambda: Market(parent=frame))
        else:
            pass
        
    def button_selected(self, button1, button2, button3, button4, special, canvas=None, side_canvas=None, c_text=None, c_image=None, h_image=None, m_image=None, s_image=None, e_image=None, event=None):
        B_COLOR = '#D9D9D9'
        T_COLOR = '#000000'
        TS_COLOR = '#000000'

        # Special condition logic
        if special == 'no':
            COLOR = '#5E5858'
            H_COLOR = '#756e6e'
            canvas.itemconfigure(side_canvas, fill=COLOR)
            canvas.itemconfigure(c_text, fill="#ffffff")

            new_image = PhotoImage(file=relative_to_assets("cono logo2.png"))
            canvas.itemconfigure(c_image, image=new_image)
            canvas.c_image_ref = new_image  # Store image reference

            h_new_image = PhotoImage(file=relative_to_assets("image_3.png"))
            canvas.itemconfigure(h_image, image=h_new_image)
            canvas.h_image_ref = h_new_image  # Store image reference

            m_new_image = PhotoImage(file=relative_to_assets("image_4.png"))
            canvas.itemconfigure(m_image, image=m_new_image)
            canvas.m_image_ref = m_new_image  # Store image reference

            s_new_image = PhotoImage(file=relative_to_assets("image_5.png"))
            canvas.itemconfigure(s_image, image=s_new_image)
            canvas.s_image_ref = s_new_image  # Store image reference

            e_new_image = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.itemconfigure(e_image, image=e_new_image)
            canvas.e_image_ref = e_new_image  # Store image reference

        elif special == "yes1":
            B_COLOR = '#8B5DFF'
            COLOR = '#000000'
            T_COLOR = '#8B5DFF'
            H_COLOR = '#141414'
            canvas.itemconfigure(side_canvas, fill=COLOR)
            canvas.itemconfigure(c_text, fill='#8B5DFF')

            h_new_image = PhotoImage(file=relative_to_assets("blue_image_3.png"))
            canvas.itemconfigure(h_image, image=h_new_image)
            canvas.h_image_ref = h_new_image  # Store image reference

            m_new_image = PhotoImage(file=relative_to_assets("blue_image_4.png"))
            canvas.itemconfigure(m_image, image=m_new_image)
            canvas.m_image_ref = m_new_image  # Store image reference

            s_new_image = PhotoImage(file=relative_to_assets("blue_image_2.png"))
            canvas.itemconfigure(s_image, image=s_new_image)
            canvas.s_image_ref = s_new_image  # Store image reference

            e_new_image = PhotoImage(file=relative_to_assets("blue_image_5.png"))
            canvas.itemconfigure(e_image, image=e_new_image)
            canvas.e_image_ref = e_new_image  # Store image reference

        else:
            COLOR = '#9B9797'
            H_COLOR = '#b8b8b8'
            canvas.itemconfigure(side_canvas, fill=COLOR)
            canvas.itemconfigure(c_text, fill="#540062")

            h_new_image = PhotoImage(file=relative_to_assets("image_3.png"))
            canvas.itemconfigure(h_image, image=h_new_image)
            canvas.h_image_ref = h_new_image  # Store image reference

            m_new_image = PhotoImage(file=relative_to_assets("image_4.png"))
            canvas.itemconfigure(m_image, image=m_new_image)
            canvas.m_image_ref = m_new_image  # Store image reference

            s_new_image = PhotoImage(file=relative_to_assets("image_5.png"))
            canvas.itemconfigure(s_image, image=s_new_image)
            canvas.s_image_ref = s_new_image  # Store image reference

            e_new_image = PhotoImage(file=relative_to_assets("image_1.png"))
            canvas.itemconfigure(e_image, image=e_new_image)
            canvas.e_image_ref = e_new_image  # Store image reference

        # Update button colors
        button1.configure(fg_color=B_COLOR, text_color=TS_COLOR)
        button2.configure(fg_color=COLOR, hover_color=H_COLOR, text_color=T_COLOR)
        button3.configure(fg_color=COLOR, hover_color=H_COLOR, text_color=T_COLOR)
        button4.configure(fg_color=COLOR, hover_color=H_COLOR, text_color=T_COLOR)
 
        
    def entertainment(self, frame):
        pass     
        
Main()