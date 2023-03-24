# Define a function that raises an error if input is not YouTube url
def validate_input(user_message):
    if not user_message.startswith('https://youtu.be') and not user_message.startswith('https://www.youtube'):
        raise ValueError("Input is not a valid YouTube url")
