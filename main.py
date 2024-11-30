from flask import Flask, request, render_template
import requests

# Initialize the Flask application
app = Flask(__name__)

# Global list to store recently viewed movies
# This list will store the titles and posters of the last 8 movies searched
recent_movies = []

@app.route('/', methods=['GET', 'POST'])  # Define the route for the homepage
def index():
    global recent_movies  # Allow modification of the global recent_movies list
    movie_info = None  # Variable to store details about the current movie
    error = None  # Variable to store error messages

    # Check if the method is POST (form submitted)
    if request.method == 'POST':
        # Get the movie name from the form input
        movie_name = request.form.get('movie_name')
        
        if movie_name:  # Ensure the user entered a movie name
            API_KEY = '********'  # Replace with your OMDb API key
            BASE_URL = 'http://www.omdbapi.com/'  # Base URL for the OMDb API

            # Parameters for the API request
            params = {'t': movie_name, 'apikey': API_KEY}
            # Make a GET request to the OMDb API
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:  # Check if the request was successful
                data = response.json()  # Parse the API response as JSON
                if data.get('Response') == 'True':  # Check if the movie was found
                    # Extract relevant movie information
                    movie_info = {
                        'Title': data.get('Title'),
                        'Year': data.get('Year'),
                        'Genre': data.get('Genre'),
                        'Director': data.get('Director'),
                        'Actors': data.get('Actors'),
                        'Plot': data.get('Plot'),
                        'IMDb Rating': data.get('imdbRating'),
                        'Poster': data.get('Poster')  # URL for the movie poster
                    }

                    # Add the movie to the recently viewed list
                    # Ensure no duplicates by filtering out existing posters
                    recent_movies = [movie for movie in recent_movies if movie['Poster'] != movie_info['Poster']]
                    # Insert the new movie at the beginning of the list
                    recent_movies.insert(0, {'Title': movie_info['Title'], 'Poster': movie_info['Poster']})

                    # Limit the recently viewed list to 8 movies
                    if len(recent_movies) > 8:
                        recent_movies = recent_movies[:8]
                else:
                    # If the movie was not found, display an error message
                    error = "Movie not found!"
            else:
                # If the API request failed, display an error message
                error = "Error fetching data from the API!"
        else:
            # If no movie name was entered, display an error message
            error = "Please enter a movie name."

    # Render the HTML template with the movie info, errors, and recent movies
    return render_template('index.html', movie_info=movie_info, error=error, recent_movies=recent_movies)

# Run the Flask app in debug mode when the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
