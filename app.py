import math  # Math module for mathematical operations
import platform  # Used to detect the device/platform name
import re  # Regular expression module for validating time input

import streamlit as st


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


# This function formats the final result as seconds or minutes:seconds.centiseconds.
def format_result(seconds):
    if seconds > 60:
        minutes = int(seconds // 60)
        remaining_seconds = seconds - minutes * 60
        return f"{minutes}:{remaining_seconds:05.2f}"
    return f"{seconds:3.2f}"


st.set_page_config(page_title="WCA Time Calculator", page_icon="⏱️")
st.title("WCA Time Calculator")
st.write("Choose whether you want to calculate an Ao5 or an Mo3.")

if "error_index" not in st.session_state:
    st.session_state.error_index = 0

# Get the device name using the platform module. If the device is a Mac (Darwin), we change the name to "Apple" for a more user-friendly message.
device_name = platform.system() or "this device"
if device_name == "Darwin":
    device_name = "Apple"

# Try to get a more specific device description from the system.
try:
    machine = platform.machine()
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
    f"That's right, I know you have a {specific_device}. Don't make me use it against you. Enter your time.",
    "This is the last message. Hope this easter egg was worth wasting your practice time. Goodbye. For now."
]

mode = st.radio("Select a mode", ["Ao5", "Mo3"], horizontal=True)
number_of_times = 5 if mode == "Ao5" else 3

# Create text inputs so the user can enter the required number of times.
inputs = []
for i in range(number_of_times):
    inputs.append(st.text_input(f"Enter time #{i + 1}", key=f"time_{i}"))

values = []
for raw_value in inputs:
    if raw_value is None or str(raw_value).strip() == "":
        continue
    if not is_valid_time(raw_value):
        st.error(error_phrases[st.session_state.error_index])
        st.session_state.error_index = (st.session_state.error_index + 1) % len(error_phrases)
        st.stop()
    values.append(math.trunc(to_seconds(raw_value) * 100) / 100)

sorted_values = sorted(values)

if mode == "Ao5":
    if len(values) >= 5:
        result = round(sum(sorted_values[1:4]) / 3, 2)
    else:
        result = None

    if len(values) == 4:
        best_possible = round(sum(sorted_values[:3]) / 3, 2)
        worst_possible = round(sum(sorted_values[-3:]) / 3, 2)
    else:
        best_possible = None
        worst_possible = None

    label = "Average of 5"
else:
    if len(values) >= 3:
        result = round(sum(values[:3]) / 3, 2)
    else:
        result = None
    best_possible = None
    worst_possible = None
    label = "Mean of 3"

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Sorted times")
    if values:
        st.code("\n".join([f"{i + 1}. {value:.2f}" for i, value in enumerate(sorted_values)]), language="text")
    else:
        st.code("-", language="text")

with col2:
    st.markdown(f"### {label}")
    if result is not None:
        st.metric(label="Result", value=format_result(result))
    else:
        st.metric(label="Result", value="-")

if mode == "Ao5" and best_possible is not None and worst_possible is not None:
    st.markdown("### Best and worst possible")
    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="BPA", value=format_result(best_possible))
    with col4:
        st.metric(label="WPA", value=format_result(worst_possible))
else:
    if mode == "Ao5":
        st.markdown("### Best and worst possible")
        st.metric(label="BPA", value="-")
        st.metric(label="WPA", value="-")

st.caption("Times are shown in seconds and rounded to two decimal places to match WCA standards.")
