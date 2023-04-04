import smtplib, os
def testing_mail():
    MY_EMAIL = os.environ["EMAIL"]
    MY_PASSWORD = os.environ["PASSWORD"]
    TO_EMAIL = "nazajeciapythona@gmail.com"


    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=TO_EMAIL,
        msg="Subject:Spojrz w gore!\n\nISS jest w Twoim zasiegu widzenia!"
)

# testing_mail()