# -*- coding: utf-8 -*-
"""Log parsing utilities for the log-analyzer-chatbot project.

Currently the project stores a sample device log in `./r1/device.csv` which
contains rows with the columns `id,date,user,pc,activity`.  The :func:`parse_logs`
helper below will open that file, iterate over its lines, and convert each
record into a simple JSON-friendly dictionary.

This module can be expanded later with more sophisticated parsing, filtering,
or even support for different log formats.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping, Optional

import click


def parse_log_file(
    path: Path | str = "../r1/logon.csv"
) -> Iterable[Mapping[str, str]]:
    """Read the specified CSV log and yield each record as a JSON-like dict.

    Parameters
    ----------
    path:
        Path to the CSV file containing logs.  By default it uses the sample
        file at ``./r1/device.csv`` relative to the current working directory.

    Yields
    ------
    Mapping[str, str]
        A mapping with keys ``id``, ``date``, ``user``, ``pc`` and ``activity``
        corresponding to each row in the CSV file.
    """

    path_obj = Path(path)

    # ``csv.DictReader`` inspects the first row for header names and uses those
    # automatically, so we don't supply ``fieldnames`` here.  This also means
    # that the header is *not* included in the rows yielded by the iterator.
    with path_obj.open("r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            yield dict(row)


@click.command()
@click.option(
    "--max-rows",
    type=int,
    default=None,
    help="Maximum number of log rows to process (default: all)",
)
@click.option(
    "--include-headers/--no-include-headers",
    default=True,
    help="Whether to include the CSV header line when printing rows",
)
def main(max_rows: Optional[int] = None, include_headers: bool = True):
    """Execute a small demo from the command line.

    Parameters
    ----------
    max_rows:
        If provided, only the first ``max_rows`` records will be printed.

        A value of ``None`` (the default) processes every line.  When
        ``include_headers`` is ``True`` the header row is printed and counts
        toward this limit; otherwise the header is ignored completely.

    include_headers:
        Whether to output the CSV header line as well.  If ``False`` the
        header is skipped and ``max_rows`` applies only to data records.
    """

    if include_headers:
        header = ",".join(["id", "date", "user", "pc", "activity"])
        print(header)
        if max_rows is not None:
            max_rows -= 1
            if max_rows <= 0:
                return

    for idx, entry in enumerate(parse_log_file()):
        if max_rows is not None and idx >= max_rows:
            break
        print(json.dumps(entry))


if __name__ == "__main__":
    # ``main`` is a click command; invoking it without arguments will
    # cause click to parse the command line and call the function.
    main()
