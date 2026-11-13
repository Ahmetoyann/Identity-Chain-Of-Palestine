const headingTags = {
	1: 'h1',
	2: 'h2',
	3: 'h3',
	4: 'h4',
	5: 'h5',
	6: 'h6',
};

export function Heading({ as, level = 2, variant, className = '', children, ...props }) {
	const Tag = as || headingTags[level] || 'h2';
	const classes = ['type-heading', variant && `type-heading--${variant}`, className]
		.filter(Boolean)
		.join(' ');

	return <Tag className={classes} {...props}>{children}</Tag>;
}

export function Eyebrow({ className = '', children, ...props }) {
	const classes = ['type-eyebrow', className].filter(Boolean).join(' ');
	return <p className={classes} {...props}>{children}</p>;
}

export function Text({ as: Tag = 'p', variant, className = '', children, ...props }) {
	const classes = ['type-text', variant && `type-text--${variant}`, className]
		.filter(Boolean)
		.join(' ');

	return <Tag className={classes} {...props}>{children}</Tag>;
}

export default Heading;
