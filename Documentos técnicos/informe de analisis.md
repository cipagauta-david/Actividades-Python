**Servicio Nacional de Aprendizaje SENA**
**Tecnología en Análisis y Desarrollo de Software (ADSO)**

**Ficha: 2922205**

---

### **Elaboración del Informe de Análisis con Listas de Chequeo para la Validación de Artefactos**

**Evidencia: GA2-220501093-AA3-EV02**

---

**Proyecto:**
Sistema Inteligente de Soporte al Cliente "NoraAI" para la Empresa **GearUp Gadgets**

**Aprendices:**
Sonia Viviana Cano Guerrero
David Santiago Jiménez Cipagauta
Juan Sebastian Rodriguez Ostios

**Año:**
2025

---
**Estado del Documento:** En Revisión

### **ÍNDICE**

**INTRODUCCIÓN**

**1. DESCRIPCIÓN DEL PROYECTO: "NoraAI"**
    1.1. Contexto y Justificación
    1.2. Alcance
    1.3. Ámbito y Descripción General del Sistema
    1.4. Perspectiva del Producto

**2. GESTIÓN DEL PROYECTO**
    2.1. Personal Involucrado
    2.2. Metodología de Trabajo

**3. ANÁLISIS DE REQUERIMIENTOS**
    3.1. Funciones del Producto
    3.2. Características de los Usuarios
    3.3. Jerarquía de Usuarios
    3.4. Restricciones del Sistema

**4. ARTEFACTOS DE DISEÑO**
    4.1. Diagramas de Actividades
    4.2. Diagrama de Clases

**5. PROCESO DE VALIDACIÓN**
    5.1. Metodología de Listas de Chequeo
    5.2. Lista de Chequeo - Módulo de Reportes
    5.3. Lista de Chequeo - Infraestructura y Servicios (Hardware)
    5.4. Lista de Chequeo - Componentes de Software

**6. FIRMAS DE APROBACIÓN**

**ANEXO A: DESCRIPCIÓN DE LA EVIDENCIA DE APRENDIZAJE**

---

### **INTRODUCCIÓN**

El objetivo de este informe es presentar los resultados del análisis y validación de los artefactos de software correspondientes al proyecto de desarrollo del sistema de soporte "NoraAI" para la empresa **GearUp Gadgets**. Para llevar a cabo esta validación, se ha empleado una metodología basada en listas de chequeo diseñadas para verificar el cumplimiento de cada uno de los requerimientos funcionales y de diseño.

Este documento está estructurado para detallar el proceso de evaluación, presentar los hallazgos y asegurar que el producto desarrollado satisface íntegramente las necesidades y especificaciones del cliente, permitiendo al equipo de soporte gestionar las solicitudes de manera ágil y consistente, y mejorando la experiencia del cliente final.

### **1. DESCRIPCIÓN DEL PROYECTO: "NoraAI"**

#### **1.1. Contexto y Justificación**

El proyecto surge de la necesidad que actualmente presenta la empresa GearUp Gadgets, la cual se enfoca en la comercialización de gadgets electrónicos. En la actualidad, su equipo de soporte se encuentra sobrecargado gestionando manualmente un alto volumen de consultas repetitivas. Partiendo de esto, se optó por suplir esta necesidad y crear una aplicación web de soporte al cliente inteligente que cumpla con todas las necesidades de la empresa.

El impacto favorable que se pretende tener con la creación de este software es automatizar la resolución de las consultas más frecuentes, permitiendo al equipo humano centrarse en casos más complejos. Esto mejorará la eficiencia operativa, estandarizará la calidad de la atención, reducirá drásticamente los tiempos de respuesta y aumentará las estadísticas de satisfacción del cliente.

#### **1.2. Alcance**

El sistema NoraAI se enfocará en resolver las cuatro consultas más frecuentes que recibe el equipo de soporte:
*   Estado de pedidos (WISMO - "¿Dónde está mi pedido?").
*   Proceso de devoluciones (RMA).
*   Consultas de compatibilidad de productos.
*   Reportes de productos dañados.

El alcance del MVP (Producto Mínimo Viable) incluye los siguientes canales y funcionalidades clave:
*   **Canales de Entrada:** Correo electrónico y un formulario web público.
*   **Procesamiento:** Un motor de IA que analiza los tickets y sugiere respuestas.
*   **Interfaz de Agente:** Un dashboard web para que los agentes revisen las sugerencias de la IA, las aprueben, las editen o escalen el ticket.
*   **Gestión de Datos:** Importación de datos de órdenes a través de archivos CSV para dar contexto a la IA.

Las funcionalidades fuera del alcance de este MVP son: la integración con WhatsApp y la implementación de flujos de trabajo avanzados con herramientas de automatización como n8n.

#### **1.3. Ámbito y Descripción General del Sistema**

NoraAI es una aplicación web de soporte al cliente, accesible desde cualquier sistema operativo a través de un navegador web, diseñada para optimizar el flujo de trabajo del equipo de GearUp Gadgets. El sistema está diseñado para que los agentes de soporte (Nivel 1 y 2) gestionen el ciclo de vida completo de los tickets de clientes.

La plataforma centraliza la gestión de los tickets, desde su recepción (vía email y formulario web) hasta su resolución. Incluye un motor de inteligencia artificial que genera respuestas sugeridas, un dashboard para la supervisión y acción por parte de los agentes, la gestión de datos de órdenes para contextualizar el soporte y la administración de los usuarios internos del sistema (agentes y administradores).

#### **1.4. Perspectiva del Producto**

NoraAI es un sistema web autocontenido que se integrará con varios servicios externos para su operación:
*   **Supabase:** Para la autenticación de usuarios (Supabase Auth) y el almacenamiento de archivos adjuntos (Supabase Storage).
*   **Mailgun:** Para la recepción (vía webhooks) y el envío de correos electrónicos.
*   **OpenRouter:** Como proveedor de servicios LLM para la generación de respuestas.
*   **Vercel y Render:** Como plataformas de hosting para el frontend y el backend, respectivamente.

El sistema no reemplaza ningún software existente, sino que se establece como la nueva herramienta principal para el equipo de soporte de Nivel 1 y Nivel 2.

### **2. GESTIÓN DEL PROYECTO**

#### **2.1. Personal Involucrado**

| NOMBRE                         | ROL                            | CATEGORÍA PROFESIONAL | RESPONSABILIDAD                          | INFORMACIÓN DE CONTACTO         |
| ------------------------------ | ------------------------------ | --------------------- | ---------------------------------------- | ------------------------------- |
| Cano Guerrero Sonia Viviana    | Analista, diseñador y programador | Estudiante de ADSO    | Análisis de información, diseño y programación | soniacanog.developer@gmail.com  |
| Jiménez Cipagauta David Santiago | Analista, diseñador y programador | Estudiante de ADSO    | Análisis de información, diseño y programación | david.jimenez@gmail.com         |
| Rodriguez Ostios Juan Sebastian  | Analista, diseñador y programador | Estudiante de ADSO    | Análisis de información, diseño y programación | jsro0310@gmail.com              |

#### **2.2. Metodología de Trabajo**

Para la gestión y ejecución del proyecto NoraAI, se ha adoptado el marco de trabajo ágil Scrum. Esta metodología fue seleccionada por su enfoque en el desarrollo iterativo e incremental, el cual permite realizar entregas de valor funcionales en ciclos cortos (Sprints), facilitando la validación temprana y la adaptación continua del producto.

La aplicación de Scrum ofrece ventajas determinantes para el éxito del proyecto, como mejorar la colaboración y la comunicación dentro del equipo, optimizar la gestión del flujo de trabajo y maximizar la productividad al enfocar los esfuerzos en objetivos concretos y alcanzables en cada ciclo. Este enfoque es especialmente relevante para NoraAI, ya que permite ajustar prioridades en respuesta a hallazgos técnicos—como la optimización de los prompts del agente de IA—y asegurar que el producto evolucione de manera constante y alineada con los requisitos del cliente.

### **3. ANÁLISIS DE REQUERIMIENTOS**

#### **3.1. Funciones del Producto**

_Figura 1: Diagrama de descomposición de requerimientos de página web._

#### **3.2. Características de los Usuarios**

El sistema NoraAI ha sido diseñado para ser utilizado por distintos perfiles de usuario, cada uno con responsabilidades y permisos específicos:
*   **Cliente:** Es el usuario final de GearUp Gadgets que busca soporte. No tiene acceso a la plataforma NoraAI, pero interactúa con ella al iniciar una solicitud de soporte por correo electrónico o formulario web y al recibir las respuestas generadas por el sistema.
*   **Agente de Soporte Nivel 1 (Triaje):** Personal cuyo objetivo principal es procesar la cola de tickets con sugerencias de la IA de la forma más rápida y eficiente posible. Su rol es validar, aprobar con un solo clic, editar o escalar las respuestas sugeridas. Requiere una interfaz clara que minimice la ambigüedad y agilice las tareas repetitivas.
*   **Agente de Soporte Nivel 2 (Especialista):** Personal con conocimiento técnico profundo, responsable de resolver los casos complejos que son escalados. Su frustración es recibir tickets sin el contexto adecuado, por lo que necesita herramientas para investigar el historial del cliente y del problema a fondo.
*   **Administrador del Sistema:** Rol con los máximos privilegios, responsable tanto de la configuración técnica como de la supervisión operativa del sistema. Sus tareas incluyen la gestión de usuarios y roles, la configuración de los agentes de IA (prompts y umbrales), y el monitoreo de los indicadores de rendimiento (KPIs) del equipo de soporte.

#### **3.3. Jerarquía de Usuarios**

La plataforma NoraAI define una jerarquía de usuarios basada en los roles y permisos dentro del sistema, diseñada para garantizar la seguridad, la eficiencia operativa y una clara separación de responsabilidades:
*   **Administrador del Sistema:** Es el rol con el nivel más alto de privilegios. Los administradores tienen acceso completo a todas las funcionalidades del sistema, incluyendo:
    *   Gestión de todos los usuarios y sus roles.
    *   Configuración de los agentes de IA, plantillas y reglas de negocio.
    *   Visualización de dashboards con métricas de rendimiento globales y por agente.
    *   Acceso sin restricciones a todos los tickets y registros de auditoría.
*   **Agente de Soporte (Nivel 1 y Nivel 2):** Es el rol operativo estándar. Los agentes son los usuarios que gestionan las interacciones diarias con los clientes. Aunque funcionalmente se dividen en Nivel 1 (Triaje) y Nivel 2 (Especialistas), ambos operan bajo el mismo rol de AGENTE en el sistema, con acceso a:
    *   Sus colas de trabajo asignadas.
    *   Crear, visualizar, editar y responder tickets.
    *   Utilizar plantillas y dejar notas internas.
    *   Visualizar su propio dashboard de rendimiento.
    *   No tienen permisos para modificar la configuración del sistema ni para gestionar otros usuarios.
*   **Cliente:** No es un usuario con acceso al dashboard de NoraAI, sino la entidad externa a la que el sistema presta servicio. Su interacción se limita a los canales de comunicación públicos (correo electrónico, formulario web) y no posee credenciales ni permisos dentro de la plataforma.

#### **3.4. Restricciones del Sistema**

**3.4.1. Dependencias de Servicios y Políticas Reguladoras:** La operatividad de NoraAI está sujeta a la adquisición de un dominio web y a la contratación de servicios de hosting. Fundamentalmente, el sistema depende de la disponibilidad y las limitaciones de los planes de nivel gratuito de servicios de terceros, incluyendo Supabase (autenticación y almacenamiento), Mailgun (gestión de email), OpenRouter (servicios LLM), Vercel (hosting de frontend) y Render (hosting de backend). El sistema operará bajo un modelo single-tenant.

**3.4.2. Limitaciones De Hardware:** No existen limitaciones a nivel de hardware. La aplicación web será desarrollada para garantizar la compatibilidad con las versiones más recientes de los principales navegadores web (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge) en sistemas operativos de escritorio.

**3.4.3. Integraciones con sistemas externos:** A diferencia de un sistema aislado, NoraAI está intrínsecamente conectado a servicios externos. Su funcionalidad principal depende de las interfaces de programación (API) de estos servicios. La configuración y mantenimiento de estas conexiones (ej. webhooks, claves API) son críticas para la operación del sistema.

**3.4.4. Requisitos de Auditoría y Trazabilidad:** El sistema mantendrá un registro detallado de eventos (LogEvento) para fines de auditoría. Un administrador podrá rastrear el ciclo de vida de un ticket, incluyendo qué agente aprobó una sugerencia de la IA, cambios de estado y asignaciones, garantizando una trazabilidad completa de las acciones.

**3.4.5. Requisitos De Lenguaje:** Toda la interfaz de usuario (UI), así como la documentación técnica y de usuario, será desarrollada íntegramente en idioma español.

**3.4.6. Fiabilidad y pruebas:** Para garantizar la credibilidad y el correcto funcionamiento, la aplicación se someterá a un plan de pruebas End-to-End (E2E). Se implementará un modo de "mock" para el adaptador LLM, que permitirá realizar demostraciones y pruebas de forma fiable y predecible, sin depender de la latencia o disponibilidad del servicio externo.

**3.4.7. Consideraciones De Seguridad:** El acceso a las funcionalidades del sistema requerirá autenticación gestionada a través de Supabase Auth. La comunicación entre el frontend y el backend estará protegida mediante el uso de JSON Web Tokens (JWT). La gestión de credenciales y la encriptación de contraseñas se delegan a Supabase, asegurando la implementación de estándares de seguridad robustos.

### **4. ARTEFACTOS DE DISEÑO**

#### **4.1. Diagramas de Actividades**

Dentro del Lenguaje Unificado de Modelado (UML), los diagramas de actividades se clasifican como diagramas de comportamiento. Su función principal es describir de manera visual y secuencial los flujos de trabajo del sistema, detallando lo que debe suceder desde una perspectiva dinámica. Para un proyecto como NoraAI, estos diagramas actúan como un puente entre el equipo de desarrollo y los responsables de negocio de GearUp Gadgets, permitiendo que todos comprendan de manera unificada los procesos clave del sistema.

La creación de diagramas de actividades para NoraAI ofrece beneficios concretos:
*   **Ilustrar los Flujos de Trabajo Clave:** Permiten describir paso a paso los casos de uso, como el flujo de triaje de un ticket o el proceso de escalado.
*   **Visualizar la Lógica de Negocio:** Demuestran la lógica de algoritmos y reglas complejas.
*   **Alinear a los Actores del Sistema:** Mapean el flujo de trabajo entre los diferentes usuarios y el sistema.
*   **Simplificar y Validar Procesos:** Facilitan la identificación de cuellos de botella o ineficiencias.
*   **Modelar Operaciones del Sistema:** Permiten modelar la secuencia de operaciones de software.

Para la modelación y representación visual de los flujos de trabajo del sistema NoraAI, se empleó la herramienta de diagramación en línea **Draw.io**.

#### **4.2. Diagrama de Clases**

El diagrama de clases es una representación estática fundamental dentro del paradigma de programación orientado a objetos. Para el proyecto NoraAI, este diagrama define la estructura de las clases que se implementarán en el backend (NestJS/TypeScript) y las relaciones que existen entre ellas, como la herencia, la agregación y la asociación.

Este diagrama es el equivalente visual del modelo lógico de datos y se puede considerar el homólogo UML del modelo Entidad-Relación (E/R). En el contexto de NoraAI, el diagrama de clases es la formalización gráfica del esquema de la base de datos definido a través del ORM Prisma.

### **5. PROCESO DE VALIDACIÓN**

#### **5.1. Metodología de Listas de Chequeo**

Las listas de chequeo consisten en un formato para realizar acciones repetitivas que hay que verificar. Con la ayuda de estas listas, se comprueba de una forma ordenada y sistemática el cumplimiento de los requisitos. Esta técnica se prepara para que su uso sea fácil e interfiera lo menos posible con la actividad de quien realiza el registro.

Los pasos para su elaboración incluyen:
*   Determinar el área que se quiere evaluar.
*   Diseñar el formato de verificación (categorías, escala, cuadrícula).
*   Asegurarse de que todas las partes del checklist estén claramente descritas.
*   Tomar nota de la información en el formato.
*   Registrarlo para su tratamiento estadístico y análisis.

#### **5.2. Lista de Chequeo - Módulo de Reportes**

| ITM | ACTIVIDAD                                                                                                                   | CUMPLE | NO CUMPLE | NO APLICA |
| :-: | --------------------------------------------------------------------------------------------------------------------------- | :----: | :-------: | :-------: |
| 01  | ¿El reporte generado (HTML/CSV) muestra el nombre del sistema "NoraAI"?                                                     |        |           |           |
| 02  | ¿El reporte incluye la fecha y hora de su generación?                                                                       |        |           |           |
| 03  | ¿Los campos de fecha en el reporte utilizan un formato consistente (ej. DD-MM-AAAA HH:mm)?                                  |        |           |           |
| 04  | ¿La exportación a CSV contiene una fila de encabezado con los nombres de las columnas?                                       |        |           |           |
| 05  | ¿El reporte de tickets incluye como mínimo los siguientes campos: ID de Ticket, Cliente, Agente Asignado, Estado, Prioridad y Fecha de Creación? |        |           |           |
| 06  | ¿El reporte en formato HTML sigue la paleta de colores y branding definidos para la aplicación?                               |        |           |           |
| 07  | ¿El sistema permite filtrar los tickets (por estado, agente, fecha) antes de generar la exportación?                          |        |           |           |
| 08  | ¿La exportación maneja correctamente campos con texto largo (ej. cuerpo de un mensaje) sin truncamiento inesperado?         |        |           |           |
| 09  | ¿Se puede generar un reporte de resumen de actividad (tickets creados vs. resueltos) para un rango de fechas específico?     |        |           |           |
| 10  | ¿El proceso de exportación de grandes volúmenes de datos se realiza de forma asíncrona para no bloquear la interfaz?         |        |           |           |

#### **5.3. Lista de Chequeo - Infraestructura y Servicios (Hardware)**

| ITM | ACTIVIDAD                                                                                                     | CUMPLE | NO CUMPLE | NO APLICA |
| :-: | ------------------------------------------------------------------------------------------------------------- | :----: | :-------: | :-------: |
| 01  | ¿El frontend de la aplicación está desplegado y operativo en Vercel?                                          |        |           |           |
| 02  | ¿El backend de la aplicación está desplegado y operativo en Render?                                           |        |           |           |
| 03  | ¿La base de datos PostgreSQL está provisionada y conectada correctamente al backend?                           |        |           |           |
| 04  | ¿El servicio de Supabase Auth está integrado para la autenticación y gestión de usuarios?                      |        |           |           |
| 05  | ¿El servicio de Supabase Storage está integrado para el almacenamiento de archivos adjuntos?                   |        |           |           |
| 06  | ¿La integración con Mailgun para el envío de correos electrónicos salientes está configurada y funcional?      |        |           |           |
| 07  | ¿El webhook de Mailgun para la recepción de correos entrantes está implementado y asegurado?                   |        |           |           |
| 08  | ¿La configuración DNS (registros MX, SPF/DKIM) para el dominio de correo es correcta para garantizar la entregabilidad? |        |           |           |
| 09  | ¿La integración con el proveedor de LLM (OpenRouter) está configurada con las credenciales correctas?          |        |           |           |
| 10  | ¿Toda la comunicación entre servicios y con el cliente final está cifrada mediante HTTPS?                       |        |           |           |

#### **5.4. Lista de Chequeo - Componentes de Software**

| ITM | ACTIVIDAD                                                                                                                   | CUMPLE | NO CUMPLE | NO APLICA |
| :-: | --------------------------------------------------------------------------------------------------------------------------- | :----: | :-------: | :-------: |
| 01  | ¿El backend está desarrollado sobre el framework NestJS con TypeScript?                                                     |        |           |           |
| 02  | ¿Se utiliza Prisma como ORM para todas las interacciones con la base de datos?                                               |        |           |           |
| 03  | ¿El frontend está desarrollado con React (Vite) y utiliza Tailwind CSS para los estilos?                                    |        |           |           |
| 04  | ¿La API del backend está protegida y requiere un token JWT válido para el acceso a endpoints privados?                       |        |           |           |
| 05  | ¿La arquitectura del sistema corresponde a un modelo single-tenant, como se especifica en los requisitos?                    |        |           |           |
| 06  | ¿El adaptador del LLM incluye un modo "mock" que permite operar la aplicación sin conexión al servicio externo para fines de demostración y pruebas? |        |           |           |

### **6. FIRMAS DE APROBACIÓN**

| **Elaboró** | **Aprobó** | **Validó** |
| :---------: | :--------: | :--------: |
|    **Firma**    |   **Firma**    |   **Firma**    |
|             |            |            |
| **Fecha:**      |  **Fecha:**    |  **Fecha:**    |