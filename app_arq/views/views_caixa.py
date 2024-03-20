from django.shortcuts import get_object_or_404, redirect, render

from ..forms import CaixaForm
from ..models import Caixa

# Create your views here.

def caixa_lista(request):
    dataset = Caixa.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'caixa/lista.html', context)

def caixa_novo(request):
    if request.method == 'POST':
        form = CaixaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('caixa_lista')  # Redirecione para a lista após criar
    else:
        form = CaixaForm()
    
    return render(request, 'caixa/criar.html', {'form': form})


# def caixa_detalhes(request, pk):
#     caixa_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'ano/detalhes.html', {'caixa_ob': caixa_ob})

def caixa_editar(request, id):
    context ={}
    caixa_ob = get_object_or_404(Caixa, id=id)
    if request.method == 'POST':
        form = CaixaForm(request.POST, instance=caixa_ob)
        if form.is_valid():
            form.save()
            return redirect('caixa_lista')
    else:
        form = CaixaForm(instance=caixa_ob)
    context = {
        'form': form,
        'caixa_ob': caixa_ob
    }
    return render(request, 'caixa/editar.html', context)

def caixa_delete(request, id):
    context ={}
    caixa_ob = get_object_or_404(Caixa, id=id)
    if request.method == 'POST':
        caixa_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('caixa_lista')
    
    context = {
        'caixa_ob': caixa_ob
    }
    
    return render(request, 'caixa/excluir.html', context)

