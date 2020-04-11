from django.views import generic
from .models import Book
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404


class BookList(generic.ListView):
    queryset = Book.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 3


# class BookDetail(generic.DetailView):
#     model = Post
#     template_name = 'book_detail.html'


def book_detail(request, slug):
    template_name = "book_detail.html"
    book = get_object_or_404(Book, slug=slug)
    comments = book.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.book = book
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "book": book,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

