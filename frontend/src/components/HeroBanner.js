import Button from './Button';
import { Heading, Text } from './Typography';

function HeroBanner({
	id = 'home',
	title,
	emphasis,
	description,
	secondLine,
	actionLabel,
	actionHref = '#content',
	onAction,
	backgroundImage,
	showKey = true,
	children,
	className = '',
}) {
	const classes = ['hero-banner', className].filter(Boolean).join(' ');
	const imageStyle = backgroundImage
		? { backgroundImage: `url("${backgroundImage}")` }
		: undefined;

	return (
		<section className={classes} id={id} aria-labelledby={`${id}-title`}>
			<div className="hero-banner__image" style={imageStyle} aria-hidden="true" />
			<div className="hero-banner__wash" aria-hidden="true" />
			{showKey && <div className="hero-banner__key" aria-hidden="true"><span /></div>}

			<div className="hero-banner__content">
				<Heading as="h1" className="hero-banner__title" id={`${id}-title`}>
					<span>{title}</span>
					{emphasis && <em>{emphasis}</em>}
				</Heading>
				{(description || secondLine) && (
					<Text className="hero-banner__copy">
						{description}
						{secondLine && <><br />{secondLine}</>}
					</Text>
				)}
				{actionLabel && (
					<Button
						className="hero-banner__action"
						href={onAction ? undefined : actionHref}
						onClick={onAction ? (event) => { event.preventDefault(); onAction(); } : undefined}
					>
						{actionLabel}
					</Button>
				)}
				{children}
			</div>
		</section>
	);
}

export default HeroBanner;
