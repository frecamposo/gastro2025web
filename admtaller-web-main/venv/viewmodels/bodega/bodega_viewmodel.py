
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import programacion_service
from services import param_service
from services import asignatura_service
from services import producto_service
from services import bodega_servicio
from infrastructure.constants import Mensajes
import json


class BodegaViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        
        self.id_producto: int
        self.nom_producto: int
        self.precio: int
        self.cod_unidad_medida: int
        self.cod_categ_producto: int

        self.producto: dict
        self.lista_unidad_medida: List[dict]
        self.lista_categoria_producto: List[dict]
        
        self.productos: List[dict] = []
        self.asignaturas: List[dict] = []
        self.docentes: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.productos = await bodega_servicio.get_lista_productos_bodega(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    async def load_retiro(self):
        if self.esta_conectado:
            # debemos recuperar un listado de los Profesores Correspondintes a los talleres
            self.productos = await bodega_servicio.get_lista_productos_bodega(self.id_usuario_conectado)
            self.asignaturas = await asignatura_service.get_asignaturas_lista(self.id_usuario_conectado)
            print("asignaturas:",self.asignaturas)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value
            
            
    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        print("ingreso a insertar listado producto en bodega para actualizar mas")
        form = await self.request.form()
        self.nom_producto = form.get("listado", "")
        
        fecha_ingreso = form.get("fecha_ingreso_form", "")
        factura = form.get("factura_form", "")
        proveedor = form.get("proveedor_form", "")
        responsable = form.get("responsable_form", "")
        cabecera={"id_ingreso":0,"fecha_ingreso":fecha_ingreso,"factura":factura,"proveedor":proveedor,"responsable":responsable}
        print("cabecera:",cabecera)
        arreglo_productos = json.loads(self.nom_producto)
        
        data_mas_cabecera=[]
        data=[]
        print("arreglo productos:",arreglo_productos)
        for producto in arreglo_productos:
            data.append({"id_producto":producto["id_producto"],"cantidad":producto["cantidad"]})            
        #print("listado productos a ingresar a bodega:",data)
        
        if True:
            self.usuario = await bodega_servicio.cabecera_bodega_mas(self.request,cabecera)
            print("cabecera ingresada:",self.usuario)
            id_ingreso=self.usuario["id_ingreso"]
            print("id ingreso:",id_ingreso)

            self.usuario = await bodega_servicio.actualizar_bodega_mas(self.request,data)
            # debe actualizar el contenido de la cabecera con el id_ingreso
            print("arreglo productos:",arreglo_productos)
            for producto in arreglo_productos:
                data_mas_cabecera.append({"id_detalle":id_ingreso,
                                          "id_producto":producto["id_producto"],
                                          "nombre":producto["nombre"],
                                          "precio":producto["precio"],
                                          "cantidad":producto["cantidad"],
                                          "total":int(producto["precio"])*int(producto["cantidad"])})
            print("data mas cabecera:",data_mas_cabecera)
            
            self.usuario = await bodega_servicio.actualizar_bodega_cabecera_mas(self.request,data_mas_cabecera)
            
            if not self.usuario:
                self.msg_error = "Error al agregar el producto"
            else:
                #self.id_producto = self.usuario["id_producto"]
                self.msg_exito = "Se ha agregado correctamente el producto"
        
        print("usuario:",self.usuario)
        return self.usuario
    
  # Función que carga datos y verifica si está conectado al sistema
    async def insert_retiro(self):
        # Recuperamos los datos desde el formulario
        print("ingreso a insertar retiro de producto en bodega para actualizar mas")
        form = await self.request.form()
        self.nom_producto = form.get("listado", "")
        
        fecha_ingreso = form.get("fecha_ingreso_form", "")
        asignatura = form.get("asignatura_form", "")
        codigo = form.get("codigo_form", "")
        seccion = form.get("seccion_form", "")
        responsable_recibe = form.get("responsable_entrega_form", "")
        responsable = form.get("responsable_form", "")
        cabecera={"id_retiro":0,
                  "fecha":fecha_ingreso,
                  "nombre_asig":asignatura,
                  "seccion":seccion,
                  "codigo_asig":codigo,
                  "responsable_retiro":responsable_recibe,
                  "responsable_entrega":responsable
                  }
        print("cabecera:",cabecera)
        arreglo_productos = json.loads(self.nom_producto)
        
        data_mas_cabecera=[]
        data=[]
        print("arreglo productos:",arreglo_productos)
        for producto in arreglo_productos:
            data.append({"id_producto":producto["id_producto"],"cantidad":producto["cantidad"]})            
        #print("listado productos a ingresar a bodega:",data)
        print("productos para retiro:",data)
        
        if True:
            self.usuario = await bodega_servicio.cabecera_bodega_retiro(self.request,cabecera)
            print("cabecera ingresada:",self.usuario)
            id_ingreso=self.usuario["id_retiro"]
            print("id retiro:",id_ingreso)
                
            self.usuario = await bodega_servicio.actualizar_bodega_menos(self.request,data)
            # debe actualizar el contenido de la cabecera con el id_ingreso
            print("arreglo productos:",arreglo_productos)
            print("data mas cabecera:",data)
            ############
            data_retiro=[]
            for producto in arreglo_productos:
                data_retiro.append({"id_detalle":id_ingreso,"id_producto":producto["id_producto"],"nombre":producto["nombre"],"precio":producto["precio"],"cantidad":producto["cantidad"],"total":int(producto["precio"])*int(producto["cantidad"]) })
            print("data retiro:",data_retiro)
            self.usuario = await bodega_servicio.grabar_detalle_retiro_bodega(self.request,data_retiro)
            return self.usuario
        
        
            for producto in arreglo_productos:
                data_mas_cabecera.append({"id_detalle":id_ingreso,
                                          "id_producto":producto["id_producto"],
                                          "nombre":producto["nombre"],
                                          "precio":producto["precio"],
                                          "cantidad":producto["cantidad"],
                                          "total":int(producto["precio"])*int(producto["cantidad"])})
            print("data mas cabecera:",data_mas_cabecera)
            
            self.usuario = await bodega_servicio.actualizar_bodega_cabecera_mas(self.request,data_mas_cabecera)
            
            if not self.usuario:
                self.msg_error = "Error al agregar el producto"
            else:
                #self.id_producto = self.usuario["id_producto"]
                self.msg_exito = "Se ha agregado correctamente el producto"
        
        print("usuario:",self.usuario)
        return self.usuario
          
  # Función que permite actualizar las cantidades y stock critico en los productos
    async def update_productos(self,id_producto: int, cantidad: float, stock_critico: float):
        if self.esta_conectado:
            resp = await bodega_servicio.actualizar_producto_bodega(self.request,id_producto,cantidad,stock_critico)
            return resp
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

  # Función que permite listar los profesores
    async def listar_profesores(self):
        if self.esta_conectado:
            self.docentes = await bodega_servicio.listar_docentes_taller(self.request)
            return self.docentes
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value