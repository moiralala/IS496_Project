/* IS496: Computer Networks
Course Mini-Project
Name and Netid of each member:
Member 1: chenzhao wang, cw107
Member 2: Zhen Li, zhenli6 */
// static/js/search.js

function search() {
    var movieQuery = document.getElementById('movie-input').value;
    var actorQuery = document.getElementById('actor-input').value;
    var genreQuery = document.getElementById('genre-input').value;
    var yearQuery = document.getElementById('year-input').value;

    var params = new URLSearchParams();
    if (movieQuery) params.append('movie_name', movieQuery);
    if (actorQuery) params.append('actor_name', actorQuery);
    if (genreQuery) params.append('genre', genreQuery);
    if (yearQuery) params.append('year', yearQuery);

    var searchURL = `/search-api?${params.toString()}`;

    // Show loading indicator
    document.getElementById('loading-indicator').style.display = 'block';
    document.getElementById('results-container').innerHTML = '';  // Clear previous results

    fetch(searchURL)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            // Hide loading indicator
            document.getElementById('loading-indicator').style.display = 'none';
        })
        .catch(error => {
            console.error('Error during search:', error);
            document.getElementById('results-container').innerHTML = `<p>Error during search: ${error.message}</p>`;
            // Hide loading indicator
            document.getElementById('loading-indicator').style.display = 'none';
        });
}

function displayResults(results) {
    var resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';  // Clear previous results

    // Append movie results, if any
    if (results.Movies && results.Movies.length > 0) {
        var moviesHeader = document.createElement('h2');
        moviesHeader.textContent = 'Movies';
        resultsContainer.appendChild(moviesHeader);

        results.Movies.forEach(movie => {
            var movieDiv = document.createElement('div');
            movieDiv.classList.add('movie-result');
            movieDiv.innerHTML = constructMovieDetails(movie);
            resultsContainer.appendChild(movieDiv);
        });
    } else {
        var noMoviesMessage = document.createElement('p');
        noMoviesMessage.textContent = 'No movies found.';
        noMoviesMessage.classList.add('no-results-message');
        resultsContainer.appendChild(noMoviesMessage);
    }

    // Append actor results, if any
    if (results.Actors && results.Actors.length > 0) {
        var actorsHeader = document.createElement('h2');
        actorsHeader.textContent = 'Actors';
        resultsContainer.appendChild(actorsHeader);

        results.Actors.forEach(actor => {
            var actorDiv = document.createElement('div');
            actorDiv.classList.add('actor-result');
            actorDiv.innerHTML = constructActorDetails(actor);
            resultsContainer.appendChild(actorDiv);
        });
    } else {
        var noActorsMessage = document.createElement('p');
        noActorsMessage.textContent = 'No actors found.';
        noActorsMessage.classList.add('no-results-message');
        resultsContainer.appendChild(noActorsMessage);
    }
}

function constructMovieDetails(movie) {
    return `
        <div class="movie-header">
            <h3>${movie.title} (${movie.year})</h3>
            <button onclick="addFavorite('${movie.movie_id}', null)">☆ Collect</button>
        </div>
        <p>Rating: ${movie.rating}</p>
        <p>Genre: ${movie.genres.join(', ')}</p>
        <p>Cast: ${movie.cast.join(', ')}</p>
        <p>Plot: ${movie.plot}</p>
    `;
}

function constructActorDetails(actor) {
    return `
        <div class="actor-header">
            <h3>${actor.name}</h3>
            <button onclick="addFavorite(null, '${actor.actor_id}')">☆ Collect</button>
        </div>
        <p>Biography: ${actor.biography.join(' ')}</p>
        <p>Filmography: ${actor.filmography.join(', ')}</p>
    `;
}

function showLoadingIndicator(show) {
    var loadingIndicator = document.getElementById('loading-indicator');
    loadingIndicator.style.display = show ? 'block' : 'none';
}

function showError(message) {
    var resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = `<p>Error during search: ${message}</p>`;
}


function addFavorite(movieId, actorId) {
    const data = { user_id: userId, movie_id: movieId, actor_id: actorId };

    fetch('/add-favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // If CSRF protection is enabled, you'll need to include the CSRF token in the request headers
            // 'X-CSRFToken': csrf_token  // You would need to set the csrf_token variable accordingly
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Use the message from the server for user feedback
    })
    .catch(error => {
        console.error('Error during favoriting:', error);
        alert(`Error adding favorite: ${error.message}`);
    });
}

