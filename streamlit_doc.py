import streamlit as st
import pandas as pd
import time


# **************** Text Utility ***************
st.title("Startup Dashboard")
# --------------> streamlit run app.py

st.header("I am learning Streamlit")
st.subheader("Salman Khan!")

st.write("This is a normal text")


st.markdown("""
### My favorite movies
- Race 3
- Humshakals
- Housefull
            """)

st.code("""
def foo(input):
    return foo**2
x = foo(2)
print(x)
""")

st.latex('x^2 + y^2 + 2 = 0')

# **************** Display Elements ***************

df = pd.DataFrame({
    "name":["Nitish","Ankit","Anupam"],
    "marks":[50,60,70],
    "package":[10,12,14]
})

st.dataframe(df)

st.metric("Revenue","Rs 3L","-3%")

st.json({
    "name":["Nitish","Ankit","Anupam"],
    "marks":[50,60,70],
    "package":[10,12,14]
})

# **************** Display Media ***************
# ----------> Helps in Image Processing


st.image("Screenshot (108).png")
# st.video("")


# **************** Creating Layouts ***************

st.sidebar.title("Sidebar ka Title")
st.sidebar.subheader("Shiva")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("Screenshot (108).png")
with col2:
    st.image("Screenshot (108).png")
with col3:
    st.image("Screenshot (108).png")
    
    

# **************** Showing Status ***************

#----> Error Message -> Success
st.error("Login Failed")
st.success("Login Successful")
st.info("Login Info")
st.warning("Login Warning")


# ----> Progess bar

# bar = st.progress(0)
# for i in range(1,101):
#     time.sleep(0.01)
#     bar.progress(i)
    


# **************** Text user input ***************

#--> Text Input
email = st.text_input("Enter Email: ")
number = st.number_input("Enter age: ")
date = st.date_input("Enter registration date: ")


#--> Buttons
email = st.text_input("Enter Email: ")
password = st.text_input("Enter Password: ")

# --> Dropdown
gender = st.selectbox("Select Gender",["Male","Female","Others"])

btn = st.button("Login")

if btn:
    if (email == "nitish@gmail.com") and (password == "1234"):
        st.balloons()
        st.write(gender)
    else:
        st.error("Login Failed")
        
# --> File upload
file = st.file_uploader("Upload a csv file")
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())








