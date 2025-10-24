# Griffe TypingDoc

Griffe extension for [`annotated-doc`](https://pypi.org/project/annotated-doc/) (originally [PEP 727](https://peps.python.org/pep-0727/)):

> Document parameters, class attributes, return types, and variables inline, with Annotated.

## Installation

```
pip install griffe-typingdoc
```

To use the extension in a MkDocs project, use this configuration:

```
# mkdocs.yml
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          extensions:
          - griffe_typingdoc
```
