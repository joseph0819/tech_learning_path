import os
import base64
from dotenv import load_dotenv
import requests
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()


# Set up Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# # Coursera API setup
# coursera_app_key = os.getenv("COURSERA_APP_KEY")
# coursera_app_secret = os.getenv("COURSERA_APP_SECRET")
# coursera_business_id = os.getenv("COURSERA_BUSINESS_ID")

# if not all([coursera_app_key, coursera_app_secret, coursera_business_id]):
#     st.error("Coursera API credentials not found. Please set the COURSERA_APP_KEY, COURSERA_APP_SECRET, and COURSERA_BUSINESS_ID environment variables.")
#     st.stop()



# Define tech interests
tech_interests = [
    "Web Development", 
    "Mobile App Development",
    "Data Science",
    "Machine Learning",
    "Artificial Intelligence",
    "Cybersecurity",
    "Cloud Computing",
    "DevOps",
    "Blockchain",
    "Internet of Things (IoT)",
    "Big Data",
    "Data Analytics",
    "UI/UX Design",
    "Game Development",
    "Augmented Reality (AR)",
    "Virtual Reality (VR)",
    "Robotics",
    "Network Engineering",
    "Database Management",
    "Full Stack Development",
    "Front-end Development",
    "Back-end Development",
    "Software Engineering",
    "Quantum Computing",
    "Embedded Systems",
    "Computer Vision",
    "Natural Language Processing",
    "Bioinformatics",
    "5G Technology",
    "Cryptocurrency",
    "IT Project Management",
    "System Administration",
    "Enterprise Architecture",
    "Information Security",
    "Digital Marketing",
    "E-commerce Development",
    "Data Visualization",
    "API Development",
    "Microservices Architecture",
    "Containerization (Docker, Kubernetes)",
    "Serverless Computing",
    "Edge Computing",
    "Distributed Systems",
    "High-Performance Computing",
    "Computer Graphics",
    "3D Modeling and Animation"
]

def get_coursera_access_token(app_key, app_secret):
    url = "https://api.coursera.com/oauth2/client_credentials/token"
    auth_string = f"{app_key}:{app_secret}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        st.error(f"Error obtaining Coursera access token: {str(e)}")
        if hasattr(e, 'response') and e.response:
            st.error(f"Response content: {e.response.content}")
        return None

def get_coursera_courses(subject, access_token):
    url = "https://api.coursera.org/api/courses.v1"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "search", "query": subject, "limit": 5, "fields": "name,slug"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        courses = response.json().get("elements", [])
        return [{"name": course["name"], "url": f"https://www.coursera.org/learn/{course['slug']}"} for course in courses]
    except requests.RequestException as e:
        st.error(f"Error fetching Coursera courses: {str(e)}")
        if hasattr(e, 'response') and e.response:
            st.error(f"Response content: {e.response.content}")
        return []

def get_ai_suggestions(interests):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""For someone interested in {', '.join(interests)}, please provide:

1. Overview:
   - Brief description of each selected technology
   - How these technologies relate to each other (if applicable)

2. Industry Trends:
   - Current trends in these fields
   - Emerging technologies or practices
   - Job market outlook

3. Advice:
   - Why these technologies are important
   - Potential challenges in learning these technologies
   - Tips for success in these fields

4. Personalized Learning Path:
   - Step-by-step guide to learning these technologies with breakdown
   - Suggest a logical order for learning multiple technologies
   - Estimated time frame for each step
   - Key concepts to focus on for each technology
   - Suggested projects or practical applications to reinforce learning

5. Resources:
   - Types of courses or certifications that would be beneficial
   - Recommended books or online resources
   - Relevant communities or forums for support and networking

Please structure your response clearly with headers and bullet points for easy readability."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating AI suggestions: {str(e)}")
        return "Unable to generate AI suggestions at this time."

def main():
    st.title("Tech Learning Path Prompt System")

     # Coursera API setup
    coursera_app_key = os.getenv("COURSERA_APP_KEY")
    coursera_app_secret = os.getenv("COURSERA_APP_SECRET")

    if not all([coursera_app_key, coursera_app_secret]):
        st.error("Coursera API credentials not found. Please set the COURSERA_APP_KEY and COURSERA_APP_SECRET environment variables.")
        st.stop()

    # Get Coursera access token
    coursera_access_token = get_coursera_access_token(coursera_app_key, coursera_app_secret)
    if not coursera_access_token:
        st.error("Failed to obtain Coursera access token.")
        st.stop()

    # User input
    selected_interests = st.multiselect(
        "Select your tech interests:", tech_interests
    )

    if st.button("Generate Learning Path"):
        if selected_interests:
            st.write("Generating personalized learning path...")
            
            # Get AI suggestions
            ai_suggestions = get_ai_suggestions(selected_interests)
            st.subheader("AI-Generated Learning Path:")
            st.write(ai_suggestions)

            # Get course recommendations
            st.subheader("Recommended Coursera Courses:")
            for interest in selected_interests:
                st.write(f"\nCourses for {interest}:")
                
                coursera_courses = get_coursera_courses(interest, coursera_access_token)
                if coursera_courses:
                    for course in coursera_courses:
                        st.markdown(f"- [{course['name']}]({course['url']})")
                else:
                    st.write("No courses found for this interest.")

        else:
            st.warning("Please select at least one interest.")

if __name__ == "__main__":
    main()