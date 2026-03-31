from django.shortcuts import render
from datetime import date
from ..models import Docs, Caixa, LogAcaoUsuario


def home(request):
    context = {}

    if request.user.is_authenticated:
        hoje = date.today()
        context = {
            'total_docs':      Docs.objects.count(),
            'docs_conferidos': Docs.objects.filter(status_doc=True).count(),
            'caixas_abertas':  Caixa.objects.filter(fk_status=1).count(),
            'cadastros_hoje':  LogAcaoUsuario.objects.filter(
                                   acao='cadastrou',
                                   create_at__date=hoje
                               ).count(),
        }

    return render(request, 'home.html', context)
