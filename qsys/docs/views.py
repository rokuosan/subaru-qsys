import glob
import re
from django.shortcuts import render
import yaml


def index(request):
    docs = get_docs()
    print(docs)

    return render(request, "docs/index.html")


def get_docs() -> tuple:
    docs = []

    for doc in glob.glob("docs/documents/**/*.md", recursive=True):
        pathname = "/".join(doc.split("/")[2:])
        filename = doc.split("/")[-1]
        dirname = doc.split("/")[-2]

        if filename == "index.md":
            if dirname == "documents":
                docs.append(("", "index"))
            else:
                docs.append((pathname[:-8], "index_" + dirname))
        else:
            docs.append((pathname[:-3], filename + "_" + dirname))
    return tuple(docs)


def doc(request):
    if request.path == "/docs/":
        if "" in [d[0] for d in get_docs()]:
            try:
                with open("docs/documents/index.md", "r") as f:
                    doc_content = f.read()
                    data = get_data(doc_content)
                    if data:
                        yml = yaml.safe_load(data)
                    doc_content = re.sub(
                        r"^\-{3}[\n\r](.+)[\n\r]\-{3}",
                        "",
                        doc_content,
                        flags=re.DOTALL,
                    )
                    return render(
                        request,
                        "docs/doc.html",
                        {
                            "doc_content": doc_content,
                            "doc_name": "index",
                            "yml": yml,
                        },
                    )
            except Exception:
                return render(request, "docs/404.html")
        else:
            return render(request, "docs/index.html")

    doc_name = request.path.replace("/docs/", "", 1)
    docs = [d[0] for d in get_docs()]
    if doc_name in docs:
        data = ""
        yml = None
        try:
            if doc_name.endswith("/"):
                doc_name = doc_name + "index"
            with open(f"docs/documents/{doc_name}.md", "r") as f:
                doc_content = f.read()
                data = get_data(doc_content)
                if data:
                    yml = yaml.safe_load(data)
        except Exception:
            return render(request, "docs/404.html")

        doc_content = re.sub(
            r"^\-{3}[\n\r](.+)[\n\r]\-{3}",
            "",
            doc_content,
            flags=re.DOTALL,
        )

        return render(
            request,
            "docs/doc.html",
            {"doc_content": doc_content, "doc_name": doc_name, "yml": yml},
        )

    else:
        return render(request, "docs/404.html")


def get_data(text):
    data = re.search(r"^\-{3}[\n\r](.+)[\n\r]\-{3}", text, flags=re.DOTALL)
    # data = re.search(r"---\n(.*)\n---", text, re.DOTALL)
    if data:
        return data.group(1)
    else:
        return None
