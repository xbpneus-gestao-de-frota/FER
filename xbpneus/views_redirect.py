"""
Views de redirecionamento para integração com site principal
"""
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def transportador_redirect(request):
    """
    Redireciona /transportador/ para a área de login
    Usado quando o site principal xbpneus.com tem link para área do transportador
    """
    return redirect('/login/')


def area_cliente_redirect(request):
    """
    Redireciona /area-cliente/ para a área de login
    Alternativa para diferentes nomes de link no site principal
    """
    return redirect('/login/')


@csrf_exempt
def health_check(request):
    """
    Endpoint de verificação de saúde do sistema
    """
    return HttpResponse("OK", content_type="text/plain")


def root_redirect(request):
    """
    Página inicial quando acessada pelo domínio principal
    Mostra informações sobre o sistema ou redireciona para login
    """
    # Se usuário já está logado, vai para o painel
    if request.user.is_authenticated:
        return redirect('/painel/')
    
    # Se não está logado, vai para login
    return redirect('/login/')

