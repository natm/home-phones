#!/usr/bin/env python
"""Home phones API runner."""
import logging
import sys
from homephones.ApiService import ApiService

LOG = logging.getLogger(__name__)

logging.getLogger().setLevel(logging.DEBUG)


def main():
    """Main entry point."""
    LOG.info('Starting server')

    svc = ApiService(args=sys.argv[1:])
    svc.run()

    sys.exit(0)


if __name__ == "__main__":
    main()
