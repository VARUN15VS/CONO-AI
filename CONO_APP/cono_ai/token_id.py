import os

def get_t_id():
    file_path = "C:\\Users\\harsh\\OneDrive\\Desktop\\CONO-AI\\CONO-AI\\tokenid.txt"
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()  # Read the first line and remove any leading/trailing whitespace
        return first_line
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None