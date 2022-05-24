from django.db import models

from users import models as usermodels
from .validators import validate_year

SCORE_REVIEW = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
)


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название категории',
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название жанра',
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор жанра'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название',
        help_text='Название произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание произведения'
    )
    year = models.IntegerField(
        verbose_name='Год',
        help_text='Год выхода произведения',
        validators=(validate_year, )
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория произведения',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        usermodels.User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Оценка',
        choices=SCORE_REVIEW,
        null=False
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
    )
    author = models.ForeignKey(
        usermodels.User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
