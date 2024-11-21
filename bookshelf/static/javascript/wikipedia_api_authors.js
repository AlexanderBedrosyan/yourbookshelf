document.getElementById('wikiForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const query = `${document.querySelector('[name="first_name"]').value.trim()} ${document.querySelector('[name="last_name"]').value.trim()} автор`;
    const resultContainer = document.querySelector('[name="bio"]');
    resultContainer.innerHTML = '';
    const missingResult = document.getElementById('missing-content');

    if (!query) {
        missingResult.innerHTML = `<p class="text-danger">Please enter a valid search term.</p>`;
        return;
    }

    try {
        const response = await fetch(`https://bg.wikipedia.org/w/api.php?origin=*&action=query&list=search&format=json&srsearch=${encodeURIComponent(query)}&uselang=en`);
        const data = await response.json();
        const pages = data.query.pages;

        if (!data.query.search.length) {
            missingResult.innerHTML = `<p class="text-danger">No results found for "${query}".</p>`;
            return;
        }

        const firstResult = data.query.search[0];
        const pageid = firstResult.pageid;

        const extractResponse = await fetch(`https://bg.wikipedia.org/w/api.php?origin=*&action=query&prop=extracts&format=json&pageids=${pageid}&exintro&explaintext`);
        const extractData = await extractResponse.json();

        const page = extractData.query.pages[pageid];
        let text = page.extract || 'No summary available.';

        if (text === 'No summary available.') {
            missingResult.innerHTML = `<p class="text-danger">No results found for "${query}".</p>`;
            return;
        }

        text = truncateToSentence(text, 1500);
        resultContainer.innerHTML = `
            ${text}
        `;
    } catch (error) {
        resultContainer.innerHTML = `<p class="text-danger">An error occurred while fetching data. Please try again later.</p>`;
        console.error(error);
    }
});

function truncateToSentence(text, maxLength) {
    if (text.length <= maxLength) return text;

    const truncated = text.slice(0, maxLength);
    const lastSentenceEnd = truncated.lastIndexOf('.');
    return lastSentenceEnd !== -1 ? truncated.slice(0, lastSentenceEnd + 1) : truncated;
}
