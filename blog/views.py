from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal,Equipement

def animal_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {'animals' : animals , 'equipements' : equipements })

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    form=MoveForm()
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)    
        if form.is_valid():
            ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            form.save()
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
            if nouveau_lieu.id_equip != 'litière' :
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
            return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form})

def animal_photo(request):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'blog/photo.html', {'animal.photo': animal.photo})

def equipement_detail(request,id_equip):
    equipement = get_object_or_404(Equipement, pk=id_equip)
    return render(request, 'blog/animal_detail.html', {'equipement': equipement})