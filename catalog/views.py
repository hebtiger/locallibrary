from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
# Create your views here.


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':
        num_instances_available,'num_authors':num_authors,  'num_visits':num_visits},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
    context_object_name = 'my_book_list'  
    template_name = 'books/my_arbitrary_template_name_list.html' 

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='白')[:5] 
    
    def get_context_data(self, **kwargs):
        context = super(BookListView,self).get_context_data(**kwargs)
        context['some_date'] = '这是一些数据'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author