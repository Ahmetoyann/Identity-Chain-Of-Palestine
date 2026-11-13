import { useState } from 'react';
import Button from './Button';

const defaultLinks = [
	{ label: 'HİKAYELER (ARŞİV)', href: '#stories' },
	{ label: 'MANİFESTO', href: '#manifesto' },
	{ label: 'İLETİŞİM', href: '#contact' },
];

function Navbar({
	brand = 'IDENTITY CHAIN',
	brandHref = '#home',
	links = defaultLinks,
	actionLabel = 'Gönüllü Ol',
	actionHref = '#volunteer',
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
				<span className="brand-mark" aria-hidden="true"><i /><i /><b /></span>
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
					<Button className="volunteer-link" href={actionHref} variant="olive" onClick={closeMenu}>
						{actionLabel}
					</Button>
				)}
			</nav>
		</header>
	);
}

export default Navbar;
