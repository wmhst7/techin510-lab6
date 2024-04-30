import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Streamlit app setup
st.title("Refined Workout Planner")

# Initialize chat session if not already done
if "chat_session" not in st.session_state:
    st.session_state.chat_session = chat
    st.session_state.messages = []

# Ask for user information
with st.form("user_info"):
    st.write("Please enter your details:")
    age = st.number_input("Age", min_value=13, max_value=100, step=1, value=20)  # Default to 20
    weight = st.number_input("Weight (in kg)", min_value=30, max_value=200, step=1, value=60)  # Default to 60
    height = st.number_input("Height (in cm)", min_value=100, max_value=250, step=1, value=180)  # Default to 180
    gender_options = ["Male", "Female", "Other"]
    gender = st.selectbox("Gender", options=gender_options)
    profession_level = st.selectbox("Sport Profession Level", options=["Beginner", "Intermediate", "Advanced", "Professional"])
    workout_places = st.multiselect("Preferred Workout Locations", options=["Gym", "Home", "Outdoor", "Tennis Court", "Basketball Court"])
    available_time = st.slider("How much time can you spend on workouts per week (hours)?", 0, 20, 3)
    goals = st.text_area("What are your fitness goals?")
    submit_button = st.form_submit_button("Generate Workout Plan")

if submit_button:
    user_details = {
        "Age": age,
        "Weight": f"{weight} kg",
        "Height": f"{height} cm",
        "Gender": gender,
        "Fitness Level": profession_level,
        "Workout Locations": ', '.join(workout_places),
        "Available Time": f"{available_time} hours per week",
        "Goals": goals
    }

    # Format the user details into a structured message
    details_message = ", ".join([f"{key}: {value}" for key, value in user_details.items()])
    st.session_state.messages.append({"role": "user", "content": details_message})

    # query = f"""
    # Generate a detailed weekly workout plan tailored to these specific characteristics and goals:
    # - {details_message}
    # """

    # query = f"""
    # Generate a comprehensive weekly workout plan tailored to the following user specifications and fitness objectives. Please provide a structured plan with detailed daily activities, including specific exercises, their durations, recommended intensity, and necessary equipment. Also include rest periods and any dietary recommendations that complement the fitness goals.

    # User Specifications:
    # - Age: {user_details['Age']}
    # - Weight: {user_details['Weight']}
    # - Height: {user_details['Height']}
    # - Gender: {user_details['Gender']}
    # - Fitness Level: {user_details['Fitness Level']}
    # - Preferred Workout Locations: {user_details['Workout Locations']}
    # - Time Available per Week: {user_details['Available Time']}
    # - Fitness Goals: {user_details['Goals']}

    # Instructions:
    # - Detail the type of exercises (e.g., cardio, strength training, flexibility).
    # - Specify the number of sets and repetitions or duration for each exercise.
    # - Suggest intensity levels (e.g., light, moderate, vigorous).
    # - List any necessary equipment for each exercise.
    # - Include appropriate warm-up and cool-down routines.
    # - Provide general dietary guidelines or tips that support the workout regimen.
    # - Mention any necessary rest days or lighter activity days to prevent overtraining.
    # """


    query = f"""
    Generate a highly personalized and detailed weekly workout plan, considering the following specific user characteristics and fitness objectives. The plan should offer a balanced mix of activities that align with the user's physical capabilities, available resources, and goals. Ensure the inclusion of clear daily schedules, exercise specifics, intensity guidelines, and recovery strategies.

    User Specifications:
    - Age: {user_details['Age']}
    - Weight: {user_details['Weight']}
    - Height: {user_details['Height']}
    - Gender: {user_details['Gender']}
    - Fitness Level: {user_details['Fitness Level']}
    - Preferred Workout Locations: {user_details['Workout Locations']}
    - Time Available per Week: {user_details['Available Time']}
    - Fitness Goals: {user_details['Goals']}

    Plan Requirements:
    - Include a mix of cardio, strength, flexibility, and balance training.
    - Specify exact exercises, durations, sets, and repetitions or interval timings.
    - Clearly state the intensity level for each exercise (e.g., light, moderate, vigorous).
    - Detail necessary equipment for each exercise, accommodating for 'no equipment' options when required.
    - Provide options for indoor and outdoor exercises, adaptable based on the user’s preferred workout locations.
    - Include warm-up before and cool-down routines after each workout session.
    - Suggest daily nutritional tips or meal ideas that support energy levels and recovery.
    - Define at least two rest days with optional light activities like yoga or walking to maintain mobility without overtaxing the body.
    - Adjust exercises and intensities for any listed medical conditions or previous injuries.
    - Offer modifications for exercises to increase or decrease difficulty based on the user’s weekly progress or feedback.

    Additional Instructions:
    - The plan should be scalable, allowing for adjustments based on progress and feedback.
    - Include motivational tips or mental health strategies to enhance focus and reduce stress.
    """


    # Show a loading spinner while waiting for response
    with st.spinner('AI is generating your personalized workout plan...'):
        response = st.session_state.chat_session.send_message(query)
        workout_plan = response.text  # Assuming response.text contains the string response
    
    # Display the generated workout plan
    st.session_state.messages.append({"role": "assistant", "content": workout_plan})
    with st.chat_message("assistant"):
        st.markdown(workout_plan)
