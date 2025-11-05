Saludos, soy Arquitecto y este es tu plan final:

## Plan de Acción Final: Asistente de Soporte al Cliente Inteligente (NoraAI) para GearUp Gadgets

Este documento consolida todas las decisiones del proyecto, estableciendo un plan de acción definitivo para un MVP (Producto Mínimo Viable) single-tenant, enfocado en funcionalidad, uso de herramientas gratuitas y entrega en un plazo académico de dos meses para un equipo de tres personas.

### 1. Resumen Ejecutivo del Proyecto
*   **Nombre del Proyecto:** Asistente de Soporte al Cliente Inteligente (NoraAI).
*   **Propósito Principal:** Construir una aplicación web para "GearUp Gadgets", una empresa ficticia de e-commerce, que automatiza el soporte al cliente. El sistema ingesta tickets vía email y un formulario web público, genera respuestas automáticas con un agente LLM configurable, y permite la supervisión y escalado a un agente humano a través de un dashboard.
*   **Público Objetivo (Problema de Negocio):** El equipo de soporte de GearUp Gadgets (compuesto por dos agentes, "Brenda" y "Carlos") está sobrecargado respondiendo las mismas cuatro preguntas repetitivas:
    1.  **"¿Dónde está mi pedido?" (WISMO):** La consulta más frecuente.
    2.  **"¿Cómo devuelvo este producto?":** Preguntas sobre el proceso de RMA.
    3.  **"¿Este accesorio es compatible con mi dispositivo?":** Consultas de pre-venta.
    4.  **"Mi producto llegó dañado":** Reclamos que requieren gestión de fotos y reemplazos.
    El objetivo del MVP es darle a Brenda y Carlos un "superpoder" para despachar el 80% de estos tickets con un solo clic, sin reemplazarlos.
*   **Alcance del MVP (Enfoque Pragmático):**
    El diseño de este proyecto es ambicioso para un equipo de tres personas en un plazo limitado. La orquestación de múltiples servicios, la creación de artefactos académicos y el desarrollo de código funcional en paralelo representa un riesgo alto. Por ello, el alcance se ha definido con un enfoque pragmático para garantizar la entrega, priorizando la evidencia reproducible sobre la complejidad de la infraestructura.
    *   **Funcionalidades Imprescindibles (En Alcance):**
        1.  **Recepción de Tickets:** Webhook de Mailgun (apoyado por modo `console-mail` para desarrollo) y un formulario web público.
        2.  **Importación de Datos:** Carga de órdenes vía archivo CSV con una interfaz de previsualización.
        3.  **Dashboard del Agente:** Flujo central de listar tickets, ver la propuesta del LLM (mock) y el ciclo de "Aprobar/Editar y Enviar".
        4.  **Integración con LLM:** Implementación de la conexión con OpenRouter para demostrar la capacidad técnica, aunque la demo principal utilice mocks locales.
        5.  **Autenticación:** Sistema de login y roles gestionado con Supabase Auth.
        6.  **Reportes Básicos:** Exportación a CSV y un reporte simple en formato HTML.
        7.  **Artefactos Académicos:** Toda la documentación requerida (BPMN, ERD, SRS, manuales) es crítica para la evaluación.
    *   **Funcionalidades Postergadas (Fuera del Alcance del MVP):**
        1.  **Integraciones Avanzadas:** La conexión con WhatsApp, n8n y conectores directos a plataformas de e-commerce (Shopify, Magento) quedan para una Fase 2.
        2.  **Generación de PDF:** Se elimina del alcance del MVP. Si se necesita un ejemplo, se generará localmente.

### 2. Arquitectura, Stack Tecnológico y Hosting
*   **Backend:** **NestJS (TypeScript)** con **Prisma** como ORM.
*   **Frontend:** **React** con **Vite** y **Tailwind CSS** para un dashboard responsive.
*   **Base de Datos:** **PostgreSQL**.
    *   **Nota de Implementación:** Para simplificar la configuración, las credenciales y la red, se utilizará una única instancia de base de datos PostgreSQL, siendo la proporcionada por Supabase la candidata ideal para unificar la DB de la aplicación con la de autenticación.
*   **Autenticación:** **Supabase Auth**. Simplifica la gestión de usuarios y seguridad, permitiendo validar tokens JWT en el backend de NestJS.
*   **Almacenamiento de Archivos:** **Supabase Storage**.
*   **Procesamiento en Segundo Plano:** **Worker simple en memoria.**
*   **Integración de LLM:** Capa de adaptación (Adapter) que soporte:
    *   **Primario (Para la Demo):** **Mocks locales deterministas.** Para garantizar una demostración fluida, predecible y sin dependencias externas, el adaptador operará leyendo respuestas predefinidas desde archivos JSON.
    *   **Secundario (Funcionalidad Requerida):** **OpenRouter.** La integración real con un proveedor de LLM a través de OpenRouter es una parte imprescindible del MVP para demostrar la capacidad técnica del sistema.
*   **Envío de Emails:**
    *   **Primario (Gratuito):** **Mailgun** (plan gratuito con ~100 emails/día).
    *   **Fallback Local:** Un modo de "fake SMTP" que imprima los emails en la consola para desarrollo y pruebas.
*   **Hosting:**
    *   **Frontend:** **Vercel** (Plan Hobby/Free).
    *   **Backend:** **Render** (ofrece horas de instancia gratuitas).
*   **Herramientas de Desarrollo:**
    *   **Webhooks locales:** **ngrok**.
    *   **Parseo de CSV:** **Papaparse** (frontend para preview) y **fast-csv** (backend).

### 3. Diseño de Base de Datos (Esquema Extendido - Single-Tenant)
Se presentan los modelos de datos utilizando la sintaxis de Prisma. Este diseño mejora la integridad referencial mediante el uso de enums y establece relaciones explícitas entre las entidades clave.

```prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Tablas de Usuarios y Clientes
model Usuario {
  id        String   @id @default(uuid()) // Corresponde al ID de Supabase Auth
  nombre    String
  correo    String   @unique
  rol       Rol      @default(AGENTE)
  creadoEn  DateTime @default(now())
  modificadoEn  DateTime @default(now())
  tickets   Ticket[] @relation("asignado")
}

model Cliente {
  id        String   @id @default(uuid())
  nombre    String?
  correo    String   @unique // Usando el identificador de pais +57 para Colombia
  telefono  String?
  creadoEn  DateTime @default(now())
  modificadoEn  DateTime @default(now())
  ordenes   Orden[]
  tickets   Ticket[]
}

// Tablas de E-commerce y Soporte
model Orden {
  id                    String       @id @default(uuid())
  clienteId             String
  estado                EstadoOrden  @default(pendiente)
  numeroSeguimiento     String?
  transportista         String?
  articulos             Json // NOTA: Se mantiene Json por flexibilidad, pero considerar un modelo ItemOrden
  ultimaActualizacionEn DateTime?
  creadoEn              DateTime     @default(now())
  modificadoEn          DateTime     @default(now())
  tickets               Ticket[]
  cliente               Cliente      @relation(fields: [clienteId], references: [id])

  @@index([clienteId])
  @@index([creadoEn])
}

model Ticket {
  id                 String        @id @default(uuid())
  clienteId          String
  assigneeId         String? // ID del usuario asignado
  historialAsignacion String? //Json que guarda el historial de asignaciones
  asunto             String?
  estado             EstadoTicket  @default(nuevo)
  prioridad          Prioridad?
  canalOrigen        Canal
  creadoEn           DateTime      @default(now())
  modificadoEn       DateTime      @default(now())
  resueltoEn         DateTime?
  requiereEscalado   Boolean       @default(false)
  sugerenciaFusionId String? // Guarda el ID del ticket con el que se sugiere la fusión.

  etiquetas          Etiqueta[] // Relación muchos-a-muchos con Etiqueta
  ordenId            String?
  mensajes           Mensaje[]
  archivos           Archivo[]
  eventos            LogEvento[]
  orden              Orden?        @relation(fields: [ordenId], references: [id])
  usuarioAsignado    Usuario?      @relation("asignado", fields: [assigneeId], references: [id])
  cliente            Cliente       @relation(fields: [clienteId], references: [id])

  // Relación opcional para la sugerencia (self-relation)
  sugerenciaFusion      Ticket?  @relation("SugerenciaDeFusion", fields: [sugerenciaFusionId], references: [id], onDelete: NoAction, onUpdate: NoAction)
  sugeridoParaFusionEn  Ticket[] @relation("SugerenciaDeFusion")

  @@index([clienteId])
  @@index([estado])
  @@index([sugerenciaFusionId])
}

model Etiqueta {
  id      String   @id @default(uuid())
  nombre  String   @unique
  tickets Ticket[]

  @@index([nombre])
}

model Mensaje {
  id                   String   @id @default(uuid())
  ticketId             String
  usuarioId            String? // null => cliente o sistema
  contenidoTexto       String
  esNotaInterna        Boolean  @default(false)
  esAutomatico         Boolean  @default(false)
  canal                Canal
  metaDatosEnvio       Json?
  enviadoEn            DateTime?
  creadoEn             DateTime @default(now())
  modificadoEn         DateTime @default(now())
  aprobadoPorUsuarioId String? // Guarda el ID del usuario de Nivel 1 que aprobó la sugerencia de la IA.
  
  // ID único del mensaje del proveedor (ej. Mailgun Message-ID) para garantizar la idempotencia del webhook.
  fuenteMessageId      String?  @unique
  
  // Sugerencia de la IA para ESTE mensaje específico
  respuestaSugeridaIA  String?  @db.Text
  confianzaIA          Float?
  // Guarda un JSON con el razonamiento o los datos que usó la IA para la trazabilidad.
  // Ej: {"agente_conocimiento_id": "xyz", "articulos_usados": [1, 5]}
  metaDatosIA          Json?

  ticket               Ticket   @relation(fields: [ticketId], references: [id])
}

model Archivo {
  id                 String   @id @default(uuid())
  ticketId           String
  mensajeId          String?
  nombreArchivo      String
  urlAlmacenamiento  String
  tipoMime           String // Tipo MIME del archivo (ej: image/jpeg, application/pdf)
  tamano             Int // Tamaño en KB -- en caso de ser decimal redondear hacia arriba
  creadoEn           DateTime @default(now())
  modificadoEn       DateTime @default(now())
}

// Tablas de Configuración y Automatización
model ConfigAgente {
  id               String   @id @default(uuid())
  nombre           String
  descripcion      String?  // Descripción del agente
  promptBase       String   @db.Text // primera parte del prompt del systemPrompt
  promptsPorCanal  Json // Segunda parte del prompt que determina el comportamiento por canal
  umbralConfianza  Float    @default(0.75)
  actualizadoEn    DateTime @updatedAt
}

model Plantilla {
  id                String   @id @default(uuid())
  nombre            String
  plantillaAsunto   String?
  plantillaCuerpo   String   @db.Text
  creadoEn           DateTime @default(now())
  modificadoEn       DateTime @default(now())
}

model Integracion {
  id           String  @id @default(uuid())
  nombre       String
  claveApiEnc  String
  endpoint     String?
  urlWebhook   String?
  configJson   Json?
  activo       Boolean @default(true)
  creadoEn           DateTime @default(now())
  modificadoEn       DateTime @default(now())
}

model BaseConocimiento {
  id        String   @id @default(uuid())
  pregunta  String
  procedimiento String   @db.Text
  respuesta String   @db.Text
  categoria String?
  creadoEn  DateTime @default(now())
  modificadoEn       DateTime @default(now())
}

// Tablas de Auditoría y Métricas
model LogEvento {
  id        String    @id @default(uuid())
  ticketId  String?
  usuarioId String?
  tabla     String  // En el caso de las notiificaciones se guardan aunque la tabla notificación exista, solo son de tipo crear (informativo), el resto si son CUD
  cud      String   // Ejemplos: CREATE, UPDATE, DELETE
  payload   Json? // solo se guardan los datos que se modrifican en caso de crear o eliminar se guarda el estado completo
  creadoEn  DateTime  @default(now())
  modificadoEn       DateTime @default(now())
  ticket    Ticket?   @relation(fields: [ticketId], references: [id])
}

view AgregadoDiarioTicket { //Prisma no permite la creación de vistas, hay que crearla manualmente pero igual te dejo el esquema
  id                    String   @id @default(uuid())
  fecha                 DateTime @unique
  // Métricas de volumen
  ticketsTotales        Int
  ticketsNuevos         Int
  ticketsActivos        Int     // tickets abiertos - cerrados
  
  // Métricas de resolución
  conteoResueltos       Int
  promedioResolucionMin Float
  ticketsSinAsignar     Int
  ticketsVencidos       Int     // tickets que exceden SLA
  
  // Métricas por canal
  conteoCorreo          Int
  conteoWhatsapp        Int
  conteoFormularioWeb   Int
  conteoApi             Int
  
  // Métricas de calidad
  conteoWismo           Int     // Where Is My Order
  conteoDevoluciones    Int
  conteoEscalados       Int
  
  // Métricas de prioridad
  conteoPrioridadBaja   Int
  conteoPrioridadMedia  Int
  conteoPrioridadAlta   Int
  conteoPrioridadUrgente Int
  
  // Métricas de eficiencia
  promedioPrimerRespuestaMin Float  // tiempo promedio primera respuesta
  porcentajeAutoResueltos   Float   // tickets resueltos automáticamente
  conteoReasignaciones      Int     // número de veces que tickets fueron reasignados
}

// Definiciones de Enums para robustez del schema
enum Rol {
  ADMINISTRADOR
  AGENTE
}

enum EstadoOrden {
  pendiente
  procesando
  en_transito
  entregado
  cancelado
  devuelto
}

enum EstadoTicket {
  // Fase 1: Entrada y Procesamiento IA
  nuevo               // Recibido, en cola para la IA.
  ia_sugerido         // IA procesado, en cola para triaje Nivel 1.
  
  // Fase 2: Interacción y Espera
  respuesta_cliente   // El cliente ha respondido a un ticket existente. Requiere atención.
  esperando_cliente   // El agente ha respondido. Esperando al cliente.
  
  // Fase 3: Escalado y Resolución Nivel 2
  escalado_nivel_2    // Triaje decidió escalar. En cola general de especialistas.
  en_progreso_nivel_2 // Un especialista Nivel 2 tiene el ticket asignado y lo está trabajando.

  // Fase 4: Estados Finales y Excepcionales
  cerrado             // Ticket resuelto y finalizado.
  reabierto           // El cliente respondió a un ticket 'cerrado'. Alta prioridad.
  fusionado           // Ticket duplicado cuyos mensajes se han movido a otro. Es un estado terminal.
}

enum Prioridad {
  baja
  media
  alta
  urgente
}

enum Canal {
  correo
  whatsapp
  formulario_web
  api
}
```

### 4. Flujo de Trabajo Detallado
Este flujo optimiza el tiempo de respuesta y la eficiencia del equipo de soporte, utilizando agentes de IA para el trabajo preliminar y personal humano para la validación y resolución de casos complejos.

#### 4.1. Fase 1: Recepción y Acuse de Recibo (100% Automático)
1.  **Entrada del Cliente:** El usuario envía su solicitud a través de un formulario web o por correo electrónico (ej. `soporte@gearup.com`).
2.  **Procesamiento de Entrada:** El sistema recibe la solicitud (vía webhook de Mailgun o endpoint del formulario). Para los emails, el sistema primero determina si es una respuesta a una conversación existente (analizando `In-Reply-To` o un ID de ticket en el asunto) o un email completamente nuevo.
    *   **Si es una respuesta:** Agrega el contenido como un nuevo `mensaje` al `ticket` existente.
    *   **Si es nuevo:** Identifica o crea un `cliente`, genera un nuevo `ticket` con `estado = 'nuevo'`, y dispara el acuse de recibo.
3.  **Respuesta Automática Inmediata (para tickets nuevos):** Inmediatamente después de la creación de un nuevo ticket, se envía una plantilla de correo al cliente confirmando la recepción y estableciendo una expectativa de tiempo de respuesta (ej. "Hemos recibido tu solicitud y te daremos una respuesta en menos de 2 horas"). Este mensaje se registra en la tabla `Mensaje`.

#### 4.2. Fase 2: Procesamiento y Enriquecimiento con IA (100% Automático)
Una vez creado el ticket, se encola un job para ser procesado por el **Motor de Inteligencia Artificial**, compuesto por varios agentes especializados.
1.  **Análisis Inicial:**
    *   **Agente de Análisis:** Lee el mensaje inicial del cliente para identificar la intención, el sentimiento, las palabras clave y la posible urgencia.
    *   **Agente de Categorización:** Asigna una categoría preliminar al ticket (ej. `etiqueta` "WISMO", "RETURN").
2.  **Generación de Solución:**
    *   **Agente de Conocimiento:** Basado en la categoría, busca en la `BaseConocimiento` y la información de la `Orden` (si está vinculada) para formular una respuesta sugerida.
    *   **Agente de Confianza:** Evalúa la respuesta sugerida y le asigna un nivel de confiabilidad (ej. 95%).
3.  **Consolidación y Actualización del Ticket:**
    *   **Agente Orquestador:** Recopila la información de los agentes anteriores y actualiza el **registro del `Mensaje` original del cliente** con la propuesta de respuesta y sus metadatos (`respuestaSugeridaIA`, `confianzaIA`, `metaDatosIA`), creando un historial de auditoría claro.
    *   Finalmente, actualiza el estado del ticket a `ia_sugerido` y notifica al frontend para que aparezca en la cola de triaje.

#### 4.3. Fase 3: Triaje y Validación Humana (Nivel 1)
Aquí interviene una persona (ej. Brenda) para garantizar la calidad antes de que la respuesta llegue al cliente.
1.  **Cola de Triaje:** El agente de Nivel 1 ve una cola de tickets en estado `ia_sugerido`.
2.  **Punto de Decisión Rápida:** Al seleccionar un ticket, el agente tiene tres opciones principales:
    *   **Aprobar y Enviar:** Si la respuesta sugerida por la IA (asociada al último mensaje del cliente) es correcta, la aprueba con un solo clic. El sistema crea un nuevo `mensaje` de salida, guarda el ID del agente en `aprobadoPorUsuarioId` y cambia el estado del ticket a `esperando_cliente` o `cerrado`.
    *   **Escalar a Cola General:** Si la respuesta es incorrecta o el caso es complejo, el agente escala el ticket. Esto cambia el estado del ticket a `escalado_nivel_2`, enviándolo a la cola de especialistas de Nivel 2.
    *   **Reasignar a Agente Específico:** Si el agente de triaje sabe quién es la persona ideal para resolver el caso, puede asignarlo directamente a un agente específico de Nivel 2, registrando la asignación en el historial del ticket.

#### 4.4. Fase 4: Resolución por Especialistas (Nivel 2)
Los tickets en estado `escalado_nivel_2` llegan al personal especializado (ej. Carlos).
1.  **Asignación de Tickets:** La asignación puede ser por especialidad o carga de trabajo. Cuando un especialista toma un ticket (acción de "Reclamar" o "Tomar"), su estado cambia a `en_progreso_nivel_2` para indicar que está siendo trabajado activamente.
2.  **Resolución:** El especialista de Nivel 2 trabaja en el ticket utilizando herramientas más avanzadas y su conocimiento experto para resolver el problema del cliente, enviando una respuesta manual.

#### 4.5. Estrategia de Integración con Órdenes
Para que el agente pueda responder preguntas de tipo WISMO, necesita acceso a la información de los pedidos. Se implementarán las siguientes opciones en orden de prioridad:
*   **MVP Rápido (Importación CSV):**
    *   **UI/UX:** Se implementará una interfaz que permita subir un archivo CSV, previsualizar el mapeo de columnas (ej. `columna X` → `campo Y`), validar los datos mostrando errores por fila y finalmente iniciar la importación. Al finalizar, se mostrará un reporte con `registros_importados`, `registros_omitidos` y un enlace para descargar un `errores.csv`.
    *   **Backend:** Se adoptará una política de **"procesamiento por fila con tolerancia a fallos"**. El job de importación procesará cada fila de forma independiente; si una fila falla la validación o inserción, se registrará el error para el reporte final sin detener la importación del resto de filas válidas.
*   **Mejorado (Post-MVP):** Un conector vía API a plataformas como Shopify o Magento (usando OAuth o una API Key) que pueble y actualice la tabla `ordenes` automáticamente.
*   **Futuro (Post-MVP):** Implementación de webhooks desde la plataforma de e-commerce para recibir actualizaciones en tiempo real sobre el estado de los pedidos y el tracking.

#### 4.6. Lógica del Motor de IA y Reglas Automáticas

##### 4.6.1. Configuraciones de Agente Especializadas (Seeds)

En lugar de un único prompt genérico, el sistema utilizará configuraciones de agente especializadas que actúan como el "Agente de Conocimiento" para cada tipo de consulta, permitiendo respuestas más precisas. A continuación se detallan los cuatro perfiles iniciales, listos para ser insertados como seeds en la tabla `ConfigAgente`.

*   **1. WISMO - ¿Dónde está mi pedido? (`id: ac-wismo-01`)**
    *   **Prompt Base:** `Eres un asistente de soporte de GearUp Gadgets. El cliente pregunta por el estado de su pedido. Si tienes número de orden o tracking, incluye carrier, número de tracking y fecha estimada de entrega. Si no hay tracking, pide información mínima (número de orden). Responde en español, tono amable y conciso, máximo 5 frases. Devuelve JSON: {"reply_text":"...","escalate":false,"confidence":0.0,"suggested_tags":["WISMO"]}. Si el pedido parece perdido o tracking failed, marca escalate=true y explica por qué.`
    *   **Umbral de Confianza:** 0.9

*   **2. Devoluciones - Proceso y RMA (`id: ac-returns-01`)**
    *   **Prompt Base:** `Eres un asistente de soporte de GearUp Gadgets. El cliente pregunta cómo devolver un artículo. Explica brevemente el paso a paso para iniciar la devolución (plazo, condiciones, enlace a política), cuándo se emitirá el RMA y tiempos estimados de reembolso o reenvío. Si falta información crítica (número de orden, motivo), pídela. Responde en español y en formato JSON: {"reply_text":"...","escalate":false,"confidence":0.0,"suggested_tags":["RETURN"]}. Si el cliente exige reembolso inmediato o hay señales de fraude, sugiere escalate=true.`
    *   **Umbral de Confianza:** 0.8

*   **3. Compatibilidad de producto (`id: ac-compat-01`)**
    *   **Prompt Base:** `Eres un asistente de soporte técnico de GearUp Gadgets. El cliente pregunta si un accesorio es compatible con su dispositivo. Si el cliente menciona modelo exacto, compara con la base de datos de productos (si está disponible) y responde sí/no con una breve explicación técnica. Si no menciona el modelo, solicita el modelo exacto y ofrece preguntas de aclaración. Responde en español y devuelve JSON: {"reply_text":"...","escalate":false,"confidence":0.0,"suggested_tags":["COMPATIBILITY"]}. Si la compatibilidad es incierta o riesgo alto, sugiere escalate=true.`
    *   **Umbral de Confianza:** 0.75

*   **4. Producto dañado (`id: ac-damaged-01`)**
    *   **Prompt Base:** `Eres un asistente de soporte de GearUp Gadgets. El cliente reporta producto dañado. Pide fotos y detalles (número de orden, fecha de recepción). Ofrece opciones: reenvío o reembolso, y explica pasos para RMA. Si hay foto adjunta o lenguaje urgente ("no funciona", "dañado"), marca escalate=true y explica razón. Responde en español y devuelve JSON: {"reply_text":"...","escalate":true_or_false,"confidence":0.0,"suggested_tags":["DAMAGED"]}. Prioriza escalado si hay evidencia visual.`
    *   **Umbral de Confianza:** 0.85
##### 4.6.2. Heurística de Escalado Automático
El sistema aplicará estas reglas para decidir si un ticket requiere atención humana inmediata:
*   **Auto-escalado si:**
    *   La respuesta del LLM indica explícitamente que se debe escalar (`llmResponse.escalate === true`).
    *   La confianza del LLM (`llmResponse.confidence`) es menor al umbral configurado (`config_agente.umbralConfianza`).
    *   El texto del mensaje contiene palabras clave de alta sensibilidad como "dañado", "no funciona", "reembolso", "legal" o "no enciende".
    *   El ticket contiene adjuntos que son identificados como imágenes (`tipoMime` `image/*`). Al detectar fotos, el sistema debe escalar el ticket y puede sugerir un checklist de acciones al agente humano.
*   **Modo de Operación:**
    *   `always_manual` (**Requerido para el MVP**): Todas las propuestas del agente LLM requerirán aprobación humana antes de ser enviadas. Este enfoque garantiza el control total y minimiza los riesgos durante la fase inicial.

### 5. Flujo de Intervención Humana (UI del Agente)
La interfaz de usuario está diseñada para que Brenda y Carlos puedan procesar tickets de forma rápida y contextual, dividiendo las responsabilidades entre triaje (Nivel 1) y resolución especializada (Nivel 2).

#### 5.1. Interfaz de Triaje (Nivel 1)
1.  **Cola de Tickets:** La vista principal mostrará la lista de tickets en estado `ia_sugerido`. Cada ítem destacará la categoría, urgencia y nivel de confianza (`confianzaIA`) sugeridos por la IA.
2.  **Panel de Decisión:** Al abrir un ticket, se presenta una vista dividida:
    *   **Izquierda:** Historial de la conversación y archivos adjuntos.
    *   **Derecha:** La propuesta completa de la IA (obtenida del `Mensaje` más reciente: `respuestaSugeridaIA`, etiquetas modificables, confianza) y, si aplica, la información de la orden vinculada y un acceso rápido al historial del cliente.
3.  **Acciones Rápidas:**
    *   **Aprobar y Enviar (1-clic):** Envía la respuesta y actualiza el estado del ticket.
    *   **Editar y Enviar:** Permite modificar la respuesta antes de enviarla.
    *   **Escalar a Cola General:** Cambia el estado del ticket a `escalado_nivel_2`, moviéndolo a la cola de Nivel 2.
    *   **Reasignar a Agente:** Abre un selector para asignar el ticket directamente a otro agente de Nivel 2.

#### 5.2. Interfaz de Resolución para Especialistas (Nivel 2)
El personal de Nivel 2 tiene dos modos de visualización para trabajar con los tickets en estado `escalado_nivel_2`.
1.  **Vista de Tabla:** Una vista tradicional tipo lista o Kanban donde pueden ver todos los tickets asignados, ordenarlos por prioridad, filtrarlos y elegir en cuál trabajar.
2.  **Vista de Flujo Continuo:** Un modo de alta productividad. Al activarlo, el sistema presenta los tickets uno por uno según una lógica de prioridad. Cuando terminan y envían uno, el siguiente aparece automáticamente.

#### 5.3. Lógica de la Cola en la "Vista de Flujo Continuo"
Para asegurar que se atiendan tanto los tickets urgentes como los de menor prioridad, el sistema sigue un ciclo predefinido:
1.  **Ciclo de Prioridad:** El sistema sirve los tickets en este orden: 4 de prioridad Urgente, 3 de prioridad Alta, 2 de prioridad Media, y 1 de prioridad Baja.
2.  **Repetición del Ciclo:** Una vez completado, el ciclo vuelve a empezar.
3.  **Manejo de Colas Vacías:** Si una categoría no tiene suficientes tickets, el sistema procesa los que hay y pasa inmediatamente a la siguiente categoría.
4.  **Manejo de Nuevos Tickets Urgentes:** Si un nuevo ticket "Urgente" llega mientras un agente está trabajando, no se interrumpe el trabajo actual. El nuevo ticket será atendido en el siguiente ciclo.
5.  **Soporte de API:** Esta lógica será encapsulada en un endpoint de API dedicado (`GET /tickets/next-in-flow`) para simplificar el frontend.

### 6. Criterios de Aceptación y Casos de Prueba del MVP
#### 6.1. Reglas Operacionales de Aceptación
*   **Vinculación Automática:** Cuando llegue un email con un `ordenId`, el ticket creado debe mostrar la orden vinculada automáticamente.
*   **Gestión de Respuestas de Email:** El sistema debe identificar correctamente los correos de respuesta y agregar el contenido como un `mensaje` al ticket existente.
*   **Rendimiento del LLM:** El LLM mock debe generar una propuesta de respuesta en menos de 1 segundo.
*   **Flujo de Aprobación:** El agente debe poder aprobar y enviar la propuesta del LLM con un solo clic. El `mensaje` de salida y el `aprobadoPorUsuarioId` deben registrarse correctamente.
*   **Flujo de Escalado:** Si `escalate=true`, el ticket debe cambiar su estado a `escalado_nivel_2` y aparecer en la cola de Nivel 2.
*   **Demostración:** El video de demostración final debe mostrar de forma fluida los 3 casos de prueba principales (WISMO, devolución, producto dañado).

#### 6.2. Plan de Pruebas y Demo (E2E con Playwright)
Se implementará un conjunto enfocado de pruebas E2E para garantizar la estabilidad de los flujos críticos, usando helpers para mockear servicios externos.

*   **Test A (WISMO - Flujo Feliz):** Simular webhook de Mailgun, esperar ticket en UI, hacer clic en "Aprobar y Enviar", y verificar en BD que el `mensaje` y `aprobadoPorUsuarioId` son correctos.
*   **Test B (Devolución - Edición Humana):** Crear ticket desde formulario web, editar la `respuestaSugeridaIA`, enviar, y verificar en BD que `esAutomatico=false` y el contenido es el correcto.
*   **Test C (Daño con Foto - Escalado Automático):** Simular webhook de Mailgun con un adjunto de imagen y verificar que el ticket se crea con estado `escalado_nivel_2`.
*   **Test D (Respuesta de Cliente - Hilo de Conversación):** Simular webhook de Mailgun con `In-Reply-To` y verificar que no se crea un ticket nuevo, sino que se agrega un `mensaje` al existente.

### 7. Métricas Clave del MVP
Desde el día del lanzamiento, se deben medir los siguientes indicadores para evaluar el éxito del proyecto.

*   **Tiempo Medio de Resolución (TTR):** Medir la diferencia promedio entre `resueltoEn` y `creadoEn`.
*   **Tasa de aprobación sin edición:** Porcentaje de respuestas sugeridas por el LLM que son enviadas por los agentes sin ninguna modificación.
*   **Tasa de escalado:** Medir el porcentaje de tickets que terminan con el estado `escalado_nivel_2`.
*   **Volumen de tickets por etiqueta:** Contar los tickets por `etiqueta` (WISMO, RETURN, DAMAGED).
*   **Precisión del LLM sobre WISMO:** Realizar verificaciones manuales periódicas para asegurar que la información de seguimiento es correcta.

### 8. Plan de Ejecución y Entrega

#### 8.1. Plan Operativo por Fines de Semana (8 Semanas)
(Objetivo: cada fin de semana produce un “artefacto verificable” o demo parcial.)

*   **Fin de semana 1 — Infra + repositorio + SCRUM:** Crear monorepo, board SCRUM, inicializar proyectos, crear README y seeds.
*   **Fin de semana 2 — Auth + CRUD básico + ERD:** Implementar autenticación, endpoints CRUD para tickets y documentar API con Swagger.
*   **Fin de semana 3 — Mailgun webhook + ticket creation:** Implementar endpoint de Mailgun y pruebas con ngrok.
*   **Fin de semana 4 — Formulario público + CSV import UI:** Implementar formulario web y UI para subir CSV de órdenes.
*   **Fin de semana 5 — LLM Adapter mock + generate proposal flow:** Implementar endpoint que lee mocks y muestra propuesta en el dashboard.
*   **Fin de semana 6 — Approve/Send + Mailgun send + Templates:** Implementar flujo de aprobación, envío de email y "Guardar como plantilla".
*   **Fin de semana 7 — File uploads & Escalation heuristics + E2E tests:** Implementar subida a Supabase Storage, regla de auto-escalado y los 4 tests E2E.
*   **Fin de semana 8 — Reports, docs y demo final:** Implementar exportación a CSV/HTML, finalizar documentos y grabar video demo.

#### Guion Recomendado para Demo (5–7 minutos)
> 1.  **Intro (30s):** Presentar el problema y el diagrama BPMN "antes".
> 2.  **Caso 1 WISMO (90s):** Mostrar webhook → ticket con sugerencia → aprobar con 1-clic → mostrar log de envío.
> 3.  **Caso 2 Devolución (90s):** Ticket desde formulario → editar la respuesta y enviar → mostrar en BD que `esAutomatico=false`.
> 4.  **Caso 3 Dañado (60s):** Email con foto → escalado automático → mostrar en la cola de Nivel 2.
> 5.  **Docs y Artefactos (60s):** Mostrar brevemente ERD, BPMN "después", y URLs desplegadas.
> 6.  **Cierre (30s):** Resumir métricas clave y próximos pasos.

#### 8.2. Asignación de Roles (Equipo de 3 Personas)
*   **Dev A (Líder Backend):** Responsable de NestJS, Prisma, Auth, Webhook, worker, LLM adapter, lógica de envío y despliegue del backend.
*   **Dev B (Líder Frontend):** Responsable de Vite, Tailwind, UI del login, dashboard de tickets, formulario web, UI de importación CSV y subida de archivos.
*   **Dev C (QA, DevOps y Documentación):** Responsable del board SCRUM, CI/CD, infraestructura de pruebas, tests E2E con Playwright y compilación de todos los manuales y video final.

#### 8.3. Entregables Finales para Evaluación (Checklist Detallado)
1.  **Diagrama de Procesos (Bizagi):** Archivos PNG y fuente del proceso "antes" y "después".
2.  **Gestión de Proyecto (SCRUM):** Tablero de proyecto activo y captura del gráfico de burndown.
3.  **Software 100% Funcional:** Video demo, repositorio de código y pruebas E2E.
4.  **Despliegue en Servidor Público:** URLs públicas y funcionales para frontend y backend.
5.  **Atributos de Calidad (ISO 25010):** Documento de Requisitos No Funcionales.
6.  **Manuales y Plan de Capacitación:** `manual_tecnico.pdf`, `manual_usuario.pdf` y `plan_capacitacion.pdf`.
7.  **Plan y Aceptación de Pruebas:** Reportes de Playwright y un "Informe de Aceptación".

---

---

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