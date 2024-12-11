document.getElementById('wikiForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const query = document.querySelector('[name="title"]').value.trim();
    const resultContainer = document.querySelector('[name="description"]');
    resultContainer.replaceChildren();
    const missingResult = document.getElementById('missing-content');

    if (!query) {
        missingResult.replaceChildren();
        const message = document.createElement('p');
        const helpMessage = document.createElement('p')

        message.classList.add('text-danger');
        helpMessage.classList.add('text-danger')

        message.textContent = 'Please enter a valid search term.';
        helpMessage.textContent = 'Please make sure to enter the title first. Note that some information may be missing if the title is not provided'

        missingResult.appendChild(message);
        missingResult.appendChild(helpMessage);
        return;
    }

    try {
        const response = await fetch(`https://bg.wikipedia.org/w/api.php?origin=*&action=query&list=search&format=json&srsearch=${encodeURIComponent(query)}&uselang=en`);
        const data = await response.json();
        const pages = data.query.pages;

        if (!data.query.search.length) {
            missingResult.replaceChildren();
            const message = document.createElement('p');
            message.classList.add('text-danger');
            message.textContent = `No results found for "${query}".`;
            missingResult.appendChild(message);
            return;
        }

        const firstResult = data.query.search[0];
        const pageid = firstResult.pageid;

        const extractResponse = await fetch(`https://bg.wikipedia.org/w/api.php?origin=*&action=query&prop=extracts&format=json&pageids=${pageid}&exintro&explaintext`);
        const extractData = await extractResponse.json();

        const page = extractData.query.pages[pageid];
        let text = page.extract || 'No summary available.';

        if (text === 'No summary available.') {
            missingResult.replaceChildren();
            const message = document.createElement('p');
            message.classList.add('text-danger');
            message.textContent = `No results found for "${query}".`;
            missingResult.appendChild(message);
            return;
        }

        text = truncateToSentence(text, 1500);
        resultContainer.textContent = text;
    } catch (error) {
        resultContainer.textContent = 'An error occurred while fetching data. Please try again later.';
        console.error(error);
    }
});

function truncateToSentence(text, maxLength) {
    if (text.length <= maxLength) return text;

    const truncated = text.slice(0, maxLength);
    const lastSentenceEnd = truncated.lastIndexOf('.');
    return lastSentenceEnd !== -1 ? truncated.slice(0, lastSentenceEnd + 1) : truncated;
}
