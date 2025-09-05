# Griffe TypingDoc

[![ci](https://github.com/mkdocstrings/griffe-typingdoc/workflows/ci/badge.svg)](https://github.com/mkdocstrings/griffe-typingdoc/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://mkdocstrings.github.io/griffe-typingdoc/)
[![pypi version](https://img.shields.io/pypi/v/griffe-typingdoc.svg)](https://pypi.org/project/griffe-typingdoc/)
[![gitter](https://img.shields.io/badge/matrix-chat-4DB798.svg?style=flat)](https://app.gitter.im/#/room/#griffe-typingdoc:gitter.im)

Griffe extension for [PEP 727 – Documentation Metadata in Typing](https://peps.python.org/pep-0727/).

## Installation

```bash
pip install griffe-typingdoc
```

To use the extension in a MkDocs project,
use this configuration:

```yaml
# mkdocs.yml
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          extensions:
          - griffe_typingdoc
```
