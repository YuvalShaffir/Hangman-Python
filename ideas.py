import hangman_helper

def filter_words_list(words, pattern, wrong_guess_lst):
    new_words_lst = []
    for word in words:
        is_in_wrong_guess = False
        is_in_pattern = True
        if len(pattern) == len(word):
            if wrong_guess_lst:
                for w_guess in wrong_guess_lst:
                    if word.find(w_guess) != -1:
                        is_in_wrong_guess = True
            # todo: check if it works
            # pattern_str = " ".join(pattern)
            check_is_patten = " ".join((len(pattern) * "_"))
            if pattern == check_is_patten and not is_in_wrong_guess:
                new_words_lst.append(word)
            else:
                correct_char_lst = []
                for chr_index in range(len(pattern)):
                    if pattern[chr_index] != "_":
                        if pattern[chr_index] != word[chr_index] or pattern.count(pattern[chr_index]) != word.count(word[chr_index]):
                            is_in_pattern = False
                        else:
                            correct_char_lst.append([pattern[chr_index]])
                            continue
                    else:
                        if word[chr_index] in correct_char_lst:
                            is_in_pattern = False

            if is_in_pattern and not is_in_wrong_guess:
                new_words_lst.append(word)
    return new_words_lst


def run_single_game(words_list, score):
    word = hangman_helper.get_random_word(words_list)
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
            words_list = filter_words_list(words_list, pattern, wrong_guess_lst)
            new_words_list = []
            if len(words_list) > hangman_helper.HINT_LENGTH:
                n = len(words_list)
                for i in range(0, hangman_helper.HINT_LENGTH):
                    new_words_list.append(words_list[i * n // hangman_helper.HINT_LENGTH])
                hangman_helper.show_suggestions(new_words_list)
            else:
                hangman_helper.show_suggestions(words_list)

    hangman_helper.display_state(pattern, wrong_guess_lst, score, msg_type(pattern, word, score))
    return score


print(run_single_game(['aaa'], 2))

def main2():
    points = hangman_helper.POINTS_INITIAL
    words_list = hangman_helper.load_words()
    points, games_played = play_game(words_list, points)
    if points > 0:
        play_more = hangman_helper.play_again(f"Games played: {games_played} "
                                              f"\n Points earned: {points}"
                                              f" \n do you want to play more?")
        if play_more:
            play_game(words_list, points)

    if points == 0:
        replay = hangman_helper.play_again(f"You have 0 points: \n Games played: {games_played}"
                                           f"\n Do you want to restart game?")
        if replay:
            play_game(words_list, hangman_helper.POINTS_INITIAL)


def play_game(words_list, points):
    games_played = 0
    want_to_play = True
    while want_to_play:
        points = run_single_game(words_list, points)
        games_played += 1
        want_to_play = hangman_helper.play_again(f"Games played: {games_played} "
                                              f"\n Points earned: {points}"
                                              f" \n do you want to play again?")
    return points, games_played
