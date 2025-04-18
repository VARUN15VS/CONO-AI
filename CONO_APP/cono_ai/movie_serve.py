import socket
import cv2
import pickle
import struct
import mysql.connector
from mysql.connector import Error

# Server configuration
HOST = '127.0.0.1'  # Localhost for same laptop
PORT = 9999

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

movies = 0
u_movies = 0
cono_movies = {}
user_movies = {}
cono_movies_details = {}
user_movies_details = {}

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass123',
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
        c = 1
        u = 1
                
        for i in range(1, mid1 + 1):
            cursor1.execute(f"SELECT * FROM movies WHERE mid = {i}")
            movie1 = cursor1.fetchone()
            if movie1:
                movie_names = movie1['mname']
                movie_images = movie1['imageurl']
                movie_path = movie1['movieurl']
                cono_movies_details[c]["name"] = movie_names
                cono_movies_details[c]["image"] = movie_images
                cono_movies[c] = movie_path
                c+=1
                movies += 1
                        
        for i in range(1, mid2 + 1):
            cursor2.execute(f"SELECT * FROM user_movies WHERE mid = {i}")
            movie2 = cursor2.fetchone()
            if movie2:
                user_movie_names = movie2['mname']
                user_movie_images = movie2['imageurl']
                user_movie_path = movie2['movieurl']
                user_movies_details[u]["name"] = user_movie_names
                user_movies_details[u]["image"] = user_movie_images
                user_movies[u] = user_movie_path
                u+=1
                u_movies += 1
                        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor1.close()
        cursor2.close()
        connection.close()

# Hardcoded list of movies with IDs and file paths
movies = {
    1: "path_to_movie1.mp4",
    2: "path_to_movie2.mp4"
}

# Wait for a connection from the client
client_socket, addr = server_socket.accept()
print(f"Connected to: {addr}")

# Send movie thumbnails and IDs to the client
thumbnails_and_ids = {1: "movie1_thumbnail.png", 2: "movie2_thumbnail.png"}
data = pickle.dumps(thumbnails_and_ids)
client_socket.sendall(struct.pack(">L", len(data)) + data)

# Receive movie ID from client
movie_id_data = client_socket.recv(4)
if movie_id_data:
    movie_id = struct.unpack('!I', movie_id_data)[0]
    print(f"Client requested movie ID: {movie_id}")
    
    # Stream the movie to the client
    video_path = cono_movies.get(movie_id)
    if video_path:
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Serialize the frame and send it over the socket
            data = pickle.dumps(frame)
            client_socket.sendall(struct.pack(">L", len(data)) + data)
        
        cap.release()
        print("Movie stream finished.")
    else:
        print("Movie not found.")
    
client_socket.close()
server_socket.close()