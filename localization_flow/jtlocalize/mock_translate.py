#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from core.localization_utils import *
from jtlocalize.core.localization_commandline_operation import LocalizationCommandLineOperation


class Replacement:
    def __init__(self):
        pass

    def regex(self):
        pass


class StaticReplacement(Replacement):
    def __init__(self, static_val):
        Replacement.__init__(self)
        self.static_val = static_val.decode("utf8")

    def regex(self):
        return self.static_val


class WrapReplacement(Replacement):
    def __init__(self, wrapping_prefix):
        Replacement.__init__(self)
        self.wrapping_prefix = wrapping_prefix.decode("utf8")

    def regex(self):
        return u"%s(\\1)" % self.wrapping_prefix


def replace_english_values(filename, replacement):
    f = open_strings_file(filename, "r+")
    compiled = re.compile('= "(.*?)";', re.MULTILINE | re.DOTALL)
    subbed = compiled.sub(u'= "%s";' % replacement.regex(), f.read())
    f.seek(0)
    f.write(subbed)
    f.truncate()
    f.close()


PRESET_REPLACEMENTS = {"chicken": StaticReplacement("Chicken"),
                       "chinese": StaticReplacement("鸡鸡鸡"),
                       "localized": WrapReplacement("LOCALIZED")}


class MockTranslateOperation(LocalizationCommandLineOperation):

    def name(self):
        return "mock_translate"

    def description(self):
        return "Localizes a given file to the given string values."

    def configure_parser(self, parser):
        parser.add_argument("file_to_mock", help="The file to localize.")

        localization_option_group = parser.add_mutually_exclusive_group(required=True)

        localization_option_group.add_argument("--preset", choices=PRESET_REPLACEMENTS.keys(),
                                               help="Choose a preset type of mock translation.")

        localization_option_group.add_argument("--static", help="Choose a static replacement of your own.")

        localization_option_group.add_argument("--wrap", help="Choose a wrapping text of your own "
                                                              "(will wrap the original string with parenthesis).")

    def run(self, parsed_args):
        mock_translate(parsed_args.file_to_mock, parsed_args.preset, parsed_args.static, parsed_args.wrap)


def mock_translate(file_to_mock, preset=None, static=None, wrap=None):
    if preset:
        replace_english_values(file_to_mock, PRESET_REPLACEMENTS[preset])

    elif static:
        replace_english_values(file_to_mock, StaticReplacement(static))

    elif wrap:
        replace_english_values(file_to_mock, WrapReplacement(wrap))


if __name__ == "__main__":
    operation = MockTranslateOperation()
    operation.run_with_standalone_parser()

