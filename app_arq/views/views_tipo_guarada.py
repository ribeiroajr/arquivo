from django.shortcuts import render, redirect, get_object_or_404
from app_arq.forms import Tipo_guardaForm
from ..models import TipoGuarda
from ..forms import Tipo_guardaForm

def tipo_guarda_novo(request):
    if request.method == 'POST':
        form = Tipo_guardaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_guarda_lista')  # Redirecione para a lista após criar
    else:
        form = Tipo_guardaForm()
    
    return render(request, 'tipo_guarda/criar.html', {'form': form})

def tipo_guarda_lista(request):
    dataset = TipoGuarda.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tipo_guarda/lista.html', context)


# def tipo_guarda_detalhes(request, pk):
#     tipo_guarda_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tipo_guarda/detalhes.html', {'tipo_guarda_ob': tipo_guarda_ob})

def tipo_guarda_editar(request, id):
    context ={}
    tipo_guarda_ob = get_object_or_404(TipoGuarda, id=id)
    if request.method == 'POST':
        form = Tipo_guardaForm(request.POST, instance=tipo_guarda_ob)
        if form.is_valid():
            form.save()
            return redirect('tipo_guarda_lista')
    else:
        form = Tipo_guardaForm(instance=tipo_guarda_ob)
    context = {
        'form': form,
        'tipo_guarda_ob': tipo_guarda_ob
    }
    return render(request, 'tipo_guarda/editar.html', context)

def tipo_guarda_delete(request, id):
    context ={}
    tipo_guarda_ob = get_object_or_404(TipoGuarda, id=id)
    if request.method == 'POST':
        tipo_guarda_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tipo_guarda_lista')
    
    context = {
        'tipo_guarda_ob': tipo_guarda_ob
    }
    
    return render(request, 'tipo_guarda/excluir.html', context)

