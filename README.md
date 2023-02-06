# Link Shortener

## Images
![Main Page](./images/main.jpg "Main Page") 

![Analytics Page](./images/analytics.jpg "Analytics Page")

![Diagram Page](./images/diagram.jpg "Diagram Page")

## Used Technologies
- Python
- Django
- Docker and Docker Compose
- Nginx and Gunicorn
- PostgresQL
- HTML, CSS, and Bootstrap
- JavaScript and jQuery
- ChartJS

## Useful Docker Commands

### Building
Development:
```bash
docker-compose up
```
### Following Logs
Development:
```bash
docker-compose -f docker-compose.yml logs -f
```
### Migration
In development migration are applied automatically in `entrypoint.sh`.