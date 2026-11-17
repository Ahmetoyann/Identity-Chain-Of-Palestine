import { useState } from 'react';
import Button from './Button';

const defaultLinks = [
	{ label: 'ARŞİV', href: '/archive' },
	{ label: 'MANİFESTO', href: '/manifesto' },
	{ label: 'SSS', href: '/faq' },
	{ label: 'İLETİŞİM', href: '/contact' },
];

function Navbar({
	brand = 'KENETLEN',
	brandHref = '/',
	links = defaultLinks,
	actionLabel = 'Gönüllü Ol',
	actionHref = '/archive',
	onAction,
	className = '',
}) {
	const [menuOpen, setMenuOpen] = useState(false);
	const classes = ['site-header', className].filter(Boolean).join(' ');

	function closeMenu() {
		setMenuOpen(false);
	}

	return (
		<header className={classes}>
			<a className="brand" href={brandHref} aria-label={`${brand} ana sayfa`}>
				<img className="brand-logo" src="/yeni_ana_logo_transparent.png" alt="" />
				<span className="brand-name">{brand}</span>
			</a>

			<button
				className={`menu-toggle${menuOpen ? ' is-open' : ''}`}
				type="button"
				aria-label={menuOpen ? 'Menüyü kapat' : 'Menüyü aç'}
				aria-expanded={menuOpen}
				onClick={() => setMenuOpen((isOpen) => !isOpen)}
			>
				<span />
				<span />
			</button>

			<nav className={`primary-nav${menuOpen ? ' is-open' : ''}`} aria-label="Ana gezinme">
				{links.map(({ label, href }) => (
					<a key={`${label}-${href}`} href={href} onClick={closeMenu}>{label}</a>
				))}
				{actionLabel && (
					<Button className="volunteer-link" href={onAction ? undefined : actionHref} variant="olive" onClick={(event) => {
						closeMenu();
						if (onAction) {
							event.preventDefault();
							onAction();
						}
					}}>
						{actionLabel}
					</Button>
				)}
			</nav>
		</header>
	);
}

export default Navbar;
