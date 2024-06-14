
from django.urls import path, include

from home_page.views import home_page
from posts.views import articles_page_pat, article_detail_page_pat, articles_page_doc, article_detail_page_doc, \
    add_article_page_doc, article_detail_page_admin, articles_page_admin, add_article_page_admin, add_article_post

app_name = "posts"

urlpatterns = [
    path("all_articles_pat/", articles_page_pat, name="all_articles_pat"),
    path("article_detail_pat/<article_id>/", article_detail_page_pat, name="article_detail_pat"),

    path("all_articles_doc/", articles_page_doc, name="all_articles_doc"),
    path("all_articles_admin/", articles_page_admin, name="all_articles_admin"),
    path("article_detail_doc/<article_id>/", article_detail_page_doc, name="article_detail_doc"),
    path("article_detail_admin/<article_id>/", article_detail_page_admin, name="article_detail_admin"),

    path("add_article_doc/", add_article_page_doc, name="add_article_doc"),

    path("add_article_post/", add_article_post, name="add_article_post"),
    path("add_article_admin/", add_article_page_admin, name="add_article_admin"),

]
