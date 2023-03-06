#################################################################
# FILE : hangman.py
# WRITER : Yuval Shaffir , yuval.shaffir , 208448068
# EXERCISE : ex4
# DESCRIPTION: The hangman game.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none.
# NOTES:
#################################################################
import hangman_helper


def update_word_pattern(word, pattern, letter):
    """called if the letter is in the word, and updates the pattern to reveal the letter."""
    word_lst = list(word)
    pattern_lst = list(pattern)
    for char_index in range(len(word_lst)):
        if word_lst[char_index] == letter:
            pattern_lst[char_index] = letter
    return "".join(pattern_lst)


def filter_words_list(words, pattern, wrong_guess_lst):
    """called if user asked for a hint, returns a list with the possible words."""
    new_words_lst = []
    for word in words:
        is_in_wrong_guess = False
        if len(pattern) == len(word):
            if wrong_guess_lst:  # checks if word in wrong guess list
                for w_guess in wrong_guess_lst:
                    if word.find(w_guess) != -1:
                        is_in_wrong_guess = True
            if pattern == " ".join((len(pattern) * "_")) and not is_in_wrong_guess:
                new_words_lst.append(word)
            else:
                new_words_lst = word_pattern_check(new_words_lst, pattern, word, is_in_wrong_guess)
    return new_words_lst


def word_pattern_check(new_words_lst, pattern, word, is_in_wrong_guess):
    """check if the word's and pattern's letters are in the same index and amount."""
    is_in_pattern = True
    correct_char_lst = []
    for chr_index in range(len(pattern)):
        if pattern[chr_index] != "_":
            same_amount_of_letters = pattern.count(pattern[chr_index]) != word.count(word[chr_index])
            if pattern[chr_index] != word[chr_index] or same_amount_of_letters:
                is_in_pattern = False
            else:
                correct_char_lst.append([pattern[chr_index]])
                continue
        else:
            # False if letter that isn't in pattern was found already.
            if word[chr_index] in correct_char_lst:
                is_in_pattern = False
    if is_in_pattern and not is_in_wrong_guess:
        new_words_lst.append(word)
    return new_words_lst


def input_is_letter(choice, word, past_choices_lst, wrong_guess_lst, pattern, score, msg):
    """input type: letter.
       function checks if the letter is in the word.
       output: returns the score, updated pattern with letter (if correct) or letter in wrong guess list"""
    # checks if choice is in length 1 and lowercase.
    if len(choice) != 1 or type(choice) != str or not choice.islower():
        msg = "The letter is not the correct length or is not a character"
        return score, pattern, wrong_guess_lst, msg
    # checks if choice was chosen before.
    for past_choice in past_choices_lst:
        if choice == past_choice:
            msg = "The letter was chosen already"
            return score, pattern, wrong_guess_lst, msg
    score -= 1
    n = 0
    for letter in word:
        if choice == letter:
            past_choices_lst.append(choice)
            pattern = update_word_pattern(word, pattern, choice)
            msg = "The letter is in the word!"
            n += 1
    if n > 0:
        past_choices_lst.append(choice)
        score += n * (n + 1) // 2
    else:
        msg = "The letter is not in the word"
        if choice not in wrong_guess_lst:
            past_choices_lst.append(choice)
            wrong_guess_lst.append(choice)
    return score, pattern, wrong_guess_lst, msg


def input_is_word(score, choice, word, pattern, msg):
    """input type: word.
       function checks if the chosen word is in the pattern word.
       output: score, updated pattern (depends if the word is inside or not)"""
    score -= 1
    if choice == word:
        pattern_not_underline = len(pattern) - pattern.count("_")
        n = len(choice) - pattern_not_underline
        score += n * (n + 1) // 2
        pattern = word
    else:
        msg = "Your choice is not the word."
    return score, pattern, msg


def msg_type(pattern, word, score):
    """the function decides the message incase the user won or lost."""
    if pattern == word:
        message = f"Congratulations you found the word: {word}"
        return message
    if score == 0:
        message = f"You did not find the word, the word is: {word}"
        return message


def run_single_game(word_list, score):
    """runs a single game, the user inputs a letter/word/asks for hint, and continues until
    the pattern is revealed completely or he lost all points"""
    word = hangman_helper.get_random_word(word_list)
    pattern = "_" * len(word)
    wrong_guess_lst = []
    msg = ""
    past_choices_lst = []
    while pattern != word and score > 0:
        hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)
        input_type, choice = hangman_helper.get_input()
        if input_type == hangman_helper.LETTER:
            score, pattern, wrong_guess_lst, msg = input_is_letter(choice, word,
                                                                   past_choices_lst,
                                                                   wrong_guess_lst,
                                                                   pattern, score, msg)
        elif input_type == hangman_helper.WORD:
            score, pattern, msg = input_is_word(score, choice, word, pattern, msg)
        elif input_type == hangman_helper.HINT:
            score -= 1
            hint_list = filter_words_list(word_list, pattern, wrong_guess_lst)
            check_hint_list_length(hint_list)
    hangman_helper.display_state(pattern, wrong_guess_lst, score, msg_type(pattern, word, score))
    return score


def check_hint_list_length(hint_list):
    """check if the list of hints is in a specific length."""
    new_words_list = []
    if len(hint_list) > hangman_helper.HINT_LENGTH:
        n = len(hint_list)
        for i in range(0, hangman_helper.HINT_LENGTH):
            new_words_list.append(hint_list[i * n // hangman_helper.HINT_LENGTH])
        hangman_helper.show_suggestions(new_words_list)
    else:
        hangman_helper.show_suggestions(hint_list)


def main():
    """the main functions that runs the game, displays the updated state of the game in each turn,
    and replays the game if the user chooses to."""
    points = hangman_helper.POINTS_INITIAL
    words_list = hangman_helper.load_words()
    points = run_single_game(words_list, points)
    games_played = 1
    while points >= 0:
        if points > 0:
            play_more = hangman_helper.play_again(f"Games played: {games_played} "
                                                  f"\n Points earned: {points}"
                                                  f" \n do you want to play more?")
            if play_more:
                points = run_single_game(words_list, points)
                games_played += 1
                continue
            else:
                break
        if points == 0:
            replay = hangman_helper.play_again(f"You have 0 points: \n Games played: {games_played}"
                                               f"\n Do you want to restart game?")
            if replay:
                games_played = 0
                points = hangman_helper.POINTS_INITIAL
                points = run_single_game(words_list, points)
                games_played += 1
            else:
                break


if __name__ == "__main__":
    main()
