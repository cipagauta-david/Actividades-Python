### **Especificación de Requisitos de Software (SRS)**
### **Asistente de Soporte al Cliente Inteligente (NoraAI)**

**Versión 1.1**
**Fecha: 25 de octubre de 2025**
**Historial de Cambios:**
N/A
### 1. Introducción

#### 1.1 Visión y Objetivos Estratégicos
NoraAI es una plataforma de inteligencia de soporte diseñada para transformar el centro de contacto de GearUp Gadgets de un centro de costos reactivo a un motor de eficiencia, retención de clientes e inteligencia de negocio. Los objetivos estratégicos del producto son:

**Objetivos Estratégicos Principales**
*   **Optimizar la Eficiencia Operativa:** Reducir directamente el tiempo y coste por interacción al automatizar la recopilación de datos, la formulación de borradores de respuesta y agilizar la acción humana a través de un flujo de trabajo de "un solo clic". La eficiencia se medirá a través de KPIs clave como:
    *   Reducir el **Costo por Contacto** en un 25% en los primeros 12 meses.
    *   Disminuir drásticamente el **Tiempo Medio de Resolución (TTR)** para tickets de alta frecuencia.
    *   Incrementar la **Tasa de Resolución en el Primer Contacto (FCR)** para consultas automatizables en un 40%.
    *   Reducir el **Tiempo de Primera Respuesta (FRT)** a menos de 5 minutos para el 90% de las consultas.
*   **Mejorar y Estandarizar la Experiencia del Cliente (CX):** Garantizar un estándar mínimo de calidad y velocidad en cada respuesta inicial. Al proporcionar a los agentes un contexto completo y una respuesta sugerida, se minimiza la variabilidad en el tono y la precisión. El objetivo es:
    *   Aumentar la **Puntuación de Satisfacción del Cliente (CSAT)** en 10 puntos a través de la integración de encuestas de feedback post-resolución.
    *   **Estandarizar la Calidad del Servicio:** Garantizar que todos los clientes reciban un nivel de respuesta base consistente y de alta calidad, independientemente del agente que intervenga.
*   **Escalar las Operaciones de Soporte:** Absorber un aumento en el volumen de tickets sin un aumento lineal en el personal, actuando como un "multiplicador de fuerza" para el equipo de soporte. Se medirá por:
    *   Permitir que el negocio maneje un incremento del 50% en el volumen de consultas con solo un 10% de aumento en el personal de soporte.
    *   Fomentar una alta **Tasa de Adopción Interna** de las herramientas de IA (>80% de uso de la aprobación en 1-clic por parte del Nivel 1).
*   **Generar Inteligencia de Negocio:** Centralizar y analizar interacciones para identificar problemas recurrentes en productos, oportunidades de venta cruzada y patrones de consulta de clientes.
*   **Mitigación de Riesgos Operativos:** Mitigar el riesgo de error humano y de comunicación inconsistente mediante la centralización de la lógica de respuesta (`ConfigAgente`) y la creación de un rastro de auditoría completo a través de un registro de eventos inmutable.

**Objetivos Estratégicos Secundarios**
*   **Reducir el Desgaste del Agente (Agent Burnout):** Automatizar las tareas monótonas y repetitivas permite que los agentes se centren en problemas más estimulantes, aumentando la satisfacción laboral.
*   **Acelerar la Formación de Nuevos Agentes (Onboarding):** NoraAI actúa como un "copiloto" que guía a los nuevos agentes, sugiriendo respuestas y procedimientos correctos.
*   **Identificar Patrones de Falla de Producto y Servicio:** La categorización automática y el análisis de los tickets proveen datos estructurados para detectar problemas recurrentes.
*   **Crear un Activo de Conocimiento Corporativo:** Cada ticket resuelto y cada respuesta validada por un humano enriquece el sistema, construyendo una base de conocimiento dinámica.

#### 1.2 Propósito
Este documento define los requisitos funcionales y no funcionales para el Producto Mínimo Viable (MVP) del sistema "NoraAI", que constituye el primer paso hacia la visión estratégica descrita anteriormente. El propósito de NoraAI es construir una aplicación web para la empresa de e-commerce "GearUp Gadgets" que automatice y optimice el soporte al cliente. El sistema ingesta tickets de soporte, genera respuestas sugeridas mediante un agente LLM, y provee un dashboard para que los agentes humanos supervisen, aprueben y gestionen estas interacciones.

#### 1.3 Alcance del Producto
El sistema NoraAI se enfocará en resolver las cuatro consultas más frecuentes que recibe el equipo de soporte:
1.  Estado de pedidos (WISMO - "¿Dónde está mi pedido?").
2.  Proceso de devoluciones (RMA).
3.  Consultas de compatibilidad de productos.
4.  Reportes de productos dañados.

El alcance del MVP incluye los siguientes canales y funcionalidades clave:
*   **Canales de Entrada:** Correo electrónico y un formulario web público.
*   **Procesamiento:** Un motor de IA que analiza los tickets y sugiere respuestas.
*   **Interfaz de Agente:** Un dashboard web para que los agentes revisen las sugerencias de la IA, las aprueben, las editen o escalen el ticket.
*   **Gestión de Datos:** Importación de datos de órdenes a través de archivos CSV para dar contexto a la IA.

Las funcionalidades fuera del alcance de este MVP son: la integración con WhatsApp y la implementación de flujos de trabajo avanzados con herramientas de automatización como n8n.

#### 1.4 Definiciones, Acrónimos y Abreviaturas
*   **API:** Interfaz de Programación de Aplicaciones.
*   **CSAT:** Customer Satisfaction Score (Puntuación de Satisfacción del Cliente).
*   **CSV:** Comma-Separated Values (Valores Separados por Comas).
*   **CX:** Customer Experience (Experiencia del Cliente).
*   **DNS:** Domain Name System (Sistema de Nombres de Dominio).
*   **ERP:** Enterprise Resource Planning (Planificación de Recursos Empresariales).
*   **FCR:** First Contact Resolution (Tasa de Resolución en el Primer Contacto).
*   **FRT:** First Response Time (Tiempo de Primera Respuesta).
*   **HTML:** HyperText Markup Language.
*   **IA:** Inteligencia Artificial.
*   **JWT:** JSON Web Token.
*   **KPI:** Key Performance Indicator (Indicador Clave de Rendimiento).
*   **LLM:** Large Language Model (Modelo Lingüístico Grande).
*   **MVP:** Minimum Viable Product (Producto Mínimo Viable).
*   **ORM:** Object-Relational Mapping (Mapeo Objeto-Relacional).
*   **RMA:** Return Merchandise Authorization (Autorización de Devolución de Mercancía).
*   **SLA:** Service Level Agreement (Acuerdo de Nivel de Servicio).
*   **SPF/DKIM:** Sender Policy Framework / DomainKeys Identified Mail (Estándares de autenticación de correo electrónico).
*   **SRS:** Software Requirements Specification (Especificación de Requisitos de Software).
*   **SSE:** Server-Sent Events.
*   **TTR:** Time to Resolution (Tiempo Medio de Resolución).
*   **UI:** User Interface (Interfaz de Usuario).
*   **WISMO:** Where Is My Order? (¿Dónde está mi pedido?).

#### 1.5 Referencias
*   Documento "Plan de Acción Final: Asistente de Soporte al Cliente Inteligente (NoraAI)".

#### 1.6 Vista General del Documento
Este documento está organizado en tres secciones principales. La Sección 1 introduce la visión, propósito y alcance del proyecto. La Sección 2 proporciona una descripción general del producto, sus usuarios y sus restricciones. La Sección 3 detalla los requisitos específicos, incluyendo interfaces, requisitos funcionales y no funcionales, y la estructura de la base de datos.

### 2. Descripción General

#### 2.1 Perspectiva del Producto
NoraAI es un sistema web autocontenido que se integrará con varios servicios externos para su operación:
*   **Supabase:** Para la autenticación de usuarios (Supabase Auth) y el almacenamiento de archivos adjuntos (Supabase Storage).
*   **Mailgun:** Para la recepción (vía webhooks) y el envío de correos electrónicos.
*   **OpenRouter:** Como proveedor de servicios LLM para la generación de respuestas.
*   **Vercel y Render:** Como plataformas de hosting para el frontend y el backend, respectivamente.

El sistema no reemplaza ningún software existente, sino que se establece como la nueva herramienta principal para el equipo de soporte de Nivel 1 y Nivel 2.

#### 2.2 Funciones del Producto
Las principales funciones del sistema son:
1.  **Ingesta de Tickets:** Recepción de solicitudes de clientes a través de correo electrónico y un formulario web.
2.  **Procesamiento con IA:** Análisis automático de nuevos tickets para categorizarlos, enriquecerlos con datos de órdenes y generar una respuesta sugerida.
3.  **Flujo de Triaje (Nivel 1):** Presentación de las sugerencias de la IA a un agente humano para su revisión y aprobación rápida ("1-clic").
4.  **Flujo de Resolución (Nivel 2):** Gestión de tickets complejos que son escalados manual o automáticamente.
5.  **Gestión de Datos de Órdenes:** Capacidad para importar información de pedidos desde un archivo CSV.
6.  **Reportes y Exportación:** Generación de reportes de actividad y exportación de datos de tickets en formato CSV.

#### 2.3 Características de los Usuarios
*   **Cliente:** Usuario final de GearUp Gadgets que busca soporte.
*   **Agente de Soporte Nivel 1 (Triaje):** Personal (ej. Brenda) cuyo objetivo es procesar la cola de triaje rápidamente. Su frustración es la ambigüedad y las tareas repetitivas. Requiere una interfaz rápida y eficiente.
*   **Agente de Soporte Nivel 2 (Especialista):** Personal (ej. Carlos) con conocimiento técnico profundo, responsable de resolver casos complejos que requieren investigación. Su frustración es recibir tickets mal escalados o sin contexto suficiente.
*   **Administrador del Sistema:** Rol técnico y de gestión con los máximos privilegios. Es responsable de la configuración técnica del sistema (gestión de usuarios, APIs, `ConfigAgente`) y de la supervisión operativa. Para el alcance del MVP, este rol absorbe las responsabilidades de supervisión, incluyendo la visualización de KPIs de rendimiento del equipo, la calidad de las respuestas y la salud general de la operación de soporte.
*   **Sistema Externo:** Aplicaciones de terceros (ej. plataforma E-commerce, ERP) que podrían interactuar con NoraAI mediante API/Webhooks en futuras versiones.

El alcance del presente MVP se centra en las funcionalidades requeridas por los roles de **Agente de Soporte (Nivel 1 y 2)**, **Administrador del Sistema** y en la interacción con el **Cliente**.

#### 2.4 Restricciones
*   **Tecnológicas:** El sistema debe ser desarrollado utilizando el stack tecnológico definido: NestJS (Backend), React (Frontend), PostgreSQL (Base de Datos), Prisma (ORM).
*   **Operativas:** El sistema operará en un modelo single-tenant.
*   **Dependencia de Servicios:** El sistema dependerá de la disponibilidad y los planes de nivel gratuito de servicios de terceros (Supabase, Mailgun, OpenRouter, Vercel, Render).
*   **Modo de Demostración:** Para garantizar la fiabilidad durante las demostraciones, el adaptador LLM debe tener un modo de "mock" que lea respuestas predefinidas de archivos JSON locales.

#### 2.5 Supuestos y Dependencias
*   **Supuestos:** Se asume que GearUp Gadgets puede proporcionar los datos de sus órdenes de e-commerce en un formato CSV consistente. Se asume la disponibilidad de credenciales y configuración para todos los servicios de terceros requeridos.
*   **Dependencias:** El funcionamiento del sistema depende críticamente de la disponibilidad de las APIs de Mailgun, Supabase y OpenRouter. La funcionalidad de correo electrónico depende de una configuración DNS correcta (registros MX, SPF/DKIM).

### 3. Requisitos Específicos

#### 3.1 Requisitos de Interfaz Externa

##### 3.1.1 Interfaces de Usuario
*   **UI-01: Dashboard de Administración:** Una interfaz para usuarios con rol de Administrador. Debe incluir widgets que muestren KPIs operativos clave (TTR, FCR, CSAT), rendimiento del equipo y volumen de tickets, además de accesos a las áreas de configuración del sistema.
*   **UI-02: Dashboard de Agente - Vista de Triaje (Nivel 1):** Una interfaz que muestra una lista de tickets en estado `ia_sugerido`, priorizada visualmente por indicadores de SLA. Al seleccionar un ticket, se mostrará una vista dividida con el historial de la conversación a la izquierda y la propuesta de la IA a la derecha, junto con acciones rápidas (Aprobar, Editar, Escalar).
*   **UI-03: Dashboard de Agente - Vista de Especialista (Nivel 2):** Una interfaz que muestra la cola de tickets en estado `escalado_nivel_2` en formato de tabla o Kanban, con indicadores de SLA. Incluirá un modo opcional de "flujo continuo".
*   **UI-04: Interfaz de Importación de CSV:** Una página que permite a un usuario subir un archivo CSV, previsualizar los datos y mapear las columnas a los campos de la base de datos `Orden`.

##### 3.1.2 Interfaces de Software
*   **API-01: Mailgun API:** El sistema se integrará con la API de Mailgun para el envío de correos electrónicos salientes.
*   **API-02: Mailgun Inbound Webhook:** El sistema expondrá un endpoint (`POST /webhooks/mailgun/inbound`) para recibir y procesar correos entrantes.
*   **API-03: OpenRouter API:** El sistema se comunicará con OpenRouter para enviar el contexto del ticket y recibir las sugerencias del LLM.
*   **API-04: Supabase Auth:** El sistema utilizará Supabase para la autenticación de agentes. El backend validará los tokens JWT emitidos por Supabase.
*   **API-05: Supabase Storage:** El sistema utilizará la API de Supabase para subir y gestionar los archivos adjuntos a los tickets.
*   **API-06: Public Ticket Creation API:** El sistema expondrá un endpoint seguro para que sistemas externos autenticados (ej. E-commerce) puedan crear tickets programáticamente.

##### 3.1.3 Interfaces de Comunicación
*   **COM-01:** Toda la comunicación entre el cliente (navegador) y los servidores se realizará a través del protocolo HTTPS.
*   **COM-02:** El sistema deberá utilizar un mecanismo de comunicación en tiempo real (SSE o WebSocket simple) para notificar al frontend cuando una propuesta de la IA esté lista para un ticket.

#### 3.2 Requisitos Funcionales

##### RF-TICKET: Gestión de Tickets
*   **RF-TICKET-001:** El sistema deberá crear un registro de `Ticket` y `Mensaje` cuando se reciba una solicitud a través del webhook de Mailgun.
*   **RF-TICKET-002:** El sistema deberá crear un registro de `Ticket` y `Mensaje` cuando se envíe una solicitud desde el formulario web público.
*   **RF-TICKET-003:** El sistema deberá identificar si un correo entrante es una respuesta a un ticket existente (usando `In-Reply-To` o un ID en el asunto) y agregar el contenido como un nuevo `Mensaje` a ese ticket, en lugar de crear uno nuevo.
*   **RF-TICKET-004:** El sistema deberá asociar cada ticket a un `Cliente`, creando un nuevo cliente si el correo electrónico del remitente no existe.
*   **RF-TICKET-005:** Si el cuerpo o asunto de un mensaje contiene un ID de orden, el sistema deberá intentar vincular el `Ticket` a una `Orden` existente en la base de datos.
*   **RF-TICKET-006:** El sistema deberá enviar un correo electrónico de acuse de recibo automático al cliente inmediatamente después de la creación de un nuevo ticket.
*   **RF-TICKET-007:** Tras la resolución de un ticket, el sistema deberá poder enviar un correo de seguimiento solicitando feedback de satisfacción (CSAT).
*   **RF-TICKET-008:** El sistema deberá poder crear un ticket a partir de una solicitud recibida a través de la API pública de creación de tickets.

##### RF-IA: Procesamiento con IA y Automatización
*   **RF-IA-001:** Tras la creación de un ticket, el sistema deberá iniciar un proceso en segundo plano para generar una propuesta de respuesta utilizando el adaptador LLM.
*   **RF-IA-002:** El sistema deberá utilizar configuraciones de agente especializadas (`ConfigAgente`) basadas en el tipo de consulta para construir el prompt enviado al LLM.
*   **RF-IA-003:** La respuesta del LLM (texto sugerido, confianza, etiquetas, prioridad, recomendación de estado y escalado) deberá ser almacenada en los campos correspondientes del `Ticket`.
*   **RF-IA-004:** Una vez que la propuesta de la IA se haya generado, el estado del ticket deberá cambiar a `ia_sugerido`.
*   **RF-IA-005:** El sistema deberá implementar una heurística de escalado automático que cambie el estado del ticket a `escalado_nivel_2` si se cumple alguna de las siguientes condiciones:
    *   La respuesta del LLM indica explícitamente `escalate: true`.
    *   La confianza del LLM es menor que el `umbralConfianza` del agente.
    *   El mensaje del cliente contiene palabras clave de alta sensibilidad (ej. "dañado", "legal").
    *   El ticket contiene un archivo adjunto de tipo imagen (`image/*`).

##### RF-AGENT: Flujo de Trabajo del Agente
*   **RF-AGENT-001:** La UI de Triaje deberá mostrar una lista de tickets cuyo estado sea `ia_sugerido`.
*   **RF-AGENT-002:** Al seleccionar un ticket, la UI de Triaje deberá presentar la sugerencia de la IA de forma clara y diferenciada del historial de mensajes del cliente, facilitando su comparación y revisión.
*   **RF-AGENT-003:** Un agente de Nivel 1 debe poder aprobar la sugerencia de la IA con un solo clic. Esta acción deberá:
    *   Crear un `Mensaje` de salida.
    *   Registrar el ID del agente en `aprobadoPorUsuarioId`.
    *   Enviar el mensaje al cliente por correo electrónico.
    *   Cambiar el estado del ticket a `esperando_cliente` o `cerrado`.
*   **RF-AGENT-004:** Un agente de Nivel 1 debe poder editar el texto de la `respuestaSugeridaIA` antes de enviarlo.
*   **RF-AGENT-005:** Un agente de Nivel 1 debe poder escalar un ticket, lo que cambia su estado a `escalado_nivel_2`.
*   **RF-AGENT-006:** La UI de Especialistas deberá mostrar una lista de tickets cuyo estado sea `escalado_nivel_2`.
*   **RF-AGENT-007:** El sistema debe permitir a los agentes utilizar y gestionar plantillas de respuesta.
*   **RF-AGENT-008:** El sistema deberá permitir a los agentes dejar notas internas en un ticket y @mencionar a otros agentes para colaboración interna.
*   **RF-AGENT-009:** El sistema deberá monitorizar los Acuerdos de Nivel de Servicio (SLAs) y priorizar o resaltar visualmente los tickets que se acerquen a su vencimiento.

##### RF-DATA: Gestión de Datos
*   **RF-DATA-001:** El sistema deberá proporcionar una interfaz para subir un archivo CSV de órdenes.
*   **RF-DATA-002:** La interfaz de importación deberá permitir previsualizar los datos y mostrar errores de validación por fila.
*   **RF-DATA-003:** La importación de CSV se procesará de forma asíncrona en segundo plano para no bloquear la interfaz de usuario.
*   **RF-DATA-004:** El sistema deberá permitir la exportación de una lista filtrada de tickets a un archivo CSV.
*   **RF-DATA-005:** El sistema deberá poder generar un reporte de resumen de tickets en formato HTML o CSV.

##### RF-FILE: Gestión de Archivos
*   **RF-FILE-001:** El sistema deberá poder procesar archivos adjuntos de los correos electrónicos entrantes.
*   **RF-FILE-002:** Los archivos adjuntos deberán ser almacenados de forma segura en Supabase Storage, y la URL de acceso se guardará en el registro `Archivo`.

##### RF-ADMIN: Funcionalidades de Administración
*   **RF-ADMIN-001:** Un administrador debe poder gestionar usuarios, roles y permisos granulares.
*   **RF-ADMIN-002:** Un administrador debe poder configurar y auditar los cambios en las configuraciones de los agentes de IA (`ConfigAgente`), como prompts y umbrales.
*   **RF-ADMIN-003:** Un administrador debe poder configurar reglas de negocio, SLAs y horarios de oficina del sistema.
*   **RF-ADMIN-004:** Un administrador debe poder visualizar dashboards de rendimiento del equipo y de agentes individuales.
*   **RF-ADMIN-005:** Un administrador debe poder revisar el historial completo de cualquier ticket, incluyendo las acciones de la IA y de los agentes.

#### 3.3 Requisitos No Funcionales

*   **NFR-PERF-001 (Rendimiento):** La exportación de grandes volúmenes de tickets a CSV deberá realizarse mediante streaming para evitar timeouts y un uso excesivo de memoria.
*   **NFR-PERF-002 (Rendimiento):** En modo "mock", la generación de una propuesta de respuesta por parte del LLM Adapter debe completarse en menos de 1 segundo.
*   **NFR-PERF-003 (Rendimiento):** La acción completa de aprobación en 1-clic (desde el clic del agente hasta la confirmación en la UI) debe ser percibida como instantánea por el usuario, completándose en menos de 2 segundos.
*   **NFR-SEC-001 (Seguridad):** El acceso a los endpoints del backend debe estar protegido y requerir un token JWT válido emitido por Supabase Auth.
*   **NFR-USAB-001 (Usabilidad):** La acción de "Aprobar y Enviar" para un agente de Nivel 1 debe poder completarse con un solo clic desde la vista del ticket.
*   **NFR-RELI-001 (Fiabilidad):** El sistema debe incluir un modo de "mailer de consola" para el desarrollo y las pruebas locales, que imprima los correos electrónicos en la terminal en lugar de enviarlos a través de Mailgun, eliminando así la dependencia del servicio externo en el entorno de desarrollo.
*   **NFR-MAINT-001 (Mantenibilidad):** El repositorio debe incluir un script de `seed` que pueble la base de datos con datos de prueba consistentes, incluyendo las configuraciones de los agentes de IA (`ConfigAgente`), para facilitar el desarrollo y las pruebas.