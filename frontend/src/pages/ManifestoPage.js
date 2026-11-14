function ManifestoPage() {
	return (
		<main className="content-page manifesto-page">
			<header className="content-page__header">
				<p className="eyebrow">ŞEFFAFLIK · HAKKINDA</p>
				<h1>Bir ismin arkasında bir hayat var.</h1>
				<p className="content-page__intro">Identity Chain of Palestine, kişileri sayılara indirgemeden hatırlamak ve güvenli, rızaya dayalı dayanışma yolları oluşturmak için tasarlanan bir gönüllülük girişimidir.</p>
			</header>
			<div className="manifesto-principles">
				<article>
					<span>01</span>
					<div><h2>Önce doğrulama</h2><p>Bir profil yayımlanmadan önce kimlik ve kaynak bilgileri ekip tarafından doğrulanmalı; yayımlanacak her ayrıntı için açık ve belgelenmiş rıza alınmalıdır. Mevcut temsili profiller kurgusaldır, gerçek kişileri anlatmaz.</p></div>
				</article>
				<article>
					<span>02</span>
					<div><h2>Mahremiyet varsayılan olmalı</h2><p>Hassas konum, kimlik numarası ve aile iletişim bilgileri herkese açık arşivde tutulmaz. Yalnızca amaç için gerekli asgari bilgi işlenir; erişim yetkisi sınırlandırılır.</p></div>
				</article>
				<article>
					<span>03</span>
					<div><h2>İnsana saygı</h2><p>Hikâyeler kişinin onurunu koruyan bir dille sunulur. Travmatik ayrıntılar, doğrulanmamış iddialar veya duygusal baskı yaratacak içerikler kullanılmaz.</p></div>
				</article>
				<article>
					<span>04</span>
					<div><h2>Şeffaf gönüllülük</h2><p>Bu bir gönüllülük hareketidir, kar amacı gütmez. Eşleşme, bağış ve eylem rehberi dağıtım süreçleri güvenli operasyon koşulları tamamlanana kadar etkin değildir.</p></div>
				</article>
			</div>
			<p className="manifesto-page__note">Veri işleme ve yayın ilkelerimiz, gerçek profiller yayımlanmadan önce hukuki ve güvenlik incelemesinden geçirilecektir.</p>
		</main>
	);
}

export default ManifestoPage;
