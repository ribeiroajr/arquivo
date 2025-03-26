import django
import statistics
from django.contrib import admin
from django.urls import path
from app_arq.views.views_cod import *
from app_arq.views.views_ano import *
from app_arq.views.views_om import *
from app_arq.views.views_doc import *
from app_arq.views.views_caixa import *
from app_arq.views.views_tcu import *
from app_arq.views.views_tipo import *
from app_arq.views.views_home import *
from app_arq.views.views_tipo_guarada import *
from app_arq.views.views_status import *
from app_arq.views.views_log import *
from app_arq.views.views_graficos import *
from . import views

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from core import settings

urlpatterns = [
    path('', home, name='home'),
    path('cod_lista', cod_lista, name='cod_lista'),
    path('cod_editar/<int:id>/', cod_editar, name='cod_editar'),
    path('cod_delete/<int:id>/', cod_delete, name='cod_delete'),
    path('cod_novo', cod_novo, name='cod_novo'),

    path('om_lista', om_lista, name='om_lista'),
    path('om_editar/<int:id>/', om_editar, name='om_editar'),
    path('om_delete/<int:id>/', om_delete, name='om_delete'),
    path('om_novo', om_novo, name='om_novo'),
    
    path('get_codigo_details/', get_codigo_details, name='get_codigo_details'),

    path('doc_lista', doc_lista, name='doc_lista'),
    path('doc_editar/<int:id>/', doc_editar, name='doc_editar'),
    path('doc_delete/<int:id>/', doc_delete, name='doc_delete'),
    path('doc_novo', doc_novo, name='doc_novo'),

    path('caixa_lista', caixa_lista, name='caixa_lista'),
    path('caixa_editar/<int:id>/', caixa_editar, name='caixa_editar'),
    path('caixa_delete/<int:id>/', caixa_delete, name='caixa_delete'),
    path('caixa_novo', caixa_novo, name='caixa_novo'),

    path('ano_lista', ano_lista, name='ano_lista'),
    path('ano_editar/<int:id>/', ano_editar, name='ano_editar'),
    path('ano_delete/<int:id>/', ano_delete, name='ano_delete'),
    path('ano_novo', ano_novo, name='ano_novo'),

    path('tcu_lista', tcu_lista, name='tcu_lista'),
    path('tcu_editar/<int:id>/', tcu_editar, name='tcu_editar'),
    path('tcu_delete/<int:id>/', tcu_delete, name='tcu_delete'),
    path('tcu_novo', tcu_novo, name='tcu_novo'),

    path('status_lista', status_lista, name='status_lista'),
    path('status_editar/<int:id>/', status_editar, name='status_editar'),
    path('status_delete/<int:id>/', status_delete, name='status_delete'),
    path('status_novo', status_novo, name='status_novo'),

    path('tipo_lista', tipo_lista, name='tipo_lista'),
    path('tipo_editar/<int:id>/', tipo_editar, name='tipo_editar'),
    path('tipo_delete/<int:id>/', tipo_delete, name='tipo_delete'),
    path('tipo_novo', tipo_novo, name='tipo_novo'),
    
    path('tipo_guarda_lista', tipo_guarda_lista, name='tipo_guarda_lista'),
    path('tipo_guarda_editar/<int:id>/', tipo_guarda_editar, name='tipo_guarda_editar'),
    path('tipo_guarda_delete/<int:id>/', tipo_guarda_delete, name='tipo_guarda_delete'),
    path('tipo_guarda_novo', tipo_guarda_novo, name='tipo_guarda_novo'),
    
    path('listar_logs', listar_logs, name='listar_logs'),
    
    path('sgc_ajax_load_related_data/', sgc_ajax_load_related_data, name="sgc_ajax_load_related_data"),
        
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/ciaer.ico'))),
    
    path('', views.pagination, name="pagination"),

    path('graficos/', gerar_graficos, name='gerar_graficos'),

# ]  + statistics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
