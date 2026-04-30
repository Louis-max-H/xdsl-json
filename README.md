# xdsl-template

A template for projects using xDSL.

## Usage

```bash
git clone https://github.com/Louis-max-H/xdsl-json
make install
uv run python src/xdsljson/compiler.py 
```

## Example project structure

```text
.
├── docs/
│   ├── index.md              # Hand-written documentation splash page
│   └── reference.md          # Auto-generated source code documentation
├── src/
│   └── xdsltemplate/         # Project source code:
│       ├── dialects/         # - custom IR dialect implementations
│       ├── frontend/         # - Parsing and lexing implementations (convert json to xDSL)
│       └── transforms/       # - Rewriting transformation implementations
└── tests/                    # All tests, both pytest and filecheck
    └── filecheck/            # filecheck .mlir files
```

## Developer features for free

- Developer tools including auto-formatting, linting, and type-checking as both
  pre-commit hooks and GitHub Actions.
- Testing through both pytest and LLVM filecheck
- Documentation website, optionally deployed to GitHub pages
