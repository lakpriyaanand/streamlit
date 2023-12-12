import streamlit as st

st.title('Paradise to get largest of 3 numbers')

st.header('Enter your inputs here: ')

num1 = st.number_input('input 1st number')
num2 = st.number_input('input 2nd number')
num3 = st.number_input('input 3rd number')

def maximum():
    lis = [num1 , num2 , num3]
    a = max(lis)
    st.success(f"Maximum = {a}")

if st.button("Calculate result"):
    maximum()
