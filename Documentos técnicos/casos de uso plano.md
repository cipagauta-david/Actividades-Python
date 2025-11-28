# **Catálogo de Casos de Uso del Sistema de Soporte Inteligente**

## **ID de Caso de Uso UC-01**

### **Nombre**
Enviar PQRS vía Formulario Web

### **Actor Primario**
Cliente

### **Actor Secundario(s)**
**Sistema** (Para invocar `UC-23: Crear Ticket`)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Asegurar que los datos de entrada estén validados y completos para facilitar el procesamiento automático y reducir el TTR.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Ofrecer un canal estructurado que guía al cliente a proporcionar la información clave desde el inicio, estandarizando la calidad del servicio.

### **Requisitos asociados**
**Funcionales:**
- **RF-TICKET-002:** Especifica la creación de un `Ticket` y `Mensaje` desde el formulario.
- **RF-TICKET-004:** Define la asociación o creación de un `Cliente`.
- **RF-TICKET-005:** Menciona la vinculación opcional a una `Orden` existente.
- **RF-TICKET-006:** Exige el envío de un acuse de recibo por correo.
- **RF-IA-001:** Indica que la creación del ticket debe iniciar el procesamiento de la IA.
**Interfaces:**
- **COM-01:** Toda la comunicación debe ser a través de HTTPS.

### **Descripción**
El Cliente, un usuario final de GearUp Gadgets, accede a un formulario público en el sitio web para enviar una solicitud de soporte. El cliente completa los campos requeridos, adjunta archivos opcionalmente y envía el formulario. El sistema valida los datos, crea un ticket y notifica al cliente que su solicitud ha sido recibida.

### **Precondición**
1. El Cliente tiene acceso a un navegador web y conexión a internet.
2. El Cliente conoce la URL de la página de soporte de GearUp Gadgets.

### **Secuencia Normal (Flujo Principal)**
1. El **Cliente** navega a la página de soporte y accede al formulario de contacto.
2. El **Sistema** presenta el formulario web con los siguientes campos: Nombre Completo (requerido), Email de Contacto (requerido, debe ser un formato de email válido), ID de Orden (opcional), Asunto (requerido), Mensaje (requerido), Adjuntar Archivo(s) (opcional).
3. El **Cliente** completa la información solicitada en el formulario.
4. El **Cliente** hace clic en el botón "Enviar Solicitud".
5. El **Sistema** realiza una validación de los datos en el navegador (client-side) para asegurar que los campos requeridos están completos y el formato del email es correcto.
6. El navegador del **Cliente** envía los datos del formulario de forma segura (vía HTTPS) al backend de NoraAI.
7. El **Sistema** recibe la solicitud e invoca el proceso interno **`UC-23: Crear Ticket`**. Este proceso se encarga de:
   1. Realizar una validación de seguridad y de negocio de los datos (server-side).
   2. Crear o encontrar el registro del `Cliente` basado en el email.
   3. Crear el registro del `Ticket` y el `Mensaje` inicial.
   4. Vincular el `Ticket` a una `Orden` si se proporcionó un ID de orden válido.
   5. Almacenar los archivos adjuntos (si los hay) y vincularlos al `Mensaje`.
8. Tras la creación exitosa del ticket, el **Sistema** dispara dos acciones en paralelo:
   1. Inicia el proceso en segundo plano para el análisis con IA (`RF-IA-001`).
   2. Envía un correo electrónico de acuse de recibo al **Cliente** (`RF-TICKET-006`).
9. El **Sistema** redirige al **Cliente** a una página de confirmación mostrando un mensaje de éxito: "¡Gracias! Hemos recibido tu solicitud. Tu número de ticket es [ID del Ticket]. Recibirás una confirmación en tu correo electrónico en breve."

### **Postcondición**
1. Se ha creado un nuevo registro de `Ticket` y `Mensaje` en la base de datos.
2. El `Ticket` está en el estado inicial `pendiente_ia`, listo para ser procesado.
3. Se ha enviado un correo de acuse de recibo a la dirección proporcionada por el cliente.
4. El cliente ve una página de confirmación en su navegador.

### **Excepciones (Flujos Alternativos)**
**E1: Falla la validación de datos.**
  - En el paso 5, el Cliente envía el formulario con datos inválidos (ej. email mal formado, campo requerido vacío).
  - El Sistema no envía la solicitud. En su lugar, resalta los campos con errores y muestra mensajes descriptivos junto a ellos (ej. "Por favor, introduce una dirección de correo válida."). Los datos que sí eran correctos se conservan en el formulario.
  **E2: Falla la comunicación con el servidor.**
  - En el paso 6, ocurre un error de red o el servidor no está disponible.
  - El Sistema muestra un mensaje de error genérico en la página del formulario: "Lo sentimos, no hemos podido procesar tu solicitud en este momento. Por favor, inténtalo de nuevo más tarde o contáctanos directamente por correo electrónico."
  **E3: Falla el proceso de creación del ticket.**
  - En el paso 7, el backend no puede crear el ticket por una razón interna (ej. error de base de datos).
  - El Sistema registra el error internamente para su auditoría y devuelve una respuesta de error al frontend.
  - El frontend muestra el mismo mensaje de error genérico descrito en E2.
  ### **Rendimiento**
La respuesta del sistema tras el envío del formulario (paso 9) debe mostrarse al cliente en **menos de 3 segundos** bajo condiciones de carga normales.

### **Frecuencia**
Media-Alta. Se anticipa que será un canal de entrada principal para nuevos clientes o para problemas no relacionados con una conversación de correo electrónico existente.

### **Comentarios**
- Es imperativo que el formulario esté protegido contra spam (ej. utilizando un CAPTCHA invisible o un honeypot) para evitar la creación masiva de tickets basura.
- La validación de datos debe existir tanto en el frontend (para una experiencia de usuario fluida) como en el backend (por seguridad y para garantizar la integridad de los datos).


## **ID de Caso de Uso UC-02**

### **Nombre**
Enviar PQRS vía Email

### **Actor Primario**
Cliente

### **Actor Secundario(s)**
**Sistema de Email (Mailgun)**, **Sistema** (Para invocar `UC-25: Notificar Nuevo Email`)

### **Objetivos asociados**
1. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Proveer un canal de soporte universal y de baja fricción.
2. **Optimizar la Eficiencia Operativa:** Traducir de forma fiable cada correo electrónico entrante en un ticket estructurado, automatizando la creación de tickets.

### **Requisitos asociados**
**Funcionales:**
- **RF-TICKET-001:** El sistema deberá crear un ticket al recibir una solicitud vía webhook de Mailgun.
- **RF-TICKET-003:** El sistema debe ser capaz de diferenciar un nuevo correo de una respuesta (este UC cubre el caso del nuevo correo).
- **RF-TICKET-004:** Se debe asociar cada ticket a un `Cliente`.
- **RF-TICKET-006:** El sistema debe enviar un correo de acuse de recibo.
- **RF-FILE-001:** El sistema debe procesar los archivos adjuntos.
**Interfaces:**
- **API-02:** El sistema debe exponer un endpoint de webhook para Mailgun.

### **Descripción**
El Cliente redacta y envía un correo electrónico (Petición, Queja, Reclamo o Sugerencia) a la dirección de soporte designada por GearUp Gadgets. Esta acción, externa a NoraAI, desencadena un proceso automático que recibe el correo, lo convierte en un nuevo ticket de soporte dentro del sistema y notifica al cliente que su solicitud ha sido registrada.

### **Precondición**
1. El Cliente conoce la dirección de correo electrónico de soporte (ej. `soporte@gearupgadgets.com`).
2. La infraestructura de recepción de correo del sistema (registros DNS MX, configuración de Mailgun, y el endpoint del webhook) está correctamente configurada y operativa.

### **Secuencia Normal (Flujo Principal)**
1. El **Cliente** utiliza su programa de correo preferido para redactar y enviar un email a la dirección de soporte. El email contiene un asunto, un cuerpo y, opcionalmente, archivos adjuntos. (Esta acción es externa al sistema NoraAI).
2. El **Proveedor de Email (Mailgun)** recibe el correo electrónico enviado por el cliente.
3. El **Proveedor de Email** invoca inmediatamente el webhook configurado en NoraAI (`API-02`), enviando una solicitud HTTP POST con el contenido completo del correo (remitente, destinatarios, asunto, cuerpo, adjuntos, etc.) en un formato JSON estructurado.
4. El **Sistema** recibe la solicitud en su endpoint de webhook e invoca el proceso **`UC-25: Notificar Nuevo Email`**.
5. El proceso `UC-25` analiza las cabeceras del correo y, al no encontrar un `In-Reply-To` o un ID de ticket de referencia, determina que se trata de una nueva solicitud.
6. El **Sistema** invoca el proceso **`UC-23: Crear Ticket`**, que se encarga de:
   1. Validar y limpiar los datos recibidos del webhook.
   2. Crear o encontrar el registro del `Cliente` basado en el email del remitente.
   3. Crear un nuevo `Ticket` y el `Mensaje` inicial a partir del cuerpo del correo.
   4. Procesar, almacenar y asociar los archivos adjuntos al `Mensaje`.
7. Tras la creación exitosa del ticket, el **Sistema** dispara dos acciones en paralelo:
   1. Inicia el proceso en segundo plano para el análisis con IA (`RF-IA-001`).
   2. Envía un correo electrónico de acuse de recibo al **Cliente**, incluyendo el ID único del nuevo ticket (`RF-TICKET-006`).
   ### **Postcondición**
1. Se ha creado un nuevo `Ticket` con su `Mensaje` inicial en la base de datos.
2. El `Ticket` se encuentra en el estado `pendiente_ia`.
3. Los archivos adjuntos, si los había, están almacenados y asociados al ticket.
4. El `Cliente` ha recibido un correo de confirmación con el número de su ticket.

### **Excepciones (Flujos Alternativos)**
**E1: El email es identificado como spam.**
  - En el paso 3, el Proveedor de Email marca el correo con una alta probabilidad de ser spam.
  - El Sistema recibe el webhook con esta información.
  - En lugar de crear un ticket normal, el sistema puede estar configurado para: a) descartarlo silenciosamente, o b) crearlo con un estado especial `spam` para revisión manual, evitando que entre en la cola de trabajo principal.
  **E2: Falla la entrega del webhook.**
  - El endpoint de NoraAI no está disponible cuando Mailgun intenta enviar la notificación.
  - Mailgun intentará reenviar el webhook varias veces según su política de reintentos.
  - Desde la perspectiva del cliente, habrá un retraso en recibir el acuse de recibo. Si el problema persiste, nunca lo recibirá. El sistema debe tener monitoreo sobre su endpoint para detectar estas fallas.
  **E3: Falla el procesamiento interno del ticket.**
  - En el paso 6, ocurre un error interno (ej. la base de datos está caída).
  - El Sistema debe registrar el error detallado para la depuración y responder al webhook con un código de error del servidor (ej. `5xx`). Esto le indica a Mailgun que la entrega falló y que debe reintentar más tarde.
  **E4: El email es una respuesta a un ticket existente.**
  - En el paso 5, el sistema detecta cabeceras como `In-Reply-To` o un ID de ticket en el asunto.
  - El flujo de ejecución se desvía al caso de uso **`UC-03: Responder a un Ticket (Correo) Existente`**, y no se crea un nuevo ticket.
  ### **Rendimiento**
El tiempo transcurrido desde que el sistema recibe el webhook (paso 4) hasta que el cliente recibe el correo de acuse de recibo (paso 7b) debe ser, en promedio, **inferior a 60 segundos**.

### **Frecuencia**
Muy Alta. Se espera que este sea el principal canal de entrada de solicitudes de soporte.

### **Comentarios**
- La fiabilidad de este flujo depende críticamente de la correcta configuración de los registros DNS (MX, SPF, DKIM) del dominio `gearupgadgets.com` para asegurar la correcta recepción y autenticidad de los correos.
- La lógica para diferenciar entre un nuevo correo y una respuesta (E4) es una de las reglas de negocio más importantes para evitar la duplicación de tickets.


## **ID de Caso de Uso UC-03**

### **Nombre**
Responder a un Ticket (Correo) Existente

### **Actor Primario**
Cliente

### **Actor Secundario(s)**
**Sistema de Email (Mailgun)**, **Sistema** (Para actualizar el `Ticket`)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Evitar la creación de tickets duplicados y reactivar casos en espera, manteniendo un flujo de trabajo limpio.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Asegurar la continuidad de la conversación en un único hilo, creando una interacción fácil de seguir.

### **Requisitos asociados**
**Funcionales:**
- **RF-TICKET-003:** Identificar si un correo entrante es una respuesta a un ticket existente y agregarlo como un `Mensaje` a ese ticket.
- **RF-FILE-001:** Procesar los archivos adjuntos en la respuesta.
**Interfaces:**
- **API-02:** Utiliza el mismo webhook de Mailgun que `UC-02` para recibir el correo.

### **Descripción**
Un Cliente responde a un correo electrónico que forma parte de una conversación de soporte existente (un ticket). El sistema debe ser capaz de identificar a qué ticket pertenece la respuesta y añadir el contenido del correo como un nuevo mensaje dentro de ese ticket, en lugar de crear uno nuevo.

### **Precondición**
1. Existe un `Ticket` en el sistema asociado al `Cliente`.
2. El Cliente ha recibido previamente al menos un correo electrónico del sistema relacionado con ese ticket (ej. el acuse de recibo o una respuesta de un agente).
3. El Cliente utiliza la función "Responder" de su cliente de correo.

### **Secuencia Normal (Flujo Principal)**
1. El **Cliente** responde a un correo electrónico del ticket. (Acción externa al sistema).
2. El **Proveedor de Email (Mailgun)** recibe el correo y, al igual que en `UC-02`, invoca el webhook de NoraAI (`API-02`) con los datos del email.
3. El **Sistema** recibe la solicitud en su endpoint de webhook e invoca el proceso **`UC-25: Notificar Nuevo Email`**.
4. El proceso `UC-25` analiza las cabeceras del correo. Detecta la presencia de una cabecera `In-Reply-To` o `References`, o un identificador de ticket (ej. `[TICKET-12345]`) en el asunto.
5. Usando esta información, el **Sistema** busca y encuentra el `Ticket` correspondiente en la base de datos.
6. El **Sistema** ejecuta las siguientes acciones:
   1. Crea un nuevo registro de `Mensaje` con el contenido del cuerpo del correo y lo asocia al `Ticket` encontrado.
   2. Procesa y almacena cualquier archivo adjunto, asociándolo al nuevo `Mensaje`.
   3. Actualiza el estado del `Ticket`. Típicamente, si el estado era `esperando_cliente`, lo cambia a `abierto` (o `pendiente_triaje` si se requiere nueva evaluación de la IA).
7. El **Sistema** notifica a los agentes suscritos (o al agente asignado) que el ticket ha recibido una nueva respuesta del cliente.

### **Postcondición**
1. No se ha creado ningún ticket nuevo.
2. Se ha añadido un nuevo `Mensaje` al historial del ticket existente.
3. El estado del ticket se ha actualizado para reflejar que requiere atención de un agente.
4. Los agentes pertinentes son notificados de la actualización.

### **Excepciones (Flujos Alternativos)**
**E1: El ID del ticket no se encuentra.**
  - El sistema extrae un ID de ticket del asunto o las cabeceras, pero no existe un ticket con ese ID en la base de datos (pudo ser un error de tipeo del cliente o un ticket muy antiguo y purgado).
  - En este caso, el sistema trata el correo como una nueva solicitud y procede con el flujo de `UC-02` para crear un nuevo ticket. Opcionalmente, puede enviar una notificación de error al cliente.
  **E2: El ticket está cerrado.**
  - El cliente responde a un ticket que ya tiene el estado `cerrado` o `resuelto`.
  - El sistema puede estar configurado para: a) reabrir automáticamente el ticket cambiando su estado a `abierto` y añadiendo el mensaje, o b) crear un nuevo ticket "de seguimiento", vinculándolo al ticket cerrado original. La opción 'a' suele ser la preferida para MVP.
  ### **Rendimiento**
El procesamiento del webhook y la actualización del ticket deben completarse en **menos de 5 segundos**.

### **Frecuencia**
Muy Alta. Es el flujo natural para cualquier conversación de soporte que requiera más de una interacción.

### **Comentarios**
- La robustez del parser para identificar el ID del ticket (tanto en cabeceras como en el asunto) es crucial para el funcionamiento de este caso de uso. El sistema debe ser tolerante a variaciones como "Re: [TICKET-123]" o "FWD: [TICKET-123]".
- La política sobre cómo manejar respuestas a tickets cerrados (E2) es una decisión de negocio importante que debe ser configurable.


## **ID de Caso de Uso UC-04**

### **Nombre**
Aprobar Respuesta Sugerida por la IA

### **Actor Primario**
Agente de Triaje

### **Actor Secundario(s)**
**Cliente** (Recibe el mensaje), **Sistema de Email (Mailgun)**

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Reducir drásticamente el Tiempo de Primera Respuesta (FRT) y el costo por contacto en consultas de alta frecuencia.
2. **Reducir el Desgaste del Agente (Agent Burnout):** Permitir que los agentes resuelvan un alto volumen de consultas comunes con un esfuerzo mínimo.
3. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Asegurar que las respuestas sigan un tono y una calidad estandarizados.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-001:** La UI de Triaje debe mostrar los tickets con estado `ia_sugerido`.
- **RF-AGENT-002:** La UI debe presentar la sugerencia de la IA de forma clara para su revisión.
- **RF-AGENT-003:** Un agente debe poder aprobar la sugerencia con un solo clic, lo cual debe enviar el correo y actualizar el estado del ticket.
**No Funcionales:**
- **NFR-PERF-003:** La acción de aprobación en 1-clic debe ser percibida como instantánea (< 2 segundos).
- **NFR-USAB-001:** La acción debe poder completarse con un solo clic.

### **Descripción**
El Agente de Triaje revisa la respuesta generada automáticamente por la IA para un ticket entrante. Si considera que la sugerencia es precisa y completa, la aprueba con un solo clic. Esta acción desencadena el envío de la respuesta al cliente y actualiza el estado del ticket, completando el ciclo de interacción para esa consulta.

### **Precondición**
1. El actor debe estar autenticado en el sistema y poseer el rol de `Agente de Triaje` o superior.
2. Existe un `Ticket` en el sistema con estado `ia_sugerido`.
3. La IA (`UC-24`) ya ha generado una propuesta de respuesta para dicho ticket.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente** selecciona un ticket de la cola de triaje en la UI (`UI-02`).
2. El **Sistema** muestra la vista de detalle del ticket, presentando el historial de la conversación a la izquierda y la respuesta sugerida por la IA a la derecha.
3. El **Agente** lee la sugerencia y la valida mentalmente, determinando que es correcta.
4. El **Agente** hace clic en el botón "Aprobar y Enviar".
5. El **Sistema** ejecuta las siguientes acciones en una única transacción:
   1. Crea un nuevo `Mensaje` de salida con el texto de la sugerencia, registrando al Agente como `aprobadoPorUsuarioId`.
   2. Envía un correo electrónico al `Cliente` con el contenido del mensaje.
   3. Actualiza el estado del `Ticket` a `esperando_cliente` o `cerrado`, según la recomendación de la IA.
   4. Registra un `LogEvento` de auditoría.
6. El **Sistema** refresca la interfaz, muestra una notificación de éxito ("Respuesta enviada correctamente") y retira el ticket de la cola de triaje del agente.

### **Postcondición**
1. Se ha enviado un correo electrónico con la respuesta al cliente.
2. Se ha guardado un nuevo `Mensaje` en el historial del ticket.
3. El estado del `Ticket` es `esperando_cliente` o `cerrado`.
4. El ticket ya no aparece en la cola de `ia_sugerido`.

### **Excepciones (Flujos Alternativos)**
**E1: Falla el servicio de envío de correos.**
  - En el paso 5b, el proveedor externo (Mailgun) devuelve un error.
  - El sistema anula la transacción (no se guarda el mensaje, no se cambia el estado).
  - El sistema muestra un mensaje de error al Agente: "No se pudo enviar el correo. Por favor, intente de nuevo."
  - El ticket permanece en estado `ia_sugerido`.
  **E2: El ticket fue modificado por otro proceso/agente.**
  - El Agente hace clic en "Aprobar", pero el estado del ticket en la base de datos ya no es `ia_sugerido`.
  - El sistema detecta la inconsistencia y bloquea la acción.
  - El sistema muestra un mensaje al Agente: "Este ticket ya ha sido actualizado. La página se refrescará." y actualiza la vista.
  ### **Rendimiento**
La operación completa, desde el clic del agente (paso 4) hasta la confirmación en la UI (paso 6), debe completarse en **menos de 2 segundos**.

### **Frecuencia**
Muy Alta. Se espera que sea el caso de uso más frecuente para el rol de `Agente de Triaje`.

### **Comentarios**
La simplicidad y velocidad de esta interacción es el principal generador de valor para la optimización del Nivel 1 de soporte. El diseño de la UI debe priorizar la claridad y la accesibilidad del botón de aprobación.


## **ID de Caso de Uso UC-05**

### **Nombre**
Editar y Enviar Respuesta Sugerida por la IA

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
**Cliente** (Recibe el mensaje), **Sistema de Email (Mailgun)**

### **Objetivos asociados**
1. **Mitigación de Riesgos Operativos:** Permitir la intervención humana para corregir errores, asegurando la calidad y precisión de toda la comunicación saliente.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Añadir personalización o mejorar el tono de la respuesta generada por la IA.
3. **Crear un Activo de Conocimiento Corporativo:** Utilizar cada edición como un dato valioso para retroalimentar y mejorar el sistema de IA.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-004:** Un agente de Nivel 1 debe poder editar el texto de la `respuestaSugeridaIA` antes de enviarlo.
- **RF-AGENT-002:** La UI debe presentar la sugerencia de forma clara para facilitar su revisión y edición.
- **RF-AGENT-003:** La acción de enviar desencadena la creación de un `Mensaje` y el cambio de estado del ticket.
**Interfaces:**
- **UI-02:** La vista de triaje debe contener un área de texto editable para la respuesta de la IA.

### **Descripción**
Un Agente de Triaje revisa un ticket con una respuesta sugerida por la IA. El agente considera que la sugerencia es mayormente correcta pero requiere ajustes. Modifica el texto directamente en la interfaz de usuario y luego lo envía al cliente. El sistema registra la respuesta como un mensaje manual (editado) y actualiza el estado del ticket.

### **Precondición**
1. El Agente está autenticado en el sistema.
2. Existe al menos un `Ticket` en la cola de triaje con el estado `ia_sugerido`.
3. El Agente ha seleccionado y está visualizando dicho ticket en la interfaz de triaje.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente de Triaje** selecciona un ticket de la lista en la "Vista de Triaje" (`UI-02`).
2. El **Sistema** muestra el historial de la conversación y, en un área de texto editable separada, la respuesta sugerida por la IA (`respuestaSugeridaIA`).
3. El **Agente** lee la sugerencia, identifica las partes que necesitan modificación y edita el texto directamente en el área de texto.
4. Una vez satisfecho con los cambios, el **Agente** hace clic en el botón "Enviar Respuesta".
5. El **Sistema** captura el contenido editado del área de texto.
6. El **Sistema** crea un nuevo registro de `Mensaje` asociado al `Ticket`, guardando el texto editado y marcando que fue enviado por el agente (no simplemente aprobado).
7. El **Sistema** invoca el servicio de correo (integración con Mailgun) para enviar el mensaje al cliente.
8. El **Sistema** actualiza el estado del `Ticket` al estado post-respuesta configurado (ej. `esperando_cliente` o `cerrado`).
9. El **Sistema** actualiza la interfaz de usuario, moviendo el mensaje enviado al historial de la conversación y eliminando el ticket de la cola de triaje activa.

### **Postcondición**
1. Se ha enviado un correo electrónico al cliente con el contenido modificado por el agente.
2. Se ha creado un nuevo registro de `Mensaje` en la base de datos.
3. El estado del `Ticket` ha sido actualizado.
4. El `Ticket` ya no aparece en la cola de triaje del agente.

### **Excepciones (Flujos Alternativos)**
**E1: El ticket es actualizado mientras el agente edita.**
  - Mientras el agente edita, el cliente envía un nuevo correo de respuesta.
  - El sistema detecta el cambio (ej. vía SSE). Antes de que el agente pueda enviar su respuesta, el sistema deshabilita el botón de envío y muestra una notificación: "El cliente ha enviado un nuevo mensaje. La conversación ha sido actualizada." La interfaz se refresca para mostrar el nuevo mensaje del cliente.
  **E2: Falla el envío del correo.**
  - En el paso 7, la API de Mailgun devuelve un error y el correo no puede ser enviado.
  - El sistema NO actualiza el estado del ticket y NO crea el registro del `Mensaje`.
  - El sistema muestra una notificación de error no invasiva al agente: "Error al enviar el correo. Por favor, inténtalo de nuevo." El agente puede reintentar la acción.
  ### **Rendimiento**
La confirmación de la acción en la UI (paso 9) debe ser percibida como instantánea, completándose en **menos de 2 segundos** tras el clic del agente.

### **Frecuencia**
Media. Se espera que sea menos frecuente que `UC-04` (Aprobar) a medida que la IA se optimiza, pero es un flujo de trabajo esencial para el control de calidad.

### **Comentarios**
Es crucial que el sistema diferencie entre un mensaje "aprobado" y uno "editado". Esta distinción es fundamental para las métricas de rendimiento de la IA y para los ciclos de retroalimentación.


## **ID de Caso de Uso UC-06**

### **Nombre**
Escalar Ticket a Nivel 2

### **Actor Primario**
Agente de Triaje

### **Actor Secundario(s)**
**Agente Especialista** (Recibe en la cola)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Asegurar que los tickets complejos sean manejados por el personal adecuado, optimizando el tiempo de todos los agentes y reduciendo el TTR.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Prevenir la frustración del cliente al evitar respuestas incorrectas de un agente sin el contexto necesario.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-005:** Un agente de Nivel 1 debe poder escalar un ticket, lo que cambia su estado a `escalado_nivel_2`.
- **RF-AGENT-008:** El sistema debe permitir dejar notas internas, lo cual es especialmente útil durante una escalada.
**Interfaces:**
- **UI-02:** La interfaz de triaje debe tener un botón o acción clara para "Escalar".
- **UI-03:** La interfaz de especialista debe mostrar los tickets que han sido escalados.

### **Descripción**
Un Agente de Triaje revisa un ticket y determina que la consulta es demasiado compleja para ser resuelta en el primer nivel de soporte o que la sugerencia de la IA es completamente inadecuada. El agente utiliza la acción "Escalar" para mover el ticket de la cola de triaje a la cola de especialistas de Nivel 2.

### **Precondición**
1. El Agente está autenticado en el sistema.
2. Existe al menos un `Ticket` en la cola de triaje con el estado `ia_sugerido`.
3. El Agente ha seleccionado y está visualizando dicho ticket en la interfaz.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente de Triaje** selecciona un ticket de la lista en la "Vista de Triaje".
2. El **Sistema** muestra el historial del ticket y la sugerencia de la IA.
3. El **Agente** evalúa el contenido y concluye que requiere conocimiento especializado (ej. es un problema técnico complejo, una queja sensible, etc.).
4. El **Agente** hace clic en el botón "Escalar".
5. El **Sistema** puede, opcionalmente, abrir una pequeña ventana modal para que el agente añada una nota interna para el equipo de Nivel 2 (ej. "Cliente muy molesto, requiere revisión de producto dañado").
6. El **Agente** añade la nota (o la deja en blanco) y confirma la escalada.
7. El **Sistema** actualiza el estado del `Ticket` a `escalado_nivel_2`.
8. Si se añadió una nota, el **Sistema** la guarda como una `NotaInterna` asociada al ticket.
9. El **Sistema** registra un evento en el log de auditoría del ticket indicando quién lo escaló y cuándo.
10. El **Sistema** elimina el ticket de la cola de triaje del agente y lo hace visible en la cola de Nivel 2 (`UI-03`).
11. El **Sistema** refresca la interfaz del agente para mostrar el siguiente ticket en la cola.

### **Postcondición**
1. El estado del `Ticket` es `escalado_nivel_2`.
2. El `Ticket` ya no es visible en la cola de triaje de Nivel 1.
3. El `Ticket` es ahora visible en la cola de trabajo de Nivel 2.
4. La acción de escalada ha quedado registrada en el historial del ticket.

### **Excepciones (Flujos Alternativos)**
**E1: Escalada accidental.**
  - El agente hace clic en "Escalar" por error.
  - La inclusión de un paso de confirmación (como en el paso 6) ayuda a mitigar este riesgo. Sin una confirmación, el agente necesitaría buscar el ticket y revertir la acción manualmente si tiene los permisos, o pedir a un supervisor que lo haga.
  ### **Rendimiento**
La acción de escalar un ticket y la actualización de la UI debe ser instantánea, completándose en **menos de 1 segundo**.

### **Frecuencia**
Baja a Media. En un sistema bien afinado, el escalado manual debería ser menos común que la aprobación o edición. Una alta frecuencia de escalado podría indicar que la IA no está bien calibrada o que las reglas de escalado automático (`RF-IA-005`) son insuficientes.

### **Comentarios**
La capacidad de dejar una nota interna durante la escalada (`RF-AGENT-008`) es una funcionalidad de alto valor. Acelera drásticamente el trabajo del agente de Nivel 2, ya que le proporciona un resumen del análisis del agente de Nivel 1.


## **ID de Caso de Uso UC-07**

### **Nombre**
Gestionar Etiquetas del Ticket

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
**Agente de Triaje** (Visualiza las etiquetas)

### **Objetivos asociados**
1. **Generar Inteligencia de Negocio:** Crear metadatos estructurados que permitan generar informes, identificar tendencias y encontrar tickets específicos rápidamente.
2. **Identificar Patrones de Falla de Producto y Servicio:** Facilitar la detección de problemas recurrentes a través de la categorización.
3. **Optimizar la Eficiencia Operativa:** Ofrecer a otros agentes un contexto rápido del ticket sin necesidad de leer toda la conversación.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-006:** Implícito en la gestión de tickets de Nivel 2.
- **RF-ADMIN-001:** Depende de la gestión de usuarios y roles para asegurar que solo los agentes autorizados puedan realizar la acción.
**Interfaces:**
- **UI-03:** La interfaz de especialista debe incluir un componente para la gestión de etiquetas dentro de la vista de un ticket.

### **Descripción**
Mientras un agente revisa un ticket, puede añadir o eliminar etiquetas de una lista predefinida por el administrador. Esta acción actualiza los metadatos del ticket en tiempo real, mejorando su clasificación y visibilidad sin afectar el flujo de la conversación con el cliente.

### **Precondición**
1. El Agente está autenticado en el sistema.
2. El Agente está visualizando la página de detalles de un ticket específico.
3. Existe un catálogo maestro de `Etiqueta`s en el sistema, gestionado previamente por un `Administrador` (ver `UC-17`).

### **Secuencia Normal (Flujo Principal)**
1. El **Agente** se encuentra en la vista de detalle de un ticket.
2. El **Agente** localiza la sección de "Etiquetas" en la interfaz de usuario, que muestra las etiquetas actualmente asociadas.
3. El **Agente** hace clic en el botón o control para "Editar Etiquetas".
4. El **Sistema** presenta una interfaz interactiva (ej. un campo de búsqueda con autocompletado o una lista de selección múltiple) que muestra las etiquetas disponibles del catálogo maestro.
5. El **Agente** selecciona una o más etiquetas para añadir al ticket.
6. El **Agente** desmarca o elimina una o más etiquetas que ya estaban asociadas.
7. El **Agente** confirma la acción (ya sea mediante un botón "Guardar" o la acción se ejecuta automáticamente al seleccionar/deseleccionar).
8. El **Sistema** envía una solicitud al backend para actualizar las asociaciones de etiquetas para ese ticket.
9. El **Sistema** actualiza la base de datos y refresca la sección de "Etiquetas" en la UI para reflejar los cambios, sin necesidad de recargar la página.

### **Postcondición**
1. La relación entre el `Ticket` y las `Etiqueta`s se ha actualizado en la base de datos.
2. El cambio es inmediatamente visible en la interfaz del ticket para todos los agentes.

### **Excepciones (Flujos Alternativos)**
**E1: Falla la comunicación con el servidor.**
  - En el paso 8, la solicitud para actualizar las etiquetas no llega al servidor o devuelve un error.
  - El **Sistema** no actualiza la vista de etiquetas de forma permanente. Muestra una notificación de error temporal (ej. "No se pudieron guardar las etiquetas. Inténtalo de nuevo.") y revierte la selección en la UI al estado previo.
  ### **Rendimiento**
La acción de añadir o quitar una etiqueta debe reflejarse en la interfaz de usuario en **menos de 500 milisegundos**. La carga de la lista de etiquetas disponibles debe ser casi instantánea.

### **Frecuencia**
Alta. Se espera que los agentes ajusten las etiquetas de la mayoría de los tickets que gestionan para mantener una buena organización.

### **Comentarios**
- Para mantener la consistencia de los datos, los agentes solo pueden seleccionar de la lista maestra. La creación de nuevas etiquetas es una función reservada para el `Administrador` (`UC-17`).
- La interfaz de selección de etiquetas debe ser eficiente, especialmente si el catálogo de etiquetas es grande (ej. con una función de búsqueda).


## **ID de Caso de Uso UC-08**

### **Nombre**
Resolver Ticket

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
**Cliente** (Recibe el mensaje de cierre y CSAT)

### **Objetivos asociados**
1. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Proporcionar una solución final y clara al problema del cliente para aumentar el CSAT.
2. **Optimizar la Eficiencia Operativa:** Cerrar el ciclo de soporte, actualizando el estado del ticket para sacarlo de las colas de trabajo activas y contribuir a la métrica de FCR.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-006:** Visualizar la cola de tickets asignados.
- **RF-AGENT-007:** Utilizar plantillas de respuesta.
- **RF-AGENT-008:** Dejar notas internas.
- **RF-FILE-002:** Adjuntar archivos.
- **RF-TICKET-007:** Enviar encuesta CSAT post-resolución.
**Interfaces:**
- **UI-03:** La interfaz del especialista debe proveer todas las herramientas para la investigación y comunicación.

### **Descripción**
Un Agente Especialista se asigna o selecciona un ticket escalado. El agente investiga el caso utilizando la información disponible, se comunica con el cliente a través de mensajes y, una vez que el problema está solucionado, realiza la acción final de cerrar el ticket, lo que actualiza su estado y puede desencadenar acciones posteriores como el envío de una encuesta de satisfacción.

### **Precondición**
1. El Agente está autenticado en el sistema.
2. Existe un ticket en un estado que requiere intervención manual (ej. `escalado_nivel_2` o `esperando_agente`).
3. El ticket está asignado al agente o se encuentra en una cola a la que el agente tiene acceso.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente** accede a su panel de control y selecciona un ticket de su cola de trabajo.
2. El **Sistema** carga la vista de detalle del ticket, mostrando el historial completo de la conversación, datos del cliente, historial de órdenes (`UC-09`), notas internas y cualquier otra información contextual.
3. El **Agente** investiga el problema. Este es un paso manual que puede requerir consultar sistemas externos.
4. El **Agente** redacta una respuesta para el cliente. Puede escribir un mensaje desde cero, insertar una `Plantilla` (`RF-AGENT-007`), o adjuntar archivos (`RF-FILE-002`).
5. El **Agente** envía el mensaje. El **Sistema** lo guarda, lo envía por correo al cliente y actualiza el estado del ticket a `esperando_cliente`.
6. Si el cliente responde, el ticket vuelve al estado `esperando_agente` y notifica al Agente. Los pasos 3-5 pueden repetirse varias veces.
7. Una vez que el **Agente** considera que el problema está resuelto y ha enviado la comunicación final, localiza y activa la acción "Resolver Ticket".
8. El **Sistema** puede presentar un diálogo de confirmación, solicitando opcionalmente una nota de cierre interna.
9. El **Agente** confirma la acción.
10. El **Sistema** actualiza el estado del ticket a `cerrado` (o `resuelto`).
11. El **Sistema** ejecuta cualquier automatización post-resolución, como iniciar el envío de la encuesta de satisfacción (`RF-TICKET-007`).

### **Postcondición**
1. El estado del `Ticket` se actualiza a `cerrado` en la base de datos.
2. El ticket ya no aparece en las colas de trabajo activas.
3. Se ha preservado todo el historial de la conversación, incluyendo el mensaje final.
4. Se ha podido iniciar un flujo de trabajo de encuesta de satisfacción.

### **Excepciones (Flujos Alternativos)**
**E1: El cliente reabre el ticket.**
  - Después de que el ticket ha sido marcado como `cerrado`, el cliente responde al último correo.
  - El **Sistema** detecta esta respuesta (`UC-03`), cambia el estado del ticket de `cerrado` a `reabierto` o `esperando_agente`, y lo vuelve a asignar al último agente que lo gestionó, notificándole la novedad.
  **E2: Falla el envío de un mensaje.**
  - En el paso 5, el sistema no puede enviar el correo al cliente (ej. por un fallo en la API de Mailgun).
  - El **Sistema** no debe cambiar el estado del ticket. Debe preservar el borrador del mensaje del agente y mostrar un mensaje de error claro, permitiendo al agente reintentar el envío.
  **E3: Se requiere la intervención de otro especialista.**
  - Durante la investigación (paso 3), el agente determina que no es la persona adecuada para resolver el caso.
  - El agente invoca el caso de uso **`UC-19: Reasignar Ticket Manualmente`** para transferirlo a otro colega. El caso de uso actual (`UC-08`) termina para este agente.
  ### **Rendimiento**
El envío de un mensaje y la actualización del estado del ticket deben completarse y confirmarse en la UI en **menos de 3 segundos**. Cargar la vista de un ticket con un historial extenso no debe superar los 4 segundos.

### **Frecuencia**
Muy Alta. Esta es la actividad principal y el ciclo de vida completo de la mayoría de los tickets manejados por agentes de Nivel 2.

### **Comentarios**
- Este caso de uso es compuesto y abarca varias interacciones más pequeñas. Su éxito depende de una interfaz que presente toda la información contextual de forma clara para minimizar el tiempo de investigación del agente.
- Las políticas de SLA (`RF-AGENT-009`) son cruciales aquí; la interfaz debe resaltar los tickets que se acercan a su vencimiento para ayudar al agente a priorizar su trabajo.


## **ID de Caso de Uso UC-09**

### **Nombre**
Consultar Historial del Cliente

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
Agente triaje

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Acelerar la resolución al centralizar toda la información relevante en una única vista, reduciendo el TTR.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Permitir un servicio más personalizado y proactivo, demostrando que se conoce el historial del cliente.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-009:** (Implícito) La capacidad de consultar el historial es un prerrequisito para un flujo de trabajo de agente eficiente.
- **RF-DATA-001:** Depende de que los datos de `Orden` hayan sido importados previamente.
**Interfaces:**
- **UI-02 / UI-03:** La vista del historial es un componente fundamental de la interfaz de gestión de tickets.

### **Descripción**
Mientras un Agente trabaja en un ticket activo, necesita comprender el historial completo del cliente para ofrecer una solución informada. El Agente accede a una vista unificada que consolida tanto el historial de tickets de soporte previos (abiertos y cerrados) como el historial de órdenes de compra del cliente.

### **Precondición**
1. El Agente está autenticado en el sistema.
2. El Agente tiene asignado o ha abierto un `Ticket` de un `Cliente` específico.
3. Los datos de las `Orden`es del cliente han sido previamente importados y están disponibles en la base de datos de NoraAI.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente** está en la vista de detalle de un ticket activo.
2. El **Agente** hace clic en el nombre del cliente o en un botón/enlace específico como "Ver Historial del Cliente".
3. El **Sistema** recupera de la base de datos toda la información asociada al `id` del cliente del ticket actual, incluyendo:
   1. Todos los demás `Ticket`s asociados a ese cliente.
   2. Todas las `Orden`es asociadas a ese cliente.
4. El **Sistema** presenta una "Vista de Perfil de Cliente" unificada, organizada y fácil de consultar. Esta vista contiene como mínimo dos secciones principales:
   1. **Sección de Historial de Soporte:** Una lista cronológica inversa (del más reciente al más antiguo) de todos los tickets del cliente. Cada elemento de la lista muestra información clave de un vistazo: ID del Ticket, Asunto, Fecha de Creación y Estado Actual (`abierto`, `cerrado`, `escalado`, etc.).
   2. **Sección de Historial de Órdenes:** Una lista cronológica inversa de todas las órdenes del cliente. Cada elemento muestra: ID de la Orden, Fecha de Compra, Estado de la Orden (`enviado`, `entregado`, `devuelto`) y el Monto Total.
5. El **Agente** puede interactuar con esta vista para obtener más detalles:
   1. Al hacer clic en un ticket del historial, el **Sistema** podría mostrar un resumen o abrir el historial completo de esa conversación en un modal o panel lateral.
   2. Al hacer clic en una orden, el **Sistema** muestra los detalles completos de la misma, incluyendo los productos comprados y la dirección de envío.
6. El **Agente** utiliza la información obtenida para formular una respuesta más precisa y contextualizada en el ticket activo.

### **Postcondición**
1. El Agente ha obtenido el contexto necesario sobre el cliente.
2. El estado del ticket activo y del sistema no ha cambiado (es una operación de solo lectura).
3. El Agente regresa a la vista del ticket activo para continuar con su trabajo.

### **Excepciones (Flujos Alternativos)**
**E1: Cliente sin historial previo.**
  - En el paso 3, el sistema no encuentra tickets ni órdenes previas para este cliente.
  - En el paso 4, la Vista de Perfil de Cliente muestra mensajes claros en cada sección, como "Este es el primer ticket de este cliente" y "No se encontraron órdenes para este cliente".
  **E2: Los datos de órdenes no están actualizados.**
  - El cliente menciona una orden reciente que no aparece en el historial.
  - La interfaz podría mostrar una marca de tiempo como "Datos de órdenes actualizados por última vez el [fecha/hora]" para que el agente sea consciente de la posible obsolescencia de los datos. El Agente debe proceder sabiendo que la información puede no ser completa.
  ### **Rendimiento**
La carga de la Vista de Perfil de Cliente (paso 4) debe completarse en **menos de 2 segundos** para un cliente con un historial considerable (ej. 50 tickets y 100 órdenes).

### **Frecuencia**
Alta. Se espera que los agentes consulten el historial en la mayoría de los tickets que no sean triviales.

### **Comentarios**
- El diseño de la "Vista de Perfil de Cliente" es crucial para la usabilidad. Debe priorizar la información más relevante y permitir una fácil navegación entre el historial y el ticket activo.
- Esta funcionalidad es uno de los mayores diferenciadores de valor para el agente, ya que combate directamente la frustración de recibir tickets sin contexto.


## **ID de Caso de Uso UC-10**

### **Nombre**
Adjuntar y Descargar Archivos

### **Actor Primario**
Agente Especialista (Descargar y Adjuntar), Cliente (Adjuntar vía email)

### **Actor Secundario(s)**
**Supabase Storage**

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Facilitar el intercambio de evidencia crucial (fotos, facturas) para acelerar el diagnóstico y la resolución.
2. **Mitigación de Riesgos Operativos:** Asegurar que todos los artefactos de un caso se almacenen de forma centralizada, completa y segura.

### **Requisitos asociados**
**Funcionales:**
- **RF-FILE-001:** El sistema debe procesar archivos adjuntos de correos entrantes.
- **RF-FILE-002:** Los adjuntos deben almacenarse de forma segura en Supabase Storage.
- **RF-IA-005:** (Relacionado) La presencia de un adjunto de imagen puede ser una condición para la escalada automática.
**Interfaces:**
- **API-05:** El sistema debe usar la API de Supabase Storage.

### **Descripción**
Este caso de uso cubre el ciclo de vida completo de los archivos adjuntos. Describe cómo un agente puede visualizar y descargar archivos enviados por un cliente, y cómo puede adjuntar sus propios archivos al enviar una respuesta.

### **Precondición**
1. El Agente está autenticado en el sistema y tiene un ticket abierto.
2. Para descargar: El ticket contiene al menos un archivo adjunto enviado previamente por el cliente.
3. Para adjuntar: El Agente está redactando una respuesta para el cliente.

### **Secuencia Normal (Flujo Principal)**
**Flujo A: Agente Visualiza y Descarga un Archivo del Cliente**
1. El **Sistema**, a través del proceso `UC-02`, ha recibido un email de un cliente con uno o más archivos adjuntos.
2. En la vista de detalle del ticket, el **Sistema** muestra los mensajes de la conversación. En el mensaje del cliente que contenía los adjuntos, se muestran representaciones visuales de los mismos (ej. un icono de archivo, el nombre del archivo, su tamaño y una miniatura si es una imagen).
3. El **Agente** hace clic en el nombre o la miniatura del archivo que desea ver.
4. El **Sistema** genera una URL de acceso segura y temporal desde Supabase Storage (`API-05`).
5. El navegador del **Agente** abre una nueva pestaña para mostrar el archivo (si es un formato soportado como PDF o imagen) o inicia directamente el proceso de descarga estándar del navegador.
**Flujo B: Agente Adjunta un Archivo a una Respuesta**
1. Mientras redacta una respuesta en la interfaz del ticket, el **Agente** hace clic en el botón "Adjuntar Archivo" (o arrastra y suelta un archivo en el área de respuesta).
2. El **Sistema** abre el selector de archivos del sistema operativo del Agente.
3. El **Agente** selecciona uno o más archivos para adjuntar.
4. El **Sistema** valida los archivos seleccionados en el frontend (tamaño máximo, tipo de archivo permitido).
5. Una vez validados, el **Sistema** sube los archivos de forma segura a Supabase Storage (`API-05`). Mientras se suben, la UI muestra un indicador de progreso.
6. Una vez completada la subida, el **Sistema** recibe las URLs de los archivos almacenados. La UI muestra los archivos adjuntados debajo del área de texto de la respuesta.
7. El **Agente** termina de redactar su mensaje y hace clic en "Enviar".
8. El **Sistema** crea el registro del `Mensaje` en la base de datos, lo asocia con los registros de los `Archivo`s recién subidos y envía el correo al cliente a través de Mailgun, incluyendo los archivos como adjuntos de correo estándar.

### **Postcondición**
**Flujo A (Descargar):**
- El Agente tiene una copia local del archivo del cliente. El estado del sistema no cambia.
**Flujo B (Adjuntar):**
- Se han creado uno o más registros en la tabla `Archivo`.
- Los archivos físicos están almacenados en Supabase Storage.
- Se ha enviado un correo al cliente con los archivos adjuntos.

### **Excepciones (Flujos Alternativos)**
**E1: El tipo de archivo no está permitido.**
  - En el Flujo B, paso 4, el Agente intenta subir un archivo con una extensión no permitida (ej. `.exe`).
  - La UI muestra un mensaje de error inmediato: "Tipo de archivo no permitido. Solo se aceptan [lista de tipos]". La subida se cancela.
  **E2: El archivo excede el tamaño máximo.**
  - En el Flujo B, paso 4, el Agente intenta subir un archivo más grande que el límite configurado (ej. 10 MB).
  - La UI muestra un mensaje de error: "El archivo es demasiado grande. El tamaño máximo es de 10 MB." La subida se cancela.
  **E3: Falla la subida del archivo.**
  - En el Flujo B, paso 5, ocurre un error de red o un problema con el servicio de almacenamiento.
  - La UI muestra un mensaje de error claro junto al archivo que falló, con una opción para reintentar la subida.
  **E4: Se detecta un virus en el archivo (Requisito de Seguridad Implícito).**
  - Durante la subida (Flujo B, paso 5) o al procesar un adjunto entrante (Flujo A, paso 1), un escáner de virus integrado detecta que el archivo es malicioso.
  - El **Sistema** rechaza el archivo, lo pone en cuarentena o lo elimina. Se registra un evento de seguridad. La UI informa al Agente que el archivo fue bloqueado por razones de seguridad.
  ### **Seguridad**
- **Control de Acceso:** Las URLs de los archivos en Supabase Storage deben ser firmadas y de corta duración para prevenir el acceso no autorizado.
- **Validación de Tipos:** Se debe mantener una lista blanca estricta de tipos de archivo permitidos (MIME types), tanto en el frontend como en el backend.
- **Escaneo de Malware:** Es altamente recomendable integrar un servicio de escaneo de virus para todos los archivos subidos.

### **Frecuencia**
Media. Es una función esencial, pero no se utiliza en todos los tickets.

### **Comentarios**
- La experiencia de usuario para la subida de archivos debe ser fluida, implementando "arrastrar y soltar" (drag-and-drop) y mostrando indicadores de progreso claros.
- Este caso de uso impacta directamente la lógica de negocio (`RF-IA-005`), ya que la detección de imágenes es un disparador para la escalada automática. El sistema debe tratar el procesamiento de adjuntos como un evento significativo.
- Parámetros como el **tamaño máximo por archivo** y la **lista blanca de tipos MIME permitidos** deben ser variables de configuración del sistema, no valores codificados (`hardcoded`), para facilitar su mantenimiento.
- Se debe definir una política de retención de datos para los archivos almacenados, considerando costos de almacenamiento a largo plazo y normativas de privacidad.


## **ID de Caso de Uso UC-11**

### **Nombre**
Añadir Nota Interna al Ticket

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
**Agente de Triaje** (Visualiza la nota)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Permitir que los agentes colaboren y compartan contexto crítico sobre un caso sin exponerlo al cliente, agilizando las transferencias o escalados.
2. **Mitigación de Riesgos Operativos:** Mantener un historial interno completo de decisiones y observaciones para futura referencia y auditoría.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-008:** El sistema deberá permitir a los agentes dejar notas internas y @mencionar a otros agentes.
- **RF-SUPERVISOR-002:** Las notas deben ser visibles en el historial completo revisado por supervisores.

### **Descripción**
Un agente añade un comentario privado a un ticket. Este comentario es estrictamente para uso interno y nunca es visible para el cliente final. Puede incluir texto enriquecido y menciones a otros usuarios del sistema para solicitar su ayuda o informarles.

### **Precondición**
1. El Agente ha iniciado sesión y tiene permisos de acceso al ticket en cuestión.
2. El Agente se encuentra visualizando la vista detallada del ticket.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente** selecciona la opción "Añadir Nota Interna" en la interfaz del ticket (diferenciada claramente de la opción "Responder al Cliente").
2. El **Sistema** muestra un área de texto dedicada para la nota, con un indicador visual claro (ej. fondo amarillo o icono de candado) de que es contenido privado.
3. El **Agente** redacta el contenido de la nota.
  *   *(Opcional)* El agente escribe "@" seguido del nombre de otro agente. El sistema sugiere usuarios y el agente selecciona uno para mencionarlo.
4. El **Agente** confirma la acción haciendo clic en "Guardar Nota".
5. El **Sistema** valida el contenido (no vacío) y lo guarda en la base de datos asociado al ticket y al agente autor.
6. El **Sistema** actualiza la línea de tiempo del ticket en tiempo real, mostrando la nueva nota con un estilo visual distintivo que la diferencia de los mensajes públicos.
7. *(Si hubo menciones)* El **Sistema** envía una notificación interna (in-app o email, según configuración) al agente mencionado.

### **Postcondición**
1. La nota interna queda registrada permanentemente en el historial del ticket.
2. La nota es visible solo para usuarios con rol de Agente o superior.
3. Los usuarios mencionados han recibido una notificación.

### **Excepciones (Flujos Alternativos)**
**E1: Intento de guardar una nota vacía.**
  - El Agente intenta guardar sin haber escrito texto.
  - El Sistema deshabilita el botón de guardar o muestra un mensaje de error indicando que el contenido es requerido.
  **E2: Falla al guardar la nota.**
  - Ocurre un error de red o servidor al intentar persistir la nota.
  - El Sistema muestra un mensaje de error ("No se pudo guardar la nota. Reintentando...") y permite al agente intentar de nuevo sin perder el texto escrito.
  ### **Frecuencia**
Alta. Utilizado frecuentemente en tickets complejos (`escalado_nivel_2`) o que requieren seguimiento a largo plazo.

### **Comentarios**
- Es crítico que la UI diferencie inequívocamente entre "Nota Interna" y "Respuesta Pública" para evitar que información sensible sea enviada accidentalmente al cliente.
- Las notas internas no deberían cambiar el estado del ticket (ej. de `cerrado` a `abierto`) a menos que se configure específicamente una regla para ello.


## **ID de Caso de Uso UC-12**

### **Nombre**
Gestionar Configuración de Agente IA

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Proveedor LLM (OpenRouter)**, **Agente de Triaje** (Afectado por los cambios)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Ajustar los prompts y parámetros del LLM para mejorar la precisión y balancear el costo y la calidad de las respuestas.
2. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Refinar el tono y la adherencia a las políticas de la empresa en las respuestas sugeridas.
3. **Mitigación de Riesgos Operativos:** Controlar el comportamiento de la IA y definir los umbrales de confianza para acciones automáticas.

### **Requisitos asociados**
**Funcionales:**
- **RF-ADMIN-002:** Un administrador debe poder gestionar y auditar cambios en `ConfigAgente`.
- **RF-IA-002:** El sistema debe usar estas configuraciones para generar las propuestas.

### **Descripción**
El Administrador crea, lee, actualiza o elimina (CRUD) registros de la entidad `ConfigAgente`. Estos registros actúan como "perfiles" que definen cómo se comporta la IA ante diferentes tipos de tickets (ej. un perfil para "Devoluciones", otro para "Envíos").

### **Precondición**
1. El Administrador ha iniciado sesión con una cuenta que posee privilegios de superusuario.
2. Existe al menos un proveedor de LLM configurado en el sistema.

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección de "Configuración de IA" en el panel de administración.
2. El **Sistema** muestra una lista de las configuraciones existentes (ej. "Agente General", "Especialista en RMA", "Detector de Spam").
3. El **Administrador** selecciona una configuración para editar o hace clic en "Crear Nueva Configuración".
4. El **Sistema** presenta el formulario de edición con los siguientes campos clave:
  - `Nombre/Tipo`: Identificador del perfil (ej. "wismo_agent").
  - `Prompt del Sistema`: El texto base que instruye al LLM sobre su rol y reglas.
  - `Modelo`: Selector del modelo LLM a usar (ej. GPT-4o, Claude 3.5 Sonnet).
  - `Temperatura`: Valor numérico (0.0 - 1.0) para controlar la creatividad.
  - `Umbral de Confianza`: Valor mínimo (0.0 - 1.0) para considerar una sugerencia como válida.
5. El **Administrador** modifica los parámetros deseados.
6. El **Administrador** guarda los cambios.
7. El **Sistema** valida que los valores numéricos estén en rangos permitidos y que el prompt no esté vacío.
8. El **Sistema** guarda la nueva versión de la configuración y registra el evento en el log de auditoría para trazabilidad.

### **Postcondición**
1. La configuración es actualizada en la base de datos.
2. Todos los *nuevos* tickets procesados a partir de este momento utilizarán los parámetros actualizados.
3. Se genera un registro de auditoría indicando quién hizo el cambio y cuándo.

### **Excepciones (Flujos Alternativos)**
**E1: Validación de parámetros fallida.**
  - El Administrador introduce una temperatura fuera de rango (ej. 1.5) o deja el prompt en blanco.
  - El Sistema impide guardar y muestra un error específico junto al campo inválido.
  **E2: Eliminación de una configuración en uso.**
  - El Administrador intenta borrar una configuración que es la predeterminada del sistema.
  - El Sistema bloquea la eliminación y muestra una advertencia: "No se puede eliminar la configuración activa predeterminada. Asigne otra como predeterminada primero."
  ### **Frecuencia**
Baja. Se realiza esporádicamente cuando se detecta la necesidad de mejorar el rendimiento de la IA o cambian las políticas de negocio.

### **Comentarios**
- Los cambios en estos prompts tienen un alto impacto en la operación. Se recomienda (para versiones futuras) implementar un sistema de "versiones de prompt" y un entorno de "sandbox" para probar los cambios antes de aplicarlos a producción.
- Es vital guardar un historial de cambios (quién cambió qué y cuándo) para poder revertir rápidamente si una nueva configuración causa problemas graves en las respuestas automáticas.


## **ID de Caso de Uso UC-13**

### **Nombre**
Gestionar Plantillas de Respuesta

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Agente Especialista/Triaje** (Utiliza las plantillas)

### **Objetivos asociados**
1. **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Asegurar que las respuestas para consultas comunes sean consistentes en tono, formato y precisión.
2. **Optimizar la Eficiencia Operativa:** Acelerar los tiempos de respuesta al proveer a los agentes respuestas pre-aprobadas.
3. **Acelerar la Formación de Nuevos Agentes (Onboarding):** Permitir que los nuevos agentes se apoyen en plantillas validadas mientras aprenden los procedimientos.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-007:** El sistema debe permitir a los agentes utilizar y gestionar plantillas de respuesta. (Este UC se enfoca en la parte de "gestionar", que es una función administrativa para mantener el control de calidad).
**No Funcionales:**
- **NFR-USAB-001 (implícito):** La interfaz para crear y editar plantillas debe ser intuitiva y fácil de usar para un rol administrativo.

### **Descripción**
El Administrador del sistema accede a una interfaz de configuración para realizar operaciones de creación, lectura, actualización y eliminación (CRUD) sobre el catálogo de plantillas de respuesta. Estas plantillas son fragmentos de texto reutilizables que los agentes pueden invocar y personalizar al responder a un ticket. El sistema debe soportar el uso de variables dinámicas (placeholders) para personalizar automáticamente las plantillas con datos del ticket o del cliente.

### **Precondición**
1. El usuario está autenticado en el sistema y posee el rol de `Administrador`.

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección "Configuración" > "Plantillas" de la aplicación.
2. El **Sistema** muestra una lista de todas las plantillas existentes, mostrando su nombre/título y un extracto del contenido.
3. El **Administrador** inicia una de las siguientes acciones:
  **a) Para Crear una nueva plantilla:**
    i. Hace clic en el botón "Nueva Plantilla".
    ii. El **Sistema** presenta un formulario con los campos: `Nombre` (un identificador corto y descriptivo), `Contenido` (un editor de texto enriquecido o simple), y una lista de `Variables Disponibles` (ej. `{{cliente.nombre}}`, `{{ticket.id}}`, `{{agente.nombre}}`).
    iii. El **Administrador** completa el nombre y redacta el contenido, insertando las variables necesarias.
    iv. El **Administrador** guarda la plantilla.
    v. El **Sistema** valida que el nombre y el contenido no estén vacíos, guarda la nueva plantilla en la base de datos y actualiza la lista.
  **b) Para Modificar una plantilla existente:**
    i. Busca la plantilla en la lista y hace clic en el botón "Editar".
    ii. El **Sistema** carga los datos de la plantilla en el mismo formulario de creación.
    iii. El **Administrador** realiza los cambios necesarios y guarda.
    iv. El **Sistema** valida y actualiza el registro en la base de datos.
  **c) Para Eliminar una plantilla:**
    i. Busca la plantilla en la lista y hace clic en el botón "Eliminar".
    ii. El **Sistema** muestra un cuadro de diálogo de confirmación para prevenir la eliminación accidental.
    iii. El **Administrador** confirma la acción.
    iv. El **Sistema** elimina el registro de la base de datos y actualiza la lista.
    ### **Postcondición**
1. El catálogo de plantillas disponible para los agentes está actualizado (creado, modificado o eliminado) y los cambios se reflejan de inmediato para su uso en la resolución de tickets.

### **Excepciones (Flujos Alternativos)**
**E1: Falla la validación de datos.**
  - En los pasos 3.a.v o 3.b.iv, el Administrador intenta guardar una plantilla con el campo `Nombre` o `Contenido` vacío.
  - El **Sistema** no guarda los cambios, muestra un mensaje de error descriptivo junto al campo correspondiente y mantiene al usuario en el formulario de edición.
  **E2: Intento de crear una plantilla con un nombre duplicado.**
  - El **Sistema** detecta que el `Nombre` ya existe, rechaza la operación y muestra un error: "Ya existe una plantilla con este nombre."
  ### **Rendimiento**
La carga de la lista de plantillas y las operaciones CRUD deben completarse en menos de 2 segundos.

### **Frecuencia**
Baja. Se realiza principalmente durante la configuración inicial del sistema o cuando las políticas de la empresa cambian.

### **Comentarios**
- La funcionalidad de variables (placeholders) es la clave de este caso de uso. Sin ella, la utilidad de las plantillas es muy limitada. El sistema debe tener una lógica robusta para buscar y reemplazar estas variables con los datos correctos en el momento en que un agente utiliza la plantilla.


## **ID de Caso de Uso UC-14**

### **Nombre**
Gestionar Base de Conocimiento para IA

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Proveedor LLM (OpenRouter)**

### **Objetivos asociados**
1. **Crear un Activo de Conocimiento Corporativo:** Centralizar y estructurar el conocimiento de la empresa en un repositorio único y gestionado.
2. **Mitigación de Riesgos Operativos:** Proveer al LLM una fuente de verdad para reducir alucinaciones y basar sus respuestas en políticas verificadas.
3. **Escalar las Operaciones de Soporte:** Permitir que el sistema se mantenga actualizado de forma rápida ante cambios del negocio (nuevos productos, políticas, etc.).

### **Requisitos asociados**
**Funcionales:**
- **RF-IA-002:** El sistema deberá utilizar configuraciones de agente especializadas... para construir el prompt. (La Base de Conocimiento es el componente principal para la técnica de RAG - Retrieval-Augmented Generation, que es la implementación de esta especialización).
- **RF-ADMIN-002 (implícito):** La gestión de la Base de Conocimiento es una forma de configurar el comportamiento del agente de IA.

### **Descripción**
El Administrador gestiona el ciclo de vida de los artículos en la Base de Conocimiento. Esta no es una base de conocimiento para que la lean los humanos, sino el corpus de texto que se procesará para ser utilizado por el LLM. Cada vez que se crea o actualiza un artículo, el sistema debe iniciar un proceso asíncrono en segundo plano para "vectorizar" el contenido: lo divide en fragmentos (chunks), genera una representación numérica (embedding) para cada fragmento y lo almacena en una base de datos vectorial. Este índice vectorial es lo que el sistema usará para encontrar la información más relevante para un nuevo ticket.

### **Precondición**
1. El usuario está autenticado en el sistema y posee el rol de `Administrador`.
2. La infraestructura de base de datos vectorial (ej. la extensión `pgvector` en PostgreSQL) está instalada y configurada.
3. La integración con un servicio de generación de embeddings (ej. a través de OpenRouter o directamente con un proveedor como OpenAI) está configurada.

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección "Configuración IA" > "Base de Conocimiento".
2. El **Sistema** muestra una lista de todos los artículos de conocimiento, indicando su `Título`, `Estado` (ej. Activo, Inactivo, Procesando) y `Fecha de Última Modificación`.
3. El **Administrador** crea un nuevo artículo haciendo clic en "Nuevo Artículo".
4. El **Sistema** presenta un formulario para ingresar el `Título` y el `Contenido` del artículo.
5. El **Administrador** completa los campos y guarda el artículo.
6. El **Sistema** guarda el texto del artículo en la base de datos relacional y establece su estado inicial como `Procesando`.
7. **Inmediatamente**, el **Sistema** dispara un trabajo en segundo plano (asíncrono) para la vectorización del nuevo contenido. Este trabajo:
   1. Divide el `Contenido` en fragmentos de texto (chunks).
   2. Para cada chunk, llama a la API de embeddings para obtener su vector numérico.
   3. Almacena cada chunk de texto junto con su vector en la base de datos vectorial.
8. Una vez que el trabajo en segundo plano finaliza con éxito, el **Sistema** actualiza el estado del artículo a `Activo`.

### **Postcondición**
1. El contenido del nuevo artículo ha sido procesado y sus vectores están almacenados en la base de datos vectorial.
2. La nueva información está disponible inmediatamente para ser recuperada por el sistema de IA en la próxima consulta de un ticket.

### **Excepciones (Flujos Alternativos)**
**E1: Falla el proceso de vectorización.**
  - En el paso 7, la API de embeddings no está disponible o devuelve un error.
  - El trabajo en segundo plano falla. El **Sistema** debe registrar el error detallado para su auditoría.
  - El estado del artículo se actualiza a `Error en Procesamiento`.
  - La interfaz de usuario debe mostrar este estado de error y, opcionalmente, proporcionar un botón para "Reintentar Vectorización". El contenido no será utilizado por la IA hasta que se procese con éxito.
  **E2: Actualización de un artículo existente.**
  - El Administrador edita un artículo.
  - Al guardar, el **Sistema** debe invalidar y eliminar los vectores antiguos asociados a ese artículo de la base de datos vectorial antes de iniciar el proceso de vectorización del nuevo contenido (pasos 6-8). Esto es crucial para evitar que la IA utilice información obsoleta.
  **E3: Desactivación de un artículo.**
  - El Administrador cambia el estado de un artículo a `Inactivo`.
  - El **Sistema** elimina los vectores asociados de la base de datos vectorial pero conserva el texto en la base de datos relacional, permitiendo que sea reactivado en el futuro.
  ### **Rendimiento**
- La acción de guardar el texto del artículo (paso 6) debe ser instantánea (< 1 segundo).
- El proceso de vectorización en segundo plano (paso 7) es de larga duración y su tiempo dependerá del tamaño del texto y la latencia de la API de embeddings. No debe bloquear la interfaz de usuario.

### **Frecuencia**
Media-Baja. Se actualiza conforme evoluciona el catálogo de productos o las políticas internas.

### **Comentarios**
- Este es uno de los casos de uso más críticos para la calidad del sistema. La regla "Garbage In, Garbage Out" aplica directamente aquí. La calidad, claridad y veracidad del contenido gestionado en este módulo determinará directamente la calidad de las respuestas generadas por la IA.
- La gestión de la eliminación y actualización de vectores (E2, E3) es un desafío técnico clave que debe ser implementado de forma robusta.


## **ID de Caso de Uso UC-15**

### **Nombre**
Importar Órdenes (CSV)

### **Actor Primario**
Administrador

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Enriquecer el contexto de los tickets con datos de órdenes para que la IA y los agentes resuelvan consultas de estado de pedido (WISMO) más rápido.
2. **Mitigación de Riesgos Operativos:** Proveer un mecanismo controlado y con validación para la ingesta de datos críticos para el negocio.

### **Requisitos asociados**
**Funcionales:**
- **RF-DATA-001:** Exige una interfaz para la subida de archivos CSV de órdenes.
- **RF-DATA-002:** Requiere la previsualización de datos y la visualización de errores de validación.
- **RF-DATA-003:** Especifica que el procesamiento de la importación debe ser asíncrono.
**Interfaces:**
- **UI-04:** Define la interfaz de usuario específica para la importación, previsualización y mapeo de columnas.

### **Descripción**
El Administrador accede a una sección específica del sistema para cargar un archivo CSV que contiene datos de las órdenes de venta de "GearUp Gadgets". El sistema permite previsualizar los datos, mapear las columnas del archivo a los campos de la base de datos y procesa la importación en segundo plano. El objetivo es poblar o actualizar la tabla `Orden` para enriquecer el contexto disponible para los agentes y la IA.

### **Precondición**
1. El Administrador ha iniciado sesión en el sistema y tiene los permisos necesarios.
2. El Administrador tiene un archivo en formato CSV con los datos de las órdenes listo para ser cargado.

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección de "Administración > Importación de Datos".
2. El **Sistema** presenta la interfaz `UI-04`, que incluye un control para seleccionar un archivo.
3. El **Administrador** selecciona el archivo CSV de su equipo local y lo sube.
4. El **Sistema** recibe el archivo, lo guarda temporalmente y realiza un análisis preliminar (lee las cabeceras y algunas filas de muestra).
5. El **Sistema** muestra una vista de previsualización de los datos y una interfaz de mapeo de columnas, sugiriendo automáticamente las asignaciones si los nombres de las cabeceras coinciden con los campos de la base de datos (ej. `order_id` -> `idExterno`). (`RF-DATA-002`)
6. El **Administrador** revisa y confirma (o ajusta) el mapeo de columnas y hace clic en "Iniciar Importación".
7. El **Sistema** valida la solicitud, crea un trabajo de importación en una cola de procesamiento y responde inmediatamente a la interfaz de usuario. (`RF-DATA-003`)
8. La **UI** muestra un mensaje de confirmación: "La importación ha sido iniciada. Se te notificará al finalizar." y puede mostrar el nuevo trabajo en una lista con estado "En Progreso".
9. Un **Proceso en Segundo Plano** (worker) toma el trabajo de la cola y comienza a procesar el archivo CSV fila por fila.
   1. Para cada fila, valida los datos (tipos, longitudes, formatos).
   2. Busca si ya existe una `Orden` con el mismo identificador único. Si existe, la actualiza; si no, la crea (lógica de `upsert`).
   3. Registra el resultado de cada fila (éxito o error).
10. Al finalizar el procesamiento, el **Proceso en Segundo Plano** actualiza el estado del trabajo a "Completado" y guarda un resumen (ej. "1500 filas procesadas: 1490 exitosas, 10 fallidas").
11. El **Sistema** notifica al **Administrador** sobre la finalización del trabajo (ej. mediante una notificación en la UI o un correo electrónico) con un enlace al resumen de la importación.

### **Postcondición**
1. Los datos de las órdenes del archivo CSV están creados o actualizados en la tabla `Orden` de la base de datos.
2. Se ha registrado un log detallado del proceso de importación, incluyendo las filas que fallaron y el motivo.
3. El Administrador ha sido notificado del resultado.

### **Excepciones (Flujos Alternativos)**
**E1: Formato de archivo incorrecto.**
  - En el paso 3, el Administrador sube un archivo que no es CSV (ej. `.xlsx`, `.pdf`).
  - El Sistema rechaza el archivo en el frontend o backend y muestra un error: "Formato de archivo no válido. Por favor, sube un archivo CSV."
  **E2: El archivo CSV tiene una estructura inválida.**
  - En el paso 5, el archivo no tiene las columnas requeridas para el mapeo.
  - El Sistema detecta la ausencia de columnas clave y deshabilita el botón "Iniciar Importación", mostrando un mensaje: "El archivo no contiene las columnas necesarias. Revisa el formato."
  **E3: Errores de validación en filas específicas.**
  - Durante el paso 9, el proceso en segundo plano encuentra filas con datos malformados (ej. una fecha en formato incorrecto, un campo requerido vacío).
  - El proceso ignora/descarta la fila inválida, registra el error específico y el número de línea en el log de la importación, y continúa con el resto del archivo. El trabajo se marcará como "Completado con errores".
  **E4: Falla crítica del trabajo de importación.**
  - Durante el paso 9, ocurre un error irrecuperable (ej. se pierde la conexión con la base de datos).
  - El trabajo de importación se detiene, se revierte cualquier transacción parcial si es posible, y su estado se actualiza a "Fallido". Se genera un log del error crítico para diagnóstico técnico.
  ### **Rendimiento**
La carga del archivo y la respuesta de la UI (paso 8) deben ser casi instantáneas. El procesamiento en segundo plano (paso 9) debe ser capaz de procesar al menos 10,000 registros por minuto.


## **ID de Caso de Uso UC-16**

### **Nombre**
Gestionar Usuarios

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Supabase Auth**

### **Objetivos asociados**
1. **Mitigación de Riesgos Operativos:** Controlar el acceso al sistema, asignar privilegios correctos según el rol y gestionar de forma segura el ciclo de vida del personal para mantener la seguridad de los datos.

### **Requisitos asociados**
**Funcionales:**
- **RF-ADMIN-001:** Define explícitamente la capacidad de un administrador para gestionar usuarios y roles.
**No Funcionales:**
- **NFR-SEC-001:** Requiere que el acceso a los endpoints esté protegido por JWT.
**Interfaces:**
- **API-04:** Indica la dependencia de Supabase Auth para la autenticación, lo cual impacta directamente cómo se gestionan las identidades.

### **Descripción**
El Administrador utiliza la interfaz de gestión de usuarios para realizar operaciones de Crear, Leer, Actualizar y Eliminar (CRUD) sobre las cuentas de usuario del sistema. Esto incluye invitar a nuevos agentes, cambiar sus roles (ej. de Triaje a Especialista) y desactivar sus cuentas. El sistema se coordina con un servicio de identidad externo (Supabase Auth) para la creación y gestión de credenciales.

### **Precondición**
1. El Administrador ha iniciado sesión en el sistema y tiene los permisos necesarios.
2. La integración con el servicio de autenticación (Supabase Auth) está configurada y funcionando.

### **Secuencia Normal (Flujo Principal)**
**Flujo 1: Crear un nuevo usuario**
1. El **Administrador** navega a la sección de "Administración > Gestión de Usuarios".
2. El **Sistema** muestra una lista de los usuarios existentes.
3. El **Administrador** hace clic en "Invitar Usuario".
4. El **Sistema** presenta un formulario para ingresar el Email, Nombre y Rol del nuevo usuario.
5. El **Administrador** completa los datos y envía el formulario.
6. El **Sistema** valida los datos (ej. formato de email válido).
7. El **Sistema** realiza una llamada a la API de **Supabase Auth** para invitar al nuevo usuario (`API-04`).
8. **Supabase Auth** envía un correo de invitación al email proporcionado para que el nuevo usuario establezca su contraseña.
9. Tras la confirmación exitosa de Supabase, el **Sistema** crea un registro local en su tabla `Usuario`, asociando el ID de usuario de Supabase con el rol y otros metadatos de la aplicación.
10. La lista de usuarios en la UI se actualiza, mostrando al nuevo usuario con un estado de "Invitación enviada".
**Flujo 2: Modificar el rol de un usuario existente**
1. El **Administrador**, en la lista de usuarios, localiza al usuario que desea modificar y hace clic en "Editar".
2. El **Sistema** muestra los detalles del usuario, permitiendo la edición del campo "Rol".
3. El **Administrador** cambia el rol (ej. de `Agente de Triaje` a `Agente Especialista`).
4. El **Administrador** guarda los cambios.
5. El **Sistema** actualiza el campo `rol` en su tabla local `Usuario` para ese registro. No se requiere una llamada a Supabase si el rol es un concepto puramente de la aplicación.
6. El **Sistema** muestra un mensaje de éxito y actualiza la lista.
**Flujo 3: Desactivar un usuario**
1. El **Administrador**, en la lista de usuarios, localiza al usuario y hace clic en "Desactivar".
2. El **Sistema** muestra un diálogo de confirmación.
3. El **Administrador** confirma la acción.
4. El **Sistema** realiza una llamada a la API de **Supabase Auth** para deshabilitar o eliminar al usuario de la plataforma de autenticación.
5. El **Sistema** actualiza el registro local del usuario, marcándolo como inactivo (soft delete).
6. El usuario desactivado ya no podrá iniciar sesión y su token JWT será invalidado.

### **Postcondición**
1. **Crear:** Se ha enviado una invitación y existe un nuevo registro de usuario en estado pendiente en Supabase y en la base de datos local.
2. **Actualizar:** El rol del usuario ha sido modificado en la base de datos local.
3. **Desactivar:** El usuario ya no puede autenticarse en el sistema y su estado local refleja la inactividad.

### **Excepciones (Flujos Alternativos)**
**E1: El email del nuevo usuario ya existe.**
  - En el Flujo 1, paso 7, la API de Supabase Auth devuelve un error indicando que el usuario ya está registrado.
  - El Sistema muestra un mensaje de error al Administrador: "Un usuario con este correo electrónico ya existe."
  **E2: Falla la comunicación con el servicio de autenticación.**
  - Durante la creación (paso 7) o desactivación (paso 4) de un usuario, la API de Supabase no responde o devuelve un error.
  - El Sistema no realiza ningún cambio en su base de datos local, registra el error y muestra un mensaje genérico: "No se pudo completar la operación con el servicio de autenticación. Inténtelo más tarde."
  **E3: Intento de eliminar al último administrador.**
  - En el Flujo 3, el Administrador intenta desactivar su propia cuenta o la del único usuario restante con el rol de `Administrador`.
  - El Sistema aplica una regla de negocio que impide la acción y muestra un mensaje: "No se puede eliminar al último administrador del sistema."
  ### **Seguridad**
Todas las acciones de este caso de uso deben ser registradas en un log de auditoría (`UC-22`) para rastrear quién realizó los cambios, qué cambios se hicieron y cuándo.


## **ID de Caso de Uso UC-17**

### **Nombre**
Gestionar Etiquetas Maestras

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Agente Especialista/Triaje** (Utiliza las etiquetas)

### **Objetivos asociados**
1. **Generar Inteligencia de Negocio:** Estandarizar la taxonomía de clasificación para asegurar que los datos de etiquetado sean limpios y fiables, permitiendo la generación de reportes precisos.
2. **Optimizar la Eficiencia Operativa:** Proveer a los agentes una lista predefinida de etiquetas para agilizar el proceso de categorización manual.

### **Requisitos asociados**
**Funcionales:**
- **RF-ADMIN-001:** Define la capacidad del administrador para gestionar configuraciones del sistema, incluyendo esta taxonomía.
- **RF-AGENT-007:** Este caso de uso es un prerrequisito para que los agentes puedan utilizar y gestionar etiquetas en un ticket específico.

### **Descripción**
El Administrador del sistema realiza operaciones de Crear, Leer, Actualizar y Eliminar (CRUD) sobre el catálogo central de `Etiqueta`s. Este catálogo define las opciones de clasificación que estarán disponibles para los agentes y para el motor de IA en todo el sistema.

### **Precondición**
1. El usuario está autenticado en el sistema.
2. El usuario tiene asignado el rol de `Administrador`.

### **Secuencia Normal (Flujo Principal)**
**A. Listar Etiquetas**
1. El **Administrador** navega a la sección de "Administración > Etiquetas".
2. El **Sistema** recupera y muestra una tabla con todas las etiquetas maestras existentes. Para cada etiqueta, la tabla muestra su nombre, descripción, una muestra de su color y, opcionalmente, la cantidad de tickets activos que la utilizan.
**B. Crear una Nueva Etiqueta**
1. El **Administrador** hace clic en el botón "Crear Nueva Etiqueta".
2. El **Sistema** presenta un formulario modal o una nueva página con campos para: Nombre (requerido, único), Descripción (opcional) y Selector de Color (requerido).
3. El **Administrador** completa los datos y hace clic en "Guardar".
4. El **Sistema** valida que el nombre de la etiqueta no exista ya (de forma no sensible a mayúsculas/minúsculas).
5. El **Sistema** crea un nuevo registro en la tabla `Etiqueta` y cierra el formulario.
6. El **Sistema** actualiza la tabla de etiquetas para mostrar la nueva entrada y muestra una notificación de éxito.
**C. Editar una Etiqueta Existente**
1. El **Administrador** localiza una etiqueta en la tabla y hace clic en el icono "Editar".
2. El **Sistema** presenta el mismo formulario que para la creación, pero pre-poblado con los datos de la etiqueta seleccionada.
3. El **Administrador** modifica la descripción o el color y hace clic en "Guardar". (El nombre podría ser inmutable o su edición sujeta a reglas estrictas).
4. El **Sistema** valida los datos y actualiza el registro correspondiente en la base de datos.
5. El **Sistema** actualiza la fila en la tabla y muestra una notificación de éxito.
**D. Eliminar una Etiqueta**
1. El **Administrador** hace clic en el icono "Eliminar" de una etiqueta específica.
2. El **Sistema** muestra un cuadro de diálogo de confirmación: "¿Estás seguro de que quieres eliminar la etiqueta '[Nombre de la Etiqueta]'? Esta acción no se puede deshacer."
3. El **Administrador** confirma la acción.
4. El **Sistema** verifica que la etiqueta no esté siendo utilizada por ningún `Ticket`.
5. Si la verificación es exitosa, el **Sistema** elimina el registro de la etiqueta de la base de datos.
6. El **Sistema** elimina la fila de la tabla y muestra una notificación de éxito.

### **Postcondición**
1. El catálogo de `Etiqueta`s en la base de datos refleja los cambios realizados por el Administrador.
2. Los cambios están disponibles inmediatamente para su uso en todo el sistema.

### **Excepciones (Flujos Alternativos)**
**E1: Intento de crear una etiqueta con un nombre duplicado.**
  - En el paso B.4, el sistema detecta que el nombre ya existe.
  - El **Sistema** no crea la etiqueta. Muestra un mensaje de error en el formulario: "Ya existe una etiqueta con este nombre." y resalta el campo de nombre. El formulario permanece abierto para que el Administrador corrija el error.
  **E2: Intento de eliminar una etiqueta en uso.**
  - En el paso D.4, el sistema detecta que la etiqueta está asociada a uno o más tickets.
  - El **Sistema** aborta la operación de eliminación.
  - El **Sistema** muestra un mensaje de error informativo: "No se puede eliminar la etiqueta '[Nombre de la Etiqueta]' porque está siendo utilizada por [N] tickets. Considere editarla o archivarla en su lugar."
  **E3: Error de sistema o de red.**
  - Durante cualquier operación de guardado o eliminación, se produce un error de comunicación con el servidor o un fallo en la base de datos.
  - El **Sistema** muestra una notificación de error genérica: "Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo." y registra el error detallado internamente para su posterior análisis.
  ### **Comentarios**
- Por razones de integridad de datos, es una práctica recomendada no permitir la eliminación física de etiquetas en uso (ver E2). Una alternativa superior es implementar una función de "Archivar" que la oculte de futuras asignaciones pero preserve el registro histórico en los tickets existentes.
- La validación del nombre de la etiqueta debe ser, como mínimo, *case-insensitive* para evitar duplicados como "pago" y "Pago".


## **ID de Caso de Uso UC-18**

### **Nombre**
Gestionar Integraciones

### **Actor Primario**
Administrador

### **Actor Secundario(s)**
**Servicios Externos** (Mailgun, OpenRouter, Supabase)

### **Objetivos asociados**
1. **Mitigación de Riesgos Operativos:** Centralizar la gestión de credenciales y configuración sensible en una interfaz segura para facilitar la mantenibilidad y asegurar la conectividad con servicios de terceros.

### **Requisitos asociados**
**Funcionales:**
- **RF-ADMIN-001:** Es la capacidad general del administrador para gestionar el sistema.
**Interfaces:**
- **API-01, API-02, API-03, API-04, API-05:** Este caso de uso proporciona la interfaz de usuario para configurar los parámetros (ej. claves de API) necesarios para que estas integraciones de software funcionen.

### **Descripción**
El Administrador utiliza una sección segura de la interfaz para configurar y validar los parámetros de conexión con los servicios externos de los que depende NoraAI. Esto incluye la introducción de claves de API, dominios y otros datos de configuración necesarios para Mailgun (correo), OpenRouter (LLM) y Supabase (almacenamiento y autenticación).

### **Precondición**
1. El usuario está autenticado en el sistema.
2. El usuario tiene asignado el rol de `Administrador`.
3. El Administrador tiene acceso a las credenciales (ej. claves de API) obtenidas de los paneles de administración de los servicios externos (Mailgun, OpenRouter).

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección "Administración > Integraciones".
2. El **Sistema** muestra una lista de las integraciones que requiere (ej. "Servicio de Email - Mailgun", "Proveedor LLM - OpenRouter", "Almacenamiento - Supabase Storage").
3. El **Administrador** selecciona la integración que desea configurar, por ejemplo, "Mailgun".
4. El **Sistema** presenta un formulario con los campos específicos para esa integración. Por ejemplo, para Mailgun:
  - Clave de API (campo de contraseña, requerido)
  - Dominio de envío (requerido)
  - Clave de firma del Webhook (campo de contraseña, requerido para `API-02`)
  - URL del Webhook de entrada (campo de solo lectura, para que el admin la copie y pegue en Mailgun)
5. El **Administrador** introduce o actualiza las credenciales en los campos.
6. El **Administrador** hace clic en el botón "Guardar y Probar Conexión".
7. El **Sistema** realiza dos acciones:
   1. Primero, guarda la configuración en la base de datos de forma segura (los secretos deben estar encriptados en reposo).
   2. Segundo, utiliza las nuevas credenciales para realizar una llamada de prueba a la API del servicio externo (ej. intenta enviar un email de prueba a una dirección designada usando la API de Mailgun).
8. El **Sistema** recibe una respuesta exitosa de la API externa.
9. El **Sistema** muestra una notificación de éxito persistente en la interfaz: "¡Éxito! La conexión con Mailgun se ha verificado correctamente."

### **Postcondición**
1. Las credenciales para el servicio externo están actualizadas y almacenadas de forma segura en la base de datos.
2. Se ha verificado que el sistema puede comunicarse exitosamente con el servicio externo utilizando la nueva configuración.

### **Excepciones (Flujos Alternativos)**
**E1: Falla la prueba de conexión.**
  - En el paso 7b, la llamada a la API del servicio externo falla (ej. por una clave de API incorrecta).
  - El **Sistema** recibe una respuesta de error del servicio externo.
  - El **Sistema** almacena la configuración pero la marca como "no verificada" o "con error".
  - El **Sistema** muestra una notificación de error detallada y útil: "Error al conectar con Mailgun. La API devolvió el siguiente error: '401 Unauthorized - Forbidden'. Por favor, verifica tu Clave de API."
  **E2: El servicio externo no está disponible.**
  - En el paso 7b, la llamada a la API del servicio externo falla no por credenciales incorrectas, sino por un problema de red o porque el servicio está caído (ej. timeout o error 503).
  - El **Sistema** muestra un mensaje de error específico para esta situación: "No se pudo establecer conexión con los servidores de Mailgun. Por favor, comprueba el estado del servicio e inténtalo de nuevo más tarde."
  **E3: Los datos introducidos tienen un formato inválido.**
  - En el paso 6, el Administrador intenta guardar sin rellenar un campo requerido.
  - El **Sistema**, antes de intentar guardar o probar la conexión, realiza una validación local y muestra un error junto al campo: "Este campo es requerido."
  ### **Comentarios**
- **Seguridad Crítica:** Las credenciales (claves de API, tokens, secretos de firma) NUNCA deben almacenarse como texto plano. Deben ser encriptadas en la base de datos utilizando un mecanismo de encriptación fuerte. Además, nunca deben ser expuestas de nuevo en la interfaz de usuario después de ser guardadas (los campos de contraseña siempre deben aparecer vacíos o con placeholders al volver a editar).
- La funcionalidad "Guardar y Probar" es fundamental. Separar estas acciones podría dejar al sistema en un estado no funcional si el administrador guarda credenciales incorrectas y no se da cuenta.


## **ID de Caso de Uso UC-19**

### **Nombre**
Reasignar Ticket Manualmente

### **Actor Primario**
Agente de Triaje

### **Actor Secundario(s)**
**Agente Especialista** (Recibe el ticket)

### **Actores Secundarios**
Agente Especialista, Administrador (heredan la capacidad)   

### **Objetivos asociados**
1. **Optimizar el Enrutamiento:** Permitir que un agente con conocimiento del equipo y de la carga de trabajo asigne un ticket directamente al especialista más adecuado, saltándose la cola general de Nivel 2.
2. **Mejorar la Colaboración:** Facilitar la transferencia de tickets entre colegas cuando se requiere una segunda opinión o la intervención de un experto específico.
3. **Aumentar la Velocidad de Resolución:** Reducir el tiempo que un ticket pasa en una cola general al dirigirlo inmediatamente a la persona que puede resolverlo.

### **Requisitos asociados**
**Funcionales:**
- **RF-AGENT-005 (Relacionado):** Este caso de uso es una alternativa más específica a la escalada general. Un agente puede elegir escalar a la cola o reasignar a un individuo.
- **RF-AGENT-008 (Relacionado):** La capacidad de @mencionar es clave para la colaboración, y la nota de reasignación es una forma de mención contextual.
- **RF-SUPERVISOR-002:** El historial del ticket debe reflejar claramente la acción de reasignación.
**No Funcionales:**
- **NFR-USAB-001 (Implícito):** La acción de reasignar debe ser accesible y fácil de ejecutar desde la vista del ticket.

### **Descripción**
Un Agente de Triaje, al revisar un ticket, identifica que este requiere la atención de un Agente Especialista específico. En lugar de escalarlo a la cola general de Nivel 2, el agente utiliza la funcionalidad de reasignación para transferir la propiedad del ticket directamente a su colega, añadiendo opcionalmente una nota interna para dar contexto.

### **Precondición**
1. El Agente de Triaje ha iniciado sesión en el sistema.
2. Existe al menos un ticket en un estado que permite la reasignación (ej. `ia_sugerido`, `abierto`).
3. Existen otros usuarios (Agentes Especialistas) en el sistema a los cuales se les puede asignar el ticket.

### **Secuencia Normal (Flujo Principal)**
1. El **Agente de Triaje** abre un ticket desde su vista de triaje.
2. El **Agente de Triaje** evalúa el contenido y decide que un colega específico es el más indicado para resolverlo.
3. El **Agente** selecciona la acción "Reasignar" en la interfaz del ticket.
4. El **Sistema** presenta una lista de usuarios elegibles (Agentes Especialistas, Administradores), mostrando preferiblemente su estado actual (ej. 'En línea', 'Ausente') o su carga de trabajo actual (ej. '5 tickets asignados').
5. El **Agente** selecciona al Agente Especialista deseado de la lista.
6. El **Sistema** ofrece un campo de texto para que el agente añada una nota interna explicando el motivo de la reasignación (ej. "@Carlos, este cliente tiene un problema similar al de la semana pasada. ¿Puedes echarle un vistazo?").
7. El **Agente** confirma la reasignación.
8. El **Sistema** valida la acción y actualiza el registro del `Ticket`:
   1. Cambia el campo `asignadoAUsuarioId` al ID del Agente Especialista seleccionado.
   2. Actualiza el `estado` del ticket a `escalado_nivel_2` (o `abierto`, si ya estaba en ese nivel).
   3. Crea un registro en el `LogEvento` del ticket indicando: "Reasignado por [Agente de Triaje] a [Agente Especialista] el [Fecha/Hora]".
   4. Si se añadió una nota, la guarda como un `Mensaje` de tipo `interno` asociado al ticket.
9. El **Sistema** envía una notificación en tiempo real (in-app) al Agente Especialista recién asignado.
10. El **Sistema** actualiza la interfaz del Agente de Triaje, mostrando que el ticket ya no está en su cola y confirmando la reasignación exitosa.

### **Postcondición**
1. El `Ticket` ya no está en la cola de triaje.
2. El `Ticket` está asignado al Agente Especialista seleccionado.
3. La acción de reasignación ha quedado registrada en el historial del ticket para fines de auditoría.
4. El Agente Especialista ha sido notificado de su nueva asignación.

### **Excepciones (Flujos Alternativos)**
**E1: El agente seleccionado ya no está disponible.**
  - En el paso 7, el agente de destino ha sido desactivado o ha cerrado sesión justo antes de la confirmación.
  - El Sistema invalida la acción y muestra un mensaje de error: "No se puede asignar el ticket. El usuario [Nombre] ya no está disponible. Por favor, seleccione otro agente."
  **E2: Ocurre un conflicto de concurrencia.**
  - Mientras el Agente de Triaje está decidiendo a quién reasignar, otro agente o un proceso automático cambia el estado del ticket (ej. el cliente responde).
  - En el paso 8, el Sistema detecta que el estado del ticket ha cambiado. Rechaza la acción y notifica al agente: "El estado de este ticket ha cambiado. Por favor, refresque la página para ver la última actualización antes de reasignar."
  ### **Rendimiento**
La búsqueda de agentes disponibles (paso 4) y la confirmación de la reasignación (paso 10) deben completarse en menos de 2 segundos cada una.

### **Frecuencia**
Media. Dependerá de la dinámica del equipo de soporte.

### **Comentarios**
- La notificación al agente recién asignado (paso 9) es crítica para la fluidez del proceso. Sin ella, el ticket podría quedar estancado hasta que el agente revise manualmente su cola.
- Por seguridad y auditoría, el sistema debe registrar quién realiza la reasignación y cuándo.


## **ID de Caso de Uso UC-20**

### **Nombre**
Generar Reportes (Exportar)

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
**Sistema** (Para el proceso de streaming/generación de CSV)

### **Actores Secundarios**
Supervisor de Soporte, Administrador                 

### **Objetivos asociados**
1. **Habilitar el Análisis Externo:** Permitir que los datos de los tickets sean extraídos del sistema para su análisis en herramientas de BI, hojas de cálculo u otros sistemas.
2. **Generar Inteligencia de Negocio:** Facilitar la identificación de tendencias, cuellos de botella y patrones de comportamiento de los clientes mediante el análisis de grandes volúmenes de datos.
3. **Cumplir con Requisitos de Auditoría y Archivo:** Proporcionar un mecanismo para crear copias de seguridad o archivos históricos de las interacciones con los clientes.

### **Requisitos asociados**
**Funcionales:**
- **RF-DATA-004:** El sistema deberá permitir la exportación de una lista filtrada de tickets a un archivo CSV.
- **RF-DATA-005:** El sistema deberá poder generar un reporte de resumen.
**No Funcionales:**
- **NFR-PERF-001:** La exportación de grandes volúmenes debe usar streaming para evitar timeouts y uso excesivo de memoria.

### **Descripción**
Un usuario autorizado (Agente, Supervisor o Admin) necesita obtener un conjunto de datos de tickets para análisis externo. El usuario accede a la sección de reportes, aplica una serie de filtros para definir el conjunto de datos deseado (ej. por rango de fechas, estado, etiqueta) y solicita la exportación. El sistema procesa la solicitud en segundo plano y notifica al usuario cuando el archivo CSV está listo para ser descargado.

### **Precondición**
1. El usuario ha iniciado sesión en el sistema y tiene los permisos necesarios para acceder a la funcionalidad de reportes.
2. Existen datos de tickets en la base de datos que pueden ser exportados.

### **Secuencia Normal (Flujo Principal)**
1. El **Usuario** navega a la sección "Reportes" o "Tickets" de la aplicación.
2. El **Sistema** presenta una interfaz con un conjunto de controles de filtrado, como: Rango de Fechas, Estado del Ticket, Etiqueta(s), Agente Asignado, Cliente.
3. El **Usuario** selecciona y aplica los filtros deseados.
4. El **Sistema** actualiza la vista, mostrando una vista previa paginada de los tickets que coinciden con los criterios y un contador total de registros ("Se encontraron 1,234 tickets").
5. El **Usuario** hace clic en el botón "Exportar a CSV".
6. El **Sistema** inicia un trabajo asíncrono en el backend para generar el archivo CSV. Este proceso no bloquea la interfaz del usuario.
7. El **Sistema** muestra una notificación inmediata en la UI: "Tu exportación ha comenzado. Te notificaremos cuando el archivo esté listo para descargar."
8. El trabajo en segundo plano consulta la base de datos con los filtros aplicados y procesa los resultados en un flujo (`stream`) para construir el archivo CSV, garantizando un bajo consumo de memoria (`NFR-PERF-001`).
9. Una vez que el archivo se ha generado y almacenado temporalmente de forma segura, el **Sistema** envía una notificación al usuario (ej. un ícono en la barra de navegación y/o un correo electrónico).
10. El **Usuario** hace clic en la notificación o en el enlace proporcionado.
11. El **Sistema** inicia la descarga del archivo CSV en el navegador del usuario.
12. El **Sistema** crea un registro en el `LogEvento` para auditar la acción: "El usuario [Nombre de Usuario] exportó [Número] tickets con los filtros [Resumen de Filtros] el [Fecha/Hora]".

### **Postcondición**
1. El usuario ha descargado un archivo CSV que contiene los datos de los tickets que coinciden con los filtros aplicados.
2. La acción de exportación ha quedado registrada para fines de auditoría.

### **Excepciones (Flujos Alternativos)**
**E1: No se encuentran resultados.**
  - En el paso 4, ningún ticket coincide con los filtros aplicados.
  - El Sistema muestra el mensaje "No se encontraron tickets para los criterios seleccionados." y el botón "Exportar a CSV" permanece deshabilitado.
  **E2: El proceso de exportación falla.**
  - Durante el paso 8, el trabajo en segundo plano encuentra un error irrecuperable (ej. pérdida de conexión con la base de datos).
  - El Sistema detiene el proceso, registra el error y notifica al usuario: "Lo sentimos, ha ocurrido un error al generar tu exportación. Por favor, inténtalo de nuevo más tarde."
  **E3: El conjunto de datos es demasiado grande.**
  - Si, a pesar del streaming, el conjunto de datos excede un límite de seguridad predefinido (ej. > 500,000 registros), el sistema puede detener la exportación.
  - El Sistema notifica al usuario: "El conjunto de datos es demasiado grande para exportar de una vez. Por favor, reduce el rango de fechas o aplica filtros más específicos."
  ### **Rendimiento**
El tiempo para generar la notificación de que la exportación está lista (paso 9) debería ser razonable, incluso para grandes volúmenes. Ej: para 10,000 registros, el tiempo no debería exceder los 2 minutos.

### **Frecuencia**
Baja-Media. Se espera que sea utilizada principalmente por Supervisores y Administradores de forma semanal o mensual.

### **Comentarios**
- El procesamiento asíncrono (paso 6) es fundamental para la experiencia del usuario y la estabilidad del sistema. Una exportación síncrona bloquearía el navegador y podría causar timeouts en la solicitud HTTP.
- Por motivos de seguridad de datos, los enlaces de descarga generados (paso 9) deben ser de un solo uso o tener un tiempo de expiración corto.


## **ID de Caso de Uso UC-21**

### **Nombre**
Visualizar Dashboard de Métricas

### **Actor Primario**
Agente Especialista

### **Actor Secundario(s)**
Agente triaje, Administrador

### **Objetivos asociados**
1. **Generar Inteligencia de Negocio:** Ofrecer una vista consolidada para identificar tendencias, cuellos de botella y áreas de mejora en el proceso de soporte.
2. **Optimizar la Eficiencia Operativa:** Facilitar el seguimiento del rendimiento individual y del equipo frente a los KPIs para soportar la toma de decisiones basada en datos.

### **Requisitos asociados**
**Funcionales:**
- **RF-SUPERVISOR-001:** Un supervisor debe poder visualizar dashboards de rendimiento.
- **RF-AGENT-009:** El sistema debe monitorizar SLAs y resaltar visualmente los tickets.
**Interfaces:**
- **UI-01:** Dashboard de Supervisor con KPIs clave.
- **UI-02 / UI-03:** Paneles de agente que incluyen indicadores de SLA.

### **Descripción**
Un usuario autorizado (Agente, Supervisor o Administrador) accede a una sección dedicada en la interfaz web para visualizar un panel de control con métricas y KPIs sobre la operación de soporte. La información presentada se filtra automáticamente según el rol y los permisos del usuario.

### **Precondición**
1. El usuario está autenticado en el sistema.
2. El usuario tiene al menos permisos de `Agente Especialista`.
3. Existen datos de tickets en el sistema para ser analizados y mostrados.

### **Secuencia Normal (Flujo Principal)**
1. El **Usuario** navega a la sección "Dashboard" o "Métricas" a través del menú principal de la aplicación.
2. El **Sistema** identifica el rol del usuario (Agente, Supervisor, Admin).
3. El **Sistema** recupera los datos operativos relevantes de la base de datos, aplicando los filtros de permisos correspondientes:
  - **Agente:** Métricas personales (mis tickets asignados, mi tiempo de respuesta, etc.).
  - **Supervisor:** Métricas agregadas de su equipo y métricas individuales de los agentes bajo su cargo.
  - **Administrador:** Métricas globales de todo el sistema.
4. El **Sistema** presenta el dashboard, que contiene varios widgets visuales, tales como:
  - **Tarjetas de KPIs:** Tickets Abiertos, Tickets Resueltos Hoy, Tiempo Medio de Primera Respuesta (FRT), Tiempo Medio de Resolución (TTR), Tasa de Resolución en Primer Contacto (FCR), Puntuación de Satisfacción del Cliente (CSAT).
  - **Gráficos de Tendencia:** Un gráfico de líneas mostrando el volumen de tickets creados vs. resueltos en los últimos 7/30 días.
  - **Listas de Prioridad:** Una lista de los tickets más antiguos sin resolver o aquellos que están a punto de incumplir su SLA.
5. El **Usuario** puede interactuar con el dashboard para refinar la vista, por ejemplo, cambiando el rango de fechas (hoy, últimos 7 días, último mes).
6. Si el usuario es Supervisor o Administrador, puede filtrar las métricas por agente o por equipo.

### **Postcondición**
1. El usuario ha visualizado el estado actual y el rendimiento histórico de la operación de soporte, de acuerdo con sus permisos.
2. El estado del sistema no se ha modificado (es una operación de solo lectura).

### **Excepciones (Flujos Alternativos)**
**E1: No hay datos disponibles para el período seleccionado.**
  - En el paso 5, el usuario selecciona un rango de fechas en el que no hubo actividad.
  - El Sistema, en lugar de mostrar gráficos vacíos o errores, presenta un mensaje claro en cada widget afectado: "No hay datos disponibles para el período seleccionado".
  **E2: Error al cargar los datos del dashboard.**
  - En el paso 3, el backend no puede recuperar o procesar los datos (ej. por un error en la base de datos).
  - El Sistema muestra un mensaje de error general en el área del dashboard: "No se pudieron cargar las métricas. Por favor, intente recargar la página." y registra el error técnico internamente.
  ### **Rendimiento**
La carga inicial del dashboard con los datos del período predeterminado (ej. "últimos 7 días") debe completarse en **menos de 5 segundos**. Las operaciones de filtrado deben actualizar la vista en **menos de 3 segundos**.

### **Frecuencia**
Alta. Se espera que sea una de las primeras pantallas que los Supervisores y Administradores consulten diariamente. Los agentes la consultarán periódicamente para autoevaluar su rendimiento.

### **Comentarios**
- Para optimizar el rendimiento (NFR-PERF), los cálculos de métricas complejas no deben realizarse en tiempo real sobre la base de datos transaccional en cada carga. Se debe considerar una estrategia de pre-agregación (ej. tablas de resumen actualizadas periódicamente) para garantizar tiempos de carga rápidos.


## **ID de Caso de Uso UC-22**

### **Nombre**
Auditar Log de Eventos del Sistema

### **Actor Primario**
Administrador

### **Objetivos asociados**
1. **Mitigación de Riesgos Operativos:** Garantizar la trazabilidad y rendición de cuentas a través de un registro inmutable de acciones críticas, facilitando la auditoría de seguridad y la depuración de problemas.

### **Requisitos asociados**
**Funcionales:**
- **RF-ADMIN-002:** Un administrador debe poder auditar los cambios en las configuraciones de los agentes de IA.
**No Funcionales:**
- **NFR-SEC-001:** El acceso a los endpoints debe estar protegido (este es un endpoint de alta sensibilidad).

### **Descripción**
El Administrador accede a una interfaz segura que muestra un registro cronológico de todos los eventos significativos que han ocurrido en el sistema. Puede buscar y filtrar estos registros para realizar auditorías de seguridad, monitorizar la actividad de los usuarios o diagnosticar problemas técnicos.

### **Precondición**
1. El usuario está autenticado en el sistema.
2. El usuario tiene asignado el rol de `Administrador`.
3. El sistema está configurado para registrar eventos en una tabla o servicio de logs (`LogEvento`).

### **Secuencia Normal (Flujo Principal)**
1. El **Administrador** navega a la sección "Administración" > "Auditoría" o "Log de Eventos".
2. El **Sistema** presenta una vista de tabla con el log de eventos, ordenado por fecha descendente (los más recientes primero). Cada fila representa un evento y muestra información clave como:
  - **Timestamp:** Fecha y hora exactas del evento (en UTC).
  - **Usuario:** El usuario que realizó la acción (o "Sistema" si fue una acción automática).
  - **Tipo de Evento:** Una acción descriptiva (ej. `LOGIN_SUCCESS`, `USER_CREATED`, `CONFIG_AGENT_UPDATED`, `TICKET_DELETED`).
  - **Entidad Afectada:** El tipo de objeto que fue modificado (ej. `Usuario`, `Ticket`, `ConfigAgente`).
  - **ID de la Entidad:** El identificador único del objeto afectado.
3. El **Administrador** utiliza los controles de filtrado para acotar la búsqueda. Puede filtrar por:
  - Rango de fechas.
  - Usuario específico.
  - Tipo de evento.
4. El **Administrador** aplica los filtros y el **Sistema** actualiza la tabla para mostrar solo los eventos que coinciden con los criterios.
5. El **Administrador** hace clic en una fila de un evento para ver más detalles.
6. El **Sistema** muestra una vista detallada (ej. en un modal) con toda la información del evento, que puede incluir:
  - Dirección IP de origen.
  - Agente de usuario (navegador).
  - Datos completos del cambio (ej. un "diff" o los valores "antes" y "después" de una modificación de configuración).
  ### **Postcondición**
1. El Administrador ha podido consultar y analizar la actividad del sistema para su propósito de auditoría o investigación.
2. El log de eventos no ha sido modificado. La interfaz no permite la alteración o eliminación de registros de auditoría.

### **Excepciones (Flujos Alternativos)**
**E1: La búsqueda no devuelve resultados.**
  - En el paso 4, los filtros aplicados por el Administrador no coinciden con ningún evento en la base de datos.
  - El Sistema muestra un mensaje claro en el área de la tabla: "No se encontraron eventos que coincidan con los criterios de búsqueda".
  **E2: El log de eventos es demasiado grande para mostrarlo de una vez.**
  - El Sistema no intentará cargar millones de registros en el navegador. La interfaz implementará paginación por defecto (ej. mostrando 25 o 50 eventos por página) para manejar grandes volúmenes de datos de manera eficiente. El Administrador podrá navegar entre las páginas.
  ### **Rendimiento**
Las consultas y filtrados sobre el log de eventos deben ejecutarse y mostrar resultados en **menos de 5 segundos**, incluso con un volumen de datos de varios meses.

### **Frecuencia**
Baja. Este caso de uso es para tareas específicas de administración, seguridad o depuración, no para operaciones diarias.

### **Comentarios**
- **Inmutabilidad:** El principio fundamental de un log de auditoría es su inmutabilidad. Bajo ninguna circunstancia la aplicación debe permitir la modificación o eliminación de entradas del log a través de esta interfaz.
- **Indexación:** La tabla de la base de datos que almacena los logs (`LogEvento`) debe estar correctamente indexada por `timestamp`, `usuarioId` y `tipoDeEvento` para garantizar el rendimiento de las búsquedas.
- **Eventos a Registrar:** Se deben registrar como mínimo los siguientes eventos: inicios/cierres de sesión, cambios en usuarios/roles, actualizaciones de configuraciones críticas (`ConfigAgente`, `Integracion`), importaciones/exportaciones de datos, y acciones de borrado de entidades principales.


## **ID de Caso de Uso UC-23**

### **Nombre**
Crear Ticket

### **Actor Primario**
Sistema

### **Actor Secundario(s)**
**Sistema** (Invoca `UC-24: Generar Sugerencia de Respuesta`)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Centralizar la lógica para garantizar que todos los tickets, sin importar su origen, se creen de manera consistente y entren correctamente en el flujo de trabajo.
2. **Mitigación de Riesgos Operativos:** Asegurar la integridad de los datos al vincular correctamente el ticket con un cliente, mensaje y orden.

### **Requisitos asociados**
**Funcionales:**
- **RF-TICKET-001, 002, 008:** Implementa la lógica de creación para múltiples canales.
- **RF-TICKET-004:** Lógica de `UPSERT` (crear o actualizar) para el `Cliente`.
- **RF-TICKET-005:** Lógica de vinculación a una `Orden`.
- **RF-FILE-002:** Lógica para almacenar `Archivo`s.

### **Descripción**
Este es un proceso interno y reutilizable que es invocado por otros casos de uso (`UC-01`, `UC-25`) para manejar la creación de un nuevo `Ticket` de soporte. Recibe un conjunto de datos (información del cliente, mensaje, adjuntos), los valida, y crea los registros correspondientes en la base de datos, dejando el ticket listo para el siguiente paso del flujo: el análisis por IA.

### **Precondición**
1. Otro proceso del sistema ha invocado este caso de uso.
2. Se ha proporcionado un payload de datos que contiene, como mínimo, un email de remitente y el contenido del mensaje.

### **Secuencia Normal (Flujo Principal)**
1. El **Sistema** recibe los datos del ticket a crear (ej. `nombre`, `email`, `asunto`, `cuerpo`, `archivos adjuntos`, `canal de origen`).
2. El **Sistema** realiza una validación de seguridad y de negocio de los datos (ej. sanea el HTML del cuerpo, verifica el formato del email).
3. El **Sistema** busca un `Cliente` en la base de datos usando el `email`.
   1. **Si no existe**, crea un nuevo registro de `Cliente` con el `email` y el `nombre` proporcionados.
   2. **Si existe**, utiliza el `Cliente` encontrado.
4. El **Sistema** crea un nuevo registro de `Ticket` en la base de datos, asociándolo al ID del `Cliente`, y establece su estado inicial como `pendiente_ia`.
5. Si se proporcionó un ID de `Orden` en los datos de entrada, el **Sistema** busca la orden y, si la encuentra, la asocia al `Ticket`.
6. El **Sistema** crea un registro de `Mensaje` con el contenido del `asunto` y `cuerpo`, asociándolo al `Ticket` recién creado.
7. **Si hay archivos adjuntos:**
   1. Para cada archivo, el **Sistema** lo sube al proveedor de almacenamiento (Supabase Storage) a través de su API.
   2. Tras una subida exitosa, el **Sistema** crea un registro `Archivo` en la base de datos con la URL de almacenamiento y los metadatos del archivo.
   3. Asocia cada registro `Archivo` al `Mensaje` creado en el paso 6.
8. El **Sistema** devuelve una confirmación de éxito (con el ID del nuevo ticket) al proceso que lo invocó.

### **Postcondición**
1. Se han creado los registros `Cliente` (si era nuevo), `Ticket`, `Mensaje` y `Archivo` (si aplica) en la base de datos.
2. El `Ticket` está en estado `pendiente_ia`.
3. El proceso que invocó a `UC-23` puede continuar su ejecución (ej. enviar el acuse de recibo).

### **Excepciones (Flujos Alternativos)**
**E1: Datos de entrada inválidos.**
  - En el paso 2, los datos son insuficientes o malformados (ej. falta el email).
  - El proceso falla y devuelve un error al invocador. No se crea ningún registro en la base de datos.
  **E2: Falla la conexión con la base de datos.**
  - En los pasos 3-7, el sistema no puede comunicarse con la base de datos.
  - El proceso falla, revierte cualquier transacción parcial (rollback) y devuelve un error grave al invocador.
  **E3: Falla la subida de un archivo adjunto.**
  - En el paso 7a, el servicio de almacenamiento no está disponible o rechaza el archivo.
  - El ticket y el mensaje se crean igualmente, pero se registra un error interno indicando que el archivo no pudo ser procesado. El proceso puede continuar, pero con una advertencia.
  

## **ID de Caso de Uso UC-24**

### **Nombre**
Generar Sugerencia de Respuesta

### **Actor Primario**
Sistema

### **Actor Secundario(s)**
**Proveedor LLM (OpenRouter)**

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Automatizar el análisis inicial y reducir la carga cognitiva del agente al proveer un borrador de respuesta y etiquetas sugeridas.
2. **Escalar las Operaciones de Soporte:** Aplicar reglas de negocio automáticas (ej. escalado) basadas en el análisis de la IA.
3. **Reducir el Desgaste del Agente (Agent Burnout):** Asistir al agente en las tareas más repetitivas del triaje de tickets.

### **Requisitos asociados**
**Funcionales:**
- **RF-IA-001:** Inicia este proceso tras la creación de un ticket.
- **RF-IA-002:** Utiliza la `ConfigAgente` para construir el prompt.
- **RF-IA-003:** Almacena la respuesta del LLM en el `Ticket`.
- **RF-IA-004:** Cambia el estado del ticket a `ia_sugerido`.
- **RF-IA-005:** Implementa la lógica de escalado automático.
**Interfaces:**
- **API-03:** Se comunica con la API de OpenRouter.
- **COM-02:** Notifica al frontend vía SSE/WebSocket.

### **Descripción**
Este proceso asíncrono se activa después de la creación de un ticket. El sistema recopila todo el contexto relevante del ticket, selecciona la configuración de agente IA apropiada, construye un prompt y lo envía a un servicio LLM externo. Al recibir la respuesta, la procesa, actualiza el ticket con las sugerencias y cambia su estado para que aparezca en la cola de triaje del agente de Nivel 1.

### **Precondición**
1. Un `Ticket` existe en la base de datos en estado `pendiente_ia`.
2. Las credenciales de la API del Proveedor LLM están configuradas y son válidas.
3. Existe al menos una `ConfigAgente` activa en el sistema.

### **Secuencia Normal (Flujo Principal)**
1. El **Sistema** (a través de un worker de tareas en segundo plano) recoge un `Ticket` del estado `pendiente_ia`.
2. El **Sistema** consulta la base de datos para obtener el contexto completo: el `Mensaje` inicial, datos del `Cliente` (incluido su historial si es relevante) y detalles de la `Orden` si está vinculada.
3. El **Sistema** selecciona la `ConfigAgente` más adecuada (ej. "Agente de Devoluciones") basándose en palabras clave del asunto o cuerpo del mensaje. Si no encuentra una específica, usa la configuración por defecto.
4. El **Sistema** construye el prompt final, inyectando el contexto recopilado en la plantilla de la `ConfigAgente` seleccionada.
5. El **Sistema** realiza una llamada a la API del **Proveedor LLM** (`API-03`), enviando el prompt.
6. El **Proveedor LLM** procesa la solicitud y devuelve una respuesta estructurada (JSON) que contiene el texto de la respuesta sugerida, un nivel de confianza, etiquetas sugeridas y una bandera de escalado (`escalate: true/false`).
7. El **Sistema** recibe y valida la respuesta del LLM.
8. El **Sistema** actualiza el registro del `Ticket` en la base de datos, guardando la información recibida en los campos `respuestaSugeridaIA`, `confianzaIA`, `etiquetasSugeridasIA`, etc.
9. El **Sistema** aplica la lógica de escalado automático (`RF-IA-005`).
   1. **Si** se cumple alguna condición de escalado (ej. `escalate: true`, confianza baja, palabras clave sensibles, adjunto de imagen), el estado del ticket se cambia a `escalado_nivel_2`.
   2. **Si no**, el estado del ticket se cambia a `ia_sugerido`.
10. El **Sistema** emite un evento en tiempo real (`COM-02`) para notificar a las interfaces de usuario que el ticket ha sido actualizado y está listo para revisión.

### **Postcondición**
1. El `Ticket` se ha actualizado con las sugerencias de la IA.
2. El estado del `Ticket` es ahora `ia_sugerido` o `escalado_nivel_2`.
3. El ticket es visible en la cola de trabajo correspondiente (Triaje o Especialista).

### **Excepciones (Flujos Alternativos)**
**E1: Falla la comunicación con el Proveedor LLM.**
  - En el paso 5, la API del LLM no está disponible o devuelve un error.
  - El Sistema reintenta la llamada un número configurable de veces. Si todos los intentos fallan, cambia el estado del `Ticket` a `error_ia` y notifica a los administradores.
  **E2: El Proveedor LLM tarda demasiado en responder.**
  - En el paso 6, se excede el tiempo de espera (timeout).
  - El Sistema trata esto como una falla de comunicación (ver E1).
  **E3: La respuesta del LLM es inválida.**
  - En el paso 7, la respuesta no es un JSON válido o carece de los campos esperados.
  - El Sistema no puede procesar la respuesta. Cambia el estado del `Ticket` a `error_ia` y registra el contenido de la respuesta inválida para su depuración.
  

## **ID de Caso de Uso UC-25**

### **Nombre**
Notificar Nuevo Email

### **Actor Primario**
Sistema de Email (Mailgun)

### **Actor Secundario(s)**
**Sistema** (Para la orquestación y decisión de invocar `UC-23` o `UC-03`)

### **Objetivos asociados**
1. **Optimizar la Eficiencia Operativa:** Orquestar el flujo de entrada, diferenciando entre nuevos tickets y respuestas para prevenir la duplicación y mantener conversaciones ordenadas.
2. **Mitigación de Riesgos Operativos:** Actuar como un punto de entrada seguro y fiable para todo el soporte basado en correo electrónico.

### **Requisitos asociados**
**Funcionales:**
- **RF-TICKET-001:** Desencadena la creación de un ticket para nuevos correos.
- **RF-TICKET-003:** Implementa la lógica de enrutamiento para correos de respuesta.
**Interfaces:**
- **API-02:** Define la existencia de este endpoint de webhook.

### **Descripción**
Este proceso se inicia cuando el proveedor de correo externo (Mailgun) notifica al sistema, a través de un webhook, sobre la llegada de un nuevo correo electrónico. El sistema recibe los datos del correo, determina si corresponde a un ticket nuevo o a una respuesta de un ticket existente, e invoca el caso de uso apropiado para su procesamiento.

### **Precondición**
1. El webhook de Mailgun está correctamente configurado para apuntar al endpoint `POST /webhooks/mailgun/inbound` de NoraAI.
2. El endpoint está desplegado y es accesible públicamente.

### **Secuencia Normal (Flujo Principal)**
1. El **Sistema de Email** recibe un correo dirigido a la dirección de soporte y envía una solicitud HTTP POST al endpoint del webhook de NoraAI.
2. El **Sistema** recibe la solicitud y primero verifica su autenticidad (ej. mediante la firma de la carga útil de Mailgun) para prevenir ataques.
3. El **Sistema** parsea el payload JSON para extraer las cabeceras (`In-Reply-To`, `References`, `Subject`) y el contenido del correo.
4. El **Sistema** ejecuta la lógica de enrutamiento:
   1. Busca en las cabeceras `In-Reply-To` o `References` un ID de mensaje conocido.
   2. Si no lo encuentra, busca en el `Subject` un patrón de ID de ticket (ej. `[Ticket #ABC-123]`).
5. **Si se encuentra una referencia a un ticket existente** (flujo alternativo `A1` que se convierte en principal para `UC-03`):
   1. El **Sistema** invoca el caso de uso **`UC-03: Responder a un Ticket (Correo) Existente`**, pasándole los datos del correo.
6. **Si no se encuentra ninguna referencia a un ticket existente:**
   1. El **Sistema** determina que es una nueva solicitud de soporte.
   2. Invoca el caso de uso **`UC-23: Crear Ticket`**, pasándole los datos extraídos del correo (remitente, asunto, cuerpo, adjuntos).
7. El **Sistema** responde al **Sistema de Email** con un código de estado `200 OK` para confirmar que el webhook ha sido recibido y aceptado para procesamiento.

### **Postcondición**
1. Se ha invocado el caso de uso `UC-23` o `UC-03`.
2. Se ha enviado una respuesta `200 OK` al proveedor de correo, evitando que intente reenviar el webhook.

### **Excepciones (Flujos Alternativos)**
**E1: La firma del webhook es inválida.**
  - En el paso 2, la autenticación falla.
  - El Sistema rechaza la solicitud con un código de error `403 Forbidden`, la ignora y registra un intento de acceso no autorizado.
  **E2: El payload del webhook está malformado.**
  - En el paso 3, el JSON no puede ser parseado.
  - El Sistema responde con un código `400 Bad Request` para indicar que la solicitud del cliente (Mailgun) es incorrecta.
  **E3: Falla un proceso interno invocado.**
  - En los pasos 5 o 6, el caso de uso invocado (`UC-23` o `UC-03`) devuelve un error grave (ej. la base de datos está caída).
  - El Sistema responde al webhook con un código `500 Internal Server Error`. Esto le indica a Mailgun que el procesamiento falló por un problema del servidor y que debe reintentar enviar el webhook más tarde.
