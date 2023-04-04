from myFuncs import goodInput, checking
import requests
from datetime import datetime
import smtplib
import time
import os

# Program składa się z 4 części:
# 1. Pobiera podany adres i pozyskuje dzięki pierwszego API lokalizacje geograficzną.
# 2. Dzięki drugiego API sprawdzane jest kiedy jest wschód i zachód słońca w danym regionie. Na tej podstawie określane są godziny zmroku, czyli potencjalna możliwość obserwacji ISS.
# 3. Trzecie API służy do namierzania lokalizacji geograficznej ISS w czasie rzeczywistym.
# 4. Jeśli w danym regionie jest ciemno i ISS znajduje się w podawanym na samym początku zakresie zasięgu, wysyła informacje na wybranego maila.
# Każda wartość podawana przez użytkownika jest weryfikowana pod względem poprawności. W przypadku błędnego adresu, zwracany jest HTTPError, bezpośrednio ze strony z której pozyskujemy informacje.

# W ramach projektu stworzyłem maila o loginie si haśle poniżej. Aby umożliwić wysyłanie maili z konta Gmaila poprzez Pythona należy najpierw obniżyć poziom zabezpieczeń konta.
# W tym celu włączyłem "dostęp mniej bezpiecznych aplikacji" w ustawieniach konta oraz upewniłem się, że nie ma żadnych weryfikacji dwuetapowych.

MY_EMAIL = os.environ["EMAIL"]
MY_PASSWORD = os.environ["PASSWORD"]
to_mail = "nazajeciapythona@gmail.com"

clear = lambda: os.system('cls')  # clear() - czysci konsole
clear()

print("Witaj w ISS Trackerze!")
address = input("\n👇 Podaj swoj adres w nastepujacym formacsie 👇 Nie podawaj miasta 👇  \n{ulica} {numer domu/mieszkania}, {kod pocztowy}. np. 'Cyprysowa 52, 02-265':\n")
print("")
degreeRange = 5
print("Domyslna i optymalna wartosc zakresu sprawdzania widzenia ISS od wybranej lokalizacji wynosi 5 stopni geograficznych. Mozesz jednak ja zwiekszyc.")
choice = goodInput("Wpisz o ile stopni chcesz zwiększyć zasięg sprawdzania lub wciśnij ENTER: ", list_of_choices=[""], checkForDigit=True)
if choice.isdigit():
    degreeRange += int(choice)
print("")
ask_for_mail = goodInput("Czy chcesz wiadomość na swojego maila? (bezpieczne) 'Y'/'N': ", ["y","n"], True)
if ask_for_mail == "y":
    your_mail = input("Podaj swojego maila: ")
    correct_mail = False
    while not correct_mail:
        answer = goodInput(f"Czy mail się zgadza: '{your_mail}' ?  'Y'/'N': ", ["y","n"], True)
        if answer == "y":
            correct_mail = True
        else:
            your_mail = input("Podaj swojego maila: ")
    to_mail = your_mail
    print(f"\nTak długo jak program będzie włączony:\nJeśli ISS będzie w zasięgu widzenia, program wyśle powiadomienie na Twój adres mailowy: {to_mail}")
else:
    print("\nTak długo jak program będzie włączony:\nJeśli ISS będzie w zasięgu widzenia program wyśle powiadomienie na adres mailowy: \nLogin: nazajeciapythona@gmail.com \nHasło: H3&6c7N#Ik\n")
goodInput("Wciśnij ENTER aby rozpocząć.", [""])


parameters = {
    'access_key': '29483cab8847a0721124c84888e946fb',
    'query': address,
    'limit': 1,
    }
response = requests.get("http://api.positionstack.com/v1/forward", parameters)
response.raise_for_status()
data = response.json()
MY_LAT = data["data"][0]["latitude"]
MY_LONG = data["data"][0]["longitude"]

def is_night():
    """ Na podstawie szerokości i długości geograficznych, korzystając z API udostępniającej wschód i zachód słońca, w zależnośći od położenia, sprawdza kiedy jest ciemno, a kiedy jasno. 
    Zwraca True jeśli jest noc (czyli można zaobserwować ISS) """
    parameters = {
        "lat": MY_LAT,  
        "lng": MY_LONG,
        "formatted": 0,  # Dla wartości 0 parametru formatted zwraca nam czas uniksowy, taki sam jaki zwraca nam funkcja "datetime"
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])  # Po zmienieniu parametru "formated" na 0 należy zwrócony wynik odpowiednio sformatować, aby był taki sam
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])    # jak zwraca funkcja "datetime". Z wyniku chcemy TYLKO godzine. E.g. "2015-05-21T05:05:35+00:00"

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

def is_iss_overhead():
    """ Zwraca True jeśli ISS jest w zasięgu 5 stopni od wybranego położenia geograficznego """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # Zwraca HTTPError jeśli powstał error podczas uzyskiwania url
    data = response.json()  

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    clear()

    checking()
    print(f"Your position: {MY_LAT}   {MY_LONG}")
    print(f"ISS  position: {iss_latitude}     {iss_longitude}")

    # Jeśli podana pozycja jest w zakresie +5 albo -5 stopni od pozycji ISS zwraca True. 
    if MY_LAT-degreeRange <= iss_latitude <= MY_LAT+degreeRange and MY_LONG-degreeRange <= iss_longitude <= MY_LONG+degreeRange:
        return True

x = 0  # Gdy ISS będzie w zasięgu, program wyśle maila RAZ i gdy nadal będzie w zasięgu, nie będzie wysyłać dalej co sekunde maili, tylko gdy x wzrośnie do 300
while True:
    if is_iss_overhead() and is_night():
        if x == 300:
            x = 0
        elif x == 0:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=to_mail,
                msg="Subject:Spojrz w gore!\n\nISS jest w Twoim zasiegu widzenia!"
            )
            x +=1
        else:
            x += 1
        
    time.sleep(1)


