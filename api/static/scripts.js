document.getElementById('searchBtn').addEventListener('click', searchNews);

function searchNews() {
    const keyword = document.getElementById('keyword').value;
    if (keyword) {
        fetch(`/api/search/?keyword=${keyword}`)
            .then(response => response.json())
            .then(data => {
                displayResults(data.articles);
                refreshHistoryList(); // Call the function to refresh search history
            })
            .catch(error => console.error(error));
    }
}

function displayResults(articles) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article';
        articleDiv.innerHTML = `
            <h3>${article.title}</h3>
            <p>${article.description}</p>
            <a href="${article.url}" target="_blank">Read more</a>
        `;
        resultsContainer.appendChild(articleDiv);
    });
}

function refreshHistoryList() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';

    fetch(`/api/history/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(history => {
                const historyItem = document.createElement('li');
                historyItem.innerHTML = `
                    <a href="/history/${history.id}/">${history.keyword}</a>
                `;
                historyList.appendChild(historyItem);
            });
        })
        .catch(error => console.error(error));
}
