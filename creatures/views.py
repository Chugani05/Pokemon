from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Creature


def creature_list(request: HttpRequest) -> HttpResponse:
    creatures = Creature.objects.all()
    return render(request, 'creatures/creature/creature-list.html', dict(creatures=creatures))


def creature_detail(request: HttpRequest, creature_slug: str) -> HttpResponse:
    creatures = Creature.objects.get(slug=creature_slug)
    return render(request, 'creatures/creature/creature-detail.html', dict(creature=creatures))
