from datetime import datetime
import json
from dotenv import load_dotenv
import os
import smtplib

# PDF generation class
mesocycle_text = """\
Week 1: Base Loading - Introduce all elements with moderate intensity.
Week 2: Progressive Overload - Slight increase in volume and load.
Week 3: Peak Loading - Maximize intensity; CNS stress is highest.
Week 4: Deload and Testing - Reduce volume, test performance.

Testing:
- Vertical Jump
- Broad Jump
- Flying 10m Sprint
- 5-10-5 Agility Shuttle
"""

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
START_DAY = 150

def load_program(week, day):
    with open('program.json', 'r') as f:
        program_data = json.load(f)

    week = program_data[str(week)]
    week[day]["Day"] = day
    return {
        "Week": {
            "Type": week["Type"],
            "Goal": week["Goal"],
        },
        "Day": week[day]
    }


def fmt_plan(plan):
    out = ""
    week = plan["Week"]
    day = plan["Day"]

    out += f"{week['Type']}\n{week['Goal']}\n\n"
    out += f"{day['Day']} is a {day['Type']} day, focusing on {day['Goal']}\n\n"
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
    weekday = days[datetime.now().weekday()]

    if day < START_DAY:
        print("Program not yet started")
        return


    week = 1 + ((day - START_DAY) // 7)
    plan = fmt_plan(load_program(week, weekday))

    err = send_message(PHONE, "att", plan)
    print("Errors sending:", err)

    print("Sent to ", PHONE, ":")
    print(plan)

if __name__ == "__main__":
    main()

