from django.db import models
from django.urls import reverse
import uuid 
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="输入书的流派")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('书名', max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000, help_text="输入书的简介")
    isbn = models.CharField("ISBN",max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre,help_text='选择一个流派')
    
    def __str__(self):
        return self.title
    
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = '流派'
    

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="id必须唯一")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', "维护"),
        ('o',"借出"),
        ('a','可用'),
        ('r','保留')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,default='m',help_text='帮助文档')

    class Meta:
        ordering = ["due_back"]
    
    def display_book(self):
        return self.book.title
    display_book.short_description = '书名'

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField('姓', max_length=100)
    last_name = models.CharField('名', max_length=100)
    date_of_birth = models.DateField('出生日期', null=True, blank=True)
    date_of_death = models.DateField('死亡日期', null=True, blank=True)
  
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s%s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']