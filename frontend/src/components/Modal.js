import { useEffect } from 'react';

function Modal({ open, onClose, title, children, className = '' }) {
	useEffect(() => {
		if (!open) return undefined;

		function handleKeyDown(event) {
			if (event.key === 'Escape') onClose?.();
		}

		document.addEventListener('keydown', handleKeyDown);
		return () => document.removeEventListener('keydown', handleKeyDown);
	}, [open, onClose]);

	if (!open) return null;

	const classes = ['modal__dialog', className].filter(Boolean).join(' ');

	return (
		<div className="modal" onMouseDown={(event) => {
			if (event.target === event.currentTarget) onClose?.();
		}}>
			<section className={classes} role="dialog" aria-modal="true" aria-label={title}>
				<button className="modal__close" type="button" onClick={onClose} aria-label="Kapat">
					<span />
					<span />
				</button>
				{title && <h2 className="modal__title">{title}</h2>}
				{children}
			</section>
		</div>
	);
}

export default Modal;
