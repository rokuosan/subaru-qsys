import os
from django.shortcuts import render


def index(request):
    return render(request, "docs/index.html")


def get_docs() -> tuple:
    docs = []

    for doc in os.listdir("docs/documents"):
        if doc.endswith(".md"):
            docs.append((doc, doc[:-3]))
    return tuple(docs)


def doc(request):
    request_url = request.path
    doc_name = request_url.split("/")[-1]
    docs = [d[0] for d in get_docs()]
    if doc_name in docs:
        # Read the file
        try:
            with open(f"docs/documents/{doc_name}", "r") as f:
                doc_content = f.read()
        except Exception:
            return render(request, "docs/404.html")
        return render(
            request,
            "docs/doc.html",
            {"doc_content": doc_content, "doc_name": doc_name[:-3]},
        )

    else:
        return render(request, "docs/404.html")
