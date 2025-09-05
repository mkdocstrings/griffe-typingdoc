# Griffe TypingDoc

Griffe extension for [PEP 727 – Documentation Metadata in Typing](https://peps.python.org/pep-0727/).

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
