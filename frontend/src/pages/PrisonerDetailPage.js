import { useEffect, useState } from 'react';
import Input from '../components/Input';
import {
	fetchPrisoner,
	submitContribution,
	submitSpiritualNote,
} from '../services/api';

function PrisonerDetailPage({ onOpenMatch }) {
	const slug = decodeURIComponent(window.location.pathname.split('/').filter(Boolean).at(-1) || '');
	const [person, setPerson] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [busy, setBusy] = useState('');
	const [feedback, setFeedback] = useState({ type: '', message: '' });
	const [noteFields, setNoteFields] = useState({ display_name: '', message: '', consent: false });

	useEffect(() => {
		const controller = new AbortController();
		fetchPrisoner(slug, controller.signal)
			.then((profile) => {
				setPerson(profile);
				document.title = `${profile.name} | Identity Chain of Palestine`;
			})
			.catch((requestError) => {
				if (requestError.name !== 'AbortError') setError(requestError.message);
			})
			.finally(() => setLoading(false));
		return () => controller.abort();
	}, [slug]);

	async function handleNoteSubmit(event) {
		event.preventDefault();
		setBusy('note');
		setFeedback({ type: '', message: '' });
		try {
			const result = await submitSpiritualNote(slug, { ...noteFields, website: '' });
			setFeedback({ type: 'success', message: result.message || 'Notunuz moderasyon incelemesine alındı.' });
			setNoteFields({ display_name: '', message: '', consent: false });
		} catch (requestError) {
			setFeedback({ type: 'error', message: requestError.message });
		} finally {
			setBusy('');
		}
	}

	async function handleContribution(actionType) {
		setBusy(actionType);
		setFeedback({ type: '', message: '' });
		try {
			const result = await submitContribution(slug, {
				action_type: actionType,
				idempotency_key: crypto.randomUUID(),
			});
			setPerson((current) => ({
				...current,
				prayers_count: result.prayers_count,
				good_deeds_count: result.good_deeds_count,
			}));
			setFeedback({
				type: 'success',
				message: result.status === 'duplicate' ? 'Bu katkı daha önce kaydedilmiş.' : 'Katkınız topluluk sayacına eklendi.',
			});
		} catch (requestError) {
			setFeedback({ type: 'error', message: requestError.message });
		} finally {
			setBusy('');
		}
	}

	return (
		<main className="profile-page">
			<header className="profile-page__header">
				<a className="brand" href="/" aria-label="Identity Chain ana sayfa">
					<img className="brand-logo" src="/ana_logo_transparent.png" alt="" />
					<span className="brand-name">IDENTITY CHAIN</span>
				</a>
				<a className="profile-page__back" href="/archive">← Arşive dön</a>
			</header>

			{loading && <p className="profile-page__state">Profil yükleniyor…</p>}
			{error && (
				<section className="profile-page__state" role="alert">
					<h1>Profil açılamadı</h1>
					<p>{error}</p>
					<a href="/#stories">Arşive dön</a>
				</section>
			)}
			{person && (
				<article className="profile-page__content">
					<p className="eyebrow">KİŞİSEL HİKÂYE · ARŞİV</p>
					<span className="demo-label">{person.is_demo ? 'TEMSİLİ PROFİL · GERÇEK KİŞİ DEĞİL' : 'DOĞRULANMIŞ PROFİL'}</span>
					{person.image_url && <img className="profile-page__portrait" src={person.image_url} alt={`${person.name} için temsili çizim portre`} />}
					<p className="person-card__profession">{person.profession}</p>
					<h1>{person.name}</h1>
					<p className="profile-page__lead">{person.short_bio}</p>
					<div className="profile-page__rule" />
					<section>
						<h2>Hikâyesi</h2>
						<p>{person.biography}</p>
					</section>
					<section className="profile-page__dreams">
						<h2>Yarım kalan hayaller</h2>
						<p>{person.dreams || 'Bu bilgi paylaşılmamış.'}</p>
					</section>
					<div className="profile-page__stats" aria-label="Topluluk sayaçları">
						<div><strong>{person.prayers_count}</strong><span>Dua</span></div>
						<div><strong>{person.good_deeds_count}</strong><span>İyilik</span></div>
					</div>
					{person.is_demo && (
						<section className="profile-actions" aria-labelledby="actions-title">
							<p className="eyebrow">TOPLULUK KATKISI · TEMSİLİ PROFİL</p>
							<h2 id="actions-title">Ne yapabilirim?</h2>
							<p>Bu profil kurgusaldır; sayaç ve katkı akışı örnek amaçlıdır. Gerçek kişi bilgisi içermez.</p>
							<div className="profile-action-buttons">
								<button type="button" onClick={onOpenMatch}>Çarkı çevir ve eşleş</button>
								<button type="button" disabled={Boolean(busy)} onClick={() => handleContribution('prayer')}>{busy === 'prayer' ? 'Kaydediliyor…' : 'Dua ettim'}</button>
								<button type="button" disabled={Boolean(busy)} onClick={() => handleContribution('good_deed')}>{busy === 'good_deed' ? 'Kaydediliyor…' : 'İyilik yaptım'}</button>
							</div>
							{feedback.message && <p className={`form-feedback form-feedback--${feedback.type}`} role={feedback.type === 'error' ? 'alert' : 'status'}>{feedback.message}</p>}
							<div className="profile-action-forms">
								<div className="profile-action-form profile-match-action">
									<h3>Kardeşinle eşleş</h3>
									<p>Çark yalnızca temsili profillerden birini seçer. Gerçek kişiyle temas kurulmaz.</p>
									<button type="button" onClick={onOpenMatch}>Çarkı çevir</button>
								</div>
								<form className="profile-action-form" onSubmit={handleNoteSubmit}>
									<h3>Manevi not bırak</h3>
									<p>Notlar yayınlanmadan önce moderasyon incelemesinden geçer.</p>
									<Input name="display_name" label="Görünen ad (isteğe bağlı)" value={noteFields.display_name} onChange={(event) => setNoteFields({ ...noteFields, display_name: event.target.value })} maxLength={80} />
									<Input as="textarea" name="message" label="Notunuz" value={noteFields.message} onChange={(event) => setNoteFields({ ...noteFields, message: event.target.value })} minLength={5} maxLength={1200} rows={4} required />
									<label className="consent-control"><input type="checkbox" checked={noteFields.consent} onChange={(event) => setNoteFields({ ...noteFields, consent: event.target.checked })} required /><span>Notumun incelenmesini ve onaylanırsa yayımlanmasını kabul ediyorum.</span></label>
									<button type="submit" disabled={Boolean(busy)}>{busy === 'note' ? 'Gönderiliyor…' : 'Moderasyona gönder'}</button>
								</form>
							</div>
							{person.approved_notes?.length > 0 && (
								<div className="approved-notes"><h3>Onaylanan notlar</h3>{person.approved_notes.map((note, index) => <blockquote key={`${note.display_name}-${index}`}><p>{note.message}</p><cite>{note.display_name}</cite></blockquote>)}</div>
							)}
						</section>
					)}
					{!person.is_demo && <p className="profile-page__notice">Eşleşme ve katkı işlemleri bu profil için henüz etkin değildir.</p>}
					<section className="profile-guide" aria-labelledby="guide-title">
						<h2 id="guide-title">Eylem rehberi</h2>
						{person.is_matched
							? <a href={`/api/v1/prisoners/${encodeURIComponent(person.slug)}/action-guide/pdf`} download="identity-chain-eylem-rehberi.pdf">Eylem rehberini indir (PDF) ↓</a>
							: <p>Eylem rehberi, ekip tarafından onaylanan eşleşmeden sonra açılır.</p>}
					</section>
				</article>
			)}
		</main>
	);
}

export default PrisonerDetailPage;