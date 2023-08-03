from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


def get_subs(category):
    user_email = []
    for user in category.subscribes.all():
        user_email.append(user_email)
    return user_email


def weekly_post_sub(instance, category):
    template = 'email/week_selection.html'
    user_emails = get_subs(category)
    email_subject = f'Selection for the week in your favorite category - "{category}"'
    html = render_to_string(
        template_name=template,
        context={
            'category': category,
            'posts': instance,
        },
    )
    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email='rassylkovna@yandex.ru',
        to=user_emails
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()
