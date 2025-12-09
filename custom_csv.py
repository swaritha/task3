"""
Custom CSV reader and writer implementation.

- CustomCsvReader: reads CSV rows from a file object.
- CustomCsvWriter: writes CSV rows to a file object.
"""


class CustomCsvReader:
    """Simple CSV reader supporting quotes, escaped quotes and newlines."""

    def __init__(self, file_obj):
        """
        file_obj: an opened file object in text mode (e.g. open('file.csv')).
        """
        self.file = file_obj
        self._buffer = ""
        self._index = 0          # position in buffer
        self._pushback_char = None
        self._eof = False

    def __iter__(self):
        return self

    # ---------- low-level helpers ----------

    def _load_next_line(self):
        """Load the next line from the file into the buffer."""
        line = self.file.readline()
        if line == "":
            self._eof = True
            self._buffer = ""
            self._index = 0
        else:
            self._buffer = line
            self._index = 0

    def _next_char(self):
        """
        Return the next character from the file, or None if end of file.
        """
        if self._pushback_char is not None:
            ch = self._pushback_char
            self._pushback_char = None
            return ch

        if self._eof:
            return None

        if self._index >= len(self._buffer):
            self._load_next_line()
            if self._eof:
                return None

        ch = self._buffer[self._index]
        self._index += 1
        return ch

    def _push_back(self, ch):
        """Push one character back to be read again."""
        self._pushback_char = ch

    # ---------- iterator main method ----------

    def __next__(self):
        """
        Parse characters until we have one complete CSV row.

        Returns:
            list[str]: one row of fields.

        Raises:
            StopIteration: when no more data is available.
        """
        fields = []
        current_field = []
        in_quotes = False

        while True:
            ch = self._next_char()

            # End of file
            if ch is None:
                if in_quotes:
                    # File ended while inside quotes – treat as end of field/row.
                    pass

                if current_field or fields:
                    fields.append("".join(current_field))
                    return fields
                else:
                    raise StopIteration

            # Quote handling
            if ch == '"':
                if not in_quotes:
                    # starting quoted field
                    in_quotes = True
                else:
                    # we are in quotes; could be end of field or escaped quote
                    next_ch = self._next_char()
                    if next_ch == '"':
                        # escaped quote
                        current_field.append('"')
                    else:
                        # end of quoted field
                        in_quotes = False
                        if next_ch is not None:
                            self._push_back(next_ch)
                continue

            # Comma (only ends field if not in quotes)
            if ch == ',' and not in_quotes:
                fields.append("".join(current_field))
                current_field = []
                continue

            # Newline (row end) when not in quotes
            if (ch == '\n' or ch == '\r') and not in_quotes:
                if ch == '\r':
                    # handle \r\n
                    next_ch = self._next_char()
                    if next_ch != '\n' and next_ch is not None:
                        self._push_back(next_ch)
                fields.append("".join(current_field))
                return fields

            # Normal character (or comma/newline inside quotes)
            current_field.append(ch)


class CustomCsvWriter:
    """Simple CSV writer supporting quoting and escaping."""

    def __init__(self, file_obj):
        """
        file_obj: an opened file object in text mode (write mode).
        """
        self.file = file_obj

    def _format_field(self, value):
        """
        Turn a Python string into a properly escaped CSV field.

        Rules:
        - If the field contains a comma, quote, or newline, wrap in double quotes.
        - Inside quoted fields, each " becomes "" (two quotes).
        """
        if value is None:
            value = ""
        else:
            value = str(value)

        # escape internal quotes
        escaped = value.replace('"', '""')

        # if contains special chars, wrap in quotes
        if any(ch in escaped for ch in [',', '"', '\n', '\r']):
            return f'"{escaped}"'
        else:
            return escaped

    def writerow(self, row):
        """
        Write a single row (list of values) to the CSV file.
        """
        formatted_fields = [self._format_field(value) for value in row]
        line = ",".join(formatted_fields) + "\n"
        self.file.write(line)

    def writerows(self, rows):
        """Write multiple rows to the file."""
        for row in rows:
            self.writerow(row)
