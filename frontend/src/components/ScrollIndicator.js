function ScrollIndicator({ href = '#content', label = 'KEŞFET', className = '' }) {
	const classes = ['scroll-indicator', className].filter(Boolean).join(' ');

	return (
		<a className={classes} href={href} aria-label={`${label} bölümüne kaydır`}>
			<span className="scroll-indicator__line" aria-hidden="true" />
			<small>{label}</small>
		</a>
	);
}

export default ScrollIndicator;
