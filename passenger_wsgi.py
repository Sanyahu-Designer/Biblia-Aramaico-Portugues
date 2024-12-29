import os
import sys

# Adicione o caminho para o projeto
sys.path.insert(0, '/home/netsarim/staging')

# Adicione o caminho para o ambiente virtual
sys.path.insert(0, '/home/netsarim/virtualenv/staging/3.11/lib/python3.11/site-packages')

# Carregue a aplicação Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bible_project.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()