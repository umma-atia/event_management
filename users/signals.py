from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from event.models import Event


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{
            settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{
            activation_url}\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")



@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()


@receiver(m2m_changed, sender=Event.participant.through)
def send_rsvp_signal(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        users = User.objects.filter(pk__in=pk_set)
        for user in users:
            send_mail(
                'Event RSVP Confirmation',
                f'Hi {user.username}, you have successfully RSVP\'d for {instance.name}.',
                'red910630@gmail.com',
                [user.email],
                fail_silently=False,
            )        