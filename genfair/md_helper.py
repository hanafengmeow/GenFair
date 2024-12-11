import re
from typing import Optional

from mrkdwn_analysis import MarkdownAnalyzer


def get_section(
    file: str,
    header_pattern: str,
    header_level: int,
    include_header: bool = True,
    return_lines: bool = False,
) -> Optional[list[str] | str]:
    md = open(file).readlines()
    analyzer = MarkdownAnalyzer(file)
    headers = analyzer.identify_headers()['Header']
    for i in range(len(headers)):
        if header_level == headers[i]['level'] and re.search(header_pattern, headers[i]['text']):
            start = headers[i]['line'] - include_header
            end = headers[i + 1]['line'] - 1 if i < len(headers) - 1 else None
            lines = md[start:end]
            return lines if return_lines else ''.join(lines)
        