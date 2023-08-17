from django.urls import path
from . import views


app_name = "docs"


urlpatterns = []

docs = views.get_docs()
if not docs:
    urlpatterns.append(path("", views.index, name="index"))
for doc in views.get_docs():
    urlpatterns.append(path(doc[0], views.doc, name=doc[1]))
