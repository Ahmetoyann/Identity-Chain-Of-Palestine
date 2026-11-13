const variantClasses = {
	dark: 'button--dark',
	olive: 'button--olive',
	text: 'button--text',
};

function Button({
	as: Component,
	href,
	variant = 'dark',
	className = '',
	children,
	...props
}) {
	const Tag = Component || (href ? 'a' : 'button');
	const classes = ['button', variantClasses[variant] || variantClasses.dark, className]
		.filter(Boolean)
		.join(' ');

	return <Tag className={classes} href={href} {...props}>{children}</Tag>;
}

export default Button;
