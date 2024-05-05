/* IS496: Computer Networks
Course Mini-Project
Name and Netid of each member:
Member 1: chenzhao wang, cw107
Member 2: Zhen Li, zhenli6 */
document.addEventListener('DOMContentLoaded', function() {
    fetchFavorites();
});

function fetchFavorites() {
    fetch('/user-favorites-api')  // Correct API endpoint
    .then(response => response.json())
    .then(data => {
        displayFavorites(data.favorite_movies, 'favorite-movies');
        displayFavorites(data.favorite_actors, 'favorite-actors');
    })
    .catch(error => console.error('Error loading favorites:', error));
}

function displayFavorites(items, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear existing entries

    if (items.length === 0) {
        // Display a message if no favorites are found
        const noItemsMessage = document.createElement('p');
        noItemsMessage.textContent = `You do not have collected favorites now${containerId === 'favorite-movies' ? 'moive' : 'actors'}。`;
        noItemsMessage.className = 'no-items-message'; // Optional: Add a class for styling
        container.appendChild(noItemsMessage);
    } else {
        const list = document.createElement('ul');
        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = formatItem(item);
            list.appendChild(listItem);
        });
        container.appendChild(list);
    }
}

function formatItem(item) {
    if (item.movie_id) {
        return `${item.title} (${item.year}), Rating: ${item.rating}`;
    } else {
        return `${item.name}, Known for: ${item.known_for.join(', ')}`;
    }
}

