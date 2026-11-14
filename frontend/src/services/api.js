const API_BASE_URL = process.env.REACT_APP_API_URL || '/api/v1';

async function request(path, options = {}) {
	let response;
	try {
		response = await fetch(`${API_BASE_URL}${path}`, {
			...options,
			headers: { Accept: 'application/json', ...options.headers },
		});
	} catch (error) {
		if (error.name === 'AbortError') throw error;
		throw new Error('API sunucusuna ulaşılamıyor. Backend ve PostgreSQL servislerini başlatın.');
	}

	const contentType = response.headers.get('content-type') || '';
	if (!contentType.includes('application/json')) {
		throw new Error('API yerine web sayfası yanıt verdi. Frontend proxy ayarını kontrol edin ve geliştirme sunucusunu yeniden başlatın.');
	}
	const payload = await response.json();
	if (!response.ok || !payload.success) {
		throw new Error(payload.error?.message || `İstek tamamlanamadı (${response.status}).`);
	}
	return payload.data;
}

export function fetchPrisoners(signal) {
	return request('/prisoners?page_size=100', { signal });
}

export function fetchPrisoner(slug, signal) {
	return request(`/prisoners/${encodeURIComponent(slug)}`, { signal });
}

export function requestMatch(slug, payload) {
	return request(`/prisoners/${encodeURIComponent(slug)}/match-requests`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
}

export function submitSpiritualNote(slug, payload) {
	return request(`/prisoners/${encodeURIComponent(slug)}/notes`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
}

export function submitContribution(slug, payload) {
	return request(`/prisoners/${encodeURIComponent(slug)}/contributions`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
}

export function drawVolunteerMatch(visitorId) {
	return request('/matches/draw', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ visitor_id: visitorId }),
	});
}

export function recordVolunteerAction(matchId, action) {
	return request(`/matches/${encodeURIComponent(matchId)}/actions`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(action),
	});
}

export function sendContactMessage(message) {
	return request('/contact-messages', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(message),
	});
}
