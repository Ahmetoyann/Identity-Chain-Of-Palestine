const questions = [
	{
		question: 'Bu sitedeki profiller gerçek mi?',
		answer: 'Arşivdeki 20 profil kurgusal temsili içeriktir; gerçek kişileri veya tutukluluk durumlarını temsil etmez. Gerçek profiller doğrulama, açık rıza ve yayın incelemesi tamamlanmadan eklenmeyecektir.',
	},
	{
		question: 'Bir kişiyle nasıl eşleşebilirim?',
		answer: 'Ana sayfadaki, üst menüdeki veya arşivdeki “Kardeşinle Eşleş” butonuna basın. Çark, veritabanındaki temsili profillerden birini rastgele seçer. Bu akış gerçek bir kişiyle iletişim veya eşleşme oluşturmaz.',
	},
	{
		question: 'Arşiv hangi kişisel bilgileri tutuyor?',
		answer: 'Geliştirme sürümünde arşiv temel biyografi ve hikâye alanlarını tutar. Hassas konum, kimlik numarası veya aile iletişim bilgisi alanları bulunmaz. Gerçek veriler için erişim, saklama süresi ve silme prosedürleri ayrıca belirlenmelidir.',
	},
	{
		question: 'Mektup veya dua notu gönderebilir miyim?',
		answer: 'Çark eşleşmesinden sonra yazdığınız not yalnızca kendi anonim eşleşme oturumunuza özel olarak kaydedilir; hiçbir kişiye iletilmez veya kamuya açık yayımlanmaz.',
	},
	{
		question: 'Bağış veya sadaka bağlantısı var mı?',
		answer: 'Hayır. Bu sitede bağış tahsilatı yapılmıyor. Doğrulanmamış hesaplara veya bağlantılara ödeme göndermeyin.',
	},
	{
		question: 'Eylem Rehberi PDF’ini nereden alabilirim?',
		answer: 'Çark eşleşmesi tamamlanınca eylem rehberi PDF’i aynı pencerede indirilebilir. Mevcut dosya bir başlangıç taslağıdır; resmi ya da hukuki talimat değildir.',
	},
];

function FAQPage() {
	return (
		<main className="content-page faq-page">
			<header className="content-page__header">
				<p className="eyebrow">BİLGİ · GÜVENLİK · SÜREÇ</p>
				<h1>Sıkça sorulan sorular</h1>
				<p className="content-page__intro">Mevcut özelliklerin ve geliştirme verilerinin durumu hakkında açık yanıtlar.</p>
			</header>
			<div className="faq-list">
				{questions.map(({ question, answer }) => (
					<details className="faq-item" key={question}>
						<summary>{question}<span aria-hidden="true">+</span></summary>
						<p>{answer}</p>
					</details>
				))}
			</div>
		</main>
	);
}

export default FAQPage;