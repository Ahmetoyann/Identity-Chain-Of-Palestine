function Input({
	id,
	label,
	hint,
	error,
	as: Component = 'input',
	className = '',
	...props
}) {
	const controlId = id || props.name;
	const messageId = `${controlId}-message`;
	const classes = ['field__control', error && 'field__control--error', className]
		.filter(Boolean)
		.join(' ');

	return (
		<div className="field">
			{label && <label className="field__label" htmlFor={controlId}>{label}</label>}
			<Component
				id={controlId}
				className={classes}
				aria-invalid={Boolean(error)}
				aria-describedby={hint || error ? messageId : undefined}
				{...props}
			/>
			{(hint || error) && (
				<span className={`field__message${error ? ' field__message--error' : ''}`} id={messageId}>
					{error || hint}
				</span>
			)}
		</div>
	);
}

export default Input;
