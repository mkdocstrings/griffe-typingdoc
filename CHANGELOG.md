# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.2.2](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.2) - 2023-10-16

<small>[Compare with 0.2.1](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.1...0.2.2)</small>

### Bug Fixes

- Do not always add docstrings to attributes ([02d8cb6](https://github.com/mkdocstrings/griffe-typingdoc/commit/02d8cb6d70edc3869767561e42003b6ef97ac1cd) by Timothée Mazzucotelli).

## [0.2.1](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.1) - 2023-10-05

<small>[Compare with 0.2.0](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.0...0.2.1)</small>

### Bug Fixes

- Fix casing of `deprecated`, only set metadata when annotated element is known ([98f3c2c](https://github.com/mkdocstrings/griffe-typingdoc/commit/98f3c2c296e946dee0fd30ae533515c1896022e1) by Sebastián Ramírez).

## [0.2.0](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.0) - 2023-09-14

<small>[Compare with 0.1.0](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.1.0...0.2.0)</small>

### Dependencies

- Depend on Griffe ([cc15edc](https://github.com/mkdocstrings/griffe-typingdoc/commit/cc15edc3b170e891fa37ff69b58eb9fea7af8fa8) by Timothée Mazzucotelli).

### Features

- Support more experimental annotations (names, deprecations, warnings, exceptions) ([afa6dd9](https://github.com/mkdocstrings/griffe-typingdoc/commit/afa6dd96fe7dc90d16934b1b191484f891f56d92) by Timothée Mazzucotelli). [Issue #1](https://github.com/mkdocstrings/griffe-typingdoc/issues/1), [PR #3](https://github.com/mkdocstrings/griffe-typingdoc/pull/3)

### Code Refactoring

- Refactor implementation with latest version in `typing_extensions`, `Doc()`, and de-indent ([c7a61c6](https://github.com/mkdocstrings/griffe-typingdoc/commit/c7a61c68a39d6dbb4955037cd18f96be214f2d0d) by Sebastián Ramírez). [PR #2](https://github.com/mkdocstrings/griffe-typingdoc/pull/2)

## [0.1.0](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.1.0) - 2023-08-29

<small>[Compare with first commit](https://github.com/mkdocstrings/griffe-typingdoc/compare/10139be2140f73617681a1f7ca2c4514ea9017e5...0.1.0)</small>

### Dependencies

- Always depend on typing-extensions, use @tiangolo's fork to test ([33d242e](https://github.com/mkdocstrings/griffe-typingdoc/commit/33d242e22237fc4652b86d44c7b8655ded661342) by Timothée Mazzucotelli).

### Features

- Support Python 3.8 thanks to typing-extensions ([489aaac](https://github.com/mkdocstrings/griffe-typingdoc/commit/489aaacd8e2cea3c57dd6c2ce7f9635e4489e8b4) by Timothée Mazzucotelli).
- Implement extension ([5fccd06](https://github.com/mkdocstrings/griffe-typingdoc/commit/5fccd065f6717e195bd7fbc7c4f487ae6bd413b1) by Timothée Mazzucotelli).
- Generate project with copier-pdm ([10139be](https://github.com/mkdocstrings/griffe-typingdoc/commit/10139be2140f73617681a1f7ca2c4514ea9017e5) by Timothée Mazzucotelli).

### Code Refactoring

- Update to support new proposal (https://peps.python.org/pep-0727/) ([bd3eecd](https://github.com/mkdocstrings/griffe-typingdoc/commit/bd3eecdc96755dc4fa50a1cd5049e8366ab2ba72) by Timothée Mazzucotelli).
- Use newer Griffe extensions ([199609f](https://github.com/mkdocstrings/griffe-typingdoc/commit/199609f053c04b8d0c21e7026c5f2eb1ad268ead) by Timothée Mazzucotelli).
- Remove CLI setup ([48dea50](https://github.com/mkdocstrings/griffe-typingdoc/commit/48dea500a5543f389816eee5ef6e98f5541d090d) by Timothée Mazzucotelli).
