from .models import Link
from hashlib import sha256
from django.forms import ModelForm, URLInput, TextInput, NumberInput

from .tasks import expire_link


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ['initial_url', 'hash_alias', 'ttl']
        widgets = {
            'initial_url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL'
            }),
            'hash_alias': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter link alias',
            }),
            'ttl': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter seconds the link will be available',
            })
        }

    def save(self, user, *args, **kwargs):
        link = super().save(commit=False)
        link.user = user
        unique_link = link.initial_url + str(user.id)
        link.hash = sha256(unique_link.encode()).hexdigest()[:6]
        link_obj, created = Link.objects.get_or_create(
            initial_url=link.initial_url,
            user=link.user,
            defaults={
                'hash': link.hash,
                'hash_alias': link.hash_alias,
                'ttl': link.ttl,
            }
        )
        if not created:
            link_obj.active = True
            link_obj.hash_alias = link.hash_alias
            link_obj.ttl = link.ttl
            link_obj.save(update_fields=['hash_alias', 'active', 'ttl'])

        if link_obj.ttl:
            expire_link.apply_async((link_obj.id, ), countdown=link_obj.ttl)
        return link_obj
