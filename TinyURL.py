# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2015-2017 IzunaDevs

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import sys
try:
    import urllib.request
    import urllib.parse
except ImportError:
    import urllib
from bs4 import BeautifulSoup
import optparse
import re
try:
    parse_helper = urllib.parse
except AttributeError:
    parse_helper = urllib
try:
    request_helper = urllib.request
except AttributeError:
    request_helper = urllib


class errors:
    """
    Holds all error Classes.
    """

    class URLError(Exception):
        """
        For URL Errors.
        """
        pass

    class InvalidURL(Exception):
        """
        For Invalid URL's.
        """
        pass

    class InvalidAlias(Exception):
        """
        For Invalid Aliases.
        """
        pass

    class AliasUsed(Exception):
        """
        For already used Aliases.
        """
        pass


API_CREATE_LIST = [
    "http://tinyurl.com/api-create.php",
    "http://tinyurl.com/create.php?"]
DEFAULT_DELIM = "\n"
USAGE = """TinyURL [options] url [url url ...]

Options:

-d / --delimiter

Any number of urls may be passed and will be returned
in order with the given delimiter, default=\\n
"""
pattern = "(arp|dns|dsn|imap|http|sftp|ftp|icmp|idrp|ip|irc|pop3|par|rlogin"
pattern += "|smtp|ssl|ssh|tcp|telnet|upd|up|file|git)(s?):\/\/[\/]?"

ALL_OPTIONS = ((('-d', '--delimiter'), dict(
    dest='delimiter', default=DEFAULT_DELIM,
    help='delimiter for returned results')),)


def _build_option_parser():
    prs = optparse.OptionParser(usage=USAGE)
    for args, kwargs in ALL_OPTIONS:
        prs.add_option(*args, **kwargs)
    return prs


def create_one(url, alias=None):
    """
    Shortens a URL using the TinyURL API.
    """
    if url != '' and url is not None:
        regex = re.compile(pattern)
        searchres = regex.search(url)
        if searchres is not None:
            if alias is not None:
                if alias != '':
                    payload = {
                        'url': url,
                        'submit': 'Make TinyURL!',
                        'alias': alias
                    }
                    data = parse_helper.urlencode(payload)
                    full_url = API_CREATE_LIST[1] + data
                    ret = request_helper.urlopen(full_url)
                    soup = BeautifulSoup(ret, 'html.parser')
                    check_error = soup.p.b.string
                    if 'The custom alias' in check_error:
                        raise errors.AliasUsed(
                            "The given Alias you have provided is already"
                            " being used.")
                    else:
                        return soup.find_all(
                            'div', {'class': 'indent'}
                            )[1].b.string
                else:
                    raise errors.InvalidAlias(
                        "The given Alias cannot be 'empty'.")
            else:
                url_data = parse_helper.urlencode(dict(url=url))
                byte_data = str.encode(url_data)
                ret = request_helper.urlopen(
                    API_CREATE_LIST[0], data=byte_data).read()
                result = str(ret).replace('b', '').replace("\'", '')
                return result
        else:
            raise errors.InvalidURL("The given URL is invalid.")
    else:
        raise errors.URLError("The given URL Cannot be 'empty'.")


def create(*urls):
    """
    Shortens URL's
    """
    for url in urls:
        yield create_one(url)


def main():
    """
    Entry Point.
    """
    if len(sys.argv) > 1:
        sysargs = sys.argv[:]
        parser = _build_option_parser()
        opts, urls = parser.parse_args(sysargs[1:])
        try:
            for url in create(*urls):
                sys.stdout.write(url + opts.delimiter)
        except Exception as ex:
            print("Error: " + str(ex))
    else:
        print(USAGE)


__title__ = 'TinyURL'
__author__ = 'Decorater'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2017 Decorater'
__version__ = '0.1.10'
__build__ = 0x0001010


if __name__ == '__main__':
    main()
