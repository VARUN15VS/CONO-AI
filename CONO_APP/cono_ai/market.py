from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Frame, Label
import customtkinter as ctk
from io import BytesIO
from PIL import Image, ImageTk
import socket
import threading
import pickle
from token_id import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\harsh\OneDrive\Desktop\CONO-AI\CONO-AI\market_assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Market(Frame):
    def __init__(window, parent, width = 957, height = 680):
        super().__init__(master = parent, width = width, height = height)
        #window = Tk()
        
        window.configure(bg = "#FFFFFF")

        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 680,
            width = 957,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            957.0,
            680.0,
            fill="#8A7474",
            outline=""
        )
        
        window.create_rounded_rectangle(canvas, 270.0, 35.0, 895.0, 85.0, radius = 50, fill = "#464141", outline = "")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            window,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=767.0,
            y=35.0,
            width=50.0,
            height=50.0
        )

        button_image_hover_1 = PhotoImage(
            file=relative_to_assets("button_hover_1.png"))

        button_1.bind('<Enter>', lambda event : window.button_1_hover(event, button_1, button_image_hover_1))
        button_1.bind('<Leave>', lambda event : window.button_1_leave(event, button_1, button_image_1))

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            window,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=830.0,
            y=35.0,
            width=40.0,
            height=50.0
        )

        button_image_hover_2 = PhotoImage(
            file=relative_to_assets("button_hover_2.png"))

        button_2.bind('<Enter>', lambda event : window.button_2_hover(event, button_2, button_image_hover_2))
        button_2.bind('<Leave>', lambda event : window.button_2_leave(event, button_2, button_image_2))

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            527.5,
            60.0,
            image=entry_image_1
        )
        entry_1 = Entry(
            window,
            bd=0,
            bg="#464141",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=318.0,
            y=35.0,
            width=419.0,
            height=48.0
        )

        canvas.create_rectangle(
            20.0,
            162.0,
            922.0005493164062,
            162.0,
            fill="#000000",
            outline=""
        )

        canvas.create_text(
            27.0,
            0.0,
            anchor="nw",
            text="CONO",
            fill="#FFFFFF",
            font=("Lalezar Regular", 64 * -1)
        )

        canvas.create_text(
            120.0,
            56.0,
            anchor="nw",
            text="MARKET",
            fill="#000000",
            font=("Lalezar Regular", 36 * -1)
        )

        frame = Frame(canvas, bg = "#8A7474", width = 903, height = 512)
        canvas.create_window((20, 170), window = frame, anchor = 'nw')

        inner_canvas = Canvas(
            frame,
            bg = "#8A7474",
            height = 507,
            width = 903,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        inner_canvas.place(x=0, y=0)

        scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=inner_canvas.yview)
        scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')
        inner_canvas.configure(yscrollcommand = scrollbar.set)

        cloth_frame = Frame(inner_canvas, bg = "#8A7474")
        inner_canvas.create_window((0,0), window=cloth_frame, anchor='nw')
        window.bind('<MouseWheel>', lambda event : inner_canvas.yview_scroll(-int(event.delta/60), "units"))

        ad_frame = Frame(canvas, bg = '#ffffff', width = 200, height = 490)
        canvas.create_window((702, 184), window = ad_frame, anchor='nw')
        
        t_id = get_t_id()
        window.start_client(cloth_frame, t_id)

        window.update_scrollregion(inner_canvas, cloth_frame)

        window.pack(side = 'left', expand = True, fill = 'both')
        #window.resizable(False, False)
        #window.mainloop()

    def update_scrollregion(self, canvas, frame):
        frame.update_idletasks()  # Ensure all widgets are rendered
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)  # Start at the top
        
    def start_client(self, frame, token_id):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))

        try:
            # Send token_id to the server for verification
            client.sendall(token_id.encode('utf-8'))

            # Receive verification response from server
            verification_status = client.recv(1024).decode('utf-8')
            if verification_status != "VERIFIED":
                print("Token verification failed.")
                client.close()
                return  # Exit if token is not verified

            # If token is verified, proceed to receive data
            received_data = b""
            while True:
                part = client.recv(4096)
                if not part:
                    break
                received_data += part

            data = pickle.loads(received_data)  # Deserialize received data
            self.add_cloth_frame(frame, data)

        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client.close()

    def add_cloth_frame(self, frame, data):
        images = data["images"]
        pnames = data["names"]
        prices = data["prices"]

        # Store image references
        self.photos = []
        
        frame.update_idletasks()

        panel_frame = Frame(frame, bg="#8A7474")
        panel_frame.pack(expand=True, fill='both')

        for i, (image_data, pname, price) in enumerate(zip(images, pnames, prices)):
            image = Image.open(BytesIO(image_data))
            image = image.resize((200, 175), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)  # Keep reference to avoid garbage collection

            # Frame to hold the image and its details
            specific_frame = Frame(panel_frame, bg="#8A7474", height=300, width=280)
            specific_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)

            # Canvas for displaying the image
            new_canvas = Canvas(specific_frame, bg="#8A7474", width=200, height=175, bd=0,
                                highlightthickness=0, relief="ridge")
            new_canvas.create_image(100, 88, image=photo)
            new_canvas.pack(side='top', pady=5)

            # Box to contain the product details
            detail_box = Frame(specific_frame, bg="#464141", height=100, width=200)
            detail_box.pack(side='top', fill='x')

            # Product name
            label_name = Label(detail_box, text=pname, bg="#464141", fg="#FFFFFF")
            label_name.pack(pady=(10, 0))

            # Product price
            label_price = Label(detail_box, text=f"Price: {price}", bg="#464141", fg="#FFFFFF")
            label_price.pack()

            # 'See' button
            see_button = ctk.CTkButton(detail_box, text="See", fg_color="blue", text_color="#ffffff", command=lambda: print(f"See {pname}"))
            see_button.pack(pady=(5, 10))

    def button_1_hover(self, event, button_1, button_image_hover_1):
        button_1.config(
            image=button_image_hover_1
        )
    def button_1_leave(self, event, button_1, button_image_1):
        button_1.config(
            image=button_image_1
        )
    def button_2_hover(self, event, button_2, button_image_hover_2):
        button_2.config(
            image=button_image_hover_2
        )
    def button_2_leave(self, event, button_2, button_image_2):
        button_2.config(
            image=button_image_2
        )
    
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
        