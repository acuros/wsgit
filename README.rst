
Overview
========

imdjango is django plugin for making mobile application server(with bson protocol) immediately by reusing your django web application.
If you use imdjango, you can make your django web server as mobile application server in TCP(Not HTTP). 
What it means, you can reuse already made your all of web application server source code.

What you have to do to make mobile server is only installing imdjango and write view.

INSTALL
=======
#. Download this project on your djangoproject directory 
#. Add 'imdjango' to your ``INSTALLED_APPS`` in ``setings.py`` file::

       INSTALLED_APPS = (
           ...
           'imdjango',
       )

START SERVER
============
::

        $python manage.py runimdjango [host] [port]

Default host is 0.0.0.0, port is 9338.
You can set default host, port with ``MOBILE_HOST``, ``MOBILE_PORT`` in ``settings.py``.


Tutorial
========


Server Code
___________

urls.py ::

    url(r'^book/', include('book.urls')),

book/urls.py ::

    url('list/$', 'book.views.book_list'),

book/models.py ::

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=50)

    class Book(models.Model):
        PAGE_LIMIT = 20

        name = models.CharField(max_length=100)
        author = models.ForeignKey(Author)
        price = models.FloatField()

book/views.py ::

    from django.core.paginator import Paginator, InvalidPage, EmptyPage
    from imdjango.utils import serialize_page
    from book.models import Book, Author

    def paginate(queryset, page):
        paginator = Paginator(queryset, 20)
        try:
            page = int(page)
        except ValueError:
            page = 1
        try:
            return paginator.page(page)
        except (EmptyPage, InvalidPage):
            return paginator.page(paginator.num_pages)
            
    def book_list(request):
        books = Book.objects.all()
        if request.GET.has_key('author_name'):
            try:
                author = Author.objects.get(name=request.GET['author_name'])
            except Author.DoesNotExist:
                raise InvalidParameterError('Author not exist')
            books = books.filter(author=author)
        book_page = paginate(books, request.GET.get('page', 1))
        return dict(book_page=serialize_page(book_page))


Client Test
___________

::

    >>> s = socket(AF_INET, SOCK_STREAM)
    >>> s.connect(('localhost', 9338))
    >>> s.sendobj({'url':'/book/list/?author_name=Acuros+Kim'})
    >>> s.recvobj()
    {u'status': {u'reason': 'OK', u'code': 'OK'}, u'book_page': {u'object_list': [{u'pk': 1, u'model': u'book.book', u'fields': {u'price': 10.0, u'name': u'How to imdjango', u'author': 1}}, {u'pk': 2, u'model': u'book.book', u'fields': {u'price': 10.0, u'name': u'Foo book title', u'author': 1}}], u'num_pages': 1, u'number': 1}}
    >>> s.sendobj({'url':'/book/list/?author_name=Foo'})
    >>> s.recvobj()
    {u'status': {u'reason': 'Author not exist', u'code': 'InvalidParameterError'}}


