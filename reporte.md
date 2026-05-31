# Bug Bounty Report

## distributed-stock/order-service/db/session.py
Vulnerabilidad: Hardcoded secrets
Severidad: HIGH
Línea aproximada: 9

La línea `DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@order-db:5432/orders")` contiene una contraseña hardcoded (`password`) que se utiliza como valor predeterminado si la variable de entorno `DATABASE_URL` no está definida. Esto puede ser un riesgo para la seguridad, ya que una contraseña hardcoded puede ser descubierta por un atacante.

Sin embargo, es importante destacar que el código utiliza la biblioteca `dotenv` para cargar variables de entorno desde un archivo `.env`, lo que sugiere que la intención es que la variable `DATABASE_URL` sea configurada mediante este archivo. En este caso, la contraseña hardcoded solo se utilizaría si no se ha definido la variable `DATABASE_URL` en el archivo `.env`.

Para mitigar esta vulnerabilidad, se recomienda:

* Definir la variable `DATABASE_URL` en el archivo `.env` con una contraseña segura.
* Eliminar la contraseña hardcoded del código y utilizar una excepción o un mensaje de error si la variable `DATABASE_URL` no está definida.
* Considerar utilizar un sistema de gestión de secretos más robusto, como un gestor de configuración o un servicio de gestión de secretos en la nube.
## distributed-stock/payment-service/db/session.py
Vulnerabilidad: Hardcoded secrets
Severidad: HIGH
Línea aproximada: 9

La cadena de conexión a la base de datos incluye un usuario y una contraseña (`postgresql://user:password@payment-db:5432/payments`). Aunque se está utilizando `os.getenv` para intentar obtener el valor de `DATABASE_URL` desde una variable de entorno, si esa variable no está configurada, se utilizará el valor por defecto que incluye la contraseña en texto plano.

Para solucionar esto, se debería asegurar que la variable de entorno `DATABASE_URL` esté configurada con la cadena de conexión completa y segura, incluyendo el usuario y la contraseña, en un archivo `.env` o de otra manera segura, en lugar de depender del valor por defecto que contiene la contraseña. 

Además, la variable `DATABASE_URL` debería estar configurada de manera que sea única y exclusiva para cada entorno (desarrollo, producción, etc.) y no se compartan credenciales entre entornos.

Otra opción sería utilizar un gestor de secretos como Hashicorp's Vault o AWS Secrets Manager para almacenar y recuperar credenciales de manera segura.

Luego de corregir esto, si no se encuentran más vulnerabilidades, se puede considerar que el código es seguro.
## distributed-stock/payment-service/services/telemetry.py
Después de analizar el código proporcionado en el archivo `telemetry.py`, se ha encontrado una posible vulnerabilidad:

* Vulnerabilidad: Hardcoded secrets / Parámetros de configuración inseguros
* Severidad: MEDIUM
* Línea aproximada: 11-12

La vulnerabilidad se encuentra en la línea donde se configura el `OTLPSpanExporter`. El parámetro `insecure=True` indica que la conexión al endpoint de OpenTelemetry no utiliza un certificado SSL/TLS, lo que podría permitir a un atacante interceptar y leer los datos de telemetría que se envían.

Además, el endpoint se establece mediante una variable de entorno (`os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")`), lo que significa que si la variable de entorno no está configurada, se utilizará el valor por defecto `http://jaeger:4317`. Esto podría ser un problema si el servidor Jaeger no está configurado para aceptar conexiones inseguras o si no es el endpoint deseado.

Para abordar esta vulnerabilidad, se recomienda utilizar un certificado SSL/TLS válido para el endpoint de OpenTelemetry y configurar la conexión de manera segura. También es importante asegurarse de que la variable de entorno `OTEL_EXPORTER_OTLP_ENDPOINT` esté configurada con el valor correcto y seguro.

No se han encontrado otras vulnerabilidades como SQL injection, race conditions, command injection o path traversal en el código proporcionado.
## distributed-stock/payment-service/services/payment.py
Después de analizar el código, encontré algunas posibles vulnerabilidades de seguridad:

* Vulnerabilidad: SQL injection, Severidad: MEDIUM, Línea aproximada: 12-13
  El uso de `db.query` y `filter` no parece ser vulnerable a inyección SQL ya que se está utilizando un ORM (Object-Relational Mapping) como SQLAlchemy, que se encarga de parametrizar las consultas y evitar la inyección SQL. Sin embargo, si se utilizara una consulta SQL cruda en algún otro lugar del código, podría ser vulnerable a inyección SQL.

* Vulnerabilidad: No se encontraron hardcoded secrets.

* Vulnerabilidad: Race conditions, Severidad: MEDIUM, Línea aproximada: 12-13
  La función `charge` adquiere un bloqueo con `with_for_update()` para evitar que dos o más transacciones intenten cobrar del mismo cuenta al mismo tiempo. Sin embargo, la función `refund` no adquiere este bloqueo. Esto podría llevar a una condición de carrera si dos o más transacciones intentan reembolsar la misma cuenta al mismo tiempo.

* Vulnerabilidad: No se encontró command injection.

* Vulnerabilidad: No se encontró path traversal.

En resumen, el código parece tener algunas vulnerabilidades de seguridad, pero ninguna de ellas es crítica. La falta de bloqueo en la función `refund` podría llevar a problemas de concurrencia si no se maneja adecuadamente.
## distributed-stock/inventory-service/db/session.py
El código parece ser relativamente seguro, pero hay algunas preocupaciones potenciales:

* En la línea aproximada 10, se utiliza `os.getenv("DATABASE_URL", "postgresql://user:password@inventory-db:5432/inventory")`. La cadena de conexión a la base de datos tiene un usuario y contraseña hardcodeados (`user` y `password`). Esto es una:
 + Vulnerabilidad: Hardcoded secrets
 + Severidad: HIGH

Sin embargo, es importante destacar que si la variable de entorno `DATABASE_URL` está configurada, se utilizará esa URL en lugar de la cadena hardcodeada. Por lo tanto, si se configura correctamente la variable de entorno, la vulnerabilidad se mitiga.

Además, no se encontraron vulnerabilidades obvias de SQL injection, race conditions, command injection ni path traversal en el código proporcionado. 

Para mejorar la seguridad, se recomienda eliminar la cadena hardcodeada y utilizar solo la variable de entorno `DATABASE_URL`. También se puede considerar utilizar un sistema de manejo de secretos para almacenar y recuperar credenciales de base de datos de manera segura.
