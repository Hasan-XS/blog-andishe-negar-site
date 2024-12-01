from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post


# Post list and home page
def post_list(request):
    """
    This function is responsible for the view that displays the list of posts on the homepage.
    The main task of this function is to display the published posts, which can optionally be filtered
    using a search query.

    Steps of operation:
    1. **Getting the query**: First, the search query (query) is retrieved from the URL. If the user hasn't entered
       anything, the query will be empty.
    2. **Filtering the posts**: If a query is provided, the posts are filtered based on their titles containing
       the search term and having a "published" status.
       If no query is provided, all published posts are displayed.
    3. **Ordering the posts**: The posts are ordered by their creation date in descending order (newest first).
    4. **Pagination**: To limit the number of posts displayed on each page, pagination is used. In this case, 5 posts
       are displayed per page. The page number is obtained from the URL and the posts are split accordingly.
    5. **Rendering the posts**: Finally, the filtered and paginated posts are sent to the `index.html` template to
       be displayed on the web page.

    Parameters:
    - `request`: The HTTP request containing the search query and pagination information.

    Returns:
    - This function returns the `index.html` template with the filtered, paginated posts and the search query.
    """

    query = request.GET.get("q", "")
    if query:
        post_list = Post.objects.filter(
            title__icontains=query, status="published"
        ).order_by("-created_at")
    else:
        post_list = Post.objects.filter(status="published").order_by("-created_at")

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"page_obj": page_obj, "query": query})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
