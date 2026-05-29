"""Module entrypoint for `python -m invoice_agent`."""

from .api import main


if __name__ == "__main__":
    raise SystemExit(main())

