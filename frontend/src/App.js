
import './App.css';
import './components/components.css';
import { Button, Eyebrow, Heading, HeroBanner, Navbar } from './components';

function App() {
  return (
    <main className="site-shell">
      <Navbar />

      <HeroBanner
        id="home"
        showKey={false}
        title="Rakamlar değil, hayatlar;"
        emphasis="dosyalar değil, kardeşler."
        description="Bir isme sahip çıkmak, bir dünyayı kurtarmaktır."
        secondLine="Kardeşlik zincirimize katıl."
        backgroundImage="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=2200&q=85"
        actionLabel="KARDEŞİNİ SEÇ"
        actionHref="#stories"
      />

      <section className="next-section" id="stories">
        <Eyebrow>HER İSMİN BİR HİKAYESİ VAR</Eyebrow>
        <Heading level={2}>Bir hikayeyle başlayalım.</Heading>
        <Button variant="text" href="#volunteer" className="text-link">
          Hikayeleri keşfet <span aria-hidden="true">↗</span>
        </Button>
      </section>
      <span className="anchor-target" id="manifesto" />
      <span className="anchor-target" id="contact" />
      <span className="anchor-target" id="volunteer" />
    </main>
  );
}

export default App;
