from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import LinkForm
from .models import Link


@login_required
def index(request):
    form = LinkForm()
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            link = form.save(request.user)
            return redirect('created', link_id=link.id)

    context = {
        'form': form,
    }
    return render(request, 'main/index.html', context)


@login_required
def created(request, link_id):
    link = get_object_or_404(Link, pk=link_id)
    identifier = link.hash_alias if link.hash_alias else link.hash
    context = {
        'short_url': str('http://127.0.0.1:8000/' + identifier)
    }
    return render(request, 'main/created.html', context)


@login_required
def show_all_links(request):
    links = Link.objects.filter(user_id=request.user.id).order_by('-id')
    for link in links:
        identifier = link.hash_alias if link.hash_alias else link.hash
        link.hash = str('http://127.0.0.1:8000/' + identifier)
    return render(request, 'main/links.html', {
        'links': links,
    })


def redirect_link(request, link_hash):
    link = get_object_or_404(Link, Q(hash=link_hash) | Q(hash_alias=link_hash))
    link.clicks += 1
    link.save(update_fields=['clicks'])
    return HttpResponseRedirect(link.initial_url)
