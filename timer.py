import time
import os.path


def time_converter(time_string):
    hours_int = int(time_string[0:2])
    minutes_int = int(time_string[2:4])
    seconds_int = int(time_string[4:6])
    total_seconds = (hours_int * 3600) + (minutes_int * 60) + seconds_int
    return total_seconds


def timer_countdown(countdown_time, reminder_1, reminder_2):
    while countdown_time:
        with open('controller.txt', 'r+', encoding='utf-8') as controller_file:
            command = controller_file.read()

        if command == "run":
            print(countdown_time)
            time.sleep(1)
            countdown_time -= 1

            if countdown_time == reminder_1 and reminder_2 != 0:
                with open('alerts.txt', 'w+', encoding='utf-8') as alerts_file:
                    #alerts_file.seek(0)
                    #alerts_file.truncate()
                    alerts_file.write(str(reminder_1) + "s")
                print("You have " + str(reminder_1) + " seconds left.")
            if countdown_time == reminder_2 and reminder_1 != 0:
                with open('alerts.txt', 'w+', encoding='utf-8') as alerts_file:
                    #alerts_file.seek(0)
                    #alerts_file.truncate()
                    alerts_file.write(str(reminder_2) + "s")
                print("You have " + str(reminder_2) + " seconds left.")
            if countdown_time == 0:
                with open('alerts.txt', 'w+', encoding='utf-8') as alerts_file:
                    #alerts_file.seek(0)
                    #alerts_file.truncate()
                    alerts_file.write(str(0) + "s")
                print("Time is up!")
                # change controller.txt to stop
                with open('controller.txt', 'r+', encoding='utf-8') as controller_file:
                    controller_file.seek(0)
                    controller_file.truncate()
                    controller_file.write("stop")
                with open('time.txt', 'r+', encoding='utf-8') as time_file:
                    time_file.seek(0)
                    time_file.truncate()
                    time_file.write("000000000000000000")
        if command == "reset":
            break
    return


while True:
    if os.path.isfile("controller.txt"):
        with open('controller.txt', 'r+', encoding='utf-8') as controller_file:
            controller_command = controller_file.read()
            if controller_command == "run":
                with open('time.txt', 'r+', encoding='utf-8') as time_file:
                    time_data = time_file.read()
                    time_file.seek(0)
                    time_file.truncate()
                    time_file.write("000000000000000000")
                countdown_start = time_converter(time_data[0:6])
                prompt_1 = time_converter(time_data[6:12])
                prompt_2 = time_converter(time_data[12:18])
                timer_countdown(countdown_start, prompt_1, prompt_2)



