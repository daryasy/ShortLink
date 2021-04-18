from celery import shared_task

from main.models import Link


@shared_task
def expire_link(link_id):
    print(link_id)
    link = Link.objects.get(id=link_id)
    link.active = False
    link.save(update_fields=['active'])
