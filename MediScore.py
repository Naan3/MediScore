from enum import Enum
import datetime

class Oxygen(Enum):
    AIR = 0
    OXYGEN = 2

class Consciousness(Enum):
    ALERT = 0
    CVPU = 1  # Any non-zero value represents confusion/unconsciousness

def calculate_medi_score(oxygen: Oxygen, consciousness: Consciousness, respiration_rate, spo2, temperature, cbg,
                         fasting):
    # Oxygen score
    if oxygen == Oxygen.OXYGEN:
        oxygen_score = 2
    else:
        oxygen_score = 0

    # Consciousness score
    if consciousness != Consciousness.ALERT:
        consciousness_score = 3
    else:
        consciousness_score = 0

    # Respiration rate score
    if respiration_rate <= 8:
        respiration_score = 3
    elif 9 <= respiration_rate <= 11:
        respiration_score = 2
    elif 12 <= respiration_rate <= 20:
        respiration_score = 0
    elif 21 <= respiration_rate <= 24:
        respiration_score = 2
    else:  # respiration_rate >= 25
        respiration_score = 3

    # SpO2 score
    if spo2 <= 83:
        spo2_score = 3
    elif 84 <= spo2 <= 85:
        spo2_score = 2
    elif 86 <= spo2 <= 87:
        spo2_score = 1
    elif 88 <= spo2 <= 92 or (spo2 >= 93 and oxygen == Oxygen.AIR):
        spo2_score = 0
    elif 93 <= spo2 <= 94 and oxygen == Oxygen.OXYGEN:
        spo2_score = 1
    elif 95 <= spo2 <= 96 and oxygen == Oxygen.OXYGEN:
        spo2_score = 2
    else:  # spo2 >= 97 and oxygen == Oxygen.OXYGEN
        spo2_score = 3

    # Temperature score (rounded to 1 decimal place)
    temperature = round(temperature, 1)
    if temperature <= 35.0:
        temperature_score = 3
    elif 35.1 <= temperature <= 36.0:
        temperature_score = 2
    elif 36.1 <= temperature <= 38.0:
        temperature_score = 0
    elif 38.1 <= temperature <= 39.0:
        temperature_score = 1
    else:  # temperature >= 39.1
        temperature_score = 2

    # CBG score
    if fasting:
        if cbg <= 3.4:
            cbg_score = 3
        elif 3.5 <= cbg <= 3.9:
            cbg_score = 2
        elif 4.0 <= cbg <= 5.4:
            cbg_score = 0
        elif 5.5 <= cbg <= 5.9:
            cbg_score = 1
        else:  # cbg >= 6.0
            cbg_score = 2
    else:
        if cbg <= 4.5:
            cbg_score = 3
        elif 4.5 <= cbg <= 5.8:
            cbg_score = 2
        elif 5.9 <= cbg <= 7.8:
            cbg_score = 0
        elif 7.9 <= cbg <= 8.9:
            cbg_score = 1
        else:  # cbg >= 9.0
            cbg_score = 2

    # Calculate final Medi score
    medi_score = (
            oxygen_score +
            consciousness_score +
            respiration_score +
            spo2_score +
            temperature_score +
            cbg_score
    )

    return medi_score


def get_valid_input(prompt, valid_type, valid_values=None):
    while True:
        try:
            user_input = valid_type(input(prompt))
            if valid_values and user_input not in valid_values:
                raise ValueError("Invalid selection. Please enter a valid option.")
            return user_input
        except ValueError:
            print(f"Invalid input! Please enter a valid {valid_type.__name__} value.")

# Track previous scores
previous_scores = []

file = open("past_medi_scores.txt", "a")

# Get valid inputs from user
oxygen_input = get_valid_input("Enter oxygen level (0 for air, 2 for oxygen): ", int, [0, 2])
oxygen = Oxygen(oxygen_input)

consciousness_input = get_valid_input("Enter consciousness level (0 for alert, 1 for CVPU): ", int, [0, 1])
consciousness = Consciousness(consciousness_input)

respiration_rate = get_valid_input("Enter respiration rate: ", int)
spo2 = get_valid_input("Enter SpO2 % level: ", int)
temperature = get_valid_input("Enter temperature: ", float)
fasting_status = get_valid_input("Is the patient fasting? (1 for Yes, 0 for No): ", int, [0, 1])
fasting = True if fasting_status == 1 else False
cbg = get_valid_input("Enter Capillary Blood Glucose (CBG) level: ", float)

# Calculate and display Medi Score
medi_score = calculate_medi_score(oxygen, consciousness, respiration_rate, spo2, temperature, cbg, fasting)
print(f"The patient's Medi Score is: {medi_score}")

# Store the score with timestamp
current_time = datetime.datetime.now()
previous_scores.append((medi_score, current_time))
file.write(f"{medi_score}, {current_time}\n")
file.close()

# Read previous scores from file
def read_previous_scores(filename):

    previous_scores = []
    try:
        with open(filename, "r") as file:
            for line in file:
                try:
                    score, timestamp = line.strip().split(", ")  # Split stored values
                    previous_scores.append((int(score), datetime.datetime.fromisoformat(timestamp)))
                except ValueError:
                    continue  # Skip invalid lines if any
    except FileNotFoundError:
        print(f"File {filename} not found. No previous scores available.")

    return previous_scores

previous_scores = read_previous_scores("past_medi_scores.txt")

# Check for rapid score increase within 24 hours
for past_score, past_time in previous_scores:
    time_difference = (current_time - past_time).total_seconds() / 3600  # Convert to hours
    if time_difference <= 24 and medi_score - past_score > 2:
        print("ALERT: Medi Score has increased by more than 2 points in the last 24 hours! Immediate review recommended.")
