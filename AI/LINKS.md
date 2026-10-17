# Primary references

Verified 2026-10-10:
- https://developer.android.com/studio — official downloads and checksums.
- https://developer.android.com/studio/install — installation guidance.
- https://developer.android.com/tools/sdkmanager — SDK package and license management.

The installer pins the Linux archives observed on the official download page.
Recheck official URLs and checksums before upgrading; update the script and log.

- https://mezhdunami.ku.edu/cases.shtml — University of Kansas course, six Russian teaching cases (checked 2026-10-10).

Research for starter content and contributor workflow (2026-10-10):
- https://www.lektorek.org/lektorek/grammar.pdf — Oscar E. Swan, Polish grammar;
  declension, case use and traditional/colloquial vocative address.
- https://polski.info/grammar/numerals?hl=en — Polish cardinal and ordinal forms.
- https://russky.info/grammar/numerals?hl=en — Russian cardinal and ordinal forms.
- https://pypi.org/pypi/PyYAML/6.0.1/json — versioned wheel hashes for optional setup.
- https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project
  — fork/pull-request workflow.
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue
  — feedback through GitHub Issues.
- https://github.com/ewanold/slavic-cases — public repository URL derived from origin.

Generated sentences are original, AI-assisted drafts; reference links do not
imply copied textbook material or independent expert review.

German starter research (2026-10-11), IDS grammis primary references:
- https://grammis.ids-mannheim.de/progr@mm/6915 — noun case marking.
- https://grammis.ids-mannheim.de/fragen/28 — weak masculine nouns, Student/Nachbar.
- https://grammis.ids-mannheim.de/progr@mm/6751 — strong/weak adjective patterns.
- https://grammis.ids-mannheim.de/progr@mm/6752 — mixed pattern after indefinite articles.
All German sentences are original MIT drafts; none copied from these references.
- https://www.duden.de/sprachwissen/fuer-lernende/wortarten-numerale
  — cardinal/ordinal number classes and article-free genitive zweier/dreier.
- https://developer.android.com/guide/topics/resources/localization
  — device-locale resource selection and default fallback (checked 2026-10-11).

## Desktop editor toolkit and Windows bootstrap

- Qt for Python official setup: https://doc.qt.io/qtforpython-6/gettingstarted.html
  (Python wheels include Qt; no separate SDK needed for the editor).
- Qt for Python licensing: https://doc.qt.io/qtforpython-6/commercial/index.html
  (upstream Qt/PySide licensing remains separate from this project's MIT code).
- Microsoft's Python 3.12.10 installer manifest, used to cross-check the official
  x64 Python bootstrap SHA-256:
  https://github.com/microsoft/winget-pkgs/blob/master/manifests/p/Python/Python/3/12/3.12.10/Python.Python.3.12.installer.yaml
- Version-specific PyPI metadata URLs are recorded in committed editor requirement
  locks and requirements/sample-editor-pip.json; scripts/update-sample-editor-locks.py
  regenerates them for review. Package archives are hash-verified before installation.
