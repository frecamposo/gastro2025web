import fastapi
from fastapi_chameleon import template
from viewmodels.usuario.usuarios_viewmodel import UsuariosViewModel
from viewmodels.usuario.usuario_viewmodel import UsuarioViewModel
from viewmodels.bodega.bodega_viewmodel import BodegaViewModel
from viewmodels.producto.productos_viewmodel import ProductosViewModel
from starlette.requests import Request
from starlette import status
from services import usuario_service

router = fastapi.APIRouter()
#------------------------Rutas para la gestión de la bodega-----------------------#


@router.get("/bodega")
@template(template_file="bodega/bodega.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.load()
    
    datos = {"titulo": "Bodega Duoc",
             "esta_conectado": True,
             "ano_academ": "2024",
             "login_conectado": "usuarioejemplo",
             "cod_carrera":1,
             "nom_carrera":"Gastronomía",
             "cod_perfil_conectado":0    }
    
    return  vm.to_dict()


@router.get("/bodega/registro")
@template(template_file="bodega/bodega_ingreso.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.load()
    return  vm.to_dict()


@router.post("/bodega/registro")
@template(template_file="bodega/bodega_ingreso.pt")
async def bodega_ingresar(request: Request):
    vm = BodegaViewModel(request)
    print("Ingreso a registrar productos en bodega")
    await vm.insert()
    await vm.load()
    return  vm.to_dict()


@router.get("/bodega/listado")
@template(template_file="bodega/bodega_listado.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.load()
    return  vm.to_dict()



@router.get("/bodega/retiro")
@template(template_file="bodega/bodega_retiro.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.load_retiro()
    return  vm.to_dict()

@router.post("/bodega/retiro")
@template(template_file="bodega/bodega_retiro.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.insert_retiro()
    await vm.load_retiro()
    return  vm.to_dict()

# version de /bodega/retiro mejorada de acuerdo a lo solicitado
@router.get("/bodega/retiro_productos")
@template(template_file="bodega/bodega_retiro_prod.pt")
async def bodega(request: Request):
    vm = BodegaViewModel(request)
    await vm.load_retiro()
    return  vm.to_dict()


@router.get("/bodega/producto/lista")
@template(template_file="bodega/producto_lista.pt")
async def producto_lista(request: Request):
    vm = BodegaViewModel(request)
    await vm.load()
    return vm.to_dict() 


@router.get("/bodega/producto/actualizar/{id_producto}/{cantidad}/{stock_critico}")
@template(template_file="bodega/producto_lista.pt")
async def producto_actualizar_lista(request: Request, id_producto: int, cantidad: float, stock_critico: float):
    vm = BodegaViewModel(request)
    await vm.update_productos(id_producto, cantidad, stock_critico)
    await vm.load()
    return vm.to_dict()

@router.get("/bodega/listado_profesores")
@template(template_file="bodega/asignatura_lista_profesor.pt")
async def lista_profesores_asignaturas(request: Request):
    vm = BodegaViewModel(request)
    await vm.listar_profesores()
    await vm.load()
    return vm.to_dict()



import json

@router.get("/bodega/producto/actualizar/all/{todo}")
@template(template_file="bodega/producto_lista.pt")
async def producto_actualizar_listado(request: Request, todo:str):
    vm = BodegaViewModel(request)
    objeto_python = json.loads("["+todo+"]")
    data = (objeto_python)
    for x in data:
        for item in x.items():
            print("item:",item)
            id_producto = int(item[0])
            cantidad = float(item[1]['cantidad'])
            stock_critico = float(item[1]['stock_critico'])
            resp= await vm.update_productos(id_producto, cantidad, stock_critico)
    await vm.load()
    return vm.to_dict()

