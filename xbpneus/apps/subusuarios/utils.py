from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


def enviar_convite_subusuario(subusuario, request=None):
    """
    Envia convite por e-mail para subusuário definir sua senha
    """
    try:
        # URL para definir senha
        if request:
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
        else:
            domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
            protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'
        
        url_definir_senha = f"{protocol}://{domain}{reverse('configuracoes:subusuarios:definir_senha', kwargs={'token': subusuario.token_convite})}"
        
        # Contexto para o template
        context = {
            'subusuario': subusuario,
            'usuario_principal': subusuario.usuario_principal,
            'url_definir_senha': url_definir_senha,
            'empresa': getattr(subusuario.usuario_principal, 'empresa', None),
            'site_name': 'XBPNEUS',
            'site_url': f"{protocol}://{domain}",
        }
        
        # Renderizar template HTML
        html_message = render_to_string('subusuarios/emails/convite_subusuario.html', context)
        
        # Versão texto simples
        plain_message = strip_tags(html_message)
        
        # Assunto do e-mail
        subject = f'Convite para acessar o sistema XBPNEUS - {subusuario.usuario_principal.get_full_name() or subusuario.usuario_principal.username}'
        
        # Enviar e-mail
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@xbpneus.com'),
            recipient_list=[subusuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Marcar como enviado
        subusuario.convite_enviado = True
        subusuario.save(update_fields=['convite_enviado'])
        
        logger.info(f'Convite enviado com sucesso para {subusuario.email}')
        return True
        
    except Exception as e:
        logger.error(f'Erro ao enviar convite para {subusuario.email}: {str(e)}')
        return False


def reenviar_convite_subusuario(subusuario, request=None):
    """
    Reenvia convite para subusuário (gera novo token)
    """
    try:
        # Gerar novo token
        subusuario.gerar_novo_token_convite()
        subusuario.save()
        
        # Enviar novo convite
        return enviar_convite_subusuario(subusuario, request)
        
    except Exception as e:
        logger.error(f'Erro ao reenviar convite para {subusuario.email}: {str(e)}')
        return False


def validar_token_convite(token):
    """
    Valida token de convite e retorna o subusuário
    """
    from .models import SubUsuario
    
    try:
        subusuario = SubUsuario.objects.get(
            token_convite=token,
            ativo=True,
            senha_definida=False
        )
        return subusuario
    except SubUsuario.DoesNotExist:
        return None


def definir_senha_subusuario(subusuario, nova_senha):
    """
    Define senha do subusuário e marca como ativo
    """
    try:
        subusuario.set_senha(nova_senha)
        subusuario.primeiro_acesso = False
        subusuario.save()
        
        logger.info(f'Senha definida com sucesso para {subusuario.email}')
        return True
        
    except Exception as e:
        logger.error(f'Erro ao definir senha para {subusuario.email}: {str(e)}')
        return False


def notificar_usuario_principal_novo_subusuario(subusuario, request=None):
    """
    Notifica o usuário principal sobre novo subusuário cadastrado
    """
    try:
        # URL do painel de subusuários
        if request:
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
        else:
            domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
            protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'
        
        url_painel = f"{protocol}://{domain}{reverse('configuracoes:subusuarios:listar_subusuarios')}"
        
        # Contexto para o template
        context = {
            'subusuario': subusuario,
            'usuario_principal': subusuario.usuario_principal,
            'url_painel': url_painel,
            'site_name': 'XBPNEUS',
        }
        
        # Renderizar template HTML
        html_message = render_to_string('subusuarios/emails/notificacao_novo_subusuario.html', context)
        
        # Versão texto simples
        plain_message = strip_tags(html_message)
        
        # Assunto do e-mail
        subject = f'Novo subusuário cadastrado: {subusuario.nome}'
        
        # Enviar e-mail para o usuário principal
        if subusuario.usuario_principal.email:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@xbpneus.com'),
                recipient_list=[subusuario.usuario_principal.email],
                html_message=html_message,
                fail_silently=True,  # Não falhar se não conseguir enviar
            )
        
        logger.info(f'Notificação enviada para usuário principal: {subusuario.usuario_principal.email}')
        return True
        
    except Exception as e:
        logger.error(f'Erro ao notificar usuário principal: {str(e)}')
        return False

