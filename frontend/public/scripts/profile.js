// Profile management functionality
document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profile-form');
    const API_BASE_URL = '/api';

    // Check if user is logged in
    async function checkAuthStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/check-auth`, {
                credentials: 'include'
            });
            if (!response.ok) {
                // Redirect to login if not authenticated
                window.location.href = '/login.html';
                return false;
            }
            return true;
        } catch (error) {
            console.error('Auth check failed:', error);
            window.location.href = '/login.html';
            return false;
        }
    }

    // Function to fetch user profile data
    async function fetchProfileData() {
        if (!await checkAuthStatus()) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/profile`, {
                credentials: 'include'
            });
            if (response.ok) {
                const profileData = await response.json();
                populateProfileForm(profileData);
            }
        } catch (error) {
            console.error('Error fetching profile:', error);
        }
    }

    // Function to populate form with profile data
    function populateProfileForm(data) {
        // Add this once you have the form fields
        // Exampl document.getElementById('username').value = data.username;
    }

    // Handle profile updates
    if (profileForm) {
        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(profileForm);

            try {
                const response = await fetch(`${API_BASE_URL}/update-profile`, {
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                });

                if (response.ok) {
                    alert('Profile updated successfully');
                } else {
                    alert('Failed to update profile');
                }
            } catch (error) {
                console.error('Error updating profile:', error);
                alert('Error updating profile');
            }
        });
    }

    // Load profile data when page loads
    fetchProfileData();
});