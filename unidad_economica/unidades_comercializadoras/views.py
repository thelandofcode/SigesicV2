"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.unidades_comercializadoras.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de unidades comercializadoras
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

from unidad_economica.sub_unidad_economica.models import SubUnidadEconomica,SubUnidadEconomicaDirectorio, SubUnidadEconomicaProceso
from unidad_economica.sub_unidad_economica.forms import SubUnidadEconomicaProcesoForm
from unidad_economica.directorio.forms import DirectorioForm
from unidad_economica.directorio.models import Directorio
from base.constant import CREATE_MESSAGE

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

# Create your views here.
class UnidadComercializadoraCreate(SuccessMessageMixin,CreateView):
    """!
    Clase que registra las unidades comercializadoras

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 16-05-2016
    @version 2.0.0
    """
    model = SubUnidadEconomica
    form_class = SubUnidadEconomicaProcesoForm
    template_name = "unidades.comercializadoras.create.html"
    success_url = reverse_lazy('unidades_comercializadoras_create')
    success_message = CREATE_MESSAGE
    
    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido, en cuyo caso se procede a registrar los datos de la unidad comercializadora
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 16-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        
        ## Se crea y se guarda el modelo de directorio
        directorio = Directorio()
        directorio.prefijo_uno=form.cleaned_data['prefijo_uno'],
        directorio.direccion_uno=form.cleaned_data['direccion_uno'],
        directorio.prefijo_dos=form.cleaned_data['prefijo_dos'],
        directorio.direccion_dos=form.cleaned_data['direccion_dos'],
        directorio.prefijo_tres=form.cleaned_data['prefijo_tres'],
        directorio.direccion_tres=form.cleaned_data['direccion_tres'],
        directorio.prefijo_cuatro=form.cleaned_data['prefijo_cuatro'],
        directorio.direccion_cuatro=form.cleaned_data['direccion_cuatro'],
        directorio.parroquia = form.cleaned_data['parroquia']
        directorio.activo=True,
        directorio.save()
        
        ## Se crea y se guarda el modelo de sub_unidad_economica
        self.object = form.save(commit=False)
        self.object.nombre_sub = form.cleaned_data['nombre_sub']
        #self.object.tipo_coordenada = form.cleaned_data['tipo_coordenada']
        self.object.coordenada_geografica = form.cleaned_data['coordenada_geografica']
        self.object.telefono = form.cleaned_data['telefono']
        #modelSubUnidad.tipo_tenencia_id = form.cleaned_data['tipo_tenencia']
        self.object.m2_contruccion = form.cleaned_data['m2_contruccion']
        self.object.m2_terreno = form.cleaned_data['m2_terreno']
        self.object.autonomia_electrica = form.cleaned_data['autonomia_electrica']
        self.object.consumo_electrico = form.cleaned_data['consumo_electrico']
        self.object.cantidad_empleados = form.cleaned_data['cantidad_empleados']
        self.object.sede_servicio = form.cleaned_data['sede_servicio']
        self.object.directorio = directorio
        self.object.save()
        
        ## Se crea y se guarda en el modelo del proceso de la sub-unidad
        proceso = SubUnidadEconomicaProceso()
        #proceso.codigo_ciiu = form.cleaned_data['codigo_ciiu_id']
        proceso.capacidad_instalada_texto = form.cleaned_data['capacidad_instalada_texto']
        proceso.capacidad_instalada_select = form.cleaned_data['capacidad_instalada_select']
        proceso.capacidad_utilizada = form.cleaned_data['capacidad_utilizada']
        proceso.sub_unidad_economica = self.object
        
        ## Se crea y se guarda la tabla intermedio entre directorio-sub unidad
        directorio_subunidad = SubUnidadEconomicaDirectorio()
        directorio_subunidad.directorio = directorio
        directorio_subunidad.sub_unidad_economica = self.object
        directorio_subunidad.save()
        
        return super(SubUnidadEconomicaCreate, self).form_valid(form)