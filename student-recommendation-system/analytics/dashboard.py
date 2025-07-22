import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import time
import calendar
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import from data module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_manager import DataManager

# Initialize the data manager
data_manager = DataManager()

# Set page configuration
st.set_page_config(
    page_title="Learning Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dashboard title and description
st.title("Student Learning Analytics Dashboard")
st.markdown("""
This dashboard provides insights into student learning patterns, preferences, and recommendation effectiveness.
Use these analytics to understand user engagement and optimize the recommendation system.
""")

# Sidebar for filters and options
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Admin authentication (simple placeholder)
    admin_password = st.text_input("Admin Password", type="password")
    if not admin_password:
        st.warning("Please enter admin password to access all features")
    
    st.divider()
    
    # Time period filter
    st.subheader("Time Period")
    time_period = st.radio(
        "Select time period:",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )
    
    # Student filter (for individual student analytics)
    st.subheader("Student Selection")
    students = ["All Students", "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis", "David Wilson"]
    selected_student = st.selectbox("Select student:", students)
    
    st.divider()
    
    # Data refresh button
    if st.button("Refresh Data"):
        st.success("Data refreshed successfully!")
        st.balloons()

# Main dashboard content in tabs
tab1, tab2, tab3, tab4 = st.tabs(["User Engagement", "Subject Popularity", "Recommendation Effectiveness", "Student Analytics Tracking"])

# User Engagement Tab
with tab1:
    st.header("User Engagement Metrics")
    
    # Key metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Users",
            value="152",
            delta="↑ 12 this week"
        )
    
    with col2:
        st.metric(
            label="Active Users (Last 30 Days)",
            value="87",
            delta="↑ 5%"
        )
        
    with col3:
        st.metric(
            label="Average Session Duration",
            value="18 min",
            delta="↑ 2 min"
        )
    
    # User activity over time
    st.subheader("User Activity Over Time")
    
    # Create sample data for demonstration
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    activity_data = {
        'Date': dates,
        'New Users': [5, 7, 4, 8, 10, 12, 9, 8, 7, 6, 9, 11, 13, 10, 9, 7, 8, 12, 15, 18, 16, 14, 13, 15, 17, 19, 16, 14, 12, 10],
        'Active Users': [20, 22, 19, 25, 27, 30, 28, 26, 23, 25, 28, 31, 35, 33, 32, 29, 30, 34, 38, 42, 40, 37, 36, 38, 41, 45, 42, 38, 35, 32],
        'Sessions': [35, 38, 32, 40, 45, 48, 46, 42, 39, 41, 43, 47, 52, 50, 48, 45, 46, 51, 55, 60, 58, 54, 52, 55, 58, 63, 60, 56, 52, 48]
    }
    
    activity_df = pd.DataFrame(activity_data)
    activity_df['Date'] = activity_df['Date'].dt.strftime('%Y-%m-%d')
    
    # Create the line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['New Users'],
        mode='lines+markers',
        name='New Users'
    ))
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['Active Users'],
        mode='lines+markers',
        name='Active Users'
    ))
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['Sessions'],
        mode='lines+markers',
        name='Sessions'
    ))
    
    fig.update_layout(
        title='Daily User Activity',
        xaxis_title='Date',
        yaxis_title='Count',
        legend_title='Metric',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # User retention analysis
    st.subheader("User Retention Analysis")
    
    # Sample retention rates (percentages)
    weeks = ['Week ' + str(i) for i in range(1, 9)]
    cohorts = ['Cohort ' + str(i) for i in range(1, 9)]
    
    retention_data = [
        [100, 80, 70, 65, 60, 55, 50, 45],  # Cohort 1
        [100, 75, 65, 60, 55, 50, 45, 0],   # Cohort 2
        [100, 85, 75, 70, 65, 60, 0, 0],    # Cohort 3
        [100, 90, 80, 75, 70, 0, 0, 0],     # Cohort 4
        [100, 85, 75, 70, 0, 0, 0, 0],      # Cohort 5
        [100, 80, 70, 0, 0, 0, 0, 0],       # Cohort 6
        [100, 85, 0, 0, 0, 0, 0, 0],        # Cohort 7
        [100, 0, 0, 0, 0, 0, 0, 0],         # Cohort 8
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=retention_data,
        x=weeks,
        y=cohorts,
        colorscale='Viridis',
        showscale=True
    ))
    
    fig.update_layout(
        title='User Retention by Cohort (%)',
        xaxis_title='Week',
        yaxis_title='Cohort',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Subject Popularity Tab
with tab2:
    st.header("Subject Popularity Analysis")
    
    # Subject distribution
    st.subheader("Subject Distribution")
    
    subject_data = {
        'Computer Science': 35,
        'Mathematics': 28,
        'Physics': 15,
        'Biology': 10,
        'Chemistry': 8,
        'Economics': 12,
        'History': 7,
        'Literature': 5,
        'Psychology': 9,
        'Engineering': 18
    }
    
    subject_df = pd.DataFrame({
        'Subject': list(subject_data.keys()),
        'Count': list(subject_data.values())
    })
    
    # Create bar chart for subject popularity
    fig1 = px.bar(
        subject_df, 
        x='Subject', 
        y='Count',
        title='Most Popular Learning Subjects',
        color='Count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Subject popularity pie chart
    fig2 = px.pie(
        subject_df,
        values='Count',
        names='Subject',
        title='Subject Distribution in Recommendations',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=500)
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Trends over time
    st.subheader("Subject Popularity Trends")
    
    # Sample data for trends over time
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    trends_data = pd.DataFrame({
        'Month': months * 3,
        'Subject': ['Computer Science'] * 6 + ['Mathematics'] * 6 + ['Physics'] * 6,
        'Popularity': [30, 32, 35, 38, 40, 35, 25, 27, 28, 30, 28, 29, 12, 13, 14, 15, 17, 15]
    })
    
    fig3 = px.line(
        trends_data, 
        x='Month', 
        y='Popularity', 
        color='Subject',
        title='Subject Popularity Trends Over Time',
        markers=True
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# Recommendation Effectiveness Tab
with tab3:
    st.header("Recommendation Effectiveness")
    
    # Feedback ratings distribution
    st.subheader("Feedback Ratings Distribution")
    
    ratings = {
        "Very Helpful": 45,
        "Helpful": 30,
        "Neutral": 15,
        "Not Helpful": 7,
        "Not Relevant": 3
    }
    
    ratings_df = pd.DataFrame({
        'Rating': list(ratings.keys()),
        'Count': list(ratings.values())
    })
    
    fig = px.bar(
        ratings_df,
        x='Rating',
        y='Count',
        title='Feedback Ratings Distribution',
        color='Count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Resource type effectiveness
    st.subheader("Resource Type Effectiveness")
    
    resource_types = {
        'Online Courses': 4.5,
        'Videos': 4.3,
        'Books': 3.8,
        'Interactive Tools': 4.7,
        'Tutorials': 4.2,
        'Research Papers': 3.5,
        'Projects': 4.6
    }
    
    resource_df = pd.DataFrame({
        'Resource Type': list(resource_types.keys()),
        'Effectiveness Rating': list(resource_types.values())
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        resource_df,
        y='Resource Type',
        x='Effectiveness Rating',
        title='Resource Type Effectiveness (Rating out of 5)',
        orientation='h',
        color='Effectiveness Rating',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(xaxis_range=[0, 5])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Completion rates
    st.subheader("Recommendation Completion Rates")
    
    completion_data = {
        'Subject': ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Chemistry', 'Economics'],
        'Started': [100, 85, 70, 60, 55, 65],
        'Completed': [75, 60, 40, 35, 30, 45],
    }
    
    completion_df = pd.DataFrame(completion_data)
    completion_df['Completion Rate'] = (completion_df['Completed'] / completion_df['Started'] * 100).round(1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=completion_df['Subject'],
        y=completion_df['Started'],
        name='Started',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=completion_df['Subject'],
        y=completion_df['Completed'],
        name='Completed',
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title='Recommendation Completion by Subject',
        xaxis_title='Subject',
        yaxis_title='Count',
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add completion rate as a table
    st.subheader("Completion Rate Details")
    st.dataframe(
        completion_df[['Subject', 'Started', 'Completed', 'Completion Rate']],
        column_config={
            "Completion Rate": st.column_config.ProgressColumn(
                "Completion Rate (%)",
                format="%f%%",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
        use_container_width=True
    )

# Student Analytics Tracking Tab
with tab4:
    # Header with dynamic student selection
    if selected_student == "All Students":
        st.header("Student Analytics Tracking - Aggregate View")
        st.info("Showing aggregated data for all students. Select a specific student from the sidebar for individual analytics.")
    else:
        st.header(f"Student Analytics Tracking - {selected_student}")
    
    # Create two columns for performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Sample metrics for different students (in a real app, this would come from database)
    if selected_student == "All Students":
        avg_weekly_hours = 8.5
        total_subjects = 6
        completion_rate = 72.3
        avg_rating = 4.1
    elif selected_student == "John Smith":
        avg_weekly_hours = 10.2
        total_subjects = 5
        completion_rate = 85.7
        avg_rating = 4.5
    elif selected_student == "Emily Johnson":
        avg_weekly_hours = 7.8
        total_subjects = 4
        completion_rate = 68.9
        avg_rating = 4.2
    elif selected_student == "Michael Brown":
        avg_weekly_hours = 6.5
        total_subjects = 3
        completion_rate = 75.2
        avg_rating = 3.9
    elif selected_student == "Sarah Davis":
        avg_weekly_hours = 9.3
        total

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import time
import calendar
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import from data module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_manager import DataManager

# Initialize the data manager
data_manager = DataManager()

# Set page configuration
st.set_page_config(
    page_title="Learning Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dashboard title and description
st.title("Student Learning Analytics Dashboard")
st.markdown("""
This dashboard provides insights into student learning patterns, preferences, and recommendation effectiveness.
Use these analytics to understand user engagement and optimize the recommendation system.
""")

# Sidebar for filters and options
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Admin authentication (simple placeholder)
    admin_password = st.text_input("Admin Password", type="password")
    if not admin_password:
        st.warning("Please enter admin password to access all features")
    
    st.divider()
    
    # Time period filter
    st.subheader("Time Period")
    time_period = st.radio(
        "Select time period:",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )
    
    # Student filter (for individual student analytics)
    st.subheader("Student Selection")
    students = ["All Students", "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis", "David Wilson"]
    selected_student = st.selectbox("Select student:", students)
    
    st.divider()
    
    # Data refresh button
    if st.button("Refresh Data"):
        st.success("Data refreshed successfully!")
        st.balloons()

# Main dashboard content in tabs
tab1, tab2, tab3, tab4 = st.tabs(["User Engagement", "Subject Popularity", "Recommendation Effectiveness", "Student Analytics Tracking"])

# User Engagement Tab
with tab1:
    st.header("User Engagement Metrics")
    
    # Key metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Users",
            value="152",
            delta="↑ 12 this week"
        )
    
    with col2:
        st.metric(
            label="Active Users (Last 30 Days)",
            value="87",
            delta="↑ 5%"
        )
        
    with col3:
        st.metric(
            label="Average Session Duration",
            value="18 min",
            delta="↑ 2 min"
        )
    
    # User activity over time
    st.subheader("User Activity Over Time")
    
    # Create sample data for demonstration
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    activity_data = {
        'Date': dates,
        'New Users': [5, 7, 4, 8, 10, 12, 9, 8, 7, 6, 9, 11, 13, 10, 9, 7, 8, 12, 15, 18, 16, 14, 13, 15, 17, 19, 16, 14, 12, 10],
        'Active Users': [20, 22, 19, 25, 27, 30, 28, 26, 23, 25, 28, 31, 35, 33, 32, 29, 30, 34, 38, 42, 40, 37, 36, 38, 41, 45, 42, 38, 35, 32],
        'Sessions': [35, 38, 32, 40, 45, 48, 46, 42, 39, 41, 43, 47, 52, 50, 48, 45, 46, 51, 55, 60, 58, 54, 52, 55, 58, 63, 60, 56, 52, 48]
    }
    
    activity_df = pd.DataFrame(activity_data)
    activity_df['Date'] = activity_df['Date'].dt.strftime('%Y-%m-%d')
    
    # Create the line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['New Users'],
        mode='lines+markers',
        name='New Users'
    ))
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['Active Users'],
        mode='lines+markers',
        name='Active Users'
    ))
    
    fig.add_trace(go.Scatter(
        x=activity_df['Date'],
        y=activity_df['Sessions'],
        mode='lines+markers',
        name='Sessions'
    ))
    
    fig.update_layout(
        title='Daily User Activity',
        xaxis_title='Date',
        yaxis_title='Count',
        legend_title='Metric',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # User retention analysis
    st.subheader("User Retention Analysis")
    
    # Sample retention rates (percentages)
    weeks = ['Week ' + str(i) for i in range(1, 9)]
    cohorts = ['Cohort ' + str(i) for i in range(1, 9)]
    
    retention_data = [
        [100, 80, 70, 65, 60, 55, 50, 45],  # Cohort 1
        [100, 75, 65, 60, 55, 50, 45, 0],   # Cohort 2
        [100, 85, 75, 70, 65, 60, 0, 0],    # Cohort 3
        [100, 90, 80, 75, 70, 0, 0, 0],     # Cohort 4
        [100, 85, 75, 70, 0, 0, 0, 0],      # Cohort 5
        [100, 80, 70, 0, 0, 0, 0, 0],       # Cohort 6
        [100, 85, 0, 0, 0, 0, 0, 0],        # Cohort 7
        [100, 0, 0, 0, 0, 0, 0, 0],         # Cohort 8
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=retention_data,
        x=weeks,
        y=cohorts,
        colorscale='Viridis',
        showscale=True
    ))
    
    fig.update_layout(
        title='User Retention by Cohort (%)',
        xaxis_title='Week',
        yaxis_title='Cohort',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Subject Popularity Tab
with tab2:
    st.header("Subject Popularity Analysis")
    
    # Subject distribution
    st.subheader("Subject Distribution")
    
    subject_data = {
        'Computer Science': 35,
        'Mathematics': 28,
        'Physics': 15,
        'Biology': 10,
        'Chemistry': 8,
        'Economics': 12,
        'History': 7,
        'Literature': 5,
        'Psychology': 9,
        'Engineering': 18
    }
    
    subject_df = pd.DataFrame({
        'Subject': list(subject_data.keys()),
        'Count': list(subject_data.values())
    })
    
    # Create bar chart for subject popularity
    fig1 = px.bar(
        subject_df, 
        x='Subject', 
        y='Count',
        title='Most Popular Learning Subjects',
        color='Count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Subject popularity pie chart
    fig2 = px.pie(
        subject_df,
        values='Count',
        names='Subject',
        title='Subject Distribution in Recommendations',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=500)
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Trends over time
    st.subheader("Subject Popularity Trends")
    
    # Sample data for trends over time
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    trends_data = pd.DataFrame({
        'Month': months * 3,
        'Subject': ['Computer Science'] * 6 + ['Mathematics'] * 6 + ['Physics'] * 6,
        'Popularity': [30, 32, 35, 38, 40, 35, 25, 27, 28, 30, 28, 29, 12, 13, 14, 15, 17, 15]
    })
    
    fig3 = px.line(
        trends_data, 
        x='Month', 
        y='Popularity', 
        color='Subject',
        title='Subject Popularity Trends Over Time',
        markers=True
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# Recommendation Effectiveness Tab
with tab3:
    st.header("Recommendation Effectiveness")
    
    # Feedback ratings distribution
    st.subheader("Feedback Ratings Distribution")
    
    ratings = {
        "Very Helpful": 45,
        "Helpful": 30,
        "Neutral": 15,
        "Not Helpful": 7,
        "Not Relevant": 3
    }
    
    ratings_df = pd.DataFrame({
        'Rating': list(ratings.keys()),
        'Count': list(ratings.values())
    })
    
    fig = px.bar(
        ratings_df,
        x='Rating',
        y='Count',
        title='Feedback Ratings Distribution',
        color='Count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Resource type effectiveness
    st.subheader("Resource Type Effectiveness")
    
    resource_types = {
        'Online Courses': 4.5,
        'Videos': 4.3,
        'Books': 3.8,
        'Interactive Tools': 4.7,
        'Tutorials': 4.2,
        'Research Papers': 3.5,
        'Projects': 4.6
    }
    
    resource_df = pd.DataFrame({
        'Resource Type': list(resource_types.keys()),
        'Effectiveness Rating': list(resource_types.values())
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        resource_df,
        y='Resource Type',
        x='Effectiveness Rating',
        title='Resource Type Effectiveness (Rating out of 5)',
        orientation='h',
        color='Effectiveness Rating',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(xaxis_range=[0, 5])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Completion rates
    st.subheader("Recommendation Completion Rates")
    
    completion_data = {
        'Subject': ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Chemistry', 'Economics'],
        'Started': [100, 85, 70, 60, 55, 65],
        'Completed': [75, 60, 40, 35, 30, 45],
    }
    
    completion_df = pd.DataFrame(completion_data)
    completion_df['Completion Rate'] = (completion_df['Completed'] / completion_df['Started'] * 100).round(1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=completion_df['Subject'],
        y=completion_df['Started'],
        name='Started',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=completion_df['Subject'],
        y=completion_df['Completed'],
        name='Completed',
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title='Recommendation Completion by Subject',
        xaxis_title='Subject',
        yaxis_title='Count',
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add completion rate as a table
    st.subheader("Completion Rate Details")
    st.dataframe(
        completion_df[['Subject', 'Started', 'Completed', 'Completion Rate']],
        column_config={
            "Completion Rate": st.column_config.ProgressColumn(
                "Completion Rate (%)",
                format="%f%%",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
        use_container_width=True
    )

# Footer with note about the data
# Student Analytics Tracking Tab
with tab4:
    # Header with dynamic student selection
    if 'selected_student' in locals() and selected_student != "All Students":
        st.header(f"Student Analytics Tracking - {selected_student}")
    else:
        st.header("Student Analytics Tracking - Aggregate View")
        st.info("Showing aggregated data for all students. Select a specific student from the sidebar for individual analysis.")
    
    # Weekly learning time tracking
    st.subheader("Weekly Learning Time Tracking")
    
    # Create sample data for weekly learning time
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Generate sample data for current week
    current_week_data = {
        'Day': days_of_week,
        'Hours': [2.5, 1.8, 3.2, 2.7, 1.5, 4.0, 2.2] if selected_student == "John Smith" else
                [1.5, 2.8, 2.2, 3.0, 2.5, 1.0, 3.5] if selected_student == "Emily Johnson" else
                [2.0, 2.5, 1.8, 3.0, 2.8, 3.2, 1.5] if selected_student == "Michael Brown" else
                [3.0, 2.0, 2.5, 1.5, 3.5, 2.0, 1.0] if selected_student == "Sarah Davis" else
                [1.5, 3.0, 2.5, 3.0, 2.0, 4.5, 1.5] if selected_student == "David Wilson" else
                [2.1, 2.4, 2.4, 2.6, 2.5, 2.9, 2.3],  # Average for all students
        'Goal': [2.0] * 7 if selected_student != "All Students" else [2.5] * 7
    }
    
    # Generate sample data for previous week
    previous_week_data = {
        'Day': days_of_week,
        'Hours': [2.1, 1.5, 2.8, 2.3, 1.2, 3.5, 1.8] if selected_student == "John Smith" else
                [1.2, 2.5, 1.8, 2.7, 2.2, 0.8, 3.0] if selected_student == "Emily Johnson" else
                [1.7, 2.2, 1.5, 2.5, 2.4, 2.8, 1.2] if selected_student == "Michael Brown" else
                [2.7, 1.8, 2.2, 1.3, 3.1, 1.7, 0.8] if selected_student == "Sarah Davis" else
                [1.3, 2.7, 2.2, 2.7, 1.8, 4.0, 1.2] if selected_student == "David Wilson" else
                [1.8, 2.1, 2.2, 2.3, 2.2, 2.7, 2.0]  # Average for all students
    }
    
    # Class average data for comparison
    class_average_data = {
        'Day': days_of_week,
        'Hours': [1.8, 2.1, 2.2, 2.3, 2.2, 2.7, 2.0]
    }
    
    weekly_df = pd.DataFrame(current_week_data)
    previous_weekly_df = pd.DataFrame(previous_week_data)
    class_avg_df = pd.DataFrame(class_average_data)
    
    # Create a bar chart for weekly learning time with comparisons
    fig_weekly = go.Figure()
    
    # Add bar for previous week
    fig_weekly.add_trace(go.Bar(
        x=previous_weekly_df['Day'],
        y=previous_weekly_df['Hours'],
        name='Previous Week',
        marker_color='rgba(55, 83, 109, 0.5)',
        opacity=0.7
    ))
    
    # Add bar for current week
    fig_weekly.add_trace(go.Bar(
        x=weekly_df['Day'],
        y=weekly_df['Hours'],
        name='Current Week',
        marker_color='rgb(55, 83, 109)'
    ))
    
    # Add line for class average
    fig_weekly.add_trace(go.Scatter(
        x=class_avg_df['Day'],
        y=class_avg_df['Hours'],
        mode='lines',
        name='Class Average',
        marker_color='rgba(50, 171, 96, 0.7)',
        line=dict(width=2)
    ))
    
    # Add daily goal line
    fig_weekly.add_trace(go.Scatter(
        x=weekly_df['Day'],
        y=weekly_df['Goal'],
        mode='lines+markers',
        name='Daily Goal',
        marker_color='rgba(220, 20, 60, 0.7)',
        line=dict(dash='dash')
    ))
    fig_weekly.update_layout(
        title=f'Weekly Learning Time ({time.strftime("%b %d")} - {time.strftime("%b %d")}, {time.strftime("%Y")})',
        xaxis_title='Day of Week',
        yaxis_title='Hours',
        legend_title='Metric',
        barmode='group',
        height=400,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        )
    )
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Weekly summary with comparisons
    total_hours = weekly_df['Hours'].sum()
    prev_total_hours = previous_weekly_df['Hours'].sum()
    class_avg_hours = class_avg_df['Hours'].sum()
    goal_hours = weekly_df['Goal'].mean() * 7
    achievement_pct = (total_hours / goal_hours * 100).round(1)
    
    # Calculate week-over-week change
    wow_change = ((total_hours - prev_total_hours) / prev_total_hours * 100).round(1)
    vs_class_avg = ((total_hours - class_avg_hours) / class_avg_hours * 100).round(1)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Hours This Week",
            value=f"{total_hours:.1f}",
            delta=f"{total_hours - prev_total_hours:.1f} hrs vs. last week",
            delta_color="normal" if total_hours >= prev_total_hours else "inverse"
        )
    with col2:
        st.metric(
            label="Weekly Goal",
            value=f"{goal_hours:.1f}",
            delta=f"{achievement_pct}% Complete",
            delta_color="normal" if achievement_pct >= 85 else "inverse"
        )
    with col3:
        st.metric(
            label="Week-over-Week Change",
            value=f"{wow_change}%",
            delta="Improvement" if wow_change > 0 else "Decline",
            delta_color="normal" if wow_change > 0 else "inverse"
        )
    with col4:
        st.metric(
            label="vs. Class Average",
            value=f"{total_hours:.1f} hrs",
            delta=f"{vs_class_avg}%",
            delta_color="normal" if vs_class_avg > 0 else "inverse"
        )
    
    # Display weekly improvement insights
    if selected_student != "All Students":
        st.info(f"""
        **Weekly Insights**: 
        {selected_student}'s study time has {'increased' if wow_change > 0 else 'decreased'} by {abs(wow_change)}% compared to last week.
        {'This is a positive trend that should be maintained.' if wow_change > 0 else 'This indicates a need for improved time management.'}
        {'The student is performing above class average.' if vs_class_avg > 0 else 'The student is below class average and may need additional support.'}
        """)
    # Monthly learning tracking
    st.subheader("Monthly Learning Progress")
    
    # Create sample data for monthly tracking
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Number of days in current month
    num_days = calendar.monthrange(current_year, current_month)[1]
    days_in_month = [f"{current_month}/{day}" for day in range(1, num_days + 1)]
    
    # Generate different patterns based on selected student
    if selected_student == "John Smith":
        monthly_pattern = [np.sin(i/3.5) * 1.5 + 2.5 for i in range(num_days)]
    elif selected_student == "Emily Johnson":
        monthly_pattern = [np.cos(i/4) * 1.2 + 2.3 for i in range(num_days)]
    elif selected_student == "Michael Brown":
        monthly_pattern = [np.sin(i/5) * 1.8 + 2.0 for i in range(num_days)]
    elif selected_student == "Sarah Davis":
        monthly_pattern = [np.cos(i/6) * 1.5 + 2.5 for i in range(num_days)]
    elif selected_student == "David Wilson":
        monthly_pattern = [np.sin(i/4.5) * 2.0 + 2.0 for i in range(num_days)]
    else:  # All students
        monthly_pattern = [np.sin(i/5) * 0.8 + 2.5 for i in range(num_days)]
    
    # Ensure all values are positive
    monthly_hours = [max(1.0, round(h, 1)) for h in monthly_pattern]
    
    # Create DataFrame for monthly data
    monthly_data = {
        'Day': days_in_month,
        'Hours': monthly_hours,
        'Cumulative Hours': np.cumsum(monthly_hours)
    }
    
    monthly_df = pd.DataFrame(monthly_data)
    
    # Create monthly progress chart
    fig_monthly = go.Figure()
    
    fig_monthly.add_trace(go.Scatter(
        x=monthly_df['Day'],
        y=monthly_df['Hours'],
        mode='lines+markers',
        name='Daily Hours',
        marker=dict(size=8),
        line=dict(width=2)
    ))
    
    fig_monthly.add_trace(go.Scatter(
        x=monthly_df['Day'],
        y=monthly_df['Cumulative Hours'],
        mode='lines',
        name='Cumulative Hours',
        yaxis="y2",
        line=dict(width=3, color='rgba(55, 128, 191, 0.7)')
    ))
    
    fig_monthly.update_layout(
        title=f'Monthly Learning Progress - {calendar.month_name[current_month]} {current_year}',
        xaxis_title='Day',
        yaxis_title='Daily Hours',
        legend_title='Metric',
        height=450,
        hovermode="x unified",
        yaxis2=dict(
            title="Cumulative Hours",
            overlaying="y",
            side="right"
        )
    )
    
    # Only show some x-axis labels to avoid overcrowding
    fig_monthly.update_xaxes(
        tickvals=[f"{current_month}/{day}" for day in range(1, num_days + 1, 5)]
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Monthly learning heatmap
    st.subheader("Monthly Learning Intensity Heatmap")
    
    # Create a heatmap visualization showing daily learning intensity
    # First, reorganize the data into weeks and days
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Generate the date for each day in the month
    month_dates = [datetime(current_year, current_month, day) for day in range(1, num_days + 1)]
    
    # Create a list of weeks in the month (0-indexed week number)
    week_numbers = [(date.day - 1) // 7 for date in month_dates]
    
    # Create a list of day names for each date
    day_names = [date.strftime("%a") for date in month_dates]
    
    # Create a DataFrame with week, day, and hours
    heatmap_data = pd.DataFrame({
        'Date': [f"{date.month}/{date.day}" for date in month_dates],
        'Week': week_numbers,
        'Day': day_names,
        'Hours': monthly_hours,
        'DayNum': [date.day for date in month_dates]
    })
    
    # Pivot the data for the heatmap
    heatmap_pivot = heatmap_data.pivot_table(
        index='Week', 
        columns='Day', 
        values='Hours',
        aggfunc='first'
    ).fillna(0)
    
    # Reorder the columns to proper weekday order
    ordered_days = [day[:3] for day in week_days]
    heatmap_pivot = heatmap_pivot.reindex(columns=ordered_days, fill_value=0)
    
    # Create the heatmap
    fig_heatmap = px.imshow(
        heatmap_pivot,
        labels=dict(x="Day of Week", y="Week", color="Hours Studied"),
        x=heatmap_pivot.columns,
        y=[f"Week {i+1}" for i in range(len(heatmap_pivot))],
        color_continuous_scale='Viridis',
        aspect="auto",
        title=f"Learning Intensity Heatmap - {calendar.month_name[current_month]} {current_year}"
    )
    
    # Add custom hover data
    hovertemplate = "<b>%{x}, Week %{y}</b><br>Hours: %{z:.1f}<br><extra></extra>"
    fig_heatmap.update_traces(hovertemplate=hovertemplate)
    
    # Update layout
    fig_heatmap.update_layout(
        height=350,
        coloraxis_colorbar=dict(
            title="Hours",
            thicknessmode="pixels", thickness=15,
            lenmode="pixels", len=300,
            yanchor="top", y=1,
            ticks="outside"
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="",
        yaxis_title=""
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Weekly comparison within the month
    st.subheader("Weekly Comparison Within Month")
    
    # Calculate weekly totals
    weekly_totals = []
    weekly_averages = []
    week_labels = []
    
    for week in range(max(week_numbers) + 1):
        week_data = heatmap_data[heatmap_data['Week'] == week]
        total = week_data['Hours'].sum()
        avg = week_data['Hours'].mean()
        weekly_totals.append(total)
        weekly_averages.append(avg)
        week_labels.append(f"Week {week + 1}")
    
    # Create DataFrame for the weekly comparison
    weekly_comparison = pd.DataFrame({
        'Week': week_labels,
        'Total Hours': weekly_totals,
        'Daily Average': weekly_averages
    })
    
    # Create a bar chart with weekly comparison
    fig_weekly_comparison = go.Figure()
    
    # Add bar for total hours
    fig_weekly_comparison.add_trace(go.Bar(
        x=weekly_comparison['Week'],
        y=weekly_comparison['Total Hours'],
        name='Total Hours',
        marker_color='rgb(55, 83, 109)',
        hovertemplate='<b>%{x}</b><br>Total Hours: %{y:.1f}<extra></extra>'
    ))
    
    # Add line for daily average
    fig_weekly_comparison.add_trace(go.Scatter(
        x=weekly_comparison['Week'],
        y=weekly_comparison['Daily Average'],
        mode='lines+markers',
        name='Daily Average',
        marker=dict(size=8),
        line=dict(color='rgba(220, 20, 60, 0.7)', width=2),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Daily Average: %{y:.1f} hrs<extra></extra>'
    ))
    
    # Update layout
    fig_weekly_comparison.update_layout(
        title=f'Weekly Learning Comparison - {calendar.month_name[current_month]} {current_year}',
        xaxis_title='',
        yaxis_title='Total Hours',
        legend_title='Metric',
        height=350,
        hovermode='x unified',
        yaxis2=dict(
            title='Daily Average (hrs)',
            overlaying='y',
            side='right',
            range=[0, max(weekly_comparison['Daily Average']) * 1.5]
        ),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    st.plotly_chart(fig_weekly_comparison, use_container_width=True)
    
    # Insights and weekly progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate current week data
    current_week = max(0, max(week_numbers))
    current_week_total = weekly_totals[current_week]
    current_week_avg = weekly_averages[current_week]
    
    # Calculate previous week data if available
    if current_week > 0:
        prev_week_total = weekly_totals[current_week - 1]
        prev_week_avg = weekly_averages[current_week - 1]
        week_change = ((current_week_total - prev_week_total) / prev_week_total * 100).round(1)
        avg_change = ((current_week_avg - prev_week_avg) / prev_week_avg * 100).round(1)
    else:
        week_change = 0
        avg_change = 0
    
    # Best day calculation
    best_day_idx = monthly_hours.index(max(monthly_hours))
    best_day = days_in_month[best_day_idx]
    
    # Consistency score (standard deviation - lower is more consistent)
    consistency = (100 - min(100, np.std(monthly_hours) * 20)).round(1)
    
    with col1:
        st.metric(
            label="This Month Total",
            value=f"{sum(monthly_hours):.1f} hrs",
            delta=f"{current_week_total:.1f} hrs this week",
            delta_color="normal"
        )
    with col2:
        st.metric(
            label="Weekly Average",
            value=f"{np.mean(weekly_totals):.1f} hrs",
            delta=f"{week_change}%" if current_week > 0 else None,
            delta_color="normal" if week_change >= 0 else "inverse"
        )
    with col3:
        st.metric(
            label="Best Day",
            value=f"{best_day}",
            delta=f"{max(monthly_hours):.1f} hrs",
            delta_color="normal"
        )
    with col4:
        st.metric(
            label="Consistency Score",
            value=f"{consistency}%",
            delta="Higher is better",
            delta_color="off"
        )
    
    # Month-to-date insights
    if selected_student != "All Students":
        avg_daily = np.mean(monthly_hours)
        total_month = sum(monthly_hours)
        projected_month = total_month / datetime.now().day * num_days
        
        st.info(f"""
        **Monthly Insights**: 
        {selected_student} has studied a total of {total_month:.1f} hours this month, with an average of {avg_daily:.1f} hours per day.
        At this pace, the projected monthly total is {projected_month:.1f} hours.
        {'Consistency is good with regular daily study habits.' if consistency > 75 else 'More consistent daily study habits would improve learning outcomes.'}
        """)
    
    # Subject-specific analytics
    st.subheader("Subject-specific Learning Analytics")
    
    # Create sample subject-specific data
    if selected_student == "John Smith":
        subject_hours = {
            'Computer Science': 22,
            'Mathematics': 18,
            'Physics': 12,
            'Economics': 8,
            'Psychology': 5
        }
        proficiency = {
            'Computer Science': 85,
            'Mathematics': 78,
            'Physics': 70,
            'Economics': 60,
            'Psychology': 45
        }
    elif selected_student == "Emily Johnson":
        subject_hours = {
            'Biology': 20,
            'Chemistry': 18,
            'Mathematics': 15,
            'Literature': 12,
            'Psychology': 10
        }
        proficiency = {
            'Biology': 88,
            'Chemistry': 82,
            'Mathematics': 75,
            'Literature': 90,
            'Psychology': 80
        }
    elif selected_student != "All Students":
        subject_hours = {
            'Computer Science': 15,
            'Mathematics': 18,
            'Physics': 10,
            'Engineering': 12,
            'Economics': 8
        }
        proficiency = {
            'Computer Science': 75,
            'Mathematics': 80,
            'Physics': 65,
            'Engineering': 70,
            'Economics': 60
        }
    else:  # All students average
        subject_hours = {
            'Computer Science': 18,
            'Mathematics': 20,
            'Physics': 12,
            'Biology': 15,
            'Chemistry': 10,
            'Economics': 8,
            'History': 7,
            'Literature': 9,
            'Psychology': 11,
            'Engineering': 14
        }
        proficiency = {
            'Computer Science': 78,
            'Mathematics': 75,
            'Physics': 68,
            'Biology': 72,
            'Chemistry': 70,
            'Economics': 65,
            'History': 60,
            'Literature': 72,
            'Psychology': 68,
            'Engineering': 71
        }
    
    # Create DataFrame for subject-specific data
    subject_df = pd.DataFrame({
        'Subject': list(subject_hours.keys()),
        'Hours Spent': list(subject_hours.values()),
        'Proficiency': list(proficiency.values())
    })
    
    # Sort by hours spent
    subject_df = subject_df.sort_values('Hours Spent', ascending=False)
    
    # Create two-column layout
    col1, col2 = st.columns(2)
    
    # Hours spent per subject
    with col1:
        fig_hours = px.bar(
            subject_df, 
            y='Subject', 
            x='Hours Spent',
            orientation='h',
            title='Hours Spent per Subject',
            color='Hours Spent',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig_hours.update_layout(height=400)
        st.plotly_chart(fig_hours, use_container_width=True)
    
    # Proficiency per subject
    with col2:
        fig_prof = px.bar(
            subject_df, 
            y='Subject', 
            x='Proficiency',
            orientation='h',
            title='Proficiency Level by Subject (%)',
            color='Proficiency',
            color_continuous_scale=px.colors.sequential.Plasma,
            range_x=[0, 100]
        )
        
        fig_prof.update_layout(height=400)
        st.plotly_chart(fig_prof, use_container_width=True)
    
    # Learning Goal Completion Tracking
    st.subheader("Learning Goal Completion Tracking")
    
    # Sample learning goals
    if selected_student == "John Smith":
        goals = [
            "Complete Python Data Structures course",
            "Finish Calculus II assignments",
            "Read 3 research papers on AI ethics",
            "Complete Physics lab experiments",
            "Submit Economics research project"
        ]
        progress = [100, 85, 66, 50, 20]
        deadlines = ["2023-05-01", "2023-05-15", "2023-05-20", "2023-06-01", "2023-06-15"]
    elif selected_student == "Emily Johnson":
        goals = [
            "Complete Biology cell simulation project",
            "Study organic chemistry reactions",
            "Prepare for Mathematics midterm",
            "Read Victorian literature assignment",
            "Complete psychology research methodology"
        ]
        progress = [90, 75, 60, 100, 40]
        deadlines = ["2023-05-05", "2023-05-18", "2023-05-25", "2023-05-10", "2023-06-10"]
    elif selected_student != "All Students":
        goals = [
            "Complete programming assignment",
            "Study for upcoming exams",
            "Read required textbook chapters",
            "Finish group project",
            "Prepare presentation slides"
        ]
        progress = [85, 70, 60, 40, 90]
        deadlines = ["2023-05-08", "2023-05-20", "2023-05-15", "2023-06-05", "2023-05-12"]
    else:
        st.info("Please select a specific student to view their learning goals.")
        goals = []
        
