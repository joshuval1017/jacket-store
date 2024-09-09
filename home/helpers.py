


from django.core.mail import send_mail

from django.conf import settings 


def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_welcome_mail(email , token,date ):
    subject = "Welcome to Glowing ! Here's Your 10% Discount Coupon "
    message = f"Congratulations on successfully registering with us! To thank you for joining our community, we're excited to offer you a special 10% discount coupon. Simply use the code {token} during checkout to enjoy your savings. Hurry, this offer is valid until {date}."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

from django.core.mail import EmailMessage
from django.conf import settings
from .models import Orders



from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
import os

def generate_pdf(order):
    template_path = 'myapp/invoice_template.html'
    context = {'order': order}
    template = get_template(template_path)
    html = template.render(context)

    # Create a byte stream buffer
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    # Check for errors
    if pisa_status.err:
        return None

    # Retrieve the PDF from the buffer
    pdf = result.getvalue()
    result.close()
    return pdf


def send_order_confirmation_email(email, order_id):
    # Retrieve the order details based on order_id
    order = Orders.objects.get(pk=order_id)

    # Generate the PDF invoice
    pdf = generate_pdf(order)
    if not pdf:
        return False

    # Create email subject and message
    subject = 'Your order has been placed successfully'
    message = 'Dear {},\n\nThank you for your order. Please find attached the invoice for your order.\n\nBest regards,\nGlowing'.format(order.customer.username)

    # Create the email
    email_message = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )

    # Attach the PDF invoice
    email_message.attach(f'invoice_{order_id}.pdf', pdf, 'application/pdf')

    # Send the email
    email_message.send()

    return True