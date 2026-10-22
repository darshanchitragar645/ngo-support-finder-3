const categoryFilter = document.getElementById('categoryFilter');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const ngoList = document.getElementById('ngoList');
const ngoCount = document.getElementById('ngoCount');
const resultBadge = document.getElementById('resultBadge');
const requestForm = document.getElementById('requestForm');
const requestAlert = document.getElementById('requestAlert');

function renderNgoCards(ngos) {
    if (!Array.isArray(ngos) || ngos.length === 0) {
        ngoList.innerHTML = `
            <div class="col-12">
                <div class="alert alert-light border text-center py-4">
                    No NGOs match your search criteria.
                </div>
            </div>
        `;
        resultBadge.textContent = '0 results';
        return;
    }

    ngoList.innerHTML = ngos.map((ngo) => `
        <div class="col-12">
            <article class="ngo-card card shadow-sm border-0">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start gap-3 mb-3">
                        <div>
                            <span class="ngo-badge">${ngo.category}</span>
                            <h5 class="mt-3 mb-1">${ngo.name}</h5>
                            <div class="ngo-meta">${ngo.location}</div>
                        </div>
                    </div>

                    <p class="ngo-description mb-3"><strong>Cause:</strong> ${ngo.cause}</p>
                    <p class="ngo-description">${ngo.description}</p>

                    <ul class="contact-list">
                        <li><strong>Contact:</strong> ${ngo.contact}</li>
                        <li><strong>Email:</strong> ${ngo.email}</li>
                        <li><strong>Phone:</strong> ${ngo.phone}</li>
                        <li><strong>Website:</strong> <a href="${ngo.website}" target="_blank" rel="noreferrer">${ngo.website}</a></li>
                    </ul>
                </div>
            </article>
        </div>
    `).join('');

    resultBadge.textContent = `${ngos.length} result${ngos.length > 1 ? 's' : ''}`;
}

async function fetchNgos() {
    const category = categoryFilter.value;
    const search = searchInput.value.trim();

    try {
        const response = await fetch(`/api/ngos?category=${encodeURIComponent(category)}&q=${encodeURIComponent(search)}`);
        const data = await response.json();

        if (!data || !Array.isArray(data.ngos)) {
            renderNgoCards([]);
            return;
        }

        ngoCount.textContent = data.ngos.length;
        renderNgoCards(data.ngos);
    } catch (error) {
        console.error('Error loading NGOs:', error);
        ngoList.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">Unable to load NGOs right now. Please try again later.</div>
            </div>
        `;
    }
}

searchButton.addEventListener('click', fetchNgos);
searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        fetchNgos();
    }
});
categoryFilter.addEventListener('change', fetchNgos);

requestForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    requestAlert.classList.add('d-none');
    requestAlert.classList.remove('alert-success', 'alert-danger');

    const payload = {
        name: document.getElementById('requesterName').value.trim(),
        email: document.getElementById('requesterEmail').value.trim(),
        ngo: document.getElementById('requestedNgo').value.trim(),
        category: document.getElementById('supportCategory').value,
        message: document.getElementById('requestMessage').value.trim(),
    };

    try {
        const response = await fetch('/api/requests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (response.ok && data.success) {
            requestAlert.textContent = data.message;
            requestAlert.classList.add('alert-success');
            requestForm.reset();
        } else {
            requestAlert.textContent = data.message || 'Unable to submit your request right now.';
            requestAlert.classList.add('alert-danger');
        }

        requestAlert.classList.remove('d-none');
    } catch (error) {
        console.error('Form submission error:', error);
        requestAlert.textContent = 'Something went wrong while submitting the request.';
        requestAlert.classList.add('alert-danger');
        requestAlert.classList.remove('d-none');
    }
});

fetchNgos();
