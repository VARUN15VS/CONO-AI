
message = "Hi i am cono."

def cono_message():
    global message
    return message

prev_count = 0
count = 1

def count_checker():
    global prev_count, count
    if prev_count!=count:
        prev_count = count
        return 1
    else:
        return 0