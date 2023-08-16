from django.urls import path
from . import views


app_name = "docs"


urlpatterns = [
    path("", views.index, name="index"),
]

# Get all documents from ./documents directory
# and create a path for each one
for doc in views.get_docs():
    print("Registered: " + doc[0])
    urlpatterns.append(
        path(doc[0], views.doc, name=doc[1])
    )
