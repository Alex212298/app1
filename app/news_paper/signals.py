from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post



@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):

    postCategory_list = instance.postCategory.all()

    for category in postCategory_list:
        for sub in category.subscribes.all():
            html_content = render_to_string('post_created.html',
                                            {
                                                'user': sub,
                                                'post': instance,
                                            })

            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=instance.text,
                from_email='rassylkovna@yandex.ru',
                to=[f'{sub.email}']

            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    print("ok")