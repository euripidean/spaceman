"""
Spaceman: an intergalactic adventure.
"""
import random
import string
import pyfiglet


alphabet = list(string.ascii_lowercase)
INTRO_TEXT = 'Welcome to Spaceman!'
intro_art = pyfiglet.figlet_format(INTRO_TEXT, font="avatar")
letters_guessed = []
spaceman_body = [
    'left glove',
    'left boot',
    'right glove',
    'right boot',
    'chest plate',
    'oxygen tank',
    'helmet']

def load_word():
    """
    Reads a text file of words and randomly selects one to use as the secret word.

    Returns:
    string: The secret word to be used in the game.
    """
    file_to_read = open('words.txt', 'r', encoding='utf')
    words_list = file_to_read.readlines()
    file_to_read.close()
    words_list = words_list[0].split(' ')
    secret_word = random.choice(words_list) # pylint: disable=redefined-outer-name
    return secret_word

def is_word_guessed(word, letters):
    """
    Checks if all the letters of the secret word have been guessed.

    Returns:
        Bool: True only if all the letters of the secret word have been guessed. Else false.
    """
    correct_letters = 0
    for letter in letters:
        if letter in word:
            correct_letters += word.count(letter)
    return bool(correct_letters == len(word))

def get_guessed_word(word, letters):
    """
    Get a string showing the letters guessed so far and underscores
    for letters that have not been guessed yet.

    Returns:
        string: letters that have been guessed, underscores for unguessed letters.
    """
    string_list = []
    for letter in word:
        if letter in letters:
            string_list.append(letter)
        else:
            string_list.append('_')
    return ''.join(string_list)

def is_guess_in_word(guess, word):
    """
    Assess whether the guess is in the word.

    Return:
        Bool: True if guess is in the word, false if not.
    """
    while guess not in word:
        return False
    return True

def display():
    """
    Displays some dividing asterisks for better user experience.

    Returns:
        String: Two rows of 100 asterisks.
    """
    print('\n')
    print('*' * 100)
    print('*' * 100)
    print('\n')

def welcome_message():
    """
    Displays welcome message on first iteration of game.

    Returns:
        String: Ascii Art and instruction strings.
    """
    print(intro_art)
    print('The rules of the game are simple...')
    print('You have 7 attempts to guess the word correctly.')
    print('If you fail, the spaceman will be expelled from the air lock.')
    print('Loading secret word....')
    display()

def uh_oh():
    """
    Displays Ascii art for incorrect guess.

    Returns:
        String: Ascii art of word 'uh oh!'
    """
    uhoh_text = 'Uh oh!'
    ascii_uhoh = pyfiglet.figlet_format(uhoh_text, font="digital")
    print(ascii_uhoh)

def end_game_message():
    """
    Displays Ascii art for end of game.

    Returns:
        String: Ascii art reading 'thank you for playing'.
    """
    end_text = 'Thank you for playing!'
    ascii_end = pyfiglet.figlet_format(end_text, font="avatar")
    print(ascii_end)

def remaining_guesses(guess):
    """
    Displays remaining guesses and remaining letters of alphabet that haven't been guessed.

    Returns:
        String: Number of guesses remaining and alphabet available to guess.
    """
    alphabet_string = ''.join(alphabet)
    if 7-guess > 1:
        print(f'You have {7-guess} guesses remaining.')
    else:
        print(f'You have {7-guess} guess remaining.')
    print(f'You have the following letters available to choose from: {alphabet_string}')

def success_message(word):
    """
    Displays message if user guesses the word correctly.

    Returns:
        String: Ascii Art reading 'you win' and confirms word.
    """
    win_text = 'You win!'
    ascii_win = pyfiglet.figlet_format(win_text, font="avatar")
    print(ascii_win)
    print(f'The word was {word.upper()}. The Spaceman is saved!')
    display()

def failure_message(word):
    """
    Displays message if user fails to guess the word.
    Returns:
        String: Ascii Art reading 'you lose' and reveals word.
    """
    lose_text = 'You lose!'
    ascii_lose = pyfiglet.figlet_format(lose_text, font="avatar")
    print(ascii_lose)
    print(f'The word was {word.upper()}. Better luck next time. Not for the poor Spaceman, though.')

def play_again():
    """
    Offers user the chance to play again and validates input.

    Returns:
        Enters game function if response is Y, exits program and displays exit message
        if response is N.
    """
    play_again = input('Would you like to play again? (Y/N) > ').upper() # pylint: disable=redefined-outer-name
    if play_again not in ('Y','N'):
        play_again = input('Please enter either Y or N > ').upper()
    elif play_again == 'Y':
        secret_word = load_word() # pylint: disable=redefined-outer-name
        spaceman(secret_word)
    else:
        end_game_message()
        return

def spaceman(secret_word): # pylint: disable=redefined-outer-name
    """
    Runs gameplay for Spaceman and validates input.
    Runs while word is not guessed and number of incorrect guesses is 7 or lower.
    When word is incorrect, counts guesses.

    Returns:
     Function: If word guessed, success message, if incorrect guesses
     greater than 7, failure message.
    """
    guess_count = 0
    letters_guessed = [] # pylint: disable=redefined-outer-name
    print(f'Your secret word has {len(secret_word)} letters.\n')

    while not is_word_guessed(secret_word,letters_guessed):
        guess = input('Please enter a single letter: > ').lower()
        while (guess not in alphabet) or (guess in letters_guessed):
            if guess in letters_guessed:
                guess = input('You already guessed that letter, try another: ').lower()
            else:
                guess = input('Nice try! Enter a single letter:  > ').lower()
        print(f'You have guessed the letter {guess.upper()}.')
        letters_guessed.append(guess)
        alphabet.remove(guess)
        guess_count += 1
        if is_guess_in_word (guess, secret_word):
            print('The letter was in the word.')
            guess_count -= 1
            remaining_guesses(guess_count)
        else:
            uh_oh()
            if guess_count == len(spaceman_body):
                failure_message(secret_word)
                play_again()
                return
            print(f"The Spaceman's {spaceman_body[guess_count]} has been sucked out of the airlock!") # pylint: disable=line-too-long
            remaining_guesses(guess_count)
        print(get_guessed_word(secret_word,letters_guessed))
        display()

    success_message(secret_word)

#These function calls that will start the game
secret_word = load_word()
welcome_message()
spaceman(secret_word)
