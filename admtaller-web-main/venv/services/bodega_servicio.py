# copia de producto_servicio

from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller
from infrastructure import cookie_autoriz
from fastapi import status


async def get_lista_productos_bodega(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/lista/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")
    # Si todo está correcto, Retornamos la respuesta de la API
    productos = response.json()
    return productos

# Almacenamiento masivo de productos en bodega (actulizacion de cantidades y almacenar cabecera) -- OK
########################################################################################################
async def cabecera_bodega_mas(request: Request,cabecera: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/cabecera_in"

    async with httpx.AsyncClient() as client:
        try:
            print("cabecera api:",cabecera,"  :   ", url)
            response: Response = await client.post(url, json=cabecera, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def actualizar_bodega_mas(request: Request,productos: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/mas/{id_usuario}/"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=productos, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def actualizar_bodega_cabecera_mas(request: Request,productos: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/cabecera_mas/{id_usuario}/"
    print("cabecera retiro enviada:",productos)
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=productos, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

# Retiro de productos de bodega (actulizacion de cantidades y almacenar cabecera) (en proceso)
########################################################################################################
async def cabecera_bodega_retiro(request: Request,cabecera: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/cabecera_menos/{id_usuario}/"

    async with httpx.AsyncClient() as client:
        try:
            #print("cabecera api:",cabecera,"  :   ", url)
            response: Response = await client.post(url, json=cabecera, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def actualizar_bodega_menos(request: Request,productos: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/menos/{id_usuario}/"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=productos, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def grabar_detalle_retiro_bodega(request: Request,productos: dict) -> Optional[dict]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/detalle_retiro/{id_usuario}/"
    print("productos detalle retiro enviados:",productos)
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=productos, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def get_lista_productos(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/lista/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    productos = response.json()
    return productos

async def actualizar_producto_bodega(request: Request,id:str,cantidad:float,sc:float) -> Optional[bool]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/bodega/producto_actualizar/{id_usuario}/"
    producto = {"id_producto":id,"cantidad":cantidad,"stock_critico":sc}
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=producto, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    print("respuesta api:",respuesta)
    return respuesta

async def listar_docentes_taller(request: Request) -> Optional[bool]:
    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/lista_docentes_talleres/{id_usuario}"
    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    respuesta = response.json()
    # print("respuesta api:",respuesta)
    return respuesta



# async def delete_asignatura(request: Request, sigla: str) -> Optional[dict]:

#     # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
#     id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
#     error_message: str = None

#     # Armamos la URL de la API respectiva
#     url = f"{APITaller.URL_BASE.value}/asignatura/eliminar/{sigla}/{id_usuario}"

#     async with httpx.AsyncClient() as client:
#         try:
#             response: Response = await client.delete(url)
#             response.raise_for_status()
#         except httpx.HTTPStatusError as e:
#             error_message = e.response.json().get("detail")
#             if "409" not in str(e):
#                 raise Exception(f"Error en la llamada a la API respectiva. [{error_message}]")
#         except httpx.RequestError as e:
#             raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

#     # Si todo está correcto, Retornamos la respuesta de la API
#     eliminacion = response.json()
#     return eliminacion


# async def get_asignatura(request: Request, sigla: str) -> Optional[dict]:

#     # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
#     id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

#     # Armamos la URL de la API respectiva
#     url = f"{APITaller.URL_BASE.value}/asignatura/{sigla}/{id_usuario}"

#     async with httpx.AsyncClient() as client:
#         try:
#             response: Response = await client.get(url)
#             response.raise_for_status()
#         except httpx.HTTPStatusError as e:
#             raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
#         except httpx.RequestError as e:
#             raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

#     # Si todo está correcto, Retornamos la respuesta de la API
#     asignatura = response.json()
#     return asignatura


# async def update_asignatura(request: Request, asignatura: dict) -> Optional[dict]:
#     # Armamos la URL de la API respectiva
#     url = f"{APITaller.URL_BASE.value}/asignatura"

#     async with httpx.AsyncClient() as client:
#         try:
#             response: Response = await client.put(url, json=asignatura, follow_redirects=True)
#             response.raise_for_status()
#         except httpx.HTTPStatusError as e:
#             raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
#         except httpx.RequestError as e:
#             raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

#     # Si todo está correcto, Retornamos la respuesta de la API
#     asignatura = response.json()
#     return asignatura


# async def insert_asignatura(asignatura: dict) -> Optional[dict]:
#     # Armamos la URL de la API respectiva
#     url = f"{APITaller.URL_BASE.value}/asignatura"

#     async with httpx.AsyncClient() as client:
#         try:
#             response: Response = await client.post(url, json=asignatura, follow_redirects=True)
#             response.raise_for_status()
#         except httpx.HTTPStatusError as e:

#             if e.response.status_code == status.HTTP_409_CONFLICT:
#                 return {
#                     "msg_error": e.response.json()["detail"],
#                     }

#             raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
#         except httpx.RequestError as e:
#             raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

#     # Si todo está correcto, Retornamos la respuesta de la API
#     asignatura = response.json()
#     return asignatura


# async def get_talleres_lista(sigla: str) -> Optional[dict]:
#     # Armamos la URL de la API respectiva
#     url = f"{APITaller.URL_BASE.value}/asignatura/{sigla}/taller/lista"

#     async with httpx.AsyncClient() as client:
#         try:
#             response: Response = await client.get(url)
#             response.raise_for_status()
#         except httpx.HTTPStatusError as e:
#             raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
#         except httpx.RequestError as e:
#             raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

#     # Si todo está correcto, Retornamos la respuesta de la API
#     talleres = response.json()
#     return talleres
