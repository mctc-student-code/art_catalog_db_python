def get_non_empty_string(question):
    userInput = input(question)
    if not userInput:
        print('Please complete this field before continuing.')
        userInput = input(question)
    else:
        return userInput

def yes_no_input(question):
    userInput = input(question)
    if userInput == 'Yes' or userInput == 'yes':
        return 'Yes'
    elif userInput == 'No' or userInput == 'no':
        return 'No'
    else:
        print('Please enter Yes or No')
        userInput = input(question)



