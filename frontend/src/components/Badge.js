function Badge({ tone = 'olive', className = '', children, ...props }) {
	const classes = ['badge', `badge--${tone}`, className].filter(Boolean).join(' ');
	return <span className={classes} {...props}>{children}</span>;
}

export default Badge;
