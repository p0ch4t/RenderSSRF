# RenderSSRF

Alguna vez estuviste probando un SSRF, y tuviste que copiar el código html para renderizarlo localmente? Si esto te paso, esta tool es para vos!

Pasos para ejecutar:

1. Clone el repositorio
2. Ingrese al mismo y ejecute `python3 manage.py runserver`
3. Automáticamente se levantará un servidor web donde podrá ingresar a renderizar sus SSRF

Notas: el endpoint
 - /config --> Sirve para configurar su SSRF (se le solicita la petición de burp)
 - /browser --> Renderiza el sitio web que ingreses
