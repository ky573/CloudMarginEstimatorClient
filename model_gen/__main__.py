"""Entry point when invoked with python -m cpme_api."""

if __name__ == "__main__":
    import sys

    from model_gen.cli import main

    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m cpme_api"
    main()
