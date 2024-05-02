from django.shortcuts import render
from .models import FamousPerson
import random
import urllib.parse

# Create your views here.


def index(request):
    person1, person2 = get_people(request)
    print(person1, person2)

    return render(request, "game/index.html", {
        "person1": person1,
        "person2": person2
    })


def get_people(request):
    valid_persons = FamousPerson.objects.filter(hpi__gte=80)
    valid_person_count = valid_persons.count()
    random_index1 = random.randint(0, valid_person_count - 1)
    person1 = valid_persons[random_index1]
    random_index2 = random.randint(0, valid_person_count - 1)

    while random_index2 == random_index1:
        random_index2 = random.randint(0, valid_person_count - 1)
    person2 = valid_persons[random_index2]

    person1_data = prepare_person_data(person1)

    person2_data = prepare_person_data(person2)

    return person1_data, person2_data


def prepare_person_data(person):
    wikipedia_link = generate_wikipedia_link(person.name)
    person_data = {
        'id': person.id,
        'name': person.name,
        'occupation': person.occupation,
        'birthyear': person.birthyear,
        'deathyear': person.deathyear,
        'hpi': person.hpi,
        'wikipedia_link': wikipedia_link,
    }
    return person_data


def generate_wikipedia_link(name):
    formatted_name = urllib.parse.quote(name.replace(" ", "_"))
    return f"https://en.wikipedia.org/wiki/{formatted_name}"


def compare_ages(person1, person2):
    if person1.birthyear < person2.birthyear:
        return "Person 1"
    else:
        return "Person 2"
