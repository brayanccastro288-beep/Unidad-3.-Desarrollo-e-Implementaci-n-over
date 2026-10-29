# Sistema de Gestión de Préstamos

**Proyecto académico: Unidad 3. Desarrollo e Implementación — Avance 3**

## 1. Introducción

El presente proyecto consiste en el desarrollo de una aplicación web para la gestión de clientes, préstamos y pagos, utilizando Python como lenguaje de programación, Flask para el funcionamiento de la aplicación web y SQLite como sistema de almacenamiento de datos.

El objetivo es implementar una solución básica que permita organizar la información de los clientes, calcular los préstamos registrados y llevar un control de los pagos realizados. Este desarrollo corresponde a un prototipo académico elaborado para aplicar los conocimientos adquiridos durante el proceso de formación en ingeniería de software.

## 2. Objetivo del proyecto

Desarrollar una aplicación funcional que permita gestionar clientes, registrar préstamos y controlar los pagos mediante una interfaz web sencilla, integrando un módulo de autenticación y una base de datos para almacenar la información.

## 3. Funcionalidades implementadas

- **Módulo de autenticación:** permite ingresar al sistema mediante correo electrónico y contraseña.
- **Registro de clientes:** permite registrar y consultar los clientes almacenados.
- **Registro y cálculo de préstamos:** permite ingresar los datos de un préstamo y calcular sus cuotas según el monto, la tasa de interés y el plazo.
- **Registro de pagos:** permite registrar abonos y actualizar el saldo pendiente del préstamo.
- **Base de datos:** utiliza SQLite para almacenar la información del sistema.
- **Interfaz web:** permite acceder a las funcionalidades desde un navegador.

## 4. Tecnologías utilizadas

| Tecnología | Descripción |
|---|---|
| Python | Lenguaje utilizado para desarrollar la lógica del sistema. |
| Flask | Framework utilizado para crear la aplicación web. |
| SQLite | Base de datos utilizada para almacenar la información. |
| HTML | Estructura de los formularios y las páginas web. |
| Visual Studio Code | Entorno utilizado para escribir y ejecutar el código. |
| GitHub | Plataforma utilizada para alojar y compartir el código fuente. |

## 5. Estructura del proyecto

```text
SistemaNegocio/
├── APP.py
├── requirements.txt
├── README.md
└── negocio.db
```

**Descripción de los archivos:**

- `APP.py`: contiene el código fuente de la aplicación.
- `requirements.txt`: especifica la dependencia necesaria para ejecutar el proyecto.
- `README.md`: contiene la documentación y las instrucciones de instalación.
- `negocio.db`: almacena los datos del sistema cuando este archivo se incluye en el proyecto.

La base de datos se crea automáticamente si no existe, de acuerdo con la configuración del código fuente.

## 6. Requisitos para la ejecución

Para ejecutar el proyecto se necesita:

- Tener instalado Python 3.
- Contar con conexión a Internet para instalar Flask.
- Disponer de Visual Studio Code o una terminal de comandos.
- Descargar el repositorio de GitHub.

## 7. Instrucciones de instalación y ejecución

**Paso 1. Descargar el proyecto**

Descargar el repositorio desde GitHub y descomprimirlo, si se descarga como archivo ZIP.

**Paso 2. Abrir la carpeta**

Abrir la carpeta del proyecto en Visual Studio Code.

**Paso 3. Instalar las dependencias**

Abrir la terminal en la carpeta del proyecto y ejecutar:

```bash
python -m pip install -r requirements.txt
```

**Paso 4. Ejecutar la aplicación**

Ejecutar el siguiente comando:

```bash
python APP.py
```

**Paso 5. Acceder al sistema**

Cuando el servidor indique que está funcionando, abrir el navegador e ingresar a:

http://127.0.0.1:5000

Para acceder directamente al inicio de sesión, utilizar:

http://127.0.0.1:5000/login

## 8. Credenciales de prueba

Si se utiliza la base de datos de prueba configurada en el código, las credenciales iniciales son:

- **Correo electrónico:** admin@negocio.com
- **Contraseña:** 1234

Estas credenciales son únicamente para las pruebas académicas del prototipo.

## 9. Resultados esperados

Con la ejecución de la aplicación se espera comprobar el funcionamiento de las principales operaciones del sistema: autenticación, registro de clientes, cálculo de préstamos y registro de pagos. También se busca verificar que la información se almacene en la base de datos SQLite.

## 10. Conclusión

El desarrollo de esta aplicación permite poner en práctica conocimientos de programación en Python, desarrollo web, manejo de bases de datos y organización de funcionalidades de un sistema de información.

Aunque se trata de una versión básica, el proyecto constituye una primera aproximación a la construcción de una aplicación funcional. En futuras versiones se podrían mejorar la interfaz, las validaciones, la seguridad de las contraseñas y los mecanismos de control de acceso.

## 11. Consideraciones de seguridad

Este proyecto tiene fines académicos y no debe utilizarse directamente para administrar préstamos reales sin realizar mejoras de seguridad. Es necesario implementar almacenamiento seguro de contraseñas, proteger las sesiones y configurar adecuadamente el servidor antes de cualquier despliegue público.

## 12. Entrega académica

El repositorio de GitHub contiene el código fuente y la documentación necesaria para revisar el desarrollo del proyecto. Las instrucciones anteriores permiten instalar las dependencias y ejecutar la aplicación localmente para comprobar las funcionalidades implementadas.
