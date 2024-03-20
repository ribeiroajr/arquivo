from django.shortcuts import get_object_or_404, redirect, render

from ..forms import CaixaForm
from ..models import Caixa

# Create your views here.

def home(request):
    return render(request, 'home.html')