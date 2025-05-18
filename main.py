import datetime, pandas, random, smtplib, os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
MY_NAME = os.getenv("MY_NAME")

letter1 = "letter_templates/letter_1.txt"
letter2 = "letter_templates/letter_2.txt"
letter3 = "letter_templates/letter_3.txt"

letters = [letter1, letter2, letter3]

now = datetime.datetime.now()

data = pandas.read_csv("birthdays.csv")
birthday_name = ""

for _, row in data.iterrows():
    if row["day"] == now.day and row["month"] == now.month:
        birthday_name = row["name"]
        birthday_email = row["email"]

        with open(random.choice(letters), "r") as file:
            letter = file.read()
            letter = letter.replace("[NAME]", f"{birthday_name}")
            letter = letter.replace("[MY_NAME]", MY_NAME)

        with open("letter_templates/personalized_wishes.txt", "w") as file:
            file.write(letter)

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=birthday_email,
                msg="Subject:Happy Birthday!\n\n"
                    f"{letter}"
            )

        print(f"Sent birthday wishes to {birthday_name} ({birthday_email})")