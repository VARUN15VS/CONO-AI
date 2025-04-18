from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Label, font
import customtkinter as ctk
from VideoPlayer import *
import mysql.connector
from mysql.connector import Error

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\harsh\OneDrive\Desktop\CONO-AI\CONO-AI\entertainment_assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Entertainment(Frame):
    def __init__(window, parent, width = 957, height = 680):
        super().__init__(master = parent, width = width, height = height)
        window.configure(bg = "#FFFFFF")
        
        movies = 0
        user_movies = 0
        movie_name = []
        movie_image =[]
        movie_url =[]
        user_movie_name =[]
        user_movie_image =[]
        user_movie_url =[]
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='product_catalog'
            )
            if connection.is_connected():
                cursor1 = connection.cursor(dictionary=True)
                cursor2 = connection.cursor(dictionary=True)
                cursor1.execute("SELECT * FROM movies ORDER BY mid DESC LIMIT 1")
                last_movie = cursor1.fetchone()
                cursor2.execute("SELECT * FROM user_movies ORDER BY mid DESC LIMIT 1")
                last_user_movie = cursor2.fetchone()
                mid1 = last_movie['mid']
                mid2 = last_user_movie['mid']
                
                for i in range(1, mid1 + 1):
                    cursor1.execute(f"SELECT * FROM movies WHERE mid = {i}")
                    movie1 = cursor1.fetchone()
                    if movie1:
                        movie_names = movie1['mname']
                        movie_images = movie1['imageurl']
                        movie_path = movie1['movieurl']
                        movie_name.append(movie_names)
                        movie_image.append(movie_images)
                        movie_url.append(movie_path)
                        movies += 1
                        
                for i in range(1, mid2 + 1):
                    cursor2.execute(f"SELECT * FROM user_movies WHERE mid = {i}")
                    movie2 = cursor2.fetchone()
                    if movie2:
                        user_movie_names = movie2['mname']
                        user_movie_images = movie2['imageurl']
                        user_movie_path = movie2['movieurl']
                        user_movie_name.append(user_movie_names)
                        user_movie_image.append(user_movie_images)
                        user_movie_url.append(user_movie_path)
                        user_movies += 1
                        
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor1.close()
                cursor2.close()
                connection.close()

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
            fill="#413C3C",
            outline="")
        
        window.create_rounded_rectangle(canvas, 658.0, 35.0, 870.0, 85.0, radius = 50, fill = "#706969", outline="")
        
        cono_font = font.Font(family="Lalezar Regular", size = 40, weight="bold")
        
        canvas.create_text(
            27.0,
            7.0,
            anchor="nw",
            text="CONO",
            fill="#F22929",
            font=cono_font
        )

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
            x=736.0,
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
            x=799.0,
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
            465.5,
            60.0,
            image=entry_image_1
        )
        entry_1 = Entry(
            window,
            bd=0,
            bg="#706969",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=215.0,
            y=35.0,
            width=501.0,
            height=48.0
        )

        canvas.create_rectangle(
            37.999725341796875,
            135.5,
            941.0002746582031,
            136.5,
            fill="#FFFFFF",
            outline="")

        canvas.create_rectangle(
            38.0,
            368.0,
            941.0005493164062,
            369.0,
            fill="#FFFFFF",
            outline="")

        canvas.create_rectangle(
            38.0,
            600.5,
            941.0005493164062,
            601.5,
            fill="#FFFFFF",
            outline="")

        canvas.create_text(
            30.0,
            56.0,
            anchor="nw",
            text="MOVIES",
            fill="#DEC1C1",
            font=("Lalezar Regular", 32 * -1)
        )

        canvas.create_text(
            49.0,
            155.0,
            anchor="nw",
            text="CONO MOVIES",
            fill="#FFFFFF",
            font=("Tienne Regular", 20 * -1)
        )

        canvas.create_text(
            49.0,
            391.0,
            anchor="nw",
            text="YOUR SECTION",
            fill="#FFFFFF",
            font=("Tienne Regular", 20 * -1)
        )
        
        cono_movie_frame = Frame(canvas, bg = '#ffffff', width = 897, height = 166)
        canvas.create_window((40,180), window = cono_movie_frame, anchor = 'nw')
        
        scroll_canvas = Canvas(cono_movie_frame, bg="#413C3C", width=897, height=166, bd=0, highlightthickness=0, relief="ridge")
        scroll_canvas.pack(side='left', fill='both', expand=True)
        
        content_frame = Frame(scroll_canvas, bg="#413C3C")
        scroll_canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        for i in range(0, movies):
            window.movie_frame(content_frame, movie_image[i], movie_name[i], movie_url[i])
        
        user_movie_frame = Frame(canvas, bg = "#413C3C", width = 897, height = 166)
        canvas.create_window((40,420), window = user_movie_frame, anchor = 'nw')
        
        user_scroll_canvas = Canvas(user_movie_frame, bg="#413C3C", width=897, height=166, bd=0, highlightthickness=0, relief="ridge")
        user_scroll_canvas.pack(side='left', fill='both', expand=True)
        
        user_content_frame = Frame(user_scroll_canvas, bg="#413C3C")
        user_scroll_canvas.create_window((0, 0), window=user_content_frame, anchor='nw')
        
        for i in range(0, user_movies):
            window.movie_frame(user_content_frame, user_movie_image[i], user_movie_name[i], user_movie_url[i])
        
        window.pack(side = 'left', expand = True, fill = 'both')

    def button_2_hover(self, event, button_2, button_image_hover_2):
        button_2.config(
            image=button_image_hover_2
        )
    def button_2_leave(self, event, button_2, button_image_2):
        button_2.config(
            image=button_image_2
        )
    def button_1_hover(self, event, button_1, button_image_hover_1):
        button_1.config(
            image=button_image_hover_1
        )
    def button_1_leave(self, event, button_1, button_image_1):
        button_1.config(
            image=button_image_1
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
    
    def play_movie(self, movie_url):
        VideoPlayer(movie_url)
        #PlayVideo(movie_url)
    def movie_frame(self, c_frame, poster, m_text, movie_url):
        frame = Frame(c_frame, width=500, height=166, bg="#413C3C")
        frame.pack(side='left', fill='y', padx=5)
    
        # Create a canvas to hold the image and other widgets
        canvas = Canvas(frame, bg="#413C3C", height=166, width=600, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
    
        try:
            movie_image = PhotoImage(file=poster)
            canvas.create_image(0, 0, image=movie_image, anchor='nw')  # Ensure anchor is set to 'nw' (top-left)
        # Store the reference in a list or dictionary
            if not hasattr(self, 'image_refs'):
                self.image_refs = []
            self.image_refs.append(movie_image)
        except Exception as e:
            print(f"Failed to load image {poster}: {e}")
    
    # Create a sub-frame for text and button within the canvas
        sub_frame = Frame(canvas, bg='#000000', height=166, width=200)
        sub_frame.pack_propagate(False)
        canvas.create_window((300, 0), window=sub_frame, anchor='nw')  # Correctly position the sub-frame
    
    # Add a label for movie text
        label = Label(sub_frame, text=m_text, font=('Helvetica', 16, 'bold'), bg='#000000', fg='#ffffff', wraplength=180)
        label.pack(side='top', fill='x', padx=2, pady=10)
    
    # Add a button to play the movie
        button = ctk.CTkButton(sub_frame, text='PLAY', font=('Helvetica', 16, 'bold'), fg_color='blue', text_color='#ffffff',
                    command=lambda: self.play_movie(movie_url))
        button.pack(side='bottom', fill='none', pady=5)
        