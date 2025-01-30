from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

#send mail when a event create
@receiver(m2m_changed, sender=Event.participants.through)
def send_email_to_participants(sender, instance, action, **kwargs):
    if action == 'post_add':
        participant_emails = [p.email for p in instance.participants.all()]
        
        send_mail(
            subject="New Event Created 🎉",
            message=f"Dear Participant,\n\nYou have been added to the event: {instance.name}.\n"
                    f"Event Details:\nDate: {instance.date}\nTime: {instance.time}\nLocation: {instance.location}\n\n"
                    "Looking forward to your participation!\n\nBest Regards,\nEvent Team",
            from_email="tazulislam42609770@gmail.com",
            recipient_list=participant_emails,
            fail_silently=False,
        )