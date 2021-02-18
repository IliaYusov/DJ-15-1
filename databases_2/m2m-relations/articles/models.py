from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Scope(models.Model):

    topic = models.CharField(max_length=64, verbose_name='Тема')
    articles = models.ManyToManyField(Article, through='ArticleScope')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'


class ArticleScope(models.Model):
    article = models.ForeignKey(Article, related_name='scopes', on_delete=models.CASCADE)
    scope = models.ForeignKey(Scope, verbose_name='Раздел', on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основной')

    def __str__(self):
        return f'{self.article}_{self.scope}'

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        unique_together = ('article', 'scope')
