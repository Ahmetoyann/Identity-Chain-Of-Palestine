function Footer({ brand = 'IDENTITY CHAIN', links = [], className = '' }) {
	const classes = ['site-footer', className].filter(Boolean).join(' ');

	return (
		<footer className={classes}>
			<a className="site-footer__brand" href="#home">{brand}</a>
			{links.length > 0 && (
				<nav className="site-footer__links" aria-label="Alt gezinme">
					{links.map(({ label, href }) => <a key={`${label}-${href}`} href={href}>{label}</a>)}
				</nav>
			)}
			<small className="site-footer__copyright">© {new Date().getFullYear()} {brand}</small>
		</footer>
	);
}

export default Footer;
