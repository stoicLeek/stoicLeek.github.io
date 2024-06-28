from tabulate import tabulate

def login(name, password):
    """
    Takes user input name and password and checks if those are stored in a local dictionary.
    Params: name, password (str)
    Returns: True or False (bol)
    """
    registeredUsers = {'bob': '123', 'ann': 'pass123', 'mike': 'password123', 'liz': 'pass123'}
    dictPassword = registeredUsers.get(name)
    return True if password == dictPassword else False

# Defining printable dashed line
dashLine = 40 * '-'

# Storing user' inputs.
inputName = input('Type your username and press enter: ')
inputPassword = input('Type your password and press enter: ')
print(dashLine)

loggedIn = login(inputName, inputPassword)

# Evaluation of user credentials.
if loggedIn:
    print(f'Login success, {inputName}!')
    try:
        from task_template import TEXTS
        print('You\'ve got 3 texts to be analyzed.', dashLine, sep='\n')
    except:
        print('However I\'am unable to load texts for analysis.')
        exit()
else:
    print('You\'re not a registered user. Terminating the program...')
    exit()

# A prompt for user chosen text
strTxtNo = input('Press 1, 2 or 3 choosing one of them: ')
intTxtNo = int(strTxtNo)

# Processing the analysis, storing and printing results if correct user input.
if strTxtNo.isdigit() and intTxtNo in range(1, 1 + len(TEXTS)):
    print('Processing the analysis...', dashLine, sep='\n')

    txt = TEXTS[intTxtNo - 1]
    slicedTxt = txt.split()

    words = len(slicedTxt)
    print(f'There are {words} words.')

    title = sum(element.istitle() for element in slicedTxt)
    print(f'There are {title} titlecase words.')

    upper = sum(element.isupper() and element.isalpha() for element in slicedTxt)
    print(f'There are {upper} uppercase words.')

    lower = sum(element.islower() for element in slicedTxt)
    print(f'There are {lower} lowercase words.')

    num = sum(element.isnumeric() for element in slicedTxt)
    print(f'There are {num} numeric words.')

    sumNum = sum(float(element) for element in slicedTxt if element.isdigit())
    print(f'The sum of all the numbers is {int(sumNum) if sumNum.is_integer() else sumNum}.')

    wordsLengthTab = [len(element.strip(',.')) for element in slicedTxt if element.strip(',.').isalnum()]

    wordsLengthDict = {wordsLength: (wordsLengthTab.count(wordsLength) * '*', wordsLengthTab.count(wordsLength)) for wordsLength in wordsLengthTab}

    wordsLengthDict = dict(sorted(wordsLengthDict.items()))
    print(dashLine)

    print(tabulate([(key,) + val for key, val in wordsLengthDict.items()], headers=['LEN', 'OCCURENCES', 'NO'], tablefmt='psql', numalign='left'))

elif strTxtNo.isdigit() and intTxtNo not in range(1, 1 + len(TEXTS)):
    print('You\'ve chosen some out-of-range-number. Terminating the program...')
    exit()

else:
    print('Your input might not even be a number. Terminating the program...')
    exit()

input('Press any key to exit.')
