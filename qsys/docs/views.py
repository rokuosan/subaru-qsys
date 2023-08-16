import os
import re
from django.shortcuts import render
import yaml


def index(request):
    docs = get_docs()
    print(docs)

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
        data = ""
        yml = None
        try:
            with open(f"docs/documents/{doc_name}", "r") as f:
                doc_content = f.read()
                data = get_data(doc_content)
                if data:
                    yml = yaml.safe_load(data)
        except Exception:
            return render(request, "docs/404.html")

        if yml:
            title = yml.get("title", None)
            if title:
                doc_name = title
            doc_content = re.sub(r"---\n(.*)\n---", "", doc_content, re.DOTALL)
        else:
            doc_name = doc_name[:-3]

        return render(
            request,
            "docs/doc.html",
            {"doc_content": doc_content, "doc_name": doc_name},
        )

    else:
        return render(request, "docs/404.html")


def get_data(text):
    data = re.search(r"^\-{3}[\n\r](.+)[\n\r]\-{3}", text, re.DOTALL)
    # data = re.search(r"---\n(.*)\n---", text, re.DOTALL)
    if data:
        return data.group(1)
    else:
        return None
