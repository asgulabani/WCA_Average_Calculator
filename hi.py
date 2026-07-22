print("Welcome to the WCA Official Average Calculator!")

import math # Math module for mathematical operations
import re # Regular expression module for validating time input
import platform # Used to detect the device/platform name

while True:  # Prompt the user to choose between calculating an Ao5 or Mo3 average
    print("Choose a mode:")
    print("1) Ao5 (Average of 5)")
    print("2) Mo3 (Mean of 3)")
    mode = input("Press 1 or 2: ").strip()

    if mode == "1":
        mode_name = "Ao5"
        break
    elif mode == "2":
        mode_name = "Mo3"
        break
    else:
        print("Please press 1 or 2.")

# This function converts a time value in the format "minutes:seconds" or just seconds into total seconds.
def to_seconds(value):
    text = str(value).strip()
    if ":" in text:
        minutes_str, seconds_str = text.split(":", 1)
        return float(minutes_str) * 60 + float(seconds_str)
    return float(text)

# This function checks if the input value is a valid time format.
def is_valid_time(value):
    text = str(value).strip()
    if not text:
        return False
    pattern = r"^\d+(\.\d+)?(:\d+(\.\d+)?)?$"
    return bool(re.fullmatch(pattern, text))

# Get the device name using the platform module. If the device is a Mac (Darwin), we change the name to "Apple" for a more user-friendly message.
device_name = platform.system() or "this device"
if device_name == "Darwin":
    device_name = "Apple"

# Try to get a more specific device description from the system.
try:
    machine = platform.machine()
    processor = platform.processor()
    if device_name == "Apple":
        specific_device = "Mac"
    elif machine:
        specific_device = machine
    else:
        specific_device = "device"
except Exception:
    specific_device = "device"

# Define a list of error phrases to display when the user inputs an invalid time.
error_phrases = [
    "Bro, that is not a time.",
    "Two times, man. You need to enter your time.",
    "Lock in and stop mis-typing.",
    "You have to be messing with me rn.",
    "Come on man, this is getting annoying. Can you just enter your time?",
    "STOP LACKING AND LOCK IN! ENTER YOUR TIME BROSKIES!!!",
    "Sorry about that, but can you please stop fooling around and practice cubing?",
    "You're getting close to the end, no one knows what will happen if you keep mis-typing.",
    "Don't do it. Don't reach the end. You will regret it.",
    f"You've done it. You've reached the end of the error messages. One more time and your sweet {device_name} device is cooked.",
    f"That's right, I know you have a {specific_device}. Don't make me us it against you. Enter your time.",
    "This is the last message. Hope this easter egg was worth wasting your practice time. Goodbye. For now."
]

error_index = 0
numbers = []  # empty list to store the converted numbers

if mode_name == "Ao5":
    number_of_times = 5
else:
    number_of_times = 3

for i in range(number_of_times): # loop to get the required number of times from the user
    while True:
        raw_value = input(f"Enter time #{i + 1}: ")  # get user input
        if is_valid_time(raw_value):  # check if the input is a valid time
            break  # exit the loop if the input is valid

        print(error_phrases[error_index]) # print the error message corresponding to the current index
        error_index = (error_index + 1) % len(error_phrases) # increment the error index and wrap around if it exceeds the length of the error phrases list

    num = to_seconds(raw_value)  # convert the input to seconds
    num = math.trunc(num * 100) / 100  # truncate to two decimal places
    numbers.append(num)  # add the truncated number to the list

sorted_numbers = sorted(numbers)  # sort the list of numbers in ascending order

if mode_name == "Ao5":
    middle_average = round(sum(sorted_numbers[1:4]) / 3, 2)  # calculate the average of the three middle numbers and round to two decimal places
    result_label = "Ao5"
else:
    middle_average = round(sum(sorted_numbers) / 3, 2)  # calculate the mean of the three times and round to two decimal places
    result_label = "Mo3"

print("Your times in order from best to worst", sorted_numbers)

if middle_average > 60:
    # Convert the average to minutes and seconds format
    minutes = int(middle_average // 60)
    remaining_seconds = middle_average - minutes * 60
    print(f" WCA{result_label}: {minutes}:{remaining_seconds:05.2f}")
else:
    print(f"WCA {result_label}: {middle_average:3.2f}")