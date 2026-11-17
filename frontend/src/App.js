
import { useEffect, useState } from 'react';
import './App.css';
import './components/components.css';
import { HeroBanner, Navbar } from './components';
import ContactPage from './pages/ContactPage';
import FAQPage from './pages/FAQPage';
import ManifestoPage from './pages/ManifestoPage';
import PrisonerDetailPage from './pages/PrisonerDetailPage';
import StoriesPage from './pages/StoriesPage';
import MatchRoulette from './components/MatchRoulette';

function App() {
  const [matchOpen, setMatchOpen] = useState(false);
  const openMatch = () => setMatchOpen(true);
  const closeMatch = () => setMatchOpen(false);
  const path = window.location.pathname.replace(/\/$/, '') || '/';

  useEffect(() => {
    const titles = {
      '/': 'Bir isim, bir hayat | Kenetlen',
      '/archive': 'Canlı Arşiv | Kenetlen',
      '/manifesto': 'Manifesto | Kenetlen',
      '/contact': 'İletişim | Kenetlen',
      '/faq': 'Sıkça Sorulan Sorular | Kenetlen',
    };
    document.title = titles[path] || 'Sayfa bulunamadı | Kenetlen';
  }, [path]);

  if (path.startsWith('/prisoners/')) {
    return (
      <>
        <PrisonerDetailPage onOpenMatch={openMatch} />
        <MatchRoulette open={matchOpen} onClose={closeMatch} />
      </>
    );
  }

  const pages = {
    '/archive': <main className="archive-page"><StoriesPage onOpenMatch={openMatch} /></main>,
    '/manifesto': <ManifestoPage />,
    '/contact': <ContactPage />,
    '/faq': <FAQPage />,
  };

  const isHome = path === '/';

  return (
    <div className="site-shell">
      <Navbar
        brand="KENETLEN"
        links={[
          { label: 'ARŞİV', href: '/archive' },
          { label: 'MANİFESTO', href: '/manifesto' },
          { label: 'SSS', href: '/faq' },
          { label: 'İLETİŞİM', href: '/contact' },
        ]}
        actionLabel="Kardeşinle Eşleş"
        onAction={openMatch}
      />

      {isHome ? (
        <main className="home-page">
          <HeroBanner
            id="home"
            showKey={false}
            title="Bir isim, bir hayat,"
            emphasis="senin kardeşin."
            description="Dayanışma ve mahremiyet ilkeleriyle hazırlanan gönüllülük deneyimi."
            secondLine="Şu anki profiller temsili kurgu içerikleridir."
            actionLabel="KARDEŞİNLE EŞLEŞ"
            onAction={openMatch}
            backgroundImage={process.env.PUBLIC_URL + '/filistin-direnis-referandum.jpg'}
          />
          <section className="home-note">
            <p className="eyebrow">KİŞİLERDEN ÖNCE İLKELER</p>
            <h2>Özen, doğrulama ve mahremiyet.</h2>
            <a href="/manifesto">Çalışma ilkelerimizi okuyun <span aria-hidden="true">↗</span></a>
          </section>
        </main>
      ) : pages[path] || <NotFoundPage />}

      <MatchRoulette open={matchOpen} onClose={closeMatch} />

      <footer className="site-footer">
        <a className="site-footer__brand" href="/" aria-label="Identity Chain ana sayfa">
          <img className="brand-logo" src="/yeni_ana_logo_transparent.png" alt="" />
          <span>KENETLEN</span>
        </a>
        <nav className="site-footer__links" aria-label="Alt gezinme">
          <a href="/archive">Arşiv</a>
          <a href="/manifesto">Manifesto</a>
          <a href="/faq">SSS</a>
          <a href="/contact">İletişim</a>
        </nav>
        <small className="site-footer__copyright">Bu bir gönüllülük hareketidir, kar amacı gütmez.</small>
      </footer>
    </div>
  );
}

function NotFoundPage() {
  return (
    <section className="content-page not-found-page">
      <p className="eyebrow">404 · SAYFA BULUNAMADI</p>
      <h1>Aradığınız sayfa burada değil.</h1>
      <a href="/">Ana sayfaya dön <span aria-hidden="true">↗</span></a>
    </section>
  );
}

export default App;
