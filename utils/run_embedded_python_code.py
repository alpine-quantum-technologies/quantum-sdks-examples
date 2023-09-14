#!/usr/bin/env python3
#
# Copyright 2023 Alpine Quantum Technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pandoc filter that accumulates all Python code blocks
in a document and executes the resulting program.
Exits with status code 2 if the code execution failed.

WARNING: no sandbox: all code side effects are executed!
"""

import sys
from contextlib import redirect_stdout

import panflute as pf

collected_code = []


def action(elem, _doc):
    if isinstance(elem, pf.CodeBlock) and "python" in elem.classes:
        collected_code.append(elem.text.strip())

    return elem


def main(doc=None):
    rv = pf.run_filter(action, doc)

    code = "\n".join(collected_code)

    try:
        with redirect_stdout(sys.stderr):
            exec(code, {})
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(2)

    return rv


if __name__ == "__main__":
    main()
