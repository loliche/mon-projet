from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm, PostForm
from .models import Animal, Equipement

def animal_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {'animals' : animals , 'equipements' : equipements })

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    form=MoveForm()
    text = ''
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        #if form.is_valid():
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
        if nouveau_lieu.disponibilite == "libre" :
            text = ''
            if nouveau_lieu.id_equip == 'litière' :
                if animal.etat != 'endormi' :
                    text = f'Désolée, {animal.id_animal} ne peut pas être placé dans la litière s_il n_est pas endormi'
                else :
                    nouveau_lieu.save()
                    animal.etat = "affamé"
                    animal.save()
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
            elif nouveau_lieu.id_equip == 'mangeoire' :
                if animal.etat != 'affamé' :
                    text = f'Désolée, {animal.id_animal} ne peut pas être placé dans la mangeoire s_il n_a pas faim'
                else :
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.etat = "repus"
                    animal.save()
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
            elif nouveau_lieu.id_equip == "roue" :
                if animal.etat != 'repus' :
                    text = f'Désolée, {animal.id_animal} ne peut pas faire de sport s_il n_a pas mangé'
                else :
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.etat = "fatigué"
                    animal.save()
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
            elif nouveau_lieu.id_equip == "nid" :
                if animal.etat != 'fatigué' :
                    text = f'Désolée, {animal.id_animal} n_est pas fatigué'
                else :
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.etat = "endormi"
                    animal.save()
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
        else :
            text = f'{nouveau_lieu.id_equip} n_est pas libre'
            #return redirect('animal_detail', id_animal=id_animal )
    else:
        form = MoveForm()
    return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form, 'message' : text})

def animal_photo(request):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'blog/photo.html', {'animal.photo': animal.photo})

def equipement_detail(request,id_equip):
    equipement = get_object_or_404(Equipement, pk=id_equip)
    return render(request, 'blog/animal_detail.html', {'equipement': equipement})

def animal_new(request):
    if request.method == "POST":
        form= PostForm(request.POST)
        if form.is_valid():
            litière = Equipement.objects.get(id_equip = "litière")
            animal=form.save(commit=False)
            animal.etat = "affamé"
            animal.lieu = litière
            animal.save()
            return redirect('animal_list')
    else :
        form = PostForm()
    return render(request, 'blog/animal_edit.html', {'form' : form})