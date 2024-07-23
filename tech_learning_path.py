import os
import requests
import streamlit as st
import google.generativeai as genai

# Set up Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

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
def get_udemy_courses(subject):
    url = "https://www.udemy.com/api-2.0/courses/"
    params = {
        "search": subject,
        "price": "price-free",
        "ordering": "relevance",
        "page_size": 5
    }
    headers = {"Accept": "application/json, text/plain, */*"}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get('results', [])
    except requests.RequestException as e:
        st.error(f"Error fetching Udemy courses: {str(e)}")
        return []


def get_mit_opencourseware(subject):
    url = "https://ocw.mit.edu/api/v0/courses/"
    params = {
        "q": subject,
        "sort": "relevance",
        "page": 1,
        "page_size": 5
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        st.error(f"Error fetching MIT OpenCourseWare courses: {str(e)}")
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
            st.subheader("Recommended Courses:")
            for interest in selected_interests:
                st.write(f"\nCourses for {interest}:")
                
                udemy_courses = get_udemy_courses(interest)
                st.write("Udemy Courses:")
                for course in udemy_courses:
                    st.write(f"- {course['title']}")

                mit_courses = get_mit_opencourseware(interest)
                st.write("MIT OpenCourseWare:")
                for course in mit_courses:
                    st.write(f"- {course['title']}")

        else:
            st.warning("Please select at least one interest.")

if __name__ == "__main__":
    main()