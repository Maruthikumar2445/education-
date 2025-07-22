import os
import json
import time
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("data_manager")

# Base path for data storage
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROFILES_DIR = BASE_DIR / "profiles"
RECOMMENDATIONS_DIR = BASE_DIR / "recommendations"
PREFERENCES_DIR = BASE_DIR / "preferences"
FEEDBACK_DIR = BASE_DIR / "feedback"
ANALYTICS_DIR = BASE_DIR / "analytics"

# Ensure directories exist
for directory in [PROFILES_DIR, RECOMMENDATIONS_DIR, PREFERENCES_DIR, FEEDBACK_DIR, ANALYTICS_DIR]:
    directory.mkdir(exist_ok=True)


class DataManager:
    """
    Handles data persistence for student profiles, preferences, and recommendation history.
    Currently uses JSON files for storage, but designed to be easily upgradable to a database.
    """
    
    def __init__(self):
        """Initialize the data manager and ensure storage directories exist."""
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all necessary data directories exist."""
        os.makedirs(PROFILES_DIR, exist_ok=True)
        os.makedirs(RECOMMENDATIONS_DIR, exist_ok=True)
        os.makedirs(PREFERENCES_DIR, exist_ok=True)
        os.makedirs(FEEDBACK_DIR, exist_ok=True)
        os.makedirs(ANALYTICS_DIR, exist_ok=True)
        logger.info("Data directories initialized")
    
    def _sanitize_username(self, username: str) -> str:
        """Sanitize username for file safety."""
        return "".join(c if c.isalnum() else "_" for c in username)
    
    def _get_profile_path(self, username: str) -> Path:
        """Get the file path for a user's profile."""
        safe_username = self._sanitize_username(username)
        return PROFILES_DIR / f"{safe_username}.json"
    
    def _get_preferences_path(self, username: str) -> Path:
        """Get the file path for a user's preferences."""
        safe_username = self._sanitize_username(username)
        return PREFERENCES_DIR / f"{safe_username}.json"
    
    def _get_recommendations_path(self, username: str) -> Path:
        """Get the directory path for a user's recommendations."""
        safe_username = self._sanitize_username(username)
        user_recs_dir = RECOMMENDATIONS_DIR / safe_username
        os.makedirs(user_recs_dir, exist_ok=True)
        return user_recs_dir
        
    def _get_feedback_path(self, username: str) -> Path:
        """Get the directory path for a user's feedback."""
        safe_username = self._sanitize_username(username)
        user_feedback_dir = FEEDBACK_DIR / safe_username
        os.makedirs(user_feedback_dir, exist_ok=True)
        return user_feedback_dir

    # ----- Profile CRUD Operations -----
    
    def create_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        Create a new user profile.
        
        Args:
            profile_data: Dictionary containing user profile information.
                         Must include a 'username' key.
                         
        Returns:
            True if profile was created successfully, False otherwise.
        """
        if 'username' not in profile_data:
            logger.error("Cannot create profile: username not provided")
            return False
        
        username = profile_data['username']
        profile_path = self._get_profile_path(username)
        
        # Check if profile already exists
        if profile_path.exists():
            logger.warning(f"Profile already exists for user: {username}")
            return False
        
        # Add timestamp for creation and last update
        current_time = time.time()
        profile_data['created_at'] = current_time
        profile_data['updated_at'] = current_time
        
        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
            logger.info(f"Created profile for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error creating profile for {username}: {str(e)}")
            return False
    
    def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user profile.
        
        Args:
            username: The username of the profile to retrieve.
            
        Returns:
            Dictionary containing profile data or None if profile doesn't exist.
        """
        profile_path = self._get_profile_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Profile not found for user: {username}")
            return None
        
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            logger.info(f"Retrieved profile for user: {username}")
            return profile_data
        except Exception as e:
            logger.error(f"Error retrieving profile for {username}: {str(e)}")
            return None
    
    def update_profile(self, username: str, updated_data: Dict[str, Any]) -> bool:
        """
        Update an existing user profile.
        
        Args:
            username: The username of the profile to update.
            updated_data: Dictionary containing the updated profile information.
            
        Returns:
            True if profile was updated successfully, False otherwise.
        """
        profile_path = self._get_profile_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Cannot update: Profile not found for user: {username}")
            return False
        
        try:
            # Read existing profile
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Update with new data
            profile_data.update(updated_data)
            
            # Update timestamp
            profile_data['updated_at'] = time.time()
            
            # Write back to file
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
                
            logger.info(f"Updated profile for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error updating profile for {username}: {str(e)}")
            return False
    
    def delete_profile(self, username: str) -> bool:
        """
        Delete a user profile and all associated data.
        
        Args:
            username: The username of the profile to delete.
            
        Returns:
            True if profile was deleted successfully, False otherwise.
        """
        profile_path = self._get_profile_path(username)
        preferences_path = self._get_preferences_path(username)
        recommendations_dir = self._get_recommendations_path(username)
        feedback_dir = self._get_feedback_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Cannot delete: Profile not found for user: {username}")
            return False
        
        try:
            # Delete the profile file
            os.remove(profile_path)
            
            # Delete preferences if they exist
            if preferences_path.exists():
                os.remove(preferences_path)
            
            # Delete recommendations directory if it exists
            if recommendations_dir.exists() and recommendations_dir.is_dir():
                shutil.rmtree(recommendations_dir)
                
            # Delete feedback directory if it exists
            if feedback_dir.exists() and feedback_dir.is_dir():
                shutil.rmtree(feedback_dir)
                
            logger.info(f"Deleted profile and all associated data for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error deleting profile for {username}: {str(e)}")
            return False
    
    def list_all_profiles(self) -> List[str]:
        """
        List all usernames with profiles.
        
        Returns:
            List of usernames with profiles.
        """
        try:
            profiles = []
            for file_path in PROFILES_DIR.glob("*.json"):
                username = file_path.stem
                profiles.append(username)
            return profiles
        except Exception as e:
            logger.error(f"Error listing profiles: {str(e)}")
            return []
    
    # ----- Preferences CRUD Operations -----
    
    def save_preferences(self, username: str, preferences_data: Dict[str, Any]) -> bool:
        """
        Save user preferences.
        
        Args:
            username: The username associated with these preferences.
            preferences_data: Dictionary containing preference information.
            
        Returns:
            True if preferences were saved successfully, False otherwise.
        """
        preferences_path = self._get_preferences_path(username)
        
        # Add timestamp
        preferences_data['updated_at'] = time.time()
        
        try:
            with open(preferences_path, 'w', encoding='utf-8') as f:
                json.dump(preferences_data, f, indent=2)
            logger.info(f"Saved preferences for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error saving preferences for {username}: {str(e)}")
            return False
    
    def get_preferences(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user preferences.
        
        Args:
            username: The username associated with the preferences.
            
        Returns:
            Dictionary containing preference data or None if not found.
        """
        preferences_path = self._get_preferences_path(username)
        
        if not preferences_path.exists():
            logger.warning(f"Preferences not found for user: {username}")
            return None
        
        try:
            with open(preferences_path, 'r', encoding='utf-8') as f:
                preferences_data = json.load(f)
            logger.info(f"Retrieved preferences for user: {username}")
            return preferences_data
        except Exception as e:
            logger.error(f"Error retrieving preferences for {username}: {str(e)}")
            return None
    
    def update_preferences(self, username: str, updated_data: Dict[str, Any]) -> bool:
        """
        Update user preferences.
        
        Args:
            username: The username associated with the preferences.
            updated_data: Dictionary containing updated preference information.
            
        Returns:
            True if preferences were updated successfully, False otherwise.
        """
        preferences_path = self._get_preferences_path(username)
        
        if not preferences_path.exists():
            # If preferences don't exist yet, create them
            return self.save_preferences(username, updated_data)
        
        try:
            # Read existing preferences
            with open(preferences_path, 'r', encoding='utf-8') as f:
                preferences_data = json.load(f)
            
            # Update with new data
            preferences_data.update(updated_data)
            
            # Update timestamp
            preferences_data['updated_at'] = time.time()
            
            # Write back to file
            with open(preferences_path, 'w', encoding='utf-8') as f:
                json.dump(preferences_data, f, indent=2)
                
            logger.info(f"Updated preferences for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error updating preferences for {username}: {str(e)}")
            return False
    
    # ----- Recommendations CRUD Operations -----
    
    def save_recommendation(self, username: str, recommendation_data: Dict[str, Any]) -> str:
        """
        Save a recommendation for a user.
        
        Args:
            username: The username to associate with this recommendation.
            recommendation_data: Dictionary containing recommendation information.
            
        Returns:
            Recommendation ID if saved successfully, empty string otherwise.
        """
        recs_dir = self._get_recommendations_path(username)
        
        # Create a unique ID for this recommendation
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        rec_id = f"{timestamp}"
        recommendation_path = recs_dir / f"{rec_id}.json"
        
        # Add metadata
        recommendation_data['id'] = rec_id
        recommendation_data['created_at'] = time.time()
        recommendation_data['username'] = username
        
        try:
            with open(recommendation_path, 'w', encoding='utf-8') as f:
                json.dump(recommendation_data, f, indent=2)
            logger.info(f"Saved recommendation {rec_id} for user: {username}")
            return rec_id
        except Exception as e:
            logger.error(f"Error saving recommendation for {username}: {str(e)}")
            return ""
    
    def get_recommendation(self, username: str, rec_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific recommendation for a user.
        
        Args:
            username: The username associated with the recommendation.
            rec_id: The ID of the recommendation to retrieve.
            
        Returns:
            Dictionary containing recommendation data or None if not found.
        """
        recs_dir = self._get_recommendations_path(username)
        recommendation_path = recs_dir / f"{rec_id}.json"
        
        if not recommendation_path.exists():
            logger.warning(f"Recommendation {rec_id} not found for user: {username}")
            return None
        
        try:
            with open(recommendation_path, 'r', encoding='utf-8') as f:
                recommendation_data = json.load(f)
            logger.info(f"Retrieved recommendation {rec_id} for user: {username}")
            return recommendation_data
        except Exception as e:
            logger.error(f"Error retrieving recommendation {rec_id} for {username}: {str(e)}")
            return None
    
    def get_all_recommendations(self, username: str) -> List[Dict[str, Any]]:
        """
        Retrieve all recommendations for a user.
        
        Args:
            username: The username associated with the recommendations.
            
        Returns:
            List of dictionaries containing recommendation data.
        """
        recs_dir = self._get_recommendations_path(username)
        recommendations = []
        
        try:
            for file_path in recs_dir.glob("*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    recommendation_data = json.load(f)
                    recommendations.append(recommendation_data)
                    
            # Sort by creation time (newest first)
            recommendations.sort(key=lambda x: x.get('created_at', 0), reverse=True)
            
            logger.info(f"Retrieved {len(recommendations)} recommendations for user: {username}")
            return recommendations
        except Exception as e:
            logger.error(f"Error retrieving recommendations for {username}: {str(e)}")
            return []
    
    def delete_recommendation(self, username: str, rec_id: str) -> bool:
        """
        


    def get_topic_analytics(self) -> Dict[str, Any]:
        """
        Analyze topic preferences and recommendation patterns.
        
        Returns:
            Dictionary containing topic analytics data.
        """
        topic_data = {
            "subject_popularity": {},
            "subject_by_education_level": {},
            "subject_completion_rates": {},
            "timestamp": time.time()
        }
        
        try:
            # Collect all subjects
            all_subjects = set()
            education_level_subjects = {}
            
            # Analyze profiles for subject preferences by education level
            for file_path in PROFILES_DIR.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        profile_data = json.load(f)
                        subjects = profile_data.get("subjects", [])
                        education_level = profile_data.get("education_level", "Unknown")
                        
                        all_subjects.update(subjects)
                        
                        if education_level not in education_level_subjects:
                            education_level_subjects[education_level] = {}
                        
                        for subject in subjects:
                            education_level_subjects[education_level][subject] = \
                                education_level_subjects[education_level].get(subject, 0) + 1
                except Exception as e:
                    logger.error(f"Error analyzing profile for topics {file_path}: {str(e)}")
            
            # Calculate overall subject popularity
            subject_counts = {}
            for level_data in education_level_subjects.values():
                for subject, count in level_data.items():
                    subject_counts[subject] = subject_counts.get(subject, 0) + count
            
            topic_data["subject_popularity"] = dict(sorted(subject_counts.items(), 
                                                          key=lambda x: x[1], 
                                                          reverse=True))
            
            # Process education level data
            for level, subjects in education_level_subjects.items():
                education_level_subjects[level] = dict(sorted(subjects.items(), 
                                                            key=lambda x: x[1], 
                                                            reverse=True)[:5])
            
            topic_data["subject_by_education_level"] = education_level_subjects
            
            # Mock completion rates data for now (in a real app this would come from actual tracking)
            # This could be calculated based on user feedback or explicit completion tracking
            mock_completion_rates = {}
            for subject in all_subjects:
                mock_completion_rates[subject] = round(30 + 70 * (subject_counts.get(subject, 1) / 
                                                                 max(subject_counts.values(), default=1)), 1)
            
            topic_data["subject_completion_rates"] = mock_completion_rates
            
            return topic_data
        except Exception as e:
            logger.error(f"Error generating topic analytics: {str(e)}")
            return topic_data
    
    def get_recommendation_impact(self) -> Dict[str, Any]:
        """
        Analyze the effectiveness and impact of recommendations.
        
        Returns:
            Dictionary containing recommendation impact metrics.
        """
        impact_data = {
            "feedback_ratings": {},
            "resource_effectiveness": {},
            "retention_correlation": 0.0,
            "timestamp": time.time()
        }
        
        try:
            # Analyze feedback for ratings
            rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            resource_ratings = {}
            
            # In a real app, this would analyze actual feedback data
            # For now, we'll create simulated data
            
            # Simulate feedback distribution (mock data)
            total_recommendations = 0
            for rec_dir in RECOMMENDATIONS_DIR.glob("*"):
                if rec_dir.is_dir():
                    for _ in rec_dir.glob("*.json"):
                        total_recommendations += 1
            
            # Create simulated rating distribution
            if total_recommendations > 0:
                # Simulate a positive-skewed distribution (most ratings are good)
                rating_counts = {
                    1: int(total_recommendations * 0.05),  # 5% poor ratings
                    2: int(total_recommendations * 0.10),  # 10% below average
                    3: int(total_recommendations * 0.20),  # 20% average
                    4: int(total_recommendations * 0.35),  # 35% good
                    5: int(total_recommendations * 0.30)   # 30% excellent
                }
            
            impact_data["feedback_ratings"] = rating_counts
            
            # Simulate resource effectiveness data
            resource_types = ["Online Courses", "Videos", "Books", "Interactive Tools", 
                             "Tutorials", "Research Papers", "Projects"]
            
            resource_effectiveness = {}
            for resource in resource_types:
                # Effectiveness score from 0-100
                resource_effectiveness[resource] = round(50 + 50 * (0.5 + 0.5 * (hash(resource) % 100) / 100))
            
            impact_data["resource_effectiveness"] = resource_effectiveness
            
            # Simulate retention correlation (0-1 value)
            # In a real app, this would measure how recommendations affect user retention
            impact_data["retention_correlation"] = 0.72  # Example value
            
            return impact_data
        except Exception as e:
            logger.error(f"Error generating recommendation impact metrics: {str(e)}")
            return impact_data

import os
import json
import time
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("data_manager")

# Base path for data storage
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROFILES_DIR = BASE_DIR / "profiles"
RECOMMENDATIONS_DIR = BASE_DIR / "recommendations"
PREFERENCES_DIR = BASE_DIR / "preferences"

# Ensure directories exist
for directory in [PROFILES_DIR, RECOMMENDATIONS_DIR, PREFERENCES_DIR]:
    directory.mkdir(exist_ok=True)


class DataManager:
    """
    Handles data persistence for student profiles, preferences, and recommendation history.
    Currently uses JSON files for storage, but designed to be easily upgradable to a database.
    """
    
    def __init__(self):
        """Initialize the data manager and ensure storage directories exist."""
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all necessary data directories exist."""
        os.makedirs(PROFILES_DIR, exist_ok=True)
        os.makedirs(RECOMMENDATIONS_DIR, exist_ok=True)
        os.makedirs(PREFERENCES_DIR, exist_ok=True)
        logger.info("Data directories initialized")
    
    def _get_profile_path(self, username: str) -> Path:
        """Get the file path for a user's profile."""
        # Sanitize username for file safety
        safe_username = "".join(c if c.isalnum() else "_" for c in username)
        return PROFILES_DIR / f"{safe_username}.json"
    
    def _get_preferences_path(self, username: str) -> Path:
        """Get the file path for a user's preferences."""
        # Sanitize username for file safety
        safe_username = "".join(c if c.isalnum() else "_" for c in username)
        return PREFERENCES_DIR / f"{safe_username}.json"
    
    def _get_recommendations_path(self, username: str) -> Path:
        """Get the directory path for a user's recommendations."""
        # Sanitize username for file safety
        safe_username = "".join(c if c.isalnum() else "_" for c in username)
        user_recs_dir = RECOMMENDATIONS_DIR / safe_username
        os.makedirs(user_recs_dir, exist_ok=True)
        return user_recs_dir

    # ----- Profile CRUD Operations -----
    
    def create_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        Create a new user profile.
        
        Args:
            profile_data: Dictionary containing user profile information.
                         Must include a 'username' key.
                         
        Returns:
            True if profile was created successfully, False otherwise.
        """
        if 'username' not in profile_data:
            logger.error("Cannot create profile: username not provided")
            return False
        
        username = profile_data['username']
        profile_path = self._get_profile_path(username)
        
        # Check if profile already exists
        if profile_path.exists():
            logger.warning(f"Profile already exists for user: {username}")
            return False
        
        # Add timestamp for creation and last update
        current_time = time.time()
        profile_data['created_at'] = current_time
        profile_data['updated_at'] = current_time
        
        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
            logger.info(f"Created profile for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error creating profile for {username}: {str(e)}")
            return False
    
    def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user profile.
        
        Args:
            username: The username of the profile to retrieve.
            
        Returns:
            Dictionary containing profile data or None if profile doesn't exist.
        """
        profile_path = self._get_profile_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Profile not found for user: {username}")
            return None
        
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            logger.info(f"Retrieved profile for user: {username}")
            return profile_data
        except Exception as e:
            logger.error(f"Error retrieving profile for {username}: {str(e)}")
            return None
    
    def update_profile(self, username: str, updated_data: Dict[str, Any]) -> bool:
        """
        Update an existing user profile.
        
        Args:
            username: The username of the profile to update.
            updated_data: Dictionary containing the updated profile information.
            
        Returns:
            True if profile was updated successfully, False otherwise.
        """
        profile_path = self._get_profile_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Cannot update: Profile not found for user: {username}")
            return False
        
        try:
            # Read existing profile
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            # Update with new data
            profile_data.update(updated_data)
            
            # Update timestamp
            profile_data['updated_at'] = time.time()
            
            # Write back to file
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
                
            logger.info(f"Updated profile for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error updating profile for {username}: {str(e)}")
            return False
    
    def delete_profile(self, username: str) -> bool:
        """
        Delete a user profile and all associated data.
        
        Args:
            username: The username of the profile to delete.
            
        Returns:
            True if profile was deleted successfully, False otherwise.
        """
        profile_path = self._get_profile_path(username)
        preferences_path = self._get_preferences_path(username)
        recommendations_dir = self._get_recommendations_path(username)
        
        if not profile_path.exists():
            logger.warning(f"Cannot delete: Profile not found for user: {username}")
            return False
        
        try:
            # Delete the profile file
            os.remove(profile_path)
            
            # Delete preferences if they exist
            if preferences_path.exists():
                os.remove(preferences_path)
            
            # Delete recommendations directory if it exists
            if recommendations_dir.exists() and recommendations_dir.is_dir():
                shutil.rmtree(recommendations_dir)
                
            logger.info(f"Deleted profile and all associated data for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error deleting profile for {username}: {str(e)}")
            return False
    
    # ----- Preferences CRUD Operations -----
    
    def save_preferences(self, username: str, preferences_data: Dict[str, Any]) -> bool:
        """
        Save user preferences.
        
        Args:
            username: The username associated with these preferences.
            preferences_data: Dictionary containing preference information.
            
        Returns:
            True if preferences were saved successfully, False otherwise.
        """
        preferences_path = self._get_preferences_path(username)
        
        # Add timestamp
        preferences_data['updated_at'] = time.time()
        
        try:
            with open(preferences_path, 'w', encoding='utf-8') as f:
                json.dump(preferences_data, f, indent=2)
            logger.info(f"Saved preferences for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error saving preferences for {username}: {str(e)}")
            return False
    
    def get_preferences(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user preferences.
        
        Args:
            username: The username associated with the preferences.
            
        Returns:
            Dictionary containing preference data or None if not found.
        """
        preferences_path = self._get_preferences_path(username)
        
        if not preferences_path.exists():
            logger.warning(f"Preferences not found for user: {username}")
            return None
        
        try:
            with open(preferences_path, 'r', encoding='utf-8') as f:
                preferences_data = json.load(f)
            logger.info(f"Retrieved preferences for user: {username}")
            return preferences_data
        except Exception as e:
            logger.error(f"Error retrieving preferences for {username}: {str(e)}")
            return None
    
    # ----- Recommendations CRUD Operations -----
    
    def save_recommendation(self, username: str, recommendation_data: Dict[str, Any]) -> str:
        """
        Save a recommendation for a user.
        
        Args:
            username: The username to associate with this recommendation.
            recommendation_data: Dictionary containing recommendation information.
            
        Returns:
            Recommendation ID if saved successfully, empty string otherwise.
        """
        recs_dir = self._get_recommendations_path(username)
        
        # Create a unique ID for this recommendation
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        rec_id = f"{timestamp}"
        recommendation_path = recs_dir / f"{rec_id}.json"
        
        # Add metadata
        recommendation_data['id'] = rec_id
        recommendation_data['created_at'] = time.time()
        
        try:
            with open(recommendation_path, 'w', encoding='utf-8') as f:
                json.dump(recommendation_data, f, indent=2)
            logger.info(f"Saved recommendation {rec_id} for user: {username}")
            return rec_id
        except Exception as e:
            logger.error(f"Error saving recommendation for {username}: {str(e)}")
            return ""
    
    def get_recommendation(self, username: str, rec_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific recommendation for a user.
        
        Args:
            username: The username associated with the recommendation.
            rec_id: The ID of the recommendation to retrieve.
            
        Returns:
            Dictionary containing recommendation data or None if not found.
        """
        recs_dir = self._get_recommendations_path(username)
        recommendation_path = recs_dir / f"{rec_id}.json"
        
        if not recommendation_path.exists():
            logger.warning(f"Recommendation {rec_id} not found for user: {username}")
            return None
        
        try:
            with open(recommendation_path, 'r', encoding='utf-8') as f:
                recommendation_data = json.load(f)
            logger.info(f"Retrieved recommendation {rec_id} for user: {username}")
            return recommendation_data
        except Exception as e:
            logger.error(f"Error retrieving recommendation {rec_id} for {username}: {str(e)}")
            return None
    
    def get_all_recommendations(self, username: str) -> List[Dict[str, Any]]:
        """
        Retrieve all recommendations for a user.
        
        Args:
            username: The username associated with the recommendations.
            
        Returns:
            List of dictionaries containing recommendation data.
        """
        recs_dir = self._get_recommendations_path(username)
        recommendations = []
        
        try:
            for file_path in recs_dir.glob("*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    recommendation_data = json.load(f)
                    recommendations.append(recommendation_data)
                    
            # Sort by creation time (newest first)
            recommendations.sort(key=lambda x: x.get('created_at', 0), reverse=True)
            
            logger.info(f"Retrieved {len(recommendations)} recommendations for user: {username}")
            return recommendations
        except Exception as e:
            logger.error(f"Error retrieving recommendations for {username}: {str(e)}")
            return []
    
    def delete_recommendation(self, username: str, rec_id: str) -> bool:
        """
        Delete a specific recommendation for a user.
        
        Args:
            username: The username associated with the recommendation.
            rec_id: The ID of the recommendation to delete.
            
        Returns:
            True if recommendation was deleted successfully, False otherwise.
        """
        recs_dir = self._get_recommendations_path(username)
        recommendation_path = recs_dir / f"{rec_id}.json"
        
        if not recommendation_path.exists():
            logger.warning(f"Cannot delete: Recommendation {rec_id} not found for user: {username}")
            return False
        
        try:
            os.remove(recommendation_path)
            logger.info(f"Deleted recommendation {rec_id} for user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error deleting recommendation {rec_id} for {username}: {str(e)}")
            return False
    
    # ----- Database-ready interface methods -----
    
    def search_profiles(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for profiles matching certain criteria.
        This method would be expanded when migrating to a database.
        
        Args:
            criteria: Dictionary containing search criteria.
            
        Returns:
            List of matching profile dictionaries.
        """
        matching_profiles = []
        
        try:
            # Simple implementation for JSON storage - requires loading all profiles
            for file_path in PROFILES_DIR.glob("*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    
                    # Check if all criteria match
                    matches = True
                    for key, value in criteria.items():
                        if key not in profile_data or profile_data[key] != value:
                            matches = False
                            break
                    
                    if matches:
                        matching_profiles.append(profile_data)
            
            return matching_profiles
        except Exception as e:
            logger.error(f"Error searching profiles: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get system-wide statistics for analytics purposes.
        
        Returns:
            Dictionary containing statistical information.
        """
        stats = {
            "total_profiles": 0,
            "total_recommendations": 0,
            "active_users_last_month": 0,
            "timestamp": time.time()
        }
        
        try:
            # Count profiles
            profile_count = len(list(PROFILES_DIR.glob("*.json")))
            stats["total_profiles"] = profile_count
            
            # Count all recommendations
            rec_count = 0
            for user_dir in RECOMMENDATIONS_DIR.glob("*"):
                if user_dir.is_dir():
                    rec_count += len(list(user_dir.glob("*.json")))
            stats["total_recommendations"] = rec_count
            
            # Count active users

