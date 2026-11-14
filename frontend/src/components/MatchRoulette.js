import { useEffect, useState } from 'react';
import { drawVolunteerMatch, recordVolunteerAction } from '../services/api';

function getVisitorId() {
	const key = 'identity-chain-visitor-id';
	let visitorId = window.localStorage.getItem(key);
	if (!visitorId) {
		visitorId = window.crypto.randomUUID();
		window.localStorage.setItem(key, visitorId);
	}
	return visitorId;
}

function MatchRoulette({ open, onClose }) {
	const [phase, setPhase] = useState('idle');
	const [match, setMatch] = useState(null);
	const [error, setError] = useState('');
	const [busy, setBusy] = useState('');
	const [note, setNote] = useState('');
	const [feedback, setFeedback] = useState('');
	const [attempt, setAttempt] = useState(0);

	useEffect(() => {
		if (!open) return undefined;
		let cancelled = false;
		setPhase('spinning');
		setMatch(null);
		setError('');
		setFeedback('');
		const spinTimer = new Promise((resolve) => window.setTimeout(resolve, 2100));
		Promise.all([drawVolunteerMatch(getVisitorId()), spinTimer])
			.then(([result]) => {
				if (!cancelled) {
					setMatch(result);
					setPhase('result');
				}
			})
			.catch((requestError) => {
				if (!cancelled) {
					setError(requestError.message);
					setPhase('error');
				}
			});
		return () => {
			cancelled = true;
		};
	}, [open, attempt]);

	useEffect(() => {
		if (!open) return undefined;
		function onKeyDown(event) {
			if (event.key === 'Escape' && phase !== 'spinning') onClose();
		}
		document.addEventListener('keydown', onKeyDown);
		return () => document.removeEventListener('keydown', onKeyDown);
	}, [open, phase, onClose]);

	async function sendAction(actionType, content = undefined) {
		if (!match) return;
		setBusy(actionType);
		setFeedback('');
		try {
			await recordVolunteerAction(match.match_id, {
				visitor_id: match.visitor_id,
				action_type: actionType,
				idempotency_key: window.crypto.randomUUID(),
				...(content ? { content } : {}),
			});
			setFeedback(actionType === 'note' ? 'Notun bu temsili eşleşme oturumuna özel olarak kaydedildi.' : 'Katkın eşleşme oturumuna kaydedildi.');
			if (actionType === 'note') setNote('');
		} catch (requestError) {
			setFeedback(requestError.message);
		} finally {
			setBusy('');
		}
	}

	async function shareMatch() {
		const shareUrl = `${window.location.origin}/prisoners/${encodeURIComponent(match.prisoner.slug)}`;
		try {
			if (navigator.share) {
				await navigator.share({ title: match.prisoner.name, url: shareUrl });
			} else {
				await navigator.clipboard.writeText(shareUrl);
			}
			await sendAction('share');
		} catch (shareError) {
			if (shareError.name !== 'AbortError') setFeedback('Paylaşım tamamlanamadı.');
		}
	}

	if (!open) return null;

	const guideUrl = match
		? `/api/v1/matches/${encodeURIComponent(match.match_id)}/action-guide.pdf?visitor_id=${encodeURIComponent(match.visitor_id)}`
		: '';

	return (
		<div className="match-overlay" role="presentation" onMouseDown={(event) => {
			if (event.target === event.currentTarget && phase !== 'spinning') onClose();
		}}>
			<section className="match-dialog" role="dialog" aria-modal="true" aria-labelledby="match-dialog-title">
				<button className="match-dialog__close" type="button" onClick={onClose} aria-label="Pencereyi kapat">×</button>
				<p className="eyebrow">KARDEŞLİK ÇARKI · TEMSİLİ PROFİLLER</p>
				<h2 id="match-dialog-title">{phase === 'result' ? 'Bu turdaki eşleşmen' : 'Çark senin için dönüyor'}</h2>
				{phase === 'spinning' && (
					<div className="match-wheel" aria-label="Temsili profiller arasından seçim yapılıyor">
						<div className="match-wheel__ring"><span>Birlikte</span><span>Hatırla</span><span>Dayanış</span><span>Bağ kur</span></div>
						<div className="match-wheel__center"><img src="/ana_logo_transparent.png" alt="" /></div>
					</div>
				)}
				{phase === 'error' && <p className="match-feedback match-feedback--error" role="alert">{error}</p>}
				{phase === 'result' && match && (
					<div className="match-result">
						<img className="match-result__portrait" src={match.prisoner.image_url} alt={`${match.prisoner.name} için temsili çizim portre`} />
						<div className="match-result__copy">
							<span className="demo-label">TEMSİLİ PROFİL · GERÇEK KİŞİ DEĞİL</span>
							<p className="person-card__profession">{match.prisoner.profession}</p>
							<h3>{match.prisoner.name}</h3>
							<p>{match.prisoner.short_bio}</p>
							<a className="person-card__link" href={`/prisoners/${encodeURIComponent(match.prisoner.slug)}`}>Temsili profili incele ↗</a>
						</div>
					</div>
				)}
				{phase === 'result' && match && (
					<div className="match-actions">
						<p>Bu seçim kurgusal bir profil içindir. Eylemlerin bu oturuma özel kaydedilir; gerçek bir kişiye iletilmez.</p>
						<div className="match-action-buttons">
							<button type="button" disabled={Boolean(busy)} onClick={() => sendAction('prayer')}>{busy === 'prayer' ? 'Kaydediliyor…' : 'Dua ettim'}</button>
							<button type="button" disabled={Boolean(busy)} onClick={() => sendAction('good_deed')}>{busy === 'good_deed' ? 'Kaydediliyor…' : 'İyilik yaptım'}</button>
							<button type="button" disabled={Boolean(busy)} onClick={shareMatch}>Paylaş</button>
						</div>
						<form className="match-note-form" onSubmit={(event) => { event.preventDefault(); sendAction('note', note); }}>
							<label htmlFor="match-note">Bu eşleşme için özel not</label>
							<textarea id="match-note" value={note} maxLength={1200} minLength={3} onChange={(event) => setNote(event.target.value)} required rows={3} />
							<button type="submit" disabled={Boolean(busy)}>{busy === 'note' ? 'Kaydediliyor…' : 'Notu kaydet'}</button>
						</form>
						{feedback && <p className="match-feedback" role="status">{feedback}</p>}
						<a className="match-guide-link" href={guideUrl} download="identity-chain-eylem-rehberi.pdf">Eylem rehberini indir (PDF) ↓</a>
					</div>
				)}
				{phase === 'error' && <button className="match-retry" type="button" onClick={() => setAttempt((value) => value + 1)}>Yeniden dene</button>}
			</section>
		</div>
	);
}

export default MatchRoulette;