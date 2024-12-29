from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dictionary_app.models import AramaicWord, WordVerse, WordCrossReference, UserAnnotation
from bible_app.models import Verse

class Command(BaseCommand):
    help = 'Adiciona dados de exemplo para testar as novas funcionalidades'

    def handle(self, *args, **kwargs):
        # Criar usuário de teste se não existir
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_active': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuário de teste criado'))

        # Pegar algumas palavras e versículos existentes
        words = AramaicWord.objects.all()[:5]
        verses = Verse.objects.all()[:10]

        if not words or not verses:
            self.stdout.write(self.style.ERROR('Não há palavras ou versículos suficientes no banco de dados'))
            return

        # Criar ocorrências de palavras em versículos
        for i, word in enumerate(words):
            for j, verse in enumerate(verses[i:i+2]):  # 2 versículos por palavra
                WordVerse.objects.create(
                    word=word,
                    verse=verse,
                    position=j+1,
                    context=f"Trecho do versículo contendo a palavra {word.aramaic_word}"
                )
                self.stdout.write(self.style.SUCCESS(f'Criada ocorrência para {word.aramaic_word} em {verse}'))

        # Criar referências cruzadas
        reference_texts = [
            'Talmud Babilônico',
            'Targum Onkelos',
            'Zohar',
            'Manuscritos do Mar Morto'
        ]

        for word in words:
            for text in reference_texts[:2]:  # 2 referências por palavra
                WordCrossReference.objects.create(
                    word=word,
                    reference_text=text,
                    reference_location=f'Capítulo 1, Linha {word.id}',
                    context=f'Contexto da palavra {word.aramaic_word} em {text}',
                    url=f'https://example.com/{text.lower().replace(" ", "-")}/1',
                    notes=f'Nota sobre o uso de {word.aramaic_word} em {text}'
                )
                self.stdout.write(self.style.SUCCESS(f'Criada referência para {word.aramaic_word} em {text}'))

        # Criar anotações
        for word in words:
            # Anotação privada
            UserAnnotation.objects.create(
                user=user,
                word=word,
                content=f'Anotação privada sobre {word.aramaic_word}',
                is_public=False
            )
            
            # Anotação pública
            UserAnnotation.objects.create(
                user=user,
                word=word,
                content=f'Anotação pública sobre {word.aramaic_word}',
                is_public=True
            )
            self.stdout.write(self.style.SUCCESS(f'Criadas anotações para {word.aramaic_word}'))

        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
