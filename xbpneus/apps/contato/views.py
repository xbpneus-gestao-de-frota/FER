from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Contato


class ContatoView(TemplateView):
    """Página de contato"""
    template_name = 'contato/contato.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Contato - XBPNEUS Premium',
            'meta_description': 'Entre em contato com a XBPNEUS Premium. Estamos prontos para atendê-lo.',
            'assuntos': Contato.ASSUNTO_CHOICES
        })
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            contato = Contato.objects.create(
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone', ''),
                assunto=request.POST.get('assunto'),
                mensagem=request.POST.get('mensagem')
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('contato:contato')
            
        except Exception as e:
            messages.error(request, 'Erro ao enviar mensagem. Tente novamente.')
            return self.get(request, *args, **kwargs)

