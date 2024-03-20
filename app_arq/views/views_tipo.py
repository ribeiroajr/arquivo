from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TipoForm
from ..models import Tipo

# Create your views here.


def tipo_lista(request):
    dataset = Tipo.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tipo/lista.html', context)

def tipo_novo(request):
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_lista')  # Redirecione para a lista após criar
    else:
        form = TipoForm()
    
    return render(request, 'tipo/criar.html', {'form': form})


# def tipo_detalhes(request, pk):
#     tipo_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tipo/detalhes.html', {'tipo_ob': tipo_ob})

def tipo_editar(request, id):
    context ={}
    tipo_ob = get_object_or_404(Tipo, id=id)
    if request.method == 'POST':
        form = TipoForm(request.POST, instance=tipo_ob)
        if form.is_valid():
            form.save()
            return redirect('tipo_lista')
    else:
        form = TipoForm(instance=tipo_ob)
    context = {
        'form': form,
        'tipo_ob': tipo_ob
    }
    return render(request, 'tipo/editar.html', context)

def tipo_delete(request, id):
    context ={}
    tipo_ob = get_object_or_404(Tipo, id=id)
    if request.method == 'POST':
        tipo_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tipo_lista')
    
    context = {
        'tipo_ob': tipo_ob
    }
    
    return render(request, 'tipo/excluir.html', context)

