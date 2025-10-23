# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.3.0](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.3.0) - 2025-10-23

<small>[Compare with 0.2.9](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.9...0.3.0)</small>

### Features

- Support `annotated_doc` package ([f3c6f4e](https://github.com/mkdocstrings/griffe-typingdoc/commit/f3c6f4ee383e1b163e3901313376ac8ffb5c19cf) by Timothée Mazzucotelli).

## [0.2.9](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.9) - 2025-09-05

<small>[Compare with 0.2.8](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.8...0.2.9)</small>

### Build

- Depend on Griffe 1.14 ([bc7cf59](https://github.com/mkdocstrings/griffe-typingdoc/commit/bc7cf59666f090c1735529083cb048a3158c5051) by Timothée Mazzucotelli).

## [0.2.8](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.8) - 2025-02-18

<small>[Compare with 0.2.7](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.7...0.2.8)</small>

### Code Refactoring

- Only add docstring sections when elements are annotated with `Doc` ([514467c](https://github.com/mkdocstrings/griffe-typingdoc/commit/514467c06f4381fca9c5f96a860c8abd87c1827b) by Timothée Mazzucotelli). [Issue-13](https://github.com/mkdocstrings/griffe-typingdoc/issues/13)

## [0.2.7](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.7) - 2024-09-10

<small>[Compare with 0.2.6](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.6...0.2.7)</small>

### Bug Fixes

- Resolve names in `Unpack`, instead of naively trying to get them from the parent of the function being handled ([5e06b33](https://github.com/mkdocstrings/griffe-typingdoc/commit/5e06b33651f43b292059d27d3b232e2646a409d5) by Timothée Mazzucotelli). [Issue-11](https://github.com/mkdocstrings/griffe-typingdoc/issues/11)

## [0.2.6](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.6) - 2024-08-14

<small>[Compare with 0.2.5](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.5...0.2.6)</small>

### Build

- Depend on Griffe 0.49 ([b6d7bd9](https://github.com/mkdocstrings/griffe-typingdoc/commit/b6d7bd9ce462a8dbd067464b3d14a9dd25865957) by Timothée Mazzucotelli).

## [0.2.5](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.5) - 2024-02-08

<small>[Compare with 0.2.4](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.4...0.2.5)</small>

### Bug Fixes

- Support simple return annotations ([b4afabe](https://github.com/mkdocstrings/griffe-typingdoc/commit/b4afabed86e8b7c1905cbf672ab261be0d895e40) by Timothée Mazzucotelli). [Issue #9](https://github.com/mkdocstrings/griffe-typingdoc/issues/9)

## [0.2.4](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.4) - 2023-11-14

<small>[Compare with 0.2.3](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.3...0.2.4)</small>

### Code Refactoring

- Run static analysis only after the whole package was loaded ([08be3d0](https://github.com/mkdocstrings/griffe-typingdoc/commit/08be3d0e735b03b9ba28b055895dfa2d01778fda) by Timothée Mazzucotelli). [Issue #7](https://github.com/mkdocstrings/griffe-typingdoc/issues/7), [PR #8](https://github.com/mkdocstrings/griffe-typingdoc/pull/8)

## [0.2.3](https://github.com/mkdocstrings/griffe-typingdoc/releases/tag/0.2.3) - 2023-10-23

<small>[Compare with 0.2.2](https://github.com/mkdocstrings/griffe-typingdoc/compare/0.2.2...0.2.3)</small>

### Bug Fixes

- Fix index error when trying to access the first parameter of functions ([92e27a3](https://github.com/mkdocstrings/griffe-typingdoc/commit/92e27a3bc5f81acfdb94c24fcd33e1992e3db503) by Timothée Mazzucotelli). [Issue #7](https://github.com/mkdocstrings/griffe-typingdoc/issues/7)

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
