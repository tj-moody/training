from datetime import datetime
import json
from dotenv import load_dotenv
import os
import smtplib

days = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PHONE = os.getenv("PHONE")
START_DAY = 153

def load_program(training_day):
    week = 1 + (training_day // 7)
    day = days[training_day % 7]
    with open('program.json', 'r') as f:
        program_data = json.load(f)

    week = program_data[str(week)]
    week[day]["Day"] = day
    return {
        "Week": {
            "Type": week["Type"],
            "Goal": week["Goal"],
        },
        "Day": week[day],
        "Training Day": training_day,
    }


def fmt_plan(plan):
    training_day = plan["Training Day"]
    week = plan["Week"]
    day = plan["Day"]
    out = ""
    out += f"Day {training_day+1} of this training cycle.\n\n"
    out += f"{week['Type']}\n{week['Goal']}\n\n"
    out += f"{day['Day']} is a {day['Type']} day, focusing on {day['Goal']}.\n\n"
    out += "Today's workload: \n"
    for exercise, volume in day["Work"].items():
        out += exercise + ": " + volume + "\n"
    return out

def send_message(phone_number, carrier, message):
    if EMAIL is None or PASSWORD is None:
        return None

    recipient = phone_number + CARRIERS[carrier]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    return server.sendmail(EMAIL, recipient, message)

def main():
    day = datetime.now().timetuple().tm_yday
    day = 153
    if day < START_DAY:
        print("Program not yet started")
        return

    training_day = day - START_DAY
    plan = fmt_plan(load_program(training_day))

    if PHONE is None:
        print("Error: no phone number found. Supply PHONE value in .env")
        return

    err = send_message(PHONE, "att", plan)
    print("Errors sending:", err)

    print("Sent to ", PHONE, ":")
    print(plan)

if __name__ == "__main__":
    main()
