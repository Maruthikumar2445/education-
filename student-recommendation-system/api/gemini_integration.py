import os
import json
import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("gemini_integration")

# Load environment variables from .env file
dotenv_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Get the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found in environment variables. Please set it in the .env file.")

# Maximum retry attempts for API calls
MAX_RETRIES = 3
RETRY_DELAY = 2  # in seconds

def initialize_genai():
    """Initialize the Gemini API with the API key."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please add it to your .env file.")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Gemini API initialized successfully")

def get_model():
    """Get the Gemini model."""
    try:
        # Using the most capable Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        logger.error(f"Error getting Gemini model: {str(e)}")
        raise

def construct_prompt(user_preferences: Dict[str, Any]) -> str:
    """
    Construct a detailed prompt based on user preferences.
    
    Args:
        user_preferences: Dictionary containing user's learning preferences
        
    Returns:
        Formatted prompt string to send to Gemini
    """
    # Extract key preferences
    subjects = ", ".join(user_preferences.get("subjects", []))
    learning_style = user_preferences.get("learning_style", "")
    difficulty = user_preferences.get("difficulty_level", "Intermediate")
    goals = user_preferences.get("learning_goals", "")
    hours_per_week = user_preferences.get("time_availability", 10)
    edu_level = user_preferences.get("education_level", "")
    resource_types = ", ".join(user_preferences.get("resource_types", []))
    
    # Additional preferences
    certification = "certified courses" if user_preferences.get("certification_preferred", False) else ""
    paid_content = "including paid resources" if user_preferences.get("paid_content_included", False) else "focusing on free resources"
    
    # Construct the prompt
    prompt = f"""
    I'm looking for personalized learning recommendations based on the following preferences:
    
    Education Level: {edu_level}
    Subjects of Interest: {subjects}
    Learning Style: {learning_style}
    Difficulty Level: {difficulty}
    Time Availability: {hours_per_week} hours per week
    Learning Goals: {goals}
    Preferred Resource Types: {resource_types}
    Additional Preferences: {certification} {paid_content}
    
    Please provide a structured learning plan with specific resources, including:
    1. Top 3-5 recommended courses, books, or other resources for each subject
    2. Why these resources match my learning style and preferences
    3. A suggested schedule based on my time availability
    4. Additional tools or communities that might help me in my learning journey
    
    For each recommendation, please include:
    - Resource name and provider
    - Brief description
    - Estimated time commitment
    - Link (if applicable)
    - Cost (if applicable)
    """
    
    return prompt

def get_learning_recommendations(user_preferences: Dict[str, Any]) -> str:
    """
    Get personalized learning recommendations from Gemini based on user preferences.
    
    Args:
        user_preferences: Dictionary containing user's learning preferences
        
    Returns:
        Formatted recommendations from Gemini
    """
    if not GOOGLE_API_KEY:
        return "⚠️ API key not configured. Please set the GOOGLE_API_KEY in your .env file."
    
    # Initialize the API if not already done
    try:
        initialize_genai()
    except ValueError as e:
        return f"Error: {str(e)}"
    
    # Get the model
    try:
        model = get_model()
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"
    
    # Construct the prompt
    prompt = construct_prompt(user_preferences)
    
    # Send request to Gemini with retry logic
    for attempt in range(MAX_RETRIES):
        try:
            # Generate content
            response = model.generate_content(prompt)
            
            # Check if the response was successful
            if hasattr(response, 'text'):
                # Log successful API call
                logger.info(f"Successfully received recommendations for user: {user_preferences.get('username', 'unknown')}")
                
                # Save the response to the data directory (optional, for history)
                try:
                    save_response_to_file(user_preferences.get('username', 'unknown'), response.text)
                except Exception as e:
                    logger.warning(f"Could not save response to file: {str(e)}")
                
                return response.text
            else:
                return "Received an empty or invalid response from Gemini."
                
        except Exception as e:
            logger.warning(f"API call attempt {attempt + 1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to get recommendations after {MAX_RETRIES} attempts")
                return f"Error generating recommendations: {str(e)}"
    
    return "Failed to generate recommendations after multiple attempts. Please try again later."

def save_response_to_file(username: str, response_text: str) -> None:
    """
    Save the API response to a file for the user's history.
    
    Args:
        username: The username to associate with this response
        response_text: The text response from Gemini
    """
    # Create a timestamp for the filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Ensure the data directory exists
    data_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'data' / 'responses'
    os.makedirs(data_dir, exist_ok=True)
    
    # Create a sanitized username for the filename
    safe_username = "".join(c if c.isalnum() else "_" for c in username)
    
    # Save the response to a file
    filename = f"{safe_username}_{timestamp}.txt"
    file_path = data_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response_text)
    
    logger.info(f"Response saved to {file_path}")

# Example usage for testing:
if __name__ == "__main__":
    # Sample preferences for testing
    test_preferences = {
        "username": "test_user",
        "education_level": "Undergraduate",
        "subjects": ["Computer Science", "Mathematics"],
        "learning_style": "Visual",
        "time_availability": 15,
        "difficulty_level": "Intermediate",
        "learning_goals": "I want to improve my programming skills and learn data science fundamentals",
        "resource_types": ["Online Courses", "Videos", "Interactive Tools"],
        "certification_preferred": True,
        "paid_content_included": False
    }
    
    # Only run this if the API key is set
    if GOOGLE_API_KEY:
        print("Testing API integration...")
        recommendations = get_learning_recommendations(test_preferences)
        print("\nRecommendations Preview:")
        print(recommendations[:500] + "..." if len(recommendations) > 500 else recommendations)
    else:
        print("Skipping API test because GOOGLE_API_KEY is not set")

