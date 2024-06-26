from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from io import BytesIO
import base64
import json
import matplotlib.pyplot as plt
from also.forms import SpeciesForm
from also.models import Species, Vote
from django.http import HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def rules(request):
    return render(request, 'rules.html')


def play(request):
    return render(request, 'play.html')


def about(request):
    return render(request, 'about.html')


def education(request):
    return render(request, 'edu.html')


def detail(request, species_id):
    species = get_object_or_404(Species, pk=species_id)
    return render(request, "detail.html", {"species": species})


def species_list(request):
    all_species_list = Species.objects.order_by("species_name")
    context = {"species_list": all_species_list}
    return render(request, "species_list.html", context)


@login_required
def vote(request, species_id):
    species = get_object_or_404(Species, pk=species_id)
    user = request.user

    # Check if the user has already voted for this species
    if Vote.objects.filter(user=user, species=species).exists():
        messages.error(request, 'You have already voted for this species.')
    else:
        species.score = F("score") + 1
        species.save()
        Vote.objects.create(user=user, species=species)
        messages.success(request, 'Your vote has been recorded.')

    return redirect("species_list")


@login_required
def add_species(request):
    genome = request.GET.get('genome', '')

    if request.method == "POST":
        form = SpeciesForm(request.POST, request.FILES)
        if form.is_valid():
            species = form.save(commit=False)
            species.user = request.user
            species.save()
            return redirect('species_list')
    else:
        form = SpeciesForm(initial={'species_name': '',
                                    'species_genome': genome,
                                    'species_description': '',
                                    'can_move': False,
                                    'can_defend': False})

    return render(request, 'add_species.html', {'form': form})


def upload_sim_data(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        data = json.load(json_file)

        genome_species_data = {}

        # Collect genome and species information
        for genome_info in data['simulationGenomeData']['genomes']:
            genome = genome_info['genome']
            species_name = genome_info['speciesName']

            if genome not in genome_species_data:
                genome_species_data[genome] = {'species_names': [species_name], 'counts': []}
            else:
                genome_species_data[genome]['species_names'].append(species_name)

        times = [snapshot['time'] for snapshot in data['simulationCountData']['snapshots']]

        # Initialize counts_by_species dictionary
        counts_by_species = {species_name: [0]*len(times) for genome in genome_species_data for species_name in genome_species_data[genome]['species_names']}

        # Collect counts for each species over time
        for t_idx, snapshot in enumerate(data['simulationCountData']['snapshots']):
            species_counts = {entry['speciesName']: entry.get('aliveCount', 0) for entry in snapshot['speciesDataList']}
            for species_name in counts_by_species.keys():
                counts_by_species[species_name][t_idx] = species_counts.get(species_name, 0)

        # Filter species that reached quantity more than 5 at least once
        filtered_species = {species_name: counts for species_name, counts in counts_by_species.items() if max(counts) > 5}

        # Calculate total counts for each species
        total_counts = {species_name: sum(counts) for species_name, counts in filtered_species.items()}

        # Sort species by total count
        sorted_species = sorted(total_counts, key=total_counts.get, reverse=True)

        # Generate plots in groups of 6 species
        plots = []
        for i in range(0, len(sorted_species), 8):
            plt.figure(figsize=(10, 6))
            group_species = sorted_species[i:i+8]
            for species_name in group_species:
                plt.plot(times, filtered_species[species_name], label=species_name)
            plt.xlabel('Czas')
            plt.ylabel('Żywe organizmy')
            plt.title(f'Zmiany populacji gatunków w czasie symulacji (Grupa {i//8 + 1})')
            plt.grid(True)
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), shadow=True, ncol=4)

            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            plt.close()
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png).decode('utf-8')
            plots.append(graphic)

        return render(request, 'upload_sim_data.html', {'plots': plots, 'genome_species_data': genome_species_data})
    elif request.method == 'POST':
        return HttpResponseBadRequest("Nie wybrano pliku.")
    return render(request, 'upload_sim_data.html')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def user_page(request):
    user = request.user
    added_species = Species.objects.filter(user=user)
    voted_species_ids = Vote.objects.filter(user=user).values_list('species', flat=True)
    voted_species = Species.objects.filter(id__in=voted_species_ids)

    context = {
        'added_species': added_species,
        'voted_species': voted_species
    }
    return render(request, 'user_page.html', context)
