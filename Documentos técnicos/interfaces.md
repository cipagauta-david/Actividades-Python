
## 1. Interfaces de Usuario (UI)

Las interfaces de usuario son el corazón de la experiencia para Brenda y Carlos. Deben ser diseñadas para la máxima eficiencia y claridad.

**Enfoque de Dashboards por Rol (Decisión MVP):**
Para el MVP, se ha decidido implementar **Paneles Fijos por Rol (Role-Based Dashboards)**. Esto significa que el sistema presentará un conjunto de gráficas y métricas predefinidas y optimizadas para cada rol (Administrador y Agente), sin ofrecer personalización por parte del usuario final. Este enfoque (Nivel 1) ofrece el máximo valor para la demo con una complejidad técnica baja, evitando el riesgo de implementar paneles configurables por el usuario (Nivel 2), que exceden el alcance de este proyecto.

### UI-01: Dashboard del Administrador (Vista Estratégica)
*   **Estado:** Aprobado y Detallado.
*   **Propósito Principal:** Monitorear la salud general del sistema de soporte, identificar cuellos de botella y medir el rendimiento del equipo desde una vista de alto nivel.
*   **Componentes Clave:**
    *   **Widget 1: KPIs Generales (Hoy/Últimos 7 días):**
        *   Tickets Creados
        *   Tickets Resueltos
        *   Tiempo Medio de Primera Respuesta
        *   Tiempo Medio de Resolución
        *   *Fuente de datos: Vista `AgregadoDiarioTicket`.*
    *   **Widget 2: Carga de Trabajo Actual:**
        *   Gráfico de barras mostrando el número de tickets en cada estado (`nuevo`, `ia_sugerido`, `escalado_nivel_2`, `cerrado`).
        *   *Fuente de datos: Query `count` y `groupBy` sobre la tabla `Ticket`.*
    *   **Widget 3: Rendimiento del Equipo:**
        *   Tabla simple mostrando: `Agente`, `Tickets Asignados`, `Tickets Resueltos Hoy`.
        *   *Fuente de datos: Query `count` y `groupBy` sobre la tabla `Ticket` por `assigneeId`.*
    *   **Widget 4: Distribución de Tickets:**
        *   Gráfico de pastel por `Canal` (Email, Web, etc.).
        *   Gráfico de pastel por `Etiqueta` (WISMO, Devolución, etc.).
        *   *Fuente de datos: Query `count` y `groupBy` sobre la tabla `Ticket`.*

### UI-02: Dashboard del Agente (Vista Táctica y Operativa)
*   **Estado:** Aprobado y Detallado.
*   **Propósito Principal:** Permitir al agente entender su carga de trabajo personal de un vistazo, medir su propio rendimiento y acceder rápidamente a sus colas de trabajo.
*   **Componentes Clave:**
    *   **Widget 1: Mis Métricas (Hoy):**
        *   Mis Tickets Resueltos
        *   Mis Tickets Asignados
        *   Mi Tiempo Promedio de Respuesta
        *   *Fuente de datos: Query filtrada por `assigneeId` en la tabla `Ticket`.*
    *   **Widget 2: Mis Colas de Trabajo:**
        *   Tarjetas de acceso rápido con contadores, mostrando las colas más importantes:
            *   `[X] Tickets Reabiertos` (Máxima prioridad)
            *   `[Y] Respuestas de Clientes`
            *   `[Z] Tickets para Triaje (Nivel 1)`
            *   `[A] Mis Tickets Escalados (Nivel 2)`
            *   `[B] Esperando Respuesta del Cliente`
        *   *Fuente de datos: Queries `count` específicas por estado (`reabierto`, `respuesta_cliente`, etc.).*
    *   **Widget 3: Actividad Reciente en Mis Tickets:**
        *   Una lista simple de notificaciones: "El cliente de Ticket #123 ha respondido", "Se te ha asignado el Ticket #456".
        *   *Fuente de datos: Tabla `LogEvento` filtrada por tickets asignados al agente.*

### UI-03: Vista de Triaje de Agente (Nivel 1)
*   **Estado:** Aprobada y Detallada.
*   **Propósito Principal:** Permitir al agente de Nivel 1 (Brenda) procesar las sugerencias de la IA a la máxima velocidad posible, actuando como un validador humano.
*   **Componentes Clave:**
    1.  **Cola de Tickets (`ia_sugerido`):**
        *   Una lista de tickets. Cada fila debe mostrar: `Asunto`, `Cliente`, `ConfianzaIA` (ej. "95%"), `Etiquetas Sugeridas` ("WISMO") y un indicador visual de urgencia.
        *   La lista debe estar **ordenada por defecto por `confianzaIA` descendente**, para que el agente revise primero las sugerencias más seguras.
    2.  **Panel de Decisión (Vista Dividida):**
        *   **Izquierda (Contexto):** Historial completo de la conversación, archivos adjuntos visibles y un panel con la información clave de la `Orden` vinculada (estado, tracking, artículos).
        *   **Derecha (Acción):**
            *   **Banner de Sugerencia de Fusión:** Si `sugerenciaFusionId` existe, mostrar una alerta prominente con acciones para fusionar o ignorar.
            *   **Editor de Texto:** Pre-cargado con el contenido de `respuestaSugeridaIA` (del último mensaje del cliente).
            *   **Panel de Metadatos de IA:** Muestra `confianzaIA`, `metaDatosIA` (el "porqué" de la IA) y las etiquetas sugeridas.
            *   **Botones de Acción Rápida:**
                *   `[✅ Aprobar y Enviar]`
                *   `[✏️ Editar y Enviar]`
                *   `[➡️ Escalar a Nivel 2]`
                *   `[👤 Reasignar a...]` (con un selector de agentes)

### UI-04: Vista de Especialista de Agente (Nivel 2)
*   **Estado:** Aprobada y Detallada.
*   **Propósito Principal:** Proveer a los agentes de Nivel 2 (Carlos) una vista clara de los casos complejos que requieren intervención manual, con herramientas para una resolución eficiente.
*   **Componentes Clave:**
    1.  **Vista de Cola (Tabla):**
        *   Muestra tickets con estado `escalado_nivel_2` y `en_progreso_nivel_2`.
        *   Columnas: `Prioridad`, `Asunto`, `Cliente`, `Agente Asignado`, `Fecha de Creación`.
        *   Funcionalidades: Filtrado por etiqueta, búsqueda y ordenamiento.
    2.  **Modo "Flujo Continuo" (Opcional pero recomendado):**
        *   Un botón para activar/desactivar este modo.
        *   Al activarse, la UI presenta un ticket a la vez, siguiendo la **lógica de la cola de prioridad** definida en la sección `5.3` del plan (4 Urgentes, 3 Altas, etc.).
        *   Tras resolver un ticket (enviar mensaje o cerrar), el siguiente aparece automáticamente.

### UI-05: Interfaz de Importación de CSV
*   **Estado:** Aprobada y Detallada.
*   **Propósito Principal:** Permitir la carga masiva de datos de `Ordenes` de forma sencilla y a prueba de errores, un requisito clave para que el agente de IA pueda responder a consultas "WISMO".
*   **Componentes Clave (Flujo en 3 pasos):**
    1.  **Paso 1: Subida de Archivo:**
        *   Un componente de "arrastrar y soltar" o un selector de archivos para el CSV.
    2.  **Paso 2: Mapeo y Previsualización:**
        *   El sistema lee las cabeceras del CSV y muestra una tabla con las primeras 5-10 filas.
        *   Para cada columna de la base de datos (`estado`, `numeroSeguimiento`, etc.), se muestra un menú desplegable para que el usuario seleccione la columna correspondiente del CSV.
    3.  **Paso 3: Validación e Importación:**
        *   Al hacer clic en "Importar", se realiza una validación en el frontend (con `Papaparse`) para errores de formato básicos.
        *   Se envía el archivo al backend. La UI muestra una barra de progreso.
        *   Al finalizar, se muestra un resumen: `Registros importados`, `Registros omitidos` y un enlace para descargar un `errores.csv` si los hubo.

### A. Interfaces de Configuración y Administración del Sistema

Estas son las palancas y diales que el administrador usará para ajustar el comportamiento del sistema, especialmente el del motor de IA. Son el "panel de control del superpoder".

#### UI-06: Gestión del Agente de IA (`ConfigAgente`)
*   **Estado:** **Crítica para la Flexibilidad.**
*   **Propósito Principal:** Permitir a un administrador (o a un desarrollador en la fase inicial) **ajustar y mejorar los prompts y las reglas del agente de IA** sin necesidad de redesplegar el código. La calidad de las respuestas de la IA dependerá 100% de esta configuración.
*   **Componentes Clave:**
    1.  **Lista de Configuraciones de Agente:** Una tabla que muestre los agentes existentes (ej. "Agente WISMO", "Agente Devoluciones").
    2.  **Formulario de Edición:**
        *   `Nombre`: Un nombre descriptivo.
        *   `Descripción`: Para explicar qué hace este agente.
        *   `Prompt Base`: Un área de texto grande (`<textarea>`) para editar el prompt principal. Idealmente, debería soportar variables como `{{nombre_cliente}}` o `{{numero_orden}}` para que el backend las reemplace.
        *   `Umbral de Confianza`: Un campo numérico (de 0 a 1) para ajustar el umbral a partir del cual se considera una respuesta como de alta confianza.
        *   `Prompts por canal`: Un editor JSON para definir prompts específicos por canal.

#### UI-07: Gestión de Plantillas (`Plantilla`)
*   **Estado:** **Recomendada para Eficiencia.**
*   **Propósito Principal:** Permitir a los agentes crear y gestionar respuestas predefinidas (canned responses) para situaciones que no maneja la IA o para cuando editan una sugerencia. Esto ahorra tiempo en la resolución manual de tickets de Nivel 2.
*   **Componentes Clave:**
    *   Una interfaz CRUD (Crear, Leer, Actualizar, Borrar) para las plantillas.
    *   Cada plantilla tendría: `Nombre`, `Asunto` y `Cuerpo` (con un editor de texto enriquecido básico).
    *   **Integración:** En la vista de resolución de tickets (UI-04), debería haber un botón "Insertar Plantilla" que abra un buscador de estas respuestas.

#### UI-08: Gestión de Usuarios y Roles (`Usuario`)
*   **Estado:** **Crítica para la Administración.**
*   **Propósito Principal:** Administrar quién tiene acceso al sistema y con qué nivel de permisos.
*   **Componentes Clave:**
    *   Una tabla de usuarios que muestre `Nombre`, `Correo`, `Rol` (`AGENTE`, `ADMINISTRADOR`).
    *   Funcionalidad para invitar nuevos usuarios (que se registrarían vía Supabase Auth).
    *   Funcionalidad para cambiar el rol de un usuario existente.

#### UI-09: Gestión de Etiquetas (`Etiqueta`)
*   **Estado:** Recomendada.
*   **Propósito Principal:** Permitir a los administradores mantener una lista limpia y consistente de etiquetas para la categorización de tickets.
*   **Componentes Clave:**
    *   Interfaz CRUD simple para crear, renombrar o eliminar etiquetas.
    *   Opcional: Funcionalidad para fusionar etiquetas duplicadas (ej. "devolucion" y "devoluciones").

---

### B. Interfaces de Gestión de Datos Maestros

El sistema necesita una forma de ver y gestionar los datos centrales del negocio más allá de la importación inicial.

#### UI-10: Vista de Clientes (CRM Ligero)
*   **Estado:** **Altamente Recomendada.**
*   **Propósito Principal:** Dar a los agentes una visión de 360 grados del cliente. Cuando un agente abre un ticket, necesita ver el historial completo de esa persona para dar un soporte contextualizado y de calidad.
*   **Componentes Clave:**
    1.  **Página de Perfil del Cliente:**
        *   Información de contacto (`Nombre`, `Correo`, `Teléfono`).
        *   Una lista de **todas las órdenes** asociadas a ese cliente.
        *   Un historial de **todos los tickets** previos del cliente, con su estado final.

#### UI-11: Vista de Órdenes
*   **Estado:** Recomendada.
*   **Propósito Principal:** Complementar la importación CSV. Permite a un agente buscar una orden específica por su ID o por el correo del cliente, y ver o editar sus detalles (ej. añadir manualmente un número de seguimiento).
*   **Componentes Clave:**
    *   Una tabla de órdenes con capacidad de búsqueda y filtrado.
    *   Una vista de detalle de la orden que muestre su estado, artículos, tracking y el ticket asociado.

---

### C. Interfaces Públicas (Orientadas al Cliente)

Has diseñado excelentemente la experiencia del agente. Ahora debemos definir formalmente lo que el cliente final ve.

#### UI-12: Formulario Web Público para Creación de Tickets
*   **Estado:** **Crítica.**
*   **Propósito Principal:** Proporcionar un canal de entrada de tickets, alternativo al correo electrónico, directamente desde el sitio web de la empresa.
*   **Componentes Clave:**
    *   Un formulario simple embebible.
    *   Campos: `Nombre`, `Correo electrónico`, `Número de orden (opcional)`, `Asunto`, `Mensaje`.
    *   Un campo para adjuntar archivos.
    *   Al enviarse, crea un ticket con `Canal.web`.

#### UI-13: Plantillas de Correo Electrónico al Cliente (Transaccionales)
*   **Estado:** **Crítica.**
*   **Propósito Principal:** Son la "voz" del sistema hacia el cliente. No son interfaces gráficas, pero su diseño (contenido y branding) es fundamental.
*   **Componentes Clave (Templates a diseñar en HTML):**
    1.  **Email de Acuse de Recibo:** "Hemos recibido tu ticket (#{{ticket.id}}). Nuestro equipo lo está revisando."
    2.  **Email de Respuesta del Agente:** El contenedor para las respuestas enviadas desde la plataforma.
    3.  **Email de Cierre de Ticket:** "Tu solicitud #{{ticket.id}} ha sido resuelta. Si tienes más preguntas, responde a este correo para reabrirlo."

### Priorización para el MVP

No es necesario que construyan todas estas interfaces con un CRUD completo para la primera entrega. Aquí tienes un enfoque pragmático:

1.  **Críticas (Deben existir de alguna forma):**
    *   **UI-12 (Formulario Público) y UI-13 (Plantillas de Email):** Son la cara visible del sistema. Son indispensables.
    *   **UI-08 (Gestión de Usuarios):** Puede ser simplificado. En lugar de una UI completa, pueden manejarlo con un **script de `seed`** que cree los usuarios iniciales (Brenda, Carlos, Admin). Esto es suficiente para la demo.
    *   **UI-06 (Gestión del Agente IA):** Al igual que con los usuarios, para el MVP basta con que los prompts estén **sembrados en la base de datos a través del script de `seed`**. La capacidad de editarlos en una UI es una mejora para el futuro, pero para la demo, tenerlos fijos es aceptable.

2.  **Altamente Recomendadas (Aportan gran valor a la demo):**
    *   **UI-10 (Vista de Clientes):** Tener un enlace en la vista del ticket que lleve a un historial simple del cliente hará que la demo sea mucho más impactante. Muestra que han pensado en el contexto del agente.

3.  **Recomendadas y Postergables:**
    *   **UI-07 (Plantillas), UI-09 (Etiquetas), UI-11 (Órdenes):** El CRUD completo para estos elementos puede ser implementado post-MVP. Para la demo, los datos iniciales pueden ser cargados vía `seed`.

---

## 2. Interfaces de Software (API)

Esta sección define el contrato **RESTful API** entre el frontend de React y el backend de NestJS. Todos los endpoints estarán prefijados con `/api/v1` y requerirán un token JWT de Supabase Auth en la cabecera `Authorization`, a menos que se indique lo contrario.

### A. Endpoints de Dashboards y Vistas Agregadas

Estos endpoints están diseñados para la eficiencia, proporcionando datos pre-agregados para las vistas de dashboard y evitando múltiples peticiones desde el frontend.

#### API-01: Datos para Dashboard del Administrador (Ref: UI-01)
*   **Endpoint:** `GET /dashboards/admin`
*   **Rol Requerido:** `ADMINISTRADOR`
*   **Propósito:** Provee todos los datos necesarios para renderizar la UI-01 en una sola petición.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "kpis": {
        "today": { "created": 85, "resolved": 70, "avgFirstResponseTime": 15, "avgResolutionTime": 120 },
        "last7Days": { "created": 600, "resolved": 580, "avgFirstResponseTime": 25, "avgResolutionTime": 180 }
      },
      "workload": [
        { "status": "nuevo", "count": 10 },
        { "status": "ia_sugerido", "count": 5 },
        { "status": "escalado_nivel_2", "count": 8 },
        { "status": "cerrado", "count": 250 }
      ],
      "teamPerformance": [
        { "assigneeId": "uuid-brenda", "agentName": "Brenda", "assigned": 5, "resolvedToday": 12 },
        { "assigneeId": "uuid-carlos", "agentName": "Carlos", "assigned": 8, "resolvedToday": 9 }
      ],
      "distribution": {
        "byChannel": [{ "channel": "correo", "count": 450 }, { "channel": "formulario_web", "count": 150 }],
        "byTag": [{ "tag": "WISMO", "count": 300 }, { "tag": "Devolución", "count": 150 }]
      }
    }
    ```

#### API-02: Datos para Dashboard del Agente (Ref: UI-02)
*   **Endpoint:** `GET /dashboards/agent`
*   **Rol Requerido:** `AGENTE`
*   **Propósito:** Provee los datos personalizados para el agente que realiza la petición. El backend identificará al agente a través del JWT.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "myMetricsToday": { "resolved": 12, "assigned": 5, "avgResponseTime": 18 },
      "myQueues": {
        "forTriage": 5,
        "reopened": 2,
        "customerReplied": 7,
        "myEscalated": 8,
        "waitingForCustomer": 15
      },
      "recentActivity": [
        { "eventId": "uuid", "message": "Cliente respondió en Ticket #123", "timestamp": "2023-10-27T10:00:00Z" },
        { "eventId": "uuid", "message": "Se te asignó el Ticket #456", "timestamp": "2023-10-27T09:30:00Z" }
      ]
    }
    ```

#### API-02.1: Siguiente Ticket para "Flujo Continuo" (Ref: UI-04)
*   **Endpoint:** `GET /tickets/next-in-flow`
*   **Rol Requerido:** `AGENTE`
*   **Propósito:** Encapsula la lógica de la cola de "Flujo Continuo" (4 Urgentes, 3 Altas, etc.) en el servidor, devolviendo el siguiente ticket más apropiado para el agente que realiza la llamada.
*   **Respuesta Exitosa (200 OK):** El objeto completo del ticket o `204 No Content` si no hay tickets en la cola.

### B. Endpoints del Flujo de Tickets

Estos son los endpoints operativos que los agentes usarán constantemente a través de las UIs de gestión de tickets.

#### API-03: Gestión de Tickets (Ref: UI-03, UI-04)
*   **Listar Tickets:** `GET /tickets`
    *   **Propósito:** Obtener listas de tickets. Es la base para todas las colas.
    *   **Parámetros de Query:**
        *   `estado`: Filtra por estado (ej. `ia_sugerido`, `escalado_nivel_2`). Acepta valores múltiples separados por coma.
        *   `asignadoA`: Filtra por ID de agente (o `me` para el usuario actual).
        *   `sort`: Ordena los resultados (ej. `-confianzaIA` para descendente, `prioridad` para ascendente).
        *   `pagina`, `limite`: Para paginación.
*   **Obtener un Ticket:** `GET /tickets/:id`
    *   **Propósito:** Obtener el detalle completo de un ticket, incluyendo mensajes, cliente, orden asociada y archivos.
*   **Acciones sobre un Ticket:** `POST /tickets/:id/actions/:action`
    *   **Propósito:** Realizar acciones específicas que cambian el estado o la asignación de un ticket. Esto sigue el patrón de "Comandos" y es más explícito que usar `PUT` o `PATCH` para todo.
    *   **Endpoints de Acción:**
        *   `POST /tickets/:id/actions/approve`: **Aprobar y Enviar (Ref: UI-03).**
            *   **Payload:** `{ "editedBody": "Texto opcionalmente modificado por el agente." }`
            *   **Lógica:** Si `editedBody` es `undefined`, se usa la `respuestaSugeridaIA` del mensaje y el mensaje saliente se marca como `esAutomatico = true`. Si `editedBody` es una `string` (incluida `""`), se usa su valor y se marca como `esAutomatico = false`. El backend debe validar que el cuerpo no esté vacío antes de enviar.
        *   `POST /tickets/:id/actions/escalate`: **Escalar a Nivel 2 (Ref: UI-03).**
            *   **Payload:** `{ "internalNote": "La IA no entendió el problema real del cliente." }`
        *   `POST /tickets/:id/actions/reassign`: **Reasignar (Ref: UI-03).**
            *   **Payload:** `{ "assigneeId": "uuid-carlos", "internalNote": "Carlos es el experto en este producto." }`
        *   `POST /tickets/:id/actions/claim`: **Tomar Ticket (Nivel 2).**
            *   **Payload:** `{}`
            *   **Lógica:** Cambia el estado del ticket de `escalado_nivel_2` a `en_progreso_nivel_2` y se lo asigna al agente que realiza la llamada.
        *   `POST /tickets/:targetTicketId/actions/merge`: **Fusionar Ticket.**
            *   **Payload:** `{ "sourceTicketId": "uuid-del-ticket-a-fusionar" }`
        *   `POST /tickets/:id/actions/dismiss-merge`: **Ignorar Sugerencia de Fusión.**
            *   **Payload:** `{}`
*   **Crear un Mensaje (Responder):** `POST /tickets/:id/messages`
    *   **Propósito:** Para que un agente de Nivel 2 envíe una respuesta manual.
    *   **Payload:** `{ "body": "Texto de la respuesta.", "isInternalNote": false, "attachmentIds": ["uuid-archivo1"] }`

### C. Endpoints de Gestión y Configuración

Estos son los endpoints CRUD para las interfaces administrativas.

#### API-04: Gestión del Agente de IA (Ref: UI-06)
*   **Endpoints:**
    *   `GET /config/agents`
    *   `POST /config/agents`
    *   `GET /config/agents/:id`
    *   `PUT /config/agents/:id`
    *   `DELETE /config/agents/:id` (Borrado lógico preferido)

#### API-05: Gestión de Plantillas (Ref: UI-07)
*   **Endpoints:**
    *   `GET /templates`
    *   `POST /templates`
    *   ... (CRUD completo) ...

#### API-06: Gestión de Usuarios (Ref: UI-08)
*   **Endpoints:**
    *   `GET /users`
    *   `POST /users/invite` (El backend se comunica con Supabase Auth para enviar la invitación)
    *   `PUT /users/:id/role`
        *   **Payload:** `{ "role": "ADMINISTRADOR" }`

#### API-07: Gestión de Etiquetas (Ref: UI-09)
*   **Endpoints:** CRUD completo para `/tags`.

### D. Endpoints de Datos Maestros e Importación

Endpoints para manejar los datos del negocio.

#### API-08: Gestión de Clientes y Órdenes (Ref: UI-10, UI-11)
*   **Endpoints:** CRUD completo para `/customers` y `/orders`.
*   **Detalle del Cliente:** La respuesta de `GET /customers/:id` debe estar anidada para incluir un resumen de sus tickets y órdenes recientes, alimentando la vista 360.

#### API-09: Importación de CSV de Órdenes (Ref: UI-05)
*   **Paso 1: Previsualización:** `POST /imports/orders/preview`
    *   **Tipo de Contenido:** `multipart/form-data`
    *   **Payload:** El archivo CSV.
    *   **Respuesta:** Un JSON con las cabeceras detectadas y las primeras 10 filas para que la UI construya el mapeo.
*   **Paso 2: Ejecución:** `POST /imports/orders/run`
    *   **Tipo de Contenido:** `multipart/form-data`
    *   **Payload:** El archivo CSV y un campo `mapping` con el JSON del mapeo (ej. `{"Order ID": "id", "Tracking": "numeroSeguimiento"}`).
    *   **Respuesta:** `{ "jobId": "uuid-job" }`. La importación se ejecuta en segundo plano.
*   **Paso 3: Estado del Job:** `GET /imports/jobs/:jobId`
    *   **Respuesta:** `{ "status": "processing", "progress": 55, "errors": 0 }` o `{ "status": "completed", "imported": 990, "skipped": 10, "errorFileUrl": "..." }`.

### E. Endpoints Públicos

Endpoints que no requieren autenticación.

#### API-10: Creación de Ticket desde Formulario Web (Ref: UI-12)
*   **Endpoint:** `POST /public/tickets`
*   **Autenticación:** Ninguna (pero con limitación de tasa - rate limiting).
*   **Payload:** `{ "name": "...", "email": "...", "orderId": "...", "subject": "...", "message": "...", "attachmentIds": ["uuid-archivo1"] }`

### F. Endpoints de Utilidades

#### API-11: Subida de Archivos
*   **Endpoint:** `POST /uploads`
*   **Autenticación:** Requerida (`AGENTE` o `ADMINISTRADOR`). Para el formulario público, se necesitará un endpoint `POST /public/uploads` con una política de seguridad más estricta.
*   **Tipo de Contenido:** `multipart/form-data`
*   **Propósito:** Maneja la subida de un único archivo a Supabase Storage.
*   **Respuesta Exitosa (201 Created):** `{ "fileId": "uuid-del-archivo-generado" }`. Este ID se usa luego en los payloads de creación de tickets o mensajes (`attachmentIds`).

---

## 3. Interfaces de Comunicación (COM)

Estas interfaces definen cómo nuestro sistema se comunica con servicios externos (webhooks, emails) y cómo sus componentes internos se comunican entre sí en tiempo real.

### A. Comunicaciones Externas (Hacia/Desde el Mundo)

#### COM-01: Webhook de Email Entrante (Mailgun)
*   **Tipo:** Entrada (Inbound).
*   **Proveedor:** Mailgun.
*   **Endpoint en nuestro sistema:** `POST /webhooks/mailgun/inbound`
*   **Contrato de Payload (Esperado de Mailgun):**
    *   El backend debe estar preparado para parsear un `multipart/form-data` que contiene:
        *   `from`: Correo del remitente.
        *   `recipient`: Correo al que se envió (ej. `soporte@gearup.com`).
        *   `subject`: Asunto del correo.
        *   `body-plain`: Cuerpo del texto plano.
        *   `stripped-html`: Cuerpo del HTML sin las respuestas anteriores.
        *   `attachment-count`: Número de adjuntos.
        *   `attachment-x`: Archivos adjuntos (donde x es un número).
        *   `In-Reply-To`, `References`: Cabeceras clave para identificar si es una respuesta a un hilo existente.
        *   `Message-ID`: Identificador único del mensaje, provisto por el servidor de correo.
*   **Lógica Crítica:** Para garantizar la idempotencia y evitar la creación de mensajes duplicados por reintentos del webhook, el handler extraerá la cabecera `Message-ID` única de Mailgun y la guardará en el campo `fuenteMessageId` del nuevo registro de `Mensaje`. Una violación de la restricción de unicidad en la base de datos indicará que el mensaje ya fue procesado, permitiendo al sistema ignorar el duplicado de forma segura.

#### COM-02: Emails Transaccionales Salientes (Ref: UI-13)
*   **Tipo:** Salida (Outbound).
*   **Proveedor:** Mailgun (o similar).
*   **Disparadores:** Acciones dentro del sistema.
*   **Plantillas Clave y Variables Requeridas:**
    1.  **Acuse de Recibo:**
        *   **Disparador:** Creación de un nuevo ticket desde cualquier canal.
        *   **Variables:** `{{ticket.id}}`, `{{cliente.nombre}}`.
    2.  **Respuesta del Agente:**
        *   **Disparador:** `POST /tickets/:id/actions/approve` o `POST /tickets/:id/messages`.
        *   **Variables:** `{{ticket.id}}`, `{{agente.nombre}}`, `{{mensaje.cuerpo}}`.
    3.  **Notificación de Cierre:**
        *   **Disparador:** Cambio de estado del ticket a `cerrado`.
        *   **Variables:** `{{ticket.id}}`, `{{cliente.nombre}}`.
    4.  **Notificación de Reapertura:**
        *   **Disparador:** El cliente responde a un ticket cerrado.
        *   **Variables:** `{{ticket.id}}`, `{{cliente.nombre}}`.

### B. Comunicaciones Internas (Dentro del Sistema)

#### COM-03: Eventos en Tiempo Real al Frontend (Server-Sent Events)
*   **Tipo:** Comunicación Servidor -> Cliente.
*   **Tecnología:** Server-Sent Events (SSE) es ideal por su simplicidad para notificaciones unidireccionales.
*   **Propósito:** Notificar a las UIs de los agentes sobre cambios relevantes sin necesidad de que el usuario refresque la página, mejorando drásticamente la experiencia operativa.
*   **Canales/Eventos Clave:**
    *   `event: new_ticket_for_triage`
        *   **Datos:** `{ "ticketId": "...", "subject": "...", "confidence": 0.95 }`
        *   **UI Afectada:** UI-03 (para añadir el ticket a la cola).
    *   `event: ticket_assigned_to_me`
        *   **Datos:** `{ "ticketId": "...", "subject": "...", "priority": "alta" }`
        *   **UI Afectada:** UI-02 (para mostrar una notificación emergente y actualizar el contador de la cola).
    *   `event: customer_replied`
        *   **Datos:** `{ "ticketId": "...", "subject": "..." }`
        *   **UI Afectada:** UI-02 (para actualizar la actividad reciente y notificar al agente).
    *   `event: import_job_update`
        *   **Datos:** `{ "jobId": "...", "status": "processing", "progress": 75 }`
        *   **UI Afectada:** UI-05 (para actualizar la barra de progreso).
    *   `event: ticket_reopened`
        *   **Datos:** `{ "ticketId": "...", "assigneeId": "..." }`
        *   **UI Afectada:** UI-02 (Notificación y actualización del contador de la cola "Reabiertos").
    *   `event: merge_suggestion_available`
        *   **Datos:** `{ "ticketId": "...", "suggestedMergeWith": "..." }`
        *   **UI Afectada:** UI-03/04 (Para renderizar el banner de sugerencia de fusión).

---

## 4. Lógica de Negocio Detallada

Esta sección describe la lógica de estado y los flujos de trabajo complejos que gobiernan el comportamiento del sistema.

### 4.1. El Ciclo de Vida del Ticket: Flujo Detallado de Estados

Este es el corazón lógico del sistema. Cada transición está gatillada por un evento específico.

*   **(Evento: Cliente crea comunicación)** → **`nuevo`**
    *   **Descripción:** Un ticket virgen.
    *   **Lógica:** Creado por el webhook de email, formulario web, etc.
    *   **Siguiente Paso:** Entra automáticamente en la cola de procesamiento del worker de IA.

*   **`nuevo`** → **(Acción del Sistema: Worker IA)** → **`ia_sugerido`**
    *   **Descripción:** La IA ha analizado el ticket y generado una sugerencia.
    *   **Lógica:** El worker de IA puebla los campos `respuestaSugeridaIA`, etc. en el `Mensaje` original.
    *   **Siguiente Paso:** Aparece en la cola principal de "Triaje" para los agentes de Nivel 1.

*   **`ia_sugerido`** → **(Acción del Agente: Envía respuesta)** → **`esperando_cliente`**
    *   **Descripción:** Se ha dado una respuesta y ahora la pelota está en el tejado del cliente.
    *   **Lógica:** El agente aprueba, edita o escribe una respuesta. Se crea un `Mensaje` saliente.
    *   **Siguiente Paso:** El ticket sale de las colas activas. Se inicia un temporizador de inactividad (ej. 72 horas).

*   **`ia_sugerido`** → **(Acción del Agente: Escala)** → **`escalado_nivel_2`**
    *   **Descripción:** El agente de Nivel 1 determina que la sugerencia de la IA es incorrecta o el caso es demasiado complejo.
    *   **Lógica:** El agente hace clic en "Escalar". El estado del ticket cambia.
    *   **Siguiente Paso:** El ticket aparece en la cola de Nivel 2 (UI-04) para ser tomado por un especialista.

*   **`escalado_nivel_2`** → **(Acción del Agente N2: Toma el ticket)** → **`en_progreso_nivel_2`**
    *   **Descripción:** Un especialista ha reclamado el ticket y lo está trabajando activamente.
    *   **Lógica:** El agente de Nivel 2 usa la acción "Tomar Ticket". El ticket se le asigna.
    *   **Siguiente Paso:** El ticket permanece en este estado hasta que el especialista envíe una respuesta.

*   **`esperando_cliente`** → **(Evento: Cliente responde)** → **`respuesta_cliente`**
    *   **Descripción:** El cliente ha continuado la conversación.
    *   **Lógica:** El webhook de correo detecta una respuesta en un hilo existente (vía `In-Reply-To`).
    *   **Siguiente Paso:** El ticket aparece en una cola de alta prioridad para el `assigneeId`. **NO pasa por la IA de nuevo.**

*   **`esperando_cliente`** → **(Acción del Sistema: Inactividad)** → **`cerrado`**
    *   **Descripción:** El problema se considera resuelto por silencio del cliente.
    *   **Lógica:** Un cron job periódico busca tickets en `esperando_cliente` cuya `modificadoEn` sea mayor al umbral (ej. 72h). Para evitar condiciones de carrera (race conditions), esta transición debe ser atómica, usando una consulta condicional (ej. `UPDATE Ticket SET estado = 'cerrado' WHERE id = ? AND estado = 'esperando_cliente'`).
    *   **Siguiente Paso:** El ticket se archiva.

*   **`cerrado`** → **(Evento: Cliente responde - "Ticket Zombie")** → **`reabierto`**
    *   **Descripción:** Una alerta. Un problema que se creía resuelto no lo está.
    *   **Lógica:** El webhook de correo detecta una respuesta en un hilo de un ticket `cerrado`.
    *   **Siguiente Paso:** El ticket aparece en una cola especial de "Tickets Reabiertos" de alta visibilidad.

### 4.2. La Lógica de Fusión de Tickets: Manejo de Hilos Rotos

Este enfoque es de **asistencia inteligente**, no de automatización arriesgada.

#### Fase 1: El Algoritmo de Ingesta de Mensajes
Cuando el backend recibe un nuevo mensaje (ej. vía un webhook de email), ejecuta este flujo:
1.  **¿Es una Respuesta Directa?**
    *   Se analizan las cabeceras `In-Reply-To` / `References`.
    *   **SÍ:** Se encuentra el `ticketId` asociado. Se crea el `Mensaje` dentro de ese ticket y se actualiza su estado. Proceso finalizado.
    *   **NO:** Continuar.
2.  **¿Asunto Contiene un ID de Ticket (`#[0-9]+`)?**
    *   Se usa una expresión regular para buscar este patrón.
    *   **SÍ:** Se extrae el `ticketId`. Se crea el `Mensaje` y se actualiza el estado. Proceso finalizado.
    *   **NO:** Se asume que es un hilo nuevo. Se crea un `Ticket` con estado `nuevo` y se asocia el primer `Mensaje`. Continuar.
3.  **Disparar Job de Sugerencia de Fusión (Asíncrono)**
    *   Inmediatamente después de crear el nuevo ticket, se encola un job en segundo plano.
    *   El job ejecuta la siguiente heurística: *"Para este `clienteId`, busca otros tickets actualizados en las últimas 72 horas, cuyo estado NO sea `fusionado`."*
    *   **Si encuentra EXACTAMENTE 1 otro ticket:** Actualiza el ticket recién creado estableciendo su campo `sugerenciaFusionId` al ID del ticket encontrado y dispara el evento SSE `merge_suggestion_available`.
    *   **Si encuentra 0 o más de 1:** No hace nada.

#### Fase 2: La Experiencia del Agente (UI/UX y API)
1.  **Detección en el Frontend:**
    *   Al cargar un ticket (o al recibir el evento SSE), la app comprueba si `sugerenciaFusionId` tiene un valor.
    *   Si lo tiene, renderiza un componente de alerta:
        > 💡 **Sugerencia de Fusión:** Este ticket podría ser una continuación del **[Ticket #{sugerenciaFusionId}]**.
        > `[Ver Ticket Original]` `[Fusionar en Ticket Original]` `[Ignorar Sugerencia]`
2.  **Las Acciones del Agente y sus APIs:**
    *   **Botón `[Fusionar en Ticket Original]`:**
        *   **API Call:** `POST /api/tickets/{sugerenciaFusionId}/actions/merge` con `{ "sourceTicketId": "ID_DEL_TICKET_ACTUAL" }`
        *   **Lógica del Backend:**
            1.  Inicia una transacción de base de datos.
            2.  Reasigna todos los `Mensajes` del `sourceTicketId` al `targetTicketId`.
            3.  Cambia el estado del `sourceTicketId` a `fusionado`.
            4.  Actualiza el estado del `targetTicketId` (a `reabierto` o `respuesta_cliente` según corresponda).
            5.  **Crea un `LogEvento`** en el ticket objetivo para auditar la fusión.
            6.  Finaliza la transacción.
        *   **Resultado en Frontend:** Redirige al agente al ticket original, ahora actualizado.
    *   **Botón `[Ignorar Sugerencia]`:**
        *   **API Call:** `POST /api/tickets/{ID_DEL_TICKET_ACTUAL}/actions/dismiss-merge`
        *   **Lógica del Backend:** Pone `sugerenciaFusionId = NULL` en el ticket.
        *   **Resultado en Frontend:** El banner de alerta desaparece.
### 4.3. Caso de Uso Crítico: Gestión de Hilos Rotos y Tickets Reabiertos (Ejemplo End-to-End)

Este escenario práctico demuestra la resiliencia del sistema frente a un comportamiento común del cliente, validando la interacción entre el modelo de datos, la lógica de negocio, la API y la interfaz de usuario.

**Escenario:** Un cliente continúa una conversación creando un nuevo correo en lugar de responder al hilo existente.

1.  **Lunes, 10:00 AM:** Un cliente (`id: cli_abc`) envía un email con el asunto "Mi app no funciona". El sistema crea el **Ticket #123** con estado `nuevo`.
2.  **10:01 AM:** El worker de IA procesa el ticket, que pasa a estado `ia_sugerido`. La sugerencia de la IA se guarda en el primer mensaje del ticket.
3.  **10:05 AM:** La Agente Ana (Nivel 1) revisa la sugerencia, la edita y envía una respuesta solicitando más detalles. El ticket transita a estado `esperando_cliente`.
4.  **Jueves, 11:00 AM:** Transcurren más de 72 horas sin respuesta del cliente. Un cron job periódico detecta la inactividad y cambia automáticamente el estado del **Ticket #123** a `cerrado`.
5.  **Viernes, 9:00 AM:** El cliente, en lugar de responder al correo original, crea un **nuevo email** con el asunto "Sigue sin funcionar!!".

#### El Sistema en Acción: Lógica de Detección y Fusión

6.  **Recepción y Creación:**
    *   El webhook de Mailgun recibe el nuevo mensaje. El análisis de cabeceras no encuentra un `In-Reply-To` y el asunto no contiene el patrón `#[123]`.
    *   El sistema concluye que es un hilo nuevo y crea el **Ticket #124** para el cliente `cli_abc` en estado `nuevo`.
7.  **Job de Sugerencia Asíncrona:**
    *   Inmediatamente tras la creación del Ticket #124, se encola un job con la tarea: `suggestMerge('ticket_124', 'cli_abc')`.
    *   El job ejecuta la **heurística de fusión mejorada**: "Para el cliente `cli_abc`, buscar tickets actualizados en los últimos 7 días, excluyendo aquellos con estado `fusionado`".
    *   La búsqueda encuentra un único resultado: el **Ticket #123** (estado `cerrado`).
    *   El job actualiza el **Ticket #124** estableciendo su campo `sugerenciaFusionId = 'ticket_123'` y emite un evento `merge_suggestion_available` por SSE.
8.  **Intervención Humana Guiada (Triaje Nivel 1):**
    *   **9:15 AM:** El Agente Bruno, que está de turno, ve el **Ticket #124** aparecer en su cola de triaje (`ia_sugerido`).
    *   En la parte superior de la vista del ticket, la UI renderiza el banner de alerta:
        > 💡 **Sugerencia de Fusión:** Este ticket podría ser una continuación del **[Ticket #123]**. `[Ver Ticket Original]` `[Fusionar]` `[Ignorar]`
9.  **Ejecución de la Fusión:**
    *   Bruno hace clic en el botón `[Fusionar]`.
    *   El frontend ejecuta la llamada a la API: `POST /api/v1/tickets/123/actions/merge` con el payload `{ "sourceTicketId": "124" }`.
10. **Resultado y Consolidación del Contexto:**
    *   El backend ejecuta la lógica de fusión en una transacción:
        1.  Mueve los mensajes y archivos del Ticket #124 al Ticket #123.
        2.  Cambia el estado del Ticket #124 a `fusionado`.
        3.  Cambia el estado del Ticket #123 de `cerrado` a `reabierto`.
        4.  Asegura que la asignación del Ticket #123 se mantenga con la dueña original (Ana).
    *   Bruno es redirigido automáticamente a la vista del **Ticket #123**, que ahora:
        *   Contiene la conversación completa y cronológica.
        *   Aparece en la cola de "Reabiertos", señalando alta prioridad.
        *   Permanece asignado a la Agente Ana, que tiene todo el contexto para continuar.

**Conclusión del Caso de Uso:** El sistema ha gestionado con éxito un hilo roto y un ticket zombie, evitando la creación de información duplicada y proveyendo todo el contexto histórico al agente correcto de forma eficiente.

#### Impacto en la Arquitectura y el Plan de Pruebas

Este caso de uso valida directamente la necesidad y el diseño de:

*   **Schema de BD:** Los campos `sugerenciaFusionId` en `Ticket` y los estados `fusionado` y `reabierto` en `EstadoTicket` son indispensables.
*   **API:** El endpoint `POST /.../actions/merge` es la implementación técnica de esta lógica de negocio.
*   **UI:** El banner de sugerencia en la **UI-03** es la pieza clave que permite la intervención humana informada.
*   **Testing:** Este flujo exacto debe ser replicado en una prueba End-to-End (`Test E: Fusión de Hilos Rotos`) para garantizar su correcto funcionamiento de forma continua.