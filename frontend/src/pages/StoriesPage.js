import { useEffect, useMemo, useState } from 'react';
import { fetchPrisoners } from '../services/api';

function getInitials(name) {
	return name.split(' ').slice(-2).map((part) => part[0]).join('');
}

function StoriesPage({ onOpenMatch }) {
	const [archive, setArchive] = useState([]);
	const [matchedCount, setMatchedCount] = useState(0);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [search, setSearch] = useState('');

	useEffect(() => {
		const controller = new AbortController();
		fetchPrisoners(controller.signal)
			.then((data) => {
				setArchive(data.items);
				setMatchedCount(data.matched_count);
			})
			.catch((requestError) => {
				if (requestError.name !== 'AbortError') setError(requestError.message);
			})
			.finally(() => setLoading(false));
		return () => controller.abort();
	}, []);

	const filteredArchive = useMemo(() => {
		const normalizedSearch = search.trim().toLocaleLowerCase('tr');
		if (!normalizedSearch) return archive;
		return archive.filter((person) =>
			`${person.name} ${person.profession} ${person.short_bio}`
				.toLocaleLowerCase('tr').includes(normalizedSearch),
		);
	}, [archive, search]);

	return (
		<section className="archive-section" id="stories" aria-labelledby="archive-title">
			<div className="section-heading">
				<p className="eyebrow">CANLI ARŞİV · TEMSİLİ PROFİLLER</p>
				<div className="section-heading__row">
					<div>
						<h2 id="archive-title">Her isim, bir hayat.</h2>
						<p>Gerçek kişi bilgileri yalnızca doğrulama ve açık rıza süreçleri tamamlandıktan sonra yayımlanır.</p>
						<button className="archive-match-cta" type="button" onClick={onOpenMatch}>Kardeşinle eşleş ↗</button>
					</div>
					<label className="archive-search">
						<span>Arşivde ara</span>
						<input type="search" value={search} placeholder="İsim veya meslek" onChange={(event) => setSearch(event.target.value)} />
					</label>
				</div>
				<div className="archive-metrics" aria-live="polite">
					<p className="archive-count">{loading ? 'Arşiv yükleniyor…' : error ? 'Arşiv şu an erişilemiyor' : `${filteredArchive.length} temsili profil`}</p>
					{!loading && !error && <p className="archive-matched">{matchedCount} gönüllü eşleşmesi tamamlandı</p>}
				</div>
			</div>

			{error && (
				<div className="archive-message archive-message--error" role="alert">
					<strong>Arşiv bağlantısı kurulamadı.</strong>
					<p>{error}</p>
					<p>Geliştirme için kök klasörde <code>docker compose up --build</code> çalıştırın.</p>
				</div>
			)}
			{loading && <p className="archive-message">Arşiv yükleniyor…</p>}
			{!loading && !error && filteredArchive.length === 0 && <p className="archive-message">Aramanızla eşleşen profil bulunamadı.</p>}

			<div className="archive-grid">
				{filteredArchive.map((person, index) => (
					<article className="person-card" key={person.id} style={{ '--card-index': index }}>
						{person.image_url && <img className="person-card__portrait" src={person.image_url} alt={`${person.name} için temsili çizim portre`} loading="lazy" />}
						<div className="person-card__topline">
							{!person.image_url && <span className="person-card__initials" aria-hidden="true">{getInitials(person.name)}</span>}
							<span className="demo-label">TEMSİLİ · GERÇEK KİŞİ DEĞİL</span>
						</div>
						<p className="person-card__profession">{person.profession}</p>
						<h3>{person.name}</h3>
						<p className="person-card__summary">{person.short_bio}</p>
						<a className="person-card__link" href={`/prisoners/${encodeURIComponent(person.slug)}`}>
							Profili incele <span aria-hidden="true">↗</span>
						</a>
					</article>
				))}
			</div>

		</section>
	);
}

export default StoriesPage;
