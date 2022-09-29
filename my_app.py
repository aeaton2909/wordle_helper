# Imports
import streamlit as st
from play_wordle import PlayWorldle
import pandas as pd
# Write a page title
st.title('Wordle Helper')
para = ()
st.text(
    """This app uses information theory to help you solve Wordle!

    1) Guess a word in the Wordle app and type it in below
    2) Type in the letters that are GREEN
    3) Type in the letters that are AMBER
    4) Find the best word to guess next and repeat!

Hint: "alert" is a great guess to start with.."""
    )

if 'game_object' not in st.session_state:
    with open('valid_solutions.csv') as f:
        lines = f.readlines()
    wordle_words = [w[:5] for w in lines]

    # Intialise object with words
    st.session_state['game_object'] = PlayWorldle(wordle_words)

guessed_word = st.text_input('Word you guessed in Wordle:', 'alert')
green_chars = st.text_input('Letters that are GREEN:', )
amber_chars = st.text_input('Letters that are AMBER:', )
push_button = st.button('Find next word!')

if push_button:
    st.session_state['game_object'].enter_guess(guessed_word.lower(), 
                                                green_chars.lower(), 
                                                amber_chars.lower())
    best_choices = st.session_state['game_object'].gen_word_entropy(return_best=True)

    n_remaining = len(st.session_state['game_object'].remaining_words)
    st.write('Number of guesses:', st.session_state['game_object'].game_state)
    if n_remaining == 1:
        remaining_output = ('CONGRATULATIONS! The only word left is "{}"!'
                            .format(st.session_state['game_object'].remaining_words[0]))
        chart_data = pd.Series(st.session_state['game_object'].remaining_words_log)
        st.bar_chart(chart_data.rename(index='Remaining words'))
    elif n_remaining == 0:
        remaining_output = ('There are no words left...something went wrong!')
    else:
        remaining_output = 'There are {} remaining words!'.format(n_remaining)
        st.write('Try this word:       ', '"{}"'.format(best_choices[0]))
    st.write('', remaining_output)
