from django.core.mail import send_mail

def send_otp_email(user, code):
    send_mail(
        subject="Ваш OTP-код",
        message=f"Ваш код: {code}",
        from_email="noreply@example.com",
        recipient_list=[user.email]
    )
