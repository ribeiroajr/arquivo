from django import forms
from django.contrib.auth.models import User
from app_arq.models import *

class BaseForm(forms.ModelForm):
    fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

    class Meta:
        abstract = True

class CodigosForm(BaseForm):
    class Meta:
        model = Codigos
        fields = '__all__'

class OmForm(BaseForm):
    class Meta:
        model = Om
        fields = '__all__'

class TipoForm(BaseForm):
    class Meta:
        model = Tipo
        fields = '__all__'

class TcuForm(BaseForm):
    class Meta:
        model = Tcu
        fields = '__all__'

class AnoForm(BaseForm):
    class Meta:
        model = Ano
        fields = '__all__'

class CaixaForm(BaseForm):
    class Meta:
        model = Caixa
        fields = '__all__'
        
        
class Tipo_guardaForm(BaseForm):
    class Meta:
        model = TipoGuarda
        fields = '__all__'

class StatusForm(BaseForm):
    class Meta:
        model = Status
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        # type="date" exige YYYY-MM-DD para renderizar o valor corretamente
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class DocsForm(BaseForm):
    doc_numero = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    new_file_sigad = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))

    class Meta:
        model = Docs
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DocsForm, self).__init__(*args, **kwargs)
        self.fields["doc_data"].widget = DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields["doc_data"].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        
        self.fields['fk_codigo'].widget.attrs['class'] = 'form-control'
        self.fields['fk_tipo'].widget.attrs['class'] = 'form-control'

        self.fields['fk_doc_origem'].queryset = Om.objects.all().order_by('om')
        self.fields['fk_doc_origem'].widget.attrs['class'] = 'form-control'
        self.fields['fk_doc_destino'].queryset = Om.objects.all().order_by('om')
        self.fields['fk_doc_destino'].widget.attrs['class'] = 'form-control'


	    #self.fields['fk_doc_origem'].widget.attrs['class'] = 'form-control'
        #self.fields['fk_doc_destino'].widget.attrs['class'] = 'form-control'
        self.fields['fk_caixa'].widget.attrs['class'] = 'form-control'
        self.fields['fk_caixa'].queryset = Caixa.objects.filter(fk_status = 1)
        self.fields['fk_caixa'].widget.attrs['required'] = 'required'
        
        self.fields['fk_tcu'].widget.attrs['class'] = 'form-control'
 
        self.fields['doc_numero'].widget.attrs['class'] = 'form-control'
        self.fields['doc_numero'].required = False
        self.fields['doc_numero'].widget.attrs['value'] = 'SEM NÚMERO'
        
        
        
        self.fields['new_file_sigad'].widget.attrs['class'] = 'form-control'
        # self.fields['new_file_sigad'].widget.attrs['placeholder'] = 'NewFile/SIGAD'
        self.fields['new_file_sigad'].required = False
        self.fields['new_file_sigad'].widget.attrs['value'] = 'SEM INDEXADOR'

        self.fields['doc_corrente_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_corrente_ano'].widget.attrs['readonly'] = True

        self.fields['doc_intermediario_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
        self.fields['doc_intermediario_ano'].widget.attrs['readonly'] = True

        self.fields['doc_destinacao_final_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_destinacao_final_ano'].widget.attrs['readonly'] = True

        self.fields['doc_eliminacao_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_eliminacao_ano'].widget.attrs['readonly'] = True
        
        self.fields['doc_obs_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_obs_ano'].widget.attrs['readonly'] = True
        
        self.fields['doc_destinacao_final'].widget.attrs['class'] = 'form-control'
               
        # self.fields['doc_numero'].widget.attrs['placeholder'] = 'Numero do documento'
        
