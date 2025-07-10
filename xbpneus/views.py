from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def painel_cliente(request):
    return render(request, 'painel.html')

