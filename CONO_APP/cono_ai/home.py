from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Frame, Label
import customtkinter as ctk
from fetch_message import *
from newpeffect import *
from datetime import datetime
import time
from engine_cono import *
import threading

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\harsh\OneDrive\Desktop\CONO-AI\CONO-AI\home_assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Home(Frame):
    def __init__(self, parent, width=957, height=680):
        super().__init__(master=parent, width=width, height=height)
        self.configure(bg="#FFFFFF")

        canvas = Canvas(self, bg="#FFFFFF", height=680, width=957, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0.0, 0.0, 957.0, 680.0, fill="#000000", outline="")

        animation_frame = Frame(canvas, bg='#ffffff', width=250, height=250)
        canvas.create_window((354, 20), window=animation_frame, anchor='nw')
        MovingDots(animation_frame)

        canvas.create_line(574, 145, 674, 45, fill='#8B5DFF', width=5)
        canvas.create_line(674, 45, 684, 45, fill='#8B5DFF', width=5)

        time_frame = Frame(canvas, bg='#000000', width=200, height=85)
        canvas.create_window((684, 10), window=time_frame, anchor='nw')

        date_frame = Frame(canvas, bg='#000000', width=265, height=40)
        canvas.create_window((668, 95), window=date_frame, anchor='nw')

        time_label = ctk.CTkLabel(time_frame, text='00:00', font=('Helvetica', 64, 'bold'), text_color='#8B5DFF', fg_color='#000000')
        time_label.pack(side='top', expand=True, fill='both', padx=5)

        date_label = ctk.CTkLabel(date_frame, text='Sunday, 01 January, 2024', font=('Helvetica', 18, 'bold'), text_color='#8B5DFF', fg_color='#000000')
        date_label.pack(side='top', expand=True, fill='both')

        self.dateandtime_update(time_label, date_label)

        self.create_rounded_rectangle(canvas, 680.0, 586.0, 878.0, 636.0, radius=50, fill="#464141", outline="")
        self.create_rounded_rectangle(canvas, 90.0, 586.0, 229.0, 636.0, radius=50, fill="#464141", outline="")

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(self, image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat")
        button_1.place(x=747.0, y=586.0, width=50.0, height=50.0)

        button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))
        button_1.bind('<Enter>', lambda event: self.button_hover(event, button_1, button_image_hover_1))
        button_1.bind('<Leave>', lambda event: self.button_leave(event, button_1, button_image_1))

        message_frame = Frame(canvas, bg='#ffffff', width=850, height=250)
        canvas.create_window((50, 270), window=message_frame, anchor='nw')

        message_canvas = ctk.CTkCanvas(message_frame, bg='#000000', highlightthickness=0, width=850, height=250)
        scrollable_frame = ctk.CTkFrame(message_canvas, fg_color="#000000")
        scrollable_window = message_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        scrollable_frame.bind("<Configure>", lambda event: self.on_frame_configure(message_canvas))
        message_canvas.pack(fill='both', expand=True)
        message_canvas.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(message_canvas, event))

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        canvas.create_image(460.5, 611.0, image=entry_image_1)
        entry_1 = Entry(self, bd=0, bg="#464141", fg="#000716", highlightthickness=0)
        entry_1.place(x=204.0, y=586.0, width=513.0, height=50.0)
        entry_1.bind("<Return>", lambda event: self.add_chat_message(message_canvas, entry_1, scrollable_frame))
        self.add_chat_message_empty(message_canvas,scrollable_frame)
        
        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(self, image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("button_3 clicked"), relief="flat")
        button_3.place(x=119.0, y=586.0, width=50.0, height=50.0)

        button_image_hover_3 = PhotoImage(file=relative_to_assets("button_hover_3.png"))
        button_3.bind('<Enter>', lambda event: self.button_hover(event, button_3, button_image_hover_3))
        button_3.bind('<Leave>', lambda event: self.button_leave(event, button_3, button_image_3))
        
        state_frame = Frame(canvas, bg = '#000000', width = 400, height = 40)
        canvas.create_window((278.5,544), window=state_frame, anchor='nw')
        state_label = ctk.CTkLabel(state_frame, text = "Ask me anything!", font = ('Helvetica', 20, 'bold'), text_color = '#8B5DFF', fg_color = '#000000', width = 400)
        state_label.pack(expand = False, fill = 'y')
        
        original_text = "Ask me anything!"
        delay = 100
        self.remove_text(state_label, delay, original_text)
        
        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(self, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: self.take_command(message_canvas, entry_1, scrollable_frame, state_label), relief="flat")
        button_2.place(x=810.0, y=586.0, width=40.0, height=50.0)
        
        button_image_hover_2 = PhotoImage(file=relative_to_assets("button_hover_2.png"))
        button_2.bind('<Enter>', lambda event: self.button_hover(event, button_2, button_image_hover_2))
        button_2.bind('<Leave>', lambda event: self.button_leave(event, button_2, button_image_2))
        
        if count == 0:
            print("worked")
            increase_count()
            self.run_wish(message_canvas, entry_1, scrollable_frame)
        
        self.pack(side='left', expand=True, fill='both')
        
    def continuous_listen(self,message_canvas, entry_1, scrollable_frame):
        while True:
            detected_keyword = self.detect_keyword()  # Detect keyword in a separate function
            if detected_keyword:
                # Pause ongoing tasks, if any
                self.pause_tasks()
                
                # Listen for user command after detecting the keyword
                command_text = command()  # Replace this with your actual listening function
                self.process_command(command_text,message_canvas, entry_1, scrollable_frame)
            
            time.sleep(0.1)  # Slight delay to reduce CPU usage

    def detect_keyword(self):
        # Replace this with your actual listening/detection mechanism
        # Here, return True if any keyword like "cono" is detected
        keywords = ["cono", "hello cono", "hi cono", "okay cono", "hello kaun ho"]
        heard = listen_for_audio()  # Replace with function to get audio input
        for keyword in keywords:
            if keyword in heard.lower():
                return True
        return False

    def pause_tasks(self):
        # Logic to pause any ongoing tasks, e.g., stop animations, halt processes
        print("Pausing other tasks")

    def process_command(self, command_text,message_canvas, entry_1, scrollable_frame):
        # Process the command given by the user
        self.add_chat_message_speak(command_text, message_canvas, entry_1, scrollable_frame)
        print("Processed command:", command_text)
    
    def run_wish(self, message_canvas, entry_1, scrollable_frame):
        thread1 = threading.Thread(target=self.wish, args=(message_canvas, entry_1, scrollable_frame))
        thread1.start()
        
    def wish(self, message_canvas, entry_1, scrollable_frame):
        current_hour = datetime.now().hour
        greet = ""
        if current_hour < 12:
            greet = "Good Morning!"
        elif 12 <= current_hour < 18:
            greet = "Good Afternoon!"
        else:
            greet = "Good Evening!"
        task1 = threading.Thread(target=speak(greet))
        task1.start()
        self.add_chat_message_speak(greet, message_canvas, entry_1, scrollable_frame, sender = "cono")
        text = "I am CONO. How can i help you?"
        task2 = threading.Thread(target=speak(text))
        self.after(100, task2.start())
        self.after(100, self.add_chat_message_speak(text, message_canvas, entry_1, scrollable_frame, sender = "cono"))
        self.listening_thread = threading.Thread(target=self.continuous_listen(message_canvas, entry_1, scrollable_frame))
        self.listening_thread.daemon = True  # Daemonize thread to close with main app
        self.listening_thread.start()
        
    def take_command(self, message_canvas, entry_1, scrollable_frame, label):
        label.configure(text='Listening...')
    
        # Start listening in a new thread
        listen_thread = threading.Thread(target=self.listen_and_update, args=(message_canvas, entry_1, scrollable_frame, label))
        listen_thread.start()

    def listen_and_update(self, message_canvas, entry_1, scrollable_frame, label):
        text = command()  # Perform the command listening
        self.after(500, lambda: self.add_chat_message_speak(text, message_canvas, entry_1, scrollable_frame))  # Display message in GUI
        self.after(1000, lambda: label.configure(text='Ask me anything!'))

    def remove_text(self, state_label, delay, original_text):
        current_text = state_label.cget("text")
        if current_text:
            state_label.configure(text=current_text[:-1])
            self.after(delay, lambda: self.remove_text(state_label, delay, original_text))
        else:
            self.after(delay, lambda: self.add_text(state_label, original_text, delay))

    def add_text(self, state_label, original_text, delay):
        current_text = state_label.cget("text")
        if len(current_text) < len(original_text):
            state_label.configure(text=original_text[:len(current_text) + 1])
            self.after(delay, lambda: self.add_text(state_label, original_text, delay))
        else:
            self.after(delay, lambda: self.remove_text(state_label, delay, original_text))

    def button_hover(self, event, button, hover_image):
        button.config(image=hover_image)

    def button_leave(self, event, button, normal_image):
        button.config(image=normal_image)

    def on_frame_configure(self, canvas, event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        self.scroll_to_bottom(canvas)

    def on_mousewheel(self, canvas, event):
        canvas.yview_scroll(int(event.delta / 120), "units")

    def scroll_to_bottom(self, canvas):
        canvas.yview_moveto(1)

    def dateandtime_update(self, time_label, date_label):
        time_label.configure(text=time.strftime("%H:%M"))
        date_label.configure(text=datetime.now().strftime("%A, %d %B, %Y"))
        self.after(1000, lambda: self.dateandtime_update(time_label, date_label))
        
    def add_chat_message_speak(self, message, canvas, entry, scrollable_frame, sender="user"):
        #message = entry.get()
        if sender == "user":
            T_COLOR = "#ffffff"
        else:
            T_COLOR = "#8B5DFF"
        if message.strip():
            #bubble_color = "#8B5DFF" if sender == "user" else "#333333"
            bubble_color = '#000000'
            chat_bubble = ctk.CTkLabel(scrollable_frame, text=message, font=('Helvetica', 24), fg_color=bubble_color, text_color=T_COLOR, corner_radius=10, pady=10, padx=15, wraplength=250)
            #chat_bubble.pack(anchor="e" if sender == "user" else "w", pady=5, padx=10)
            chat_bubble.pack(anchor="center", pady=5, padx=10)
            canvas.yview_moveto(1)

    def add_chat_message(self, canvas, entry, scrollable_frame, sender="user"):
        message = entry.get()
        if message.strip():
            #bubble_color = "#8B5DFF" if sender == "user" else "#333333"
            bubble_color = '#000000'
            chat_bubble = ctk.CTkLabel(scrollable_frame, text=message, font=('Helvetica', 24), fg_color=bubble_color, text_color="white", corner_radius=10, pady=10, padx=15, wraplength=250)
            #chat_bubble.pack(anchor="e" if sender == "user" else "w", pady=5, padx=10)
            chat_bubble.pack(anchor="center", pady=5, padx=10)
            canvas.yview_moveto(1)
        entry.delete(0, 'end')

    def add_chat_message_empty(self, canvas, scrollable_frame, sender="user"):
        message = 'test test test test  test test test test test test test test test test test test test test test test test test test test test test test test test tes test test test test test test test test tes'
        if message.strip():
            #bubble_color = "#8B5DFF" if sender == "user" else "#333333"
            bubble_color = '#000000'
            chat_bubble = ctk.CTkLabel(scrollable_frame, text=message, font=('Helvetica', 24), fg_color=bubble_color, text_color="#000000", corner_radius=10, pady=10, padx=15, wraplength=820)
            chat_bubble.pack(anchor="w" if sender == "user" else "e", pady=5, padx=10)
            canvas.yview_moveto(1)
            
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        """Create a rounded rectangle on a Tkinter canvas."""
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]

        return canvas.create_polygon(points, **kwargs, smooth=True)
