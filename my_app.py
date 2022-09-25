# Imports
import streamlit as st
from play_wordle import PlayWorldle
import pandas as pd
# Write a page title
st.title('Wordle Helper')
st.text(
    'This app uses information theory to help you solve Wordle!\nType in the guessed word and the letters that are green or amber (blank if none).'
    )

if 'game_object' not in st.session_state:
    with open('valid_solutions.csv') as f:
        lines = f.readlines()
    wordle_words = [w[:5] for w in lines]

    # Intialise object with words
    st.session_state['game_object'] = PlayWorldle(wordle_words)
    
guessed_word = st.text_input('Word you guessed:', 'alert')
green_chars = st.text_input('Letters that are GREEN:', )
amber_chars = st.text_input('Letters that are AMBER:', )

push_button = st.button('Enter')

if push_button:
    st.session_state['game_object'].enter_guess(guessed_word, 
                                                green_chars, 
                                                amber_chars)
    best_choices = st.session_state['game_object'].gen_word_entropy(return_best=True)

    n_remaining = len(st.session_state['game_object'].remaining_words)
    st.write('Number of guesses:', st.session_state['game_object'].game_state)
    if n_remaining == 1:
        remaining_output = ('CONGRATULATIONS! The only word left is {}!'
                            .format(st.session_state['game_object'].remaining_words[0]))
    elif n_remaining == 0:
        remaining_output = ('There are no words left...something went wrong!')
    else:
        remaining_output = 'There are {} remaining words!'.format(n_remaining)
        st.write('Try this word:       ', best_choices[0])
    st.write('', remaining_output)


    chart_data = pd.Series(st.session_state['game_object'].remaining_words_log)
    # st.line_chart(chart_data.rename(index='Remaining words'))
    st.bar_chart(chart_data.rename(index='Remaining words'))