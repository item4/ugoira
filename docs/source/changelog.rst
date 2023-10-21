Changelog
=========

Version 0.9.1
-------------
Not released yet.

- (mics) Apply security PR from GitHub Dependabot.
- (mics) Update GitHub Actions deps.
- (mics) Update black and reformat some code.
- (mics) Update ruff.

Version 0.9.0
-------------

- (break) Drop support Python 3.8, 3.9 and 3.10.
- (break) Remove ``requests`` as core dependency for HTTP operation, and use ``httpx`` instead.
- (break) Remove ``apng`` as extra dependency for supporting APNG format and use ``Pillow`` only.
- (packaging) Add readme and repo/docs url.
- (mics) Use ``ruff`` for coding style linter.
- (mics) Use ``black`` for code formatter.
- (misc) Rewrite docs.
- (misc) Bump almost deps.
- (misc) Make ``.readthedocs.yaml`` for current Read The Docs API.
- (misc) Use GitHub Actions for CI.
- (misc) Reactivate CodeCov for coverage.

Version 0.8.0
-------------
- (break) Remove dependency with ImageMagick and use pillow now.
- (new) Support WEBP format.
- (new) Support PDF format.
- (misc) Fix docs.
- (misc) Bump deps.

Version 0.7.0
-------------
- (break) Drop support Python 3.5, 3.6, 3.7.
- (break) Use Poetry.
- (new) Try to download more nice resolution.

Version 0.6.0
-------------
- (break) Use ImageMagick 7 instead of 6.
- (break) Use Poetry.
- (break) Remove ``is_ugoira`` method.
- (break) Use ``io.BytesIO`` instead of tempfile (PR #8)
- (break) Fix to works ugoira command (Issue #5)

Version 0.5.0
-------------

- (break) Use secure protocol(HTTPS) instead of naive(HTTP)
- (break) CLI Support multiple download at once

Version 0.4.1
-------------

- (docs) Fix README in repo

Version 0.4.0
-------------

- (break) Drop Python 3.4 support
- (break) Write some type hints
- (break) Change usage of CLI
- (break) Refactor logic
- (new) Use more nice fake User-Agent
- (new) Support APNG format
- (docs) Update docs about 0.4.0 version
- (docs) Fix ugoira version on docs

Version 0.3.0
-------------

- (bugfix) Fix setup.py (PR #1)
- (break) Remove unnecessary login (PR #2)
- (docs) Fix installation docs.
- (break) Bump deps
- (bugfix) Fix broken tests
- (mics) Add lint for code style.

Version 0.2.0
-------------

- Apply Login logic.

Version 0.1.1
-------------

- Change Login URL and add login argument.

Version 0.1.1
-------------

- Change Login URL and add login argument.


Version 0.1.0
-------------

First release.
