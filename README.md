# 🎫 Ivanti Tickets Integration App

Una aplicación Python para extraer, transformar y exportar datos de incidentes y requerimientos desde Ivanti hacia formatos CSV y Excel, preparados para integración con SharePoint Lists y PowerApps.

## 📋 Descripción

Esta aplicación se conecta a la API REST de Ivanti para obtener datos de:
- **Incidentes** (Incidents)  
- **Requerimientos de Servicio** (Service Requests)

Los datos se unifican en un formato estándar y se exportan en archivos CSV y Excel (XLSX) que pueden ser fácilmente importados a SharePoint Lists y utilizados en PowerApps con Power Automate.

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Ivanti API    │───▶│  Python App      │───▶│ CSV/Excel Outputs   │
│                 │    │                  │    │                     │
│ • Incidents     │    │ • Data Fetch     │    │ • tickets_combinados│
│ • ServiceReqs   │    │ • Transform      │    │   .csv              │
│                 │    │ • Export         │    │ • tickets_combinados│
└─────────────────┘    └──────────────────┘    │   .xlsx             │
                                               └─────────────────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Microsoft 365 Ecosystem                         │
│                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ SharePoint Lists│  │   PowerApps     │  │ Power Automate  │    │
│  │                 │  │                 │  │                 │    │
│  │ • Data Storage  │  │ • UI/UX Layer   │  │ • Workflows     │    │
│  │ • List Management│ │ • Forms & Views │  │ • Automation    │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Características

- ✅ **Extracción automática** de datos desde Ivanti API
- ✅ **Paginación inteligente** para manejar grandes volúmenes de datos
- ✅ **Transformación de datos** a formato estándar
- ✅ **Zona horaria local** (America/Bogotá)
- ✅ **Exportación dual** a CSV y Excel
- ✅ **Manejo de errores** robusto
- ✅ **Configuración segura** con variables de entorno
- ✅ **Listo para SharePoint** y PowerApps

## 📊 Estructura de Datos de Salida

Los archivos generados contienen los siguientes campos unificados:

| Campo           | Tipo   | Descripción                           |
|----------------|--------|---------------------------------------|
| `Owner`        | String | Propietario del ticket                |
| `fecha_hoy`    | String | Fecha y hora de extracción            |
| `tipo`         | String | Tipo de ticket (`inc` o `req`)        |
| `fecha_creacion` | String | Fecha de creación del ticket        |
| `hora_creacion`  | String | Hora de creación del ticket         |
| `idticket`     | String | Número único del ticket               |
| `asunto`       | String | Asunto/descripción del ticket         |
| `estado`       | String | Estado actual del ticket              |

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- Acceso a la API REST de Ivanti
- Credenciales válidas (Domain API y REST API Key)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd tickets
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en el directorio `app/`:
   ```env
   DOMAIN_API='your-company.ivanticloud.com'
   REST_API_KEY='YOUR_API_KEY_HERE'
   ```

## 🏃‍♂️ Uso

### Ejecución Básica

```bash
cd app
python main.py
```

### Salida Esperada

```
Fetching incidents 0 to 100...
Retrieved 100 incidents. Total: 100
Fetching incidents 100 to 200...
Retrieved 50 incidents. Total: 150
No more incidents to fetch
Fetching service requests 0 to 100...
Retrieved 75 service requests. Total: 75
No more service requests to fetch

✓ Successfully exported 225 records to tickets_combinados.csv
  - Incidents: 150
  - Service Requests: 75
✓ Successfully exported 225 records to tickets_combinados.xlsx
```

### Archivos Generados

- `tickets_combinados.csv` - Formato CSV para importación rápida
- `tickets_combinados.xlsx` - Formato Excel con mejor formateo

## 🔧 Configuración

### Variables de Entorno

| Variable      | Descripción                           | Ejemplo                              |
|---------------|---------------------------------------|--------------------------------------|
| `DOMAIN_API`  | Dominio de tu instancia Ivanti       | `your-company.ivanticloud.com`      |
| `REST_API_KEY`| Clave de API REST de Ivanti          | `YOUR_32_CHARACTER_API_KEY_HERE`    |

### Personalización

El código es fácilmente personalizable para:
- Agregar nuevos campos de datos
- Modificar transformaciones de datos  
- Cambiar formatos de fecha/hora
- Ajustar parámetros de paginación

## 🔗 Integración con Microsoft 365

### SharePoint Lists

1. **Crear nueva lista en SharePoint**
2. **Definir columnas** según la estructura de datos
3. **Importar CSV/Excel** usando la funcionalidad nativa de SharePoint
4. **Configurar permisos** apropiados

### PowerApps

1. **Conectar a SharePoint List** como fuente de datos
2. **Crear formularios** para visualización y edición
3. **Implementar filtros** por tipo de ticket, estado, etc.
4. **Diseñar dashboards** para métricas y KPIs

### Power Automate

Ejemplos de flujos automatizados:

- **Sincronización periódica**: Ejecutar el script automáticamente
- **Notificaciones**: Alertas por nuevos tickets críticos  
- **Aprobaciones**: Workflows para resolución de tickets
- **Reportes**: Generación automática de informes

## 📁 Estructura del Proyecto

```
tickets/
├── app/
│   ├── main.py                 # Aplicación principal
│   ├── requirements.txt        # Dependencias Python
│   ├── .env                   # Variables de entorno (no versionado)
│   ├── tickets_combinados.csv # Salida CSV (generado)
│   └── tickets_combinados.xlsx # Salida Excel (generado)
├── .gitignore                 # Archivos excluidos de Git
└── README.md                  # Esta documentación
```

## 🛡️ Seguridad

- ✅ **Variables de entorno** para credenciales sensibles
- ✅ **`.gitignore`** configurado para excluir archivos sensibles
- ✅ **HTTPS** para todas las comunicaciones API
- ⚠️ **Rotación de API Keys** recomendada periódicamente

## 🐛 Solución de Problemas

### Error de Conexión
```
Error fetching data: HTTPSConnectionPool...
```
**Solución**: Verificar conectividad de red y credenciales API

### Error de Autenticación  
```
Error fetching data: 401 Unauthorized
```
**Solución**: Verificar `REST_API_KEY` en archivo `.env`

### Error de Formato de Fecha
```
Error processing data: time data '...' does not match format
```
**Solución**: El formato de fecha de Ivanti puede haber cambiado. Revisar función `transform_records`

## 📝 Dependencias

### Principales
- `requests` - Cliente HTTP para API calls
- `openpyxl` - Manipulación de archivos Excel
- `python-dotenv` - Manejo de variables de entorno

### Completas
```
certifi==2025.11.12
charset-normalizer==3.4.4
dotenv==0.9.9
et_xmlfile==2.0.0
idna==3.11
openpyxl==3.1.5
python-dotenv==1.2.1
requests==2.32.5
urllib3==2.5.0
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/NuevaCaracteristica`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Contacto

Para soporte técnico o consultas sobre integración con SharePoint/PowerApps, contactar al equipo de desarrollo.

---

**¡Listo para transformar tus datos de Ivanti en potentes aplicaciones de Microsoft 365!** 🚀