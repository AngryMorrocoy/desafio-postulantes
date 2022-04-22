## NOTA

Decidí no modificar el contenido original del README ya que en un futuro me
podría ser útil a mi mismo (hombre precavido vale el doble).

Decidí escribir el README en español todo esto a pesar de que el código está
escrito en inglés por convenciones, dado que ya estaba "empezado" de esta
forma y la comunicación ha sido en español.

# Desafio Postulantes

Con el fin de seleccionar a nuestros 2 developers, tenemos el siguente desafio.

De la siguente URL [Link](https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html) es necesario crear un código que sea capaz de parsear la pagina web y devolver un json con esta información.
![image](https://user-images.githubusercontent.com/3030497/164536276-9eb79d10-4fb0-4943-a15f-2536a8586330.png)

El JSON de respuesta puede venir en el formato que estimes conveniente.

## Preguntas Frecuentes

- Tipos de entrega, cualquiera de los siguiente sirve
  - API caso generico
  - API caso particular
  - Script para el caso particular
- Lenguaje: El que más te guste
- Plazo de Entrega: Indefinido, iremos entrevistando a los que van terminando primero.

## Proceso de desarrollo + info

Acá presento una api escrita en [Quart](), en un principio quería escribir la
api en flask, pero dado que decidí usar
[Requests-HTML](https://github.com/psf/requests-html) y el uso de async/await no
va muy de la mano con flask (o no de manera sencilla), opté por mover la
aplicación a quart que es *flask con async/await* mover el proyecto de flask a
Quart no fue más que cambiar unas líneas, ya que en esencia el código es el
mismo.

## Api

Solo hay una ruta presente, y se describe su funcionamiento a continuación:

### /api/payroll/

Esta ruta solo soporta **GET** y retorna un json con todos los datos presentes
en la *Nómina registro voluntario de instituciones financieras extranjeras e
internacionales* de la siguiente forma:

```json
{
    "results": [
        {
          "country": "CANADÁ",
          "expires_at": "Tue, 01 Jun 2021 04:00:00 GMT",
          "last_update_data": {
            "date": "Thu, 25 Jun 2020 04:00:00 GMT",
            "dr": "DR XV",
            "res_number": "1327"
          },
          "number": 1,
          "registration_data": {
            "date": "Wed, 08 Oct 2008 04:30:00 GMT",
            "dr": "DR XV",
            "res_number": "7553"
          },
          "social_reason": "BIRCHMOUNT INVESTMENTS LIMITED",
          "state": "PENDIENTE"
        },
        ...
    ]
}
```

### Ejecutar en local

En caso de desearlo, puede ejecutar el proyecto de manera local de dos formas
(esto después de clonar el repositorio). Cabe destacar que todos los comandos
que se escriben a continuación se ejecutan dentro de la raíz del proyecto.

```bash
> pip install -r requirements.txt
> python3 app.py
```

De la forma en que se ejecuta arriba, el proyecto inica en modo de desarrollo
con "*debug=True*". Si ejecutarlo en "*modo produccion*"

```bash
> hypercorn app:app
```
