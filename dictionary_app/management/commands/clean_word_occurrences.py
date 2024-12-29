from django.core.management.base import BaseCommand
from django.db import connection
from dictionary_app.models import WordOccurrence, AramaicWord

class Command(BaseCommand):
    help = 'Limpa registros problemáticos de ocorrências de palavras'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando limpeza de ocorrências...')
        
        # Remove ocorrências órfãs (onde a palavra não existe mais)
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE wo FROM dictionary_app_wordoccurrence wo
                LEFT JOIN dictionary_app_aramaicword aw ON wo.word_id = aw.id
                WHERE aw.id IS NULL
            """)
            cursor.execute("COMMIT")
            
        # Remove duplicatas mantendo apenas o registro mais antigo
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE t1 FROM dictionary_app_wordoccurrence t1
                INNER JOIN dictionary_app_wordoccurrence t2
                WHERE t1.id > t2.id 
                AND t1.word_id = t2.word_id 
                AND t1.verse_id = t2.verse_id
            """)
            cursor.execute("COMMIT")
            
        self.stdout.write(self.style.SUCCESS('Limpeza concluída com sucesso!'))
