def goodInput(question, list_of_choices=[], include_uppercase=False, checkForDigit=False):
    """ Funkcja sprawdzająca czy użytkownik wprowadził poprawny input. Jeśli input jest nieprawidłowy, zapętli pytanie. 
    \n Jako pierwszy parametr wpisz stringowe pytanie o wybór. 
    \n Jeśli wymagasz konkretnych inputów, jako drugi parametr twórz liste w której będą poprawne inputy. 
    \n Jeśli chcesz aby wielkość liter nie miała znaczenia, jako trzeci parametr podaj "True".
    \n Jeśli chcesz sprawdzić czy input jest liczbą, jako czwarty parametr podaj "True".
    \n Możesz łączyć instrukcje 'checkForDigit' z 'list_of_choices'. 
    \n Przykład: goodInput("Napisz 'TAK' lub 'NIE' lub wprowadź liczbę, ["tak", "nie",], include_uppercase=True, checkForDigit=True) 
    """
    # TODO
    # Zrobić z każdego warunku mini funkcje i umożliwić ich łączenie ze sobą
    # Rozszerzyć

    if checkForDigit == True and len(list_of_choices) != 0:
        answer = input(question)
        checking = answer.isdigit()
        while answer not in list_of_choices and checking == False:
            answer = input(question)
            checking = answer.isdigit()
        return answer

    elif checkForDigit == True:
        answer = input(question)
        checking = answer.isdigit()
        while checking == False:
            answer = input(question)
            checking = answer.isdigit()
        return answer

    elif include_uppercase == True:
        lower_list = [x.lower() for x in list_of_choices]
        answer = input(question).lower()
        while answer not in lower_list:
            answer = input(question).lower()

    elif include_uppercase == False:
        answer = input(question)
        while answer not in list_of_choices:
            answer = input(question)
    return answer


i = 0


def checking():
    """ Funkcja for fun """
    global i
    if i == 0:
        print("Checking.")
        i += 1
    elif i == 1:
        print("Checking..")
        i += 1
    else:
        print("Checking...")
        i = 0
