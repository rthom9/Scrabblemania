import time
import tkinter
from tkinter import messagebox

def set_timer(total_time, reminder1="000000", reminder2="000000"):
    """Users must provide time arguments in HHMMSS format"""
    "If timer already running, will cancel it."
    cancel_timer()
    if validate_user_input(total_time) and validate_user_input(reminder1) and validate_user_input(reminder2):
        controller_file = open('controller.txt', 'w+', encoding='utf-8')
        controller_file.write("stop")
        time_file = open('time.txt', 'w+', encoding='utf-8')
        time_file.seek(0)
        time_file.truncate()
        time_file.write(str(total_time) + str(reminder1) + str(reminder2))
        time_file.close()
        alerts_file = open('alerts.txt', 'w+', encoding='utf-8')
        alerts_file.close()
    else:
        raise TypeError("Inappropriate argument types")

def validate_user_input(user_input):
    if user_input.isnumeric() and len(user_input) == 6:
        return True
    else:
        return False

def start_timer():
    with open('controller.txt', 'r+', encoding='utf-8') as controller_file:
        controller_file.seek(0)
        controller_file.truncate()
        controller_file.write("run")

def pause_timer():
    with open('controller.txt', 'w+', encoding='utf-8') as controller_file:
        controller_file.seek(0)
        controller_file.truncate()
        controller_file.write("stop")

def cancel_timer():
    """Upon form submission"""
    with open('controller.txt', 'w+', encoding='utf-8') as controller_file:
        controller_file.seek(0)
        controller_file.truncate()
        controller_file.write("stop")
    with open('time.txt', 'w+', encoding='utf-8') as time_file:
        time_file.seek(0)
        time_file.truncate()
        time_file.write("000000000000000000")

def monitor_timer(reminder_time_1="000000", reminder_time_2="000000"):
    root = tkinter.Tk()
    root.withdraw()
    while True:
        with open('alerts.txt', 'r+', encoding='utf-8') as alerts_file:
            alert = alerts_file.read()
            if alert == "0s":
                break
            if alert == reminder_time_1:
                messagebox.showinfo("Alert", f"You have {reminder_time_1} seconds remaining.")
            if alert == reminder_time_2:
                messagebox.showinfo("Alert", f"You have {reminder_time_2} seconds remaining.")
                alerts_file.write("")
    print("")
    print("\nTime is up! Press [ENTER].")
    root.wm_attributes("-topmost", 1)
    messagebox.showinfo(title="Alert", message="You are out of time. Game has ended.", parent=root)

