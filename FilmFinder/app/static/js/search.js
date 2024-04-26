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
        <h3>${movie.title} (${movie.year})</h3>
        <p>Rating: ${movie.rating}</p>
        <p>Genre: ${movie.genres.join(', ')}</p>
        <p>Cast: ${movie.cast.join(', ')}</p>
        <p>Plot: ${movie.plot}</p>
    `;
}

function constructActorDetails(actor) {
    return `
        <h3>${actor.name}</h3>
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
