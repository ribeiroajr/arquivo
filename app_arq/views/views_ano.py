from django.shortcuts import render, redirect, get_object_or_404
from ..models import Ano
from ..forms import AnoForm


def ano_novo(request):
    if request.method == 'POST':
        form = AnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ano_lista')  # Redirecione para a lista após criar
    else:
        form = AnoForm()
    
    return render(request, 'ano/criar.html', {'form': form})

def ano_lista(request):
    dataset = Ano.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'ano/lista.html', context)


# def ano_detalhes(request, pk):
#     ano_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'ano/detalhes.html', {'ano_ob': ano_ob})

def ano_editar(request, id):
    context ={}
    ano_ob = get_object_or_404(Ano, id=id)
    if request.method == 'POST':
        form = AnoForm(request.POST, instance=ano_ob)
        if form.is_valid():
            form.save()
            return redirect('ano_lista')
    else:
        form = AnoForm(instance=ano_ob)
    context = {
        'form': form,
        'ano_ob': ano_ob
    }
    return render(request, 'ano/editar.html', context)

def ano_delete(request, id):
    context ={}
    ano_ob = get_object_or_404(Ano, id=id)
    if request.method == 'POST':
        ano_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('ano_lista')
    
    context = {
        'ano_ob': ano_ob
    }
    
    return render(request, 'ano/excluir.html', context)

