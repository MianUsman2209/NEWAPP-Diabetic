import streamlit as st
import anthropic
api_key = st.secrets["claude_api_key"]



# Function to call Claude AI API and get a personalized meal plan
def get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    # Initialize the Claude AI client with the provided API key
    client = anthropic.Client(api_key=api_key)
    
    # Define the prompt to send to Claude AI
    prompt = (
        f"My fasting sugar level is {fasting_sugar} mg/dL, "
        f"my pre-meal sugar level is {pre_meal_sugar} mg/dL, "
        f"and my post-meal sugar level is {post_meal_sugar} mg/dL. "
        f"My dietary preferences are {dietary_preferences}. "
        "Please provide a personalized meal plan that can help me manage my blood sugar levels effectively."
    )
    
    try:
        # Call Claude AI API
        response = client.completions.create(
            model="claude-3-5-sonnet-20240620",
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        
        # Print the response to understand its structure
        st.write("Response:", response)

        # Extract and return the content of the message
        if response and 'choices' in response and len(response['choices']) > 0:
            raw_context = response['choices'][0]['text']
        else:
            st.error("Unexpected response format from API.")
            return "Error: Unable to retrieve meal plan."
        
        return raw_context
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Error: Unable to retrieve meal plan."

# Streamlit app
st.title("GlucoGuide")

st.write("""
**GlucoGuide** is a personalized meal planning tool designed specifically for diabetic patients. 
By entering your sugar levels and dietary preferences, GlucoGuide generates meal plans that are 
tailored to help you manage your blood sugar levels effectively.
""")

# Sidebar inputs for sugar levels and dietary preferences
st.sidebar.header("Enter Your Details")

fasting_sugar = st.sidebar.number_input("Fasting Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)

dietary_preferences = st.sidebar.text_input("Dietary Preferences (e.g., vegetarian, low-carb)")

# Generate meal plan button
if st.sidebar.button("Generate Meal Plan"):
    # Retrieve API key from Streamlit secrets
    api_key = st.secrets["claude_api_key"]
    meal_plan = get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
    st.write("Based on your sugar levels and dietary preferences, here is a personalized meal plan:")
    st.markdown(meal_plan)

