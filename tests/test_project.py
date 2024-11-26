import pytest
from django.conf import settings
from django.db.utils import IntegrityError
from django.test import Client
from model_bakery import baker
from pytest_django.asserts import assertContains, assertRedirects

from creatures.models import Creature


@pytest.fixture
def creature():
    return baker.make(Creature, _fill_optional=True)


@pytest.mark.django_db
def test_creature_model_has_proper_fields(client: Client, creature):
    PROPER_FIELDS = (
        'id',
        'name',
        'slug',
        'type1',
        'attack',
        'defense',
        'speed',
        'generation',
    )
    for field in PROPER_FIELDS:
        assert getattr(creature, field) is not None


def test_creatures_is_the_only_installed_app():
    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    assert len(custom_apps) == 1
    assert custom_apps[0] == 'creatures.apps.CreaturesConfig'


@pytest.mark.django_db
def test_root_url_redirects_to_creature_list(client: Client):
    response = client.get('/')
    assertRedirects(response, '/creatures/')


@pytest.mark.django_db
def test_list_all_creatures(client: Client):
    DETAIL_URL = '/creatures/{slug}/'

    creatures = baker.make(Creature, _quantity=10)
    response = client.get('/creatures/')
    assert response.status_code == 200
    for creature in creatures:
        assertContains(response, creature.name)
        assertContains(response, DETAIL_URL.format(slug=creature.slug))


@pytest.mark.django_db
def test_creature_detail(client: Client, creature):
    url = f'/creatures/{creature.slug}/'
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, creature.name)
    assertContains(response, creature.type1)
    assertContains(response, creature.attack)
    assertContains(response, creature.defense)
    assertContains(response, creature.speed)
    assertContains(response, creature.generation)
    assert response.context['creature'] == creature


@pytest.mark.django_db
def test_back_button_is_present_on_creature_detail(client: Client, creature):
    url = f'/creatures/{creature.slug}/'
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, 'href="/creatures/"')


@pytest.mark.django_db
def test_creature_model_is_available_on_admin(admin_client: Client):
    response = admin_client.get('/admin/creatures/creature/')
    assert response.status_code == 200


# https://stackoverflow.com/a/54563945
@pytest.mark.django_db(transaction=True)
def test_unique_constraints_for_creature(creature):
    with pytest.raises(IntegrityError):
        baker.make(Creature, name=creature.name)
    with pytest.raises(IntegrityError):
        baker.make(Creature, slug=creature.slug)


@pytest.mark.django_db
def test_default_values_for_creature_fields():
    creature = baker.make(Creature)
    assert creature.attack == 0
    assert creature.defense == 0
    assert creature.speed == 0
    assert creature.generation == 1


@pytest.mark.django_db
def test_creature_representation(creature):
    assert str(creature) == creature.name
