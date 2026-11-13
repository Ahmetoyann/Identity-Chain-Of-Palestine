import Badge from './Badge';
import Button from './Button';
import { Heading, Text } from './Typography';

function StoryCard({
	image,
	imageAlt = '',
	category,
	title,
	description,
	href,
	actionLabel = 'Hikayeyi oku',
	className = '',
}) {
	const classes = ['story-card', className].filter(Boolean).join(' ');

	return (
		<article className={classes}>
			{image && (
				<img className="story-card__image" src={image} alt={imageAlt} loading="lazy" />
			)}
			<div className="story-card__content">
				{category && <Badge>{category}</Badge>}
				<Heading level={3} className="story-card__title">{title}</Heading>
				{description && <Text className="story-card__description">{description}</Text>}
				{href && <Button variant="text" href={href}>{actionLabel}</Button>}
			</div>
		</article>
	);
}

export default StoryCard;
