import streamlit as st
import sys
import os
import pandas as pd  # Import pandas for data handling

# Add the parent directory to sys.path to import from api module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.gemini_integration import get_learning_recommendations

# Set page configuration
st.set_page_config(
    page_title="Student Learning Recommendation System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("Student Learning Recommendation System")
st.markdown("""
This application helps students discover personalized learning resources and recommendations
based on their preferences, learning style, and educational goals.
""")

# Sidebar for user authentication (placeholder for now)
with st.sidebar:
    st.header("User Profile")
    
    # Simple authentication (to be expanded later)
    user_name = st.text_input("Username")
    if not user_name:
        st.warning("Please enter a username to save your preferences")
    
    st.divider()
    st.subheader("About")
    st.info(
        "This tool uses Gemini AI to provide personalized educational resource recommendations "
        "based on your learning preferences and goals."
    )

# Main app layout using tabs
tab1, tab2, tab3, tab4 = st.tabs(["Your Preferences", "Recommendations", "History", "Student Analytics"])

# Preferences Tab
with tab1:
    st.header("Learning Preferences")
    
    # Educational level selection
    education_level = st.selectbox(
        "Your educational level:",
        ["High School", "Undergraduate", "Graduate", "Professional Development"]
    )
    
    # Subject interests with multi-select
    subject_options = [
        "Mathematics", "Computer Science", "Physics", "Chemistry", "Biology",
        "History", "Literature", "Philosophy", "Psychology", "Economics",
        "Business", "Art", "Music", "Engineering", "Languages", "Other"
    ]
    
    subjects = st.multiselect(
        "Select your subject interests:",
        subject_options,
        default=["Mathematics", "Computer Science"]
    )
    
    # Learning style selection
    col1, col2 = st.columns(2)
    
    with col1:
        learning_style = st.radio(
            "What's your preferred learning style?",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"]
        )
        
        time_availability = st.slider(
            "How many hours per week can you dedicate to learning?",
            min_value=1,
            max_value=40,
            value=10
        )
    
    with col2:
        difficulty_level = st.select_slider(
            "Preferred difficulty level:",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate"
        )
        
        learning_goals = st.text_area(
            "What are your specific learning goals or objectives?",
            "I want to improve my skills in..."
        )
    
    # Additional preferences
    st.subheader("Additional Preferences")
    
    col3, col4 = st.columns(2)
    
    with col3:
        resource_types = st.multiselect(
            "What types of resources do you prefer?",
            ["Online Courses", "Books", "Videos", "Interactive Tools", "Research Papers", "Tutorials", "Projects"],
            default=["Online Courses", "Videos"]
        )
    
    with col4:
        certification = st.checkbox("Interested in certified courses")
        paid_content = st.checkbox("Include paid resources")
    
    # Submit button
    if st.button("Get Recommendations", type="primary"):
        if not user_name:
            st.error("Please provide a username before generating recommendations")
        elif not subjects:
            st.error("Please select at least one subject of interest")
        else:
            # Collect all user preferences into a dictionary
            user_preferences = {
                "username": user_name,
                "education_level": education_level,
                "subjects": subjects,
                "learning_style": learning_style,
                "time_availability": time_availability,
                "difficulty_level": difficulty_level,
                "learning_goals": learning_goals,
                "resource_types": resource_types,
                "certification_preferred": certification,
                "paid_content_included": paid_content
            }
            
            # Store the preferences in session state to access in other tabs
            st.session_state.user_preferences = user_preferences
            st.session_state.show_recommendations = True
            
            # Jump to recommendations tab
            st.info("Preferences saved! Check the Recommendations tab for your personalized learning plan.")

# Recommendations Tab
with tab2:
    if 'show_recommendations' in st.session_state and st.session_state.show_recommendations:
        st.header("Your Personalized Learning Recommendations")
        
        with st.spinner("Generating recommendations with Gemini AI..."):
            try:
                # Call the Gemini API through our integration module
                recommendations = get_learning_recommendations(st.session_state.user_preferences)
                
                # Display the recommendations
                st.markdown("## Based on your preferences, we recommend:")
                st.markdown(recommendations)
                
                # Add a save button (functionality to be implemented)
                if st.button("Save these recommendations to your profile"):
                    st.success("Recommendations saved to your profile!")
                    
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
                st.info("Please make sure your Gemini API key is correctly set up in the .env file")
    else:
        st.info("Complete your preferences in the 'Your Preferences' tab and click 'Get Recommendations' to see personalized suggestions.")

# History Tab
with tab3:
    st.header("Your Learning Journey")
    st.info("This tab will display your saved recommendations and learning progress. Complete your profile to start tracking your learning journey.")
    
    # Placeholder for user analytics
    if 'user_preferences' in st.session_state and st.session_state.user_preferences.get('username'):
        st.subheader(f"Welcome back, {st.session_state.user_preferences['username']}!")
        st.write("Your previous recommendations will appear here once you start saving them.")
    else:
        st.warning("Please enter a username in the sidebar to view your history.")

# Student Analytics Tab
with tab4:
    st.header("Student Analytics")
    st.markdown("This tab will display graphical representations of student learning activities.")
    
    # Sample data for weekly learning hours
    weekly_data = {
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Hours': [10, 15, 20, 25]
    }
    weekly_df = pd.DataFrame(weekly_data)
    
    # Display a bar chart for weekly learning hours
    st.subheader("Weekly Learning Hours")
    st.bar_chart(weekly_df.set_index('Week'))

    # Sample data for monthly learning hours
    monthly_data = {
        'Month': ['January', 'February', 'March', 'April'],
        'Hours': [40, 50, 60, 70]
    }
    monthly_df = pd.DataFrame(monthly_data)
    
    # Display a line chart for monthly learning hours
    st.subheader("Monthly Learning Hours")
    st.line_chart(monthly_df.set_index('Month'))
