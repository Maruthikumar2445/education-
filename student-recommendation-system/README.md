# Student Learning Recommendation System

## Overview

The Student Learning Recommendation System is an AI-powered application that provides personalized educational resource recommendations based on students' learning preferences, goals, and learning styles. The system uses Google's Gemini AI to generate tailored learning plans and resource suggestions.

![Student Learning Recommendation System](https://i.imgur.com/example-screenshot.png)

## Features

- **Personalized Learning Recommendations**: Get customized resource recommendations based on your educational level, subject interests, learning style, and goals.
- **User-Friendly Interface**: Streamlit-based UI makes it easy to input preferences and view recommendations.
- **Flexible Resource Types**: Discover various learning resources including online courses, videos, books, interactive tools, and more.
- **Learning History**: Track your recommendations and learning journey over time.
- **Analytics Dashboard**: Visualize usage patterns, popular subjects, and recommendation effectiveness (admin feature).

## Project Structure

```
student-recommendation-system/
├── app/               # Main Streamlit application
│   └── app.py         # User interface for the recommendation system
├── api/               # API integration
│   └── gemini_integration.py  # Integration with Google's Gemini AI
├── data/              # Data storage and management
│   ├── profiles/      # User profile data
│   ├── preferences/   # User preferences data
│   ├── recommendations/ # Stored recommendations
│   └── data_manager.py # Data handling utilities
├── analytics/         # Analytics dashboard
│   └── dashboard.py   # Admin dashboard for system analytics
├── .env               # Environment variables (API keys, etc.)
└── requirements.txt   # Project dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get one from [https://ai.google.dev/](https://ai.google.dev/))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/student-recommendation-system.git
   cd student-recommendation-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your API key:
   - Rename `.env.example` to `.env` (if needed)
   - Add your Google Gemini API key to the `.env` file:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

### Running the Application

Start the main application:

```
streamlit run app/app.py
```

### Using the Recommendation System

1. Enter your username in the sidebar
2. Fill out your educational level, subject interests, and learning preferences
3. Click "Get Recommendations" to receive personalized learning suggestions
4. Save recommendations you find useful to your profile
5. Track your learning journey in the History tab

### Accessing the Analytics Dashboard

Start the analytics dashboard (admin only):

```
streamlit run analytics/dashboard.py
```

## Future Enhancements

- Integration with learning management systems
- Social features for collaborative learning
- Progress tracking and achievement badges
- Mobile application
- Database migration for improved performance and scalability

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google Generative AI for powering the recommendation engine
- Streamlit for the interactive web interface

---

Created as a demonstration of AI-assisted educational technology.

