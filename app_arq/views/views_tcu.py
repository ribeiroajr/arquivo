from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TcuForm
from ..models import Tcu

# Create your views here.

def tcu_lista(request):
    dataset = Tcu.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tcu/lista.html', context)

def tcu_novo(request):
    if request.method == 'POST':
        form = TcuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tcu_lista')  # Redirecione para a lista após criar
    else:
        form = TcuForm()
    
    return render(request, 'tcu/criar.html', {'form': form})


# def tcu_detalhes(request, pk):
#     tcu_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tcu/detalhes.html', {'tcu_ob': tcu_ob})

def tcu_editar(request, id):
    context ={}
    tcu_ob = get_object_or_404(Tcu, id=id)
    if request.method == 'POST':
        form = TcuForm(request.POST, instance=tcu_ob)
        if form.is_valid():
            form.save()
            return redirect('tcu_lista')
    else:
        form = TcuForm(instance=tcu_ob)
    context = {
        'form': form,
        'tcu_ob': tcu_ob
    }
    return render(request, 'tcu/editar.html', context)

def tcu_delete(request, id):
    context ={}
    tcu_ob = get_object_or_404(Tcu, id=id)
    if request.method == 'POST':
        tcu_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tcu_lista')
    
    context = {
        'tcu_ob': tcu_ob
    }
    
    return render(request, 'tcu/excluir.html', context)

