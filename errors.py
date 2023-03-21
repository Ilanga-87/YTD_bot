# Define a function that raises an error if input is not YouTube url
def validate_input(user_message):
    if user_message == '':
        raise ValueError("Input cannot be empty")
    if user_message[:16] != 'https://youtu.be' and user_message[:19] != 'https://www.youtube':
        raise ValueError("Input is not a valid YouTube url")
