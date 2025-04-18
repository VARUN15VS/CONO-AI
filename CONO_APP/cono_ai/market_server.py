import socket
import threading
import pickle
import os
from mysql.connector import connect, Error

def get_sample_data():
    image_paths = []
    names = []
    descriptions = []
    prices = []
    total = 0

    try:
        connection = connect(
            host='localhost',
            user='root',
            password='1234',
            database='product_catalog'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products ORDER BY pid DESC LIMIT 1")
            last_product = cursor.fetchone()
            if last_product:
                last_pid = last_product['pid']
                for i in range(1, last_pid + 1):
                    cursor.execute(f"SELECT * FROM products WHERE pid = {i}")
                    product = cursor.fetchone()
                    if product:
                        product_names = product['pname']
                        purl = product['url']
                        product_desc = product['description']
                        product_price = product['price']
                        product_image_path = os.path.join(purl, "1.png")
                        if os.path.exists(product_image_path):
                            image_paths.append(product_image_path)
                            names.append(product_names)
                            descriptions.append(product_desc)
                            prices.append(product_price)
                            total += 1
                        else:
                            print(f"Image not found: {product_image_path}")
            else:
                print("No products found in the database.")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    images = []
    for img_path in image_paths:
        try:
            with open(img_path, "rb") as img_file:
                images.append(img_file.read())
        except Exception as e:
            print(f"Error reading image {img_path}: {e}")

    print("Data retrieval working")
    return {"images": images, "names": names, "prices": prices}

# Server code
"""def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen(1)
    print("Server listening on port 9999")

    while True:
        print("Waiting for a connection...")
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        try:
            data = get_sample_data()  # Get sample data to send
            serialized_data = pickle.dumps(data)
            client_socket.sendall(serialized_data)
            print("Data sent successfully.")
        except Exception as e:
            print(f"Error sending data: {e}")
        finally:
            client_socket.close()
            print("Connection closed.")"""

def start_server():
    def verify_token(token_id):
        try:
            connection = connect(
                host='localhost',
                user='root',
                password='1234',
                database='product_catalog'
            )
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                # Corrected query: Use token_id in the query
                cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE token = %s) AS id_exists", (token_id,))
                validity = cursor.fetchone()

                # Check if validity is 1 (meaning token exists)
                if validity and validity['id_exists'] == 1:
                    return True
                else:
                    return False
            else:
                return False
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen(1)
    print("Server listening on port 9999")

    while True:
        print("Waiting for a connection...")
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        try:
            # Receive token_id from client
            token_id = client_socket.recv(1024).decode('utf-8')
            print(f"Received token_id: {token_id}")

            # Verify token_id
            if verify_token(token_id):
                # Send verification success response
                client_socket.sendall("VERIFIED".encode('utf-8'))

                # Send data if verification succeeds
                data = get_sample_data()  # Function to get data to send
                serialized_data = pickle.dumps(data)
                client_socket.sendall(serialized_data)
                print("Data sent successfully.")
            else:
                # Send verification failure response
                client_socket.sendall("NOT VERIFIED".encode('utf-8'))
                print("Token verification failed.")

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            client_socket.close()
            print("Connection closed.")



if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Set to True so the server stops when the main program exits
    server_thread.start()

    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Server shutdown requested by user.")
