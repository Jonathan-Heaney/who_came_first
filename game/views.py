from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import FamousPerson
import random
import urllib.parse

# Create your views here.


def index(request):
    if 'person1_id' not in request.session or 'person2_id' not in request.session:
        person1, person2 = get_people(request)
        request.session['person1_id'] = person1["id"]
        request.session['person2_id'] = person2["id"]
        request.session['person1_birthyear'] = person1["birthyear"]
        request.session['person2_birthyear'] = person2["birthyear"]
    else:
        person1 = FamousPerson.objects.get(id=request.session['person1_id'])
        person2 = FamousPerson.objects.get(id=request.session['person2_id'])
    # person1 = request.session.pop('person1', None)
    # person2 = request.session.pop('person2', None)
    # if person1 and person2:
    #     correct_answer = compare_ages(person1, person2)
    #     print(f"Correct answer: {correct_answer}")

    # chosen_answer = request.session.pop('chosen_person_id', None)
    # print(f"Chosen answer: {chosen_answer}")

    # if chosen_answer and correct_answer:
    #     if chosen_answer == correct_answer["id"]:
    #         answer_response = "Correct!"
    #     else:
    #         answer_response = "Incorrect!"
    # else:
    #     answer_response = None

    return render(request, "game/index.html", {
        "person1": person1,
        "person2": person2,
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
    if person1["birthyear"] < person2["birthyear"]:
        return person1
    else:
        return person2


@ require_POST
def check_answer(request):
    if 'person1_id' not in request.session or 'person2_id' not in request.session:
        return redirect('index')

    correct_id = min(request.session['person1_id'], request.session['person2_id'],
                     key=lambda id: FamousPerson.objects.get(id=id).birthyear)

    print(f"Correct ID: {correct_id}")
    person_id = request.POST.get('person_id')
    print(f"Person ID: {person_id}")

    if int(person_id) == int(correct_id):
        response = "Correct"
    else:
        response = "Incorrect"

    person1 = FamousPerson.objects.get(id=request.session['person1_id'])
    person2 = FamousPerson.objects.get(id=request.session['person2_id'])

    del request.session['person1_id']
    del request.session['person2_id']

    return render(request, 'game/index.html', {
        'response': response,
        'person1': person1,
        'person2': person2
    })
