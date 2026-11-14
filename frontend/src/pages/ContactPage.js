import { useState } from 'react';
import Input from '../components/Input';
import { sendContactMessage } from '../services/api';

function ContactPage() {
	const [submitting, setSubmitting] = useState(false);
	const [feedback, setFeedback] = useState({ type: '', message: '' });

	async function handleSubmit(event) {
		event.preventDefault();
		setSubmitting(true);
		setFeedback({ type: '', message: '' });
		const form = event.currentTarget;
		const formData = new FormData(form);
		try {
			await sendContactMessage({
				name: formData.get('name'),
				email: formData.get('email'),
				subject: formData.get('subject'),
				message: formData.get('message'),
				consent: formData.get('consent') === 'on',
				website: formData.get('website'),
			});
			form.reset();
			setFeedback({ type: 'success', message: 'Mesajınız alındı. Bu yanıt yalnızca iletinin veritabanına kaydedildiğini bildirir.' });
		} catch (error) {
			setFeedback({ type: 'error', message: error.message });
		} finally {
			setSubmitting(false);
		}
	}

	return (
		<main className="content-page contact-page">
			<header className="content-page__header">
				<p className="eyebrow">İLETİŞİM VE DESTEK</p>
				<h1>Bir sorunuz mu var?</h1>
				<p className="content-page__intro">Mesajınız yalnızca ekibin iletişim amacıyla kullanılır. Lütfen hassas konum, kimlik veya üçüncü kişilere ait özel bilgileri göndermeyin.</p>
			</header>
			<div className="contact-layout">
				<form className="contact-form" onSubmit={handleSubmit}>
					<Input name="name" label="Adınız" autoComplete="name" minLength={2} maxLength={120} required />
					<Input name="email" label="E-posta adresiniz" type="email" autoComplete="email" maxLength={320} required />
					<Input name="subject" label="Konu" minLength={3} maxLength={120} required />
					<Input as="textarea" name="message" label="Mesajınız" minLength={10} maxLength={3000} rows={6} required />
					<div className="contact-form__trap" aria-hidden="true">
						<label htmlFor="contact-website">Web sitesi</label>
						<input id="contact-website" name="website" tabIndex={-1} autoComplete="off" />
					</div>
					<label className="consent-control">
						<input type="checkbox" name="consent" required />
						<span>Mesajıma yanıt vermek için adım ve e-posta adresimin işlenmesini kabul ediyorum.</span>
					</label>
					{feedback.message && <p className={`form-feedback form-feedback--${feedback.type}`} role={feedback.type === 'error' ? 'alert' : 'status'}>{feedback.message}</p>}
					<button className="contact-form__submit" type="submit" disabled={submitting}>{submitting ? 'Gönderiliyor…' : 'Mesajı gönder'}</button>
				</form>
				<aside className="contact-aside">
					<h2>Güvenli iletişim</h2>
					<p>Gönderim sırasında mesaj ve yanıt adresiniz veritabanına kaydedilir. Bu sürümde mesaj kutusu ekip içi inceleme içindir; otomatik yanıt veya acil destek hattı değildir.</p>
					<p className="contact-aside__social">Resmi sosyal medya hesapları doğrulanıp yayımlandığında burada listelenecek.</p>
				</aside>
			</div>
		</main>
	);
}

export default ContactPage;
