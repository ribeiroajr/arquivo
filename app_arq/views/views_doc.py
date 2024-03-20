from django.shortcuts import get_object_or_404, redirect, render

from ..forms import DocsForm
from ..models import Docs, Codigos
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def doc_lista(request):
    dataset = Docs.objects.all()
    context = {"dataset": dataset}
    print(dataset)
    return render(request, 'doc/lista.html', context)

## ok
# def doc_novo(request):
#     if request.method == 'POST':
#         form = DocsForm(request.POST)
#         if form.is_valid():
#             # Pegar o ano do doc_data enviado via post
#             doc_data = form.cleaned_data.get('doc_data')
#             if not doc_data:
#                 return render(request, 'doc/erro.html', {'mensagem': 'Data do documento não informada'})
            
#             doc_data_ano = doc_data.year
#             print(f'doc_data_ano: {doc_data_ano}')

#             # Pegar o fk_codigo enviado via post
#             fk_codigo = form.cleaned_data.get('fk_codigo')
#             if not fk_codigo:
#                 return render(request, 'doc/erro.html', {'mensagem': 'Código não informado'})
            
#             print(f'fk_codigo: {fk_codigo}')

#             try:
#                 # Recuperar na model Codigos de acordo com fk_codigo enviado
#                 codigos = Codigos.objects.get(pk=fk_codigo.pk)
#             except Codigos.DoesNotExist:
#                 # Trate a exceção caso o objeto não exista
#                 # Aqui você pode redirecionar para uma página de erro ou fazer o que for apropriado para o seu aplicativo
#                 return render(request, 'doc/erro.html', {'mensagem': 'Código não encontrado'})

#             # Verificar se os campos em Codigos estão preenchidos
#             # if (codigos.fase_corrente_ano is None or
#             #         codigos.fase_intermediaria_ano is None or
#             #         codigos.destinacao_final_ano is None):
#             #     return render(request, 'doc/erro.html', {'mensagem': 'Campos em Codigos não estão preenchidos'})

#             # Calcular o novo valor composto
#             novo_valor_composto = (
#                 (codigos.fase_corrente_ano or 0) +
#                 (codigos.fase_intermediaria_ano or 0) +
#                 (codigos.destinacao_final_ano or 0) +
#                 (doc_data_ano or 0)
#             )

#             print(f'novo_valor_composto: {novo_valor_composto}')

#             # Atribuir o novo valor composto ao campo doc_eliminacao_ano no formulário
#             form.cleaned_data['doc_eliminacao_ano'] = novo_valor_composto
#             # print(f'novo_valor_composto: {novo_valor_composto}')


#             # Salvar o formulário sem atribuir diretamente o objeto Codigos
#             doc = form.save(commit=False)
#             doc.fk_codigo = codigos  # Atribuir o objeto Codigos ao campo fk_codigo
            

            
#             # doc.fk_codigo_id = fk_codigo_id  # Atribuir o ID da chave estrangeira ao objeto Docs
#             doc.fase
#             doc.doc_eliminacao_ano = novo_valor_composto  # Atribuir o novo valor composto a doc_eliminacao_ano
#             doc.save()

#             return redirect('doc_lista')  # Redirecione para a lista após criar
#     else:
#         form = DocsForm()

#     return render(request, 'doc/criar.html', {'form': form})


# views.py


def get_codigo_details(request):
    codigo_id = request.GET.get('codigo_id', None)
    if codigo_id:
        codigo = Codigos.objects.filter(pk=codigo_id).first()
        if codigo:
            data = {
                'fase_corrente_ano': codigo.fase_corrente_ano,
                'fase_intermediaria_ano': codigo.fase_intermediaria_ano,
                'destinacao_final_ano': codigo.destinacao_final_ano,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Código não encontrado.'})




def doc_novo(request):
    if request.method == 'POST':
        form = DocsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doc cadastrado com sucesso.')
            return redirect('doc_novo')  # Redirecione para a lista após criar
        else:
            print("Erros de validação no formulário:")
            print(form.errors)  # Exibir erros de validação no console
    else:
        form = DocsForm()
    
    print("Renderizando o formulário...")
    print(request.method)  # Verificar se a página está sendo acessada com o método POST
    
    
    return render(request, 'doc/criar.html', {'form': form})




# def doc_detalhes(request, pk):
#     doc_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'ano/detalhes.html', {'doc_ob': doc_ob})

def doc_editar(request, id):
    context ={}
    doc_ob = get_object_or_404(Docs, id=id)
    if request.method == 'POST':
        form = DocsForm(request.POST, instance=doc_ob)
        if form.is_valid():
            form.save()
            return redirect('doc_lista')
    else:
        form = DocsForm(instance=doc_ob)
    context = {
        'form': form,
        'doc_ob': doc_ob
    }
    return render(request, 'doc/editar.html', context)

def doc_delete(request, id):
    context ={}
    doc_ob = get_object_or_404(Docs, id=id)
    if request.method == 'POST':
        doc_ob.delete()
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('doc_lista')
    
    context = {
        'doc_ob': doc_ob
    }
    
    return render(request, 'doc/excluir.html', context)

