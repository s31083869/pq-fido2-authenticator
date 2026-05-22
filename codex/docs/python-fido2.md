This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.
The content has been processed where security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*.py
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
docs/
  conf.py
examples/
  server/
    server/
      server.py
  acr122u.py
  acr122usam.py
  acr1252u.py
  bio_enrollment.py
  cred_blob.py
  credential.py
  exampleutils.py
  get_info.py
  hmac_secret.py
  large_blobs.py
  multi_device.py
  prf.py
  resident_key.py
  u2f_nfc.py
  verify_attestation_mds3.py
  verify_attestation.py
fido2/
  attestation/
    __init__.py
    android.py
    apple.py
    base.py
    packed.py
    tpm.py
    u2f.py
  client/
    __init__.py
    win_api.py
    windows.py
  ctap2/
    __init__.py
    base.py
    bio.py
    blob.py
    config.py
    credman.py
    extensions.py
    pin.py
  hid/
    __init__.py
    base.py
    freebsd.py
    linux.py
    macos.py
    netbsd.py
    openbsd.py
    windows.py
  __init__.py
  cbor.py
  cose.py
  ctap.py
  ctap1.py
  features.py
  mds3.py
  payment.py
  pcsc.py
  rpid.py
  server.py
  utils.py
  webauthn.py
tests/
  device/
    __init__.py
    conftest.py
    test_bioenroll.py
    test_client.py
    test_clientpin.py
    test_config.py
    test_credblob.py
    test_credentials.py
    test_credman.py
    test_hid.py
    test_info.py
    test_largeblobs.py
    test_payment.py
    test_prf.py
  conftest.py
  test_attestation.py
  test_cbor.py
  test_client.py
  test_cose.py
  test_ctap1.py
  test_ctap2.py
  test_hid.py
  test_mds3.py
  test_pcsc.py
  test_rpid.py
  test_server.py
  test_tpm.py
  test_utils.py
  test_webauthn.py
```

# Files

## File: docs/conf.py
```python
# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import tomllib

sys.path.insert(0, os.path.abspath("../"))


def get_version():
    with open("../pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    return pyproject["project"]["version"]


# -- Project information -----------------------------------------------------

project = "python-fido2"
copyright = "2024, Yubico"
author = "Yubico"

# The full version, including alpha/beta/rc tags
release = get_version()

# The short X.Y version
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

autodoc_typehints = "description"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

html_favicon = "favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Don't show a "View page source" link on each page.
html_show_sourcelink = False

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "python-fido2doc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "python-fido2.tex",
        "python-fido2 Documentation",
        "Yubico",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "python-fido2", "python-fido2 Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "python-fido2",
        "python-fido2 Documentation",
        author,
        "python-fido2",
        "One line description of project.",
        "Miscellaneous",
    )
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "cryptography": ("https://cryptography.io/en/latest/", None),
}


# Custom config
autoapi_dirs = ["../fido2"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_ignore = ["*/fido2/hid/*", "*/fido2/win_api.py"]


def skip_member(app, what, name, obj, skip, options):
    if what == "data" and name.endswith(".logger"):
        return True


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_member)
```

## File: examples/server/server/server.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Example demo server to use a supported web browser to call the WebAuthn APIs
to register and use a credential.

See the file README.adoc in this directory for details.

Navigate to http://localhost:5000 in a supported web browser.
"""

import os

from flask import Flask, abort, jsonify, redirect, request, session

from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity

app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(32)  # Used for session.

rp = PublicKeyCredentialRpEntity(name="Demo server", id="localhost")
server = Fido2Server(rp)


# Registered credentials are stored globally, in memory only. Single user
# support, state is lost when the server terminates.
credentials = []


@app.route("/")
def index():
    return redirect("/index.html")


@app.route("/api/register/begin", methods=["POST"])
def register_begin():
    options, state = server.register_begin(
        PublicKeyCredentialUserEntity(
            id=b"user_id",
            name="a_user",
            display_name="A. User",
        ),
        credentials,
        user_verification="discouraged",
        authenticator_attachment="cross-platform",
    )

    session["state"] = state
    print("\n\n\n\n")
    print(dict(options))
    print("\n\n\n\n")

    return jsonify(dict(options))


@app.route("/api/register/complete", methods=["POST"])
def register_complete():
    response = request.json
    print("RegistrationResponse:", response)
    auth_data = server.register_complete(session["state"], response)

    credentials.append(auth_data.credential_data)
    print("REGISTERED CREDENTIAL:", auth_data.credential_data)
    return jsonify({"status": "OK"})


@app.route("/api/authenticate/begin", methods=["POST"])
def authenticate_begin():
    if not credentials:
        abort(404)

    options, state = server.authenticate_begin(credentials)
    session["state"] = state

    return jsonify(dict(options))


@app.route("/api/authenticate/complete", methods=["POST"])
def authenticate_complete():
    if not credentials:
        abort(404)

    response = request.json
    print("AuthenticationResponse:", response)
    server.authenticate_complete(
        session.pop("state"),
        credentials,
        response,
    )
    print("ASSERTION OK")
    return jsonify({"status": "OK"})


def main():
    print(__doc__)
    # Note: using localhost without TLS, as some browsers do
    # not allow Webauthn in case of TLS certificate errors.
    # See https://lists.w3.org/Archives/Public/public-webauthn/2022Nov/0135.html
    app.run(host="localhost", debug=False)


if __name__ == "__main__":
    main()
```

## File: examples/acr122u.py
```python
import time

from fido2.pcsc import CtapPcscDevice


class Acr122uPcscDevice(object):
    def __init__(self, pcsc_device):
        self.pcsc = pcsc_device

    def reader_version(self):
        """
        Get reader's version from reader
        :return: string. Reader's version
        """

        try:
            result, sw1, sw2 = self.pcsc.apdu_exchange(b"\xff\x00\x48\x00\x00")
            if len(result) > 0:
                str_result = result + bytes([sw1]) + bytes([sw2])
                str_result = str_result.decode("utf-8")
                return str_result
        except Exception as e:
            print("Get version error:", e)
        return "n/a"

    def led_control(
        self,
        red=False,
        green=False,
        blink_count=0,
        red_end_blink=False,
        green_end_blink=False,
    ):
        """
        Reader's led control
        :param red: boolean. red led on
        :param green: boolean. green let on
        :param blink_count: int. if needs to blink value > 0. blinks count
        :param red_end_blink: boolean.
        state of red led at the end of blinking
        :param green_end_blink: boolean.
        state of green led at the end of blinking
        :return:
        """

        try:
            if blink_count > 0:
                cbyte = (
                    0b00001100
                    + (0b01 if red_end_blink else 0b00)
                    + (0b10 if green_end_blink else 0b00)
                )
                cbyte |= (0b01000000 if red else 0b00000000) + (
                    0b10000000 if green else 0b00000000
                )
            else:
                cbyte = 0b00001100 + (0b01 if red else 0b00) + (0b10 if green else 0b00)

            apdu = (
                b"\xff\x00\x40"
                + bytes([cbyte & 0xFF])
                + b"\4"
                + b"\5\3"
                + bytes([blink_count])
                + b"\0"
            )
            self.pcsc.apdu_exchange(apdu)

        except Exception as e:
            print("LED control error:", e)


dev = next(CtapPcscDevice.list_devices())

print("CONNECT: %s" % dev)
pcsc_device = Acr122uPcscDevice(dev)
pcsc_device.led_control(False, True, 0)
print("version: %s" % pcsc_device.reader_version())
pcsc_device.led_control(True, False, 0)
time.sleep(1)
pcsc_device.led_control(False, True, 3)
```

## File: examples/acr122usam.py
```python
# Copyright (c) 2019 Yubico AB
# Copyright (c) 2019 Oleg Moiseenko
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Sample work with reader:
ACR-122U-SAM or touchatag
drivers and manual link:
www.acs.com.hk/en/driver/100/acr122u-nfc-reader-with-sam-slot-proprietary/
"""

import time

from smartcard.Exceptions import CardConnectionException

from fido2.ctap1 import CTAP1
from fido2.pcsc import CtapPcscDevice
from fido2.utils import sha256


class Acr122uSamPcscDevice(CtapPcscDevice):
    def __init__(self, connection, name):
        self.ats = b""
        self.vparity = False
        self.max_block_len = 29

        try:
            super().__init__(connection, name)
        except (CardConnectionException, ValueError):
            pass
        except Exception as e:
            print(e.__class__)

        # setup reader
        if not self.set_auto_iso14443_4_activation():
            raise Exception("Set automatic iso-14443-4 activation error")

        if not self.set_default_retry_timeout():
            raise Exception("Set default retry timeout error")

        self.ats = self.get_ats()
        if self.ats == b"":
            raise Exception("No card in field")

        self._select()

    def apdu_plain(self, apdu, protocol=None):
        """Exchange data with reader.

        :param apdu: byte string. data to exchange with card
        :param protocol: protocol to exchange with card. usually set by default
        :return: byte string. response from card
        """

        # print('>> %s' % b2a_hex(apdu))
        resp, sw1, sw2 = self._conn.transmit(list(iter(apdu)), protocol)
        response = bytes(bytearray(resp))
        # print('<< [0x%04x] %s' % (sw1 * 0x100 + sw2, b2a_hex(response)))

        return response, sw1, sw2

    def pseudo_apdu_ex(self, apdu, protocol=None):
        req = b"\xff\x00\x00\x00" + bytes([len(apdu) & 0xFF]) + apdu
        resp, sw1, sw2 = self.apdu_plain(req, protocol)
        if sw1 != 0x61:
            return resp, sw1, sw2
        return self.apdu_plain(b"\xff\xc0\x00\x00" + bytes([sw2]), protocol)

    # override base method
    # commands in PN 532 User manual (UM0701-02)
    # page 178. 7.4.5 DEP chaining mechanism
    # page 136. 7.3.9 InCommunicateThru
    # chaining ISO 14443-4:2001
    # page 20. 7.5.2 Chaining
    def apdu_exchange(self, apdu, protocol=None):
        all_response = b""
        alen = 0
        while True:
            vapdu = apdu[alen : alen + self.max_block_len]
            # input chaining
            chaining = alen + len(vapdu) < len(apdu)
            vb = 0x02 | (0x01 if self.vparity else 0x00) | (0x10 if chaining else 0x00)

            # 7.3.9 InCommunicateThru
            resp, sw1, sw2 = self.pseudo_apdu_ex(
                b"\xd4\x42" + bytes([vb]) + vapdu, protocol
            )
            self.vparity = not self.vparity

            if len(resp) > 2 and resp[2] > 0:
                print("Error: 0x%02x" % resp[2])
                return b"", 0x6F, resp[2]
            if sw1 != 0x90 or len(resp) < 3 or resp[0] != 0xD5 or resp[1] != 0x43:
                return b"", 0x67, 0x00

            alen += len(vapdu)

            if not chaining:
                break

        if len(resp) > 3:
            if resp[3] & 0x10 == 0:
                return resp[4:-2], resp[-2], resp[-1]
            else:
                if resp[3] != 0xF2:
                    all_response = resp[4:]
        else:
            return b"", 0x90, 0x00

        while True:
            if len(resp) > 3 and resp[3] == 0xF2:
                # WTX
                answer = resp[3:5]
            else:
                # ACK
                answer = bytes([0xA2 | (0x01 if self.vparity else 0x00)])
                self.vparity = not self.vparity

            # 7.3.9 InCommunicateThru
            resp, sw1, sw2 = self.pseudo_apdu_ex(b"\xd4\x42" + answer, protocol)
            if len(resp) > 2 and resp[2] > 0:
                print("Error: 0x%02x" % resp[2])
                return b"", 0x6F, resp[2]
            if sw1 != 0x90 or len(resp) < 3 or resp[0] != 0xD5 or resp[1] != 0x43:
                return b"", 0x67, 0x00

            response_chaining = len(resp) > 3 and resp[3] & 0x10 != 0

            # if I block
            if len(resp) > 3 and resp[3] & 0xE0 == 0x00:
                all_response += resp[4:]

            if not response_chaining:
                break

        return all_response[:-2], resp[-2], resp[-1]

    def get_ats(self, verbose=False):
        self.field_reset()
        self.ats = b""
        resp, sw1, sw2 = self.pseudo_apdu_ex(b"\xd4\x4a\x01\x00")
        if sw1 == 0x90 and len(resp) > 8 and resp[2] > 0x00:
            if verbose:
                print("ATQA 0x%02x%02x" % (resp[4], resp[5]))
                print("SAK 0x%02x" % resp[6])
            uid_len = resp[7]
            if verbose:
                print("UID [%d] %s" % (uid_len, resp[8 : 8 + uid_len].hex()))
            self.ats = resp[8 + uid_len :]
            if verbose:
                print("ATS [%d] %s" % (len(self.ats), self.ats.hex()))
            self.vparity = False
            return self.ats
        return b""

    def set_default_retry_timeout(self):
        result, sw1, sw2 = self.pseudo_apdu_ex(b"\xd4\x32\x05\x00\x00\x00")
        if sw1 != 0x90 or sw2 != 0x00 or result != b"\xd5\x33":
            print("set default retry time error")
            return False

        # 14443 timeout. UM0701-02 PN432 user manual. page 101.
        # RFU, fATR_RES_Timeout, fRetryTimeout
        # 0b 102ms, 0c - 204ms, 0d - 409ms, 0f - 1.6s
        result, sw1, sw2 = self.pseudo_apdu_ex(b"\xd4\x32\x02\x00\x0c\x0f")
        if sw1 != 0x90 or sw2 != 0x00 or result != b"\xd5\x33":
            print("set fRetryTimeout error")
            return False
        return True

    def set_auto_iso14443_4_activation(self, activate=True):
        result, sw1, sw2 = self.pseudo_apdu_ex(
            b"\xd4\x12" + bytes([0x34 if activate else 0x24])
        )
        if sw1 != 0x90 or sw2 != 0x00 or result != b"\xd5\x13":
            print("set automatic iso-14443-4 activation error")
            return False
        return True

    def field_control(self, field_on=True):
        result, sw1, sw2 = self.pseudo_apdu_ex(
            b"\xd4\x32\x01" + bytes([0x01 if field_on else 0x00])
        )
        if sw1 != 0x90 or sw2 != 0x00 or result != b"\xd5\x33":
            print("set field state error")
            return False
        return True

    def field_reset(self):
        self.led_control(True, False)
        result = self.field_control(False)
        time.sleep(0.2)
        result |= self.field_control(True)
        self.led_control()
        return result

    def reader_version(self):
        """
        Get reader's version from reader
        :return: string. Reader's version
        """

        try:
            result, sw1, sw2 = self.apdu_plain(b"\xff\x00\x48\x00\x00")
            if len(result) > 0:
                str_result = result + bytes([sw1]) + bytes([sw2])
                str_result = str_result.decode("utf-8")
                return str_result
        except Exception as e:
            print("Get version error:", e)
        return "n/a"

    def led_control(
        self,
        red=False,
        green=False,
        blink_count=0,
        red_end_blink=False,
        green_end_blink=False,
    ):
        """
        Reader's led control
        :param red: boolean. red led on
        :param green: boolean. green let on
        :param blink_count: int. if needs to blink value > 0. blinks count
        :param red_end_blink: boolean.
        state of red led at the end of blinking
        :param green_end_blink: boolean.
        state of green led at the end of blinking
        :return:
        """

        try:
            if blink_count > 0:
                cbyte = (
                    0b00001100
                    + (0b01 if red_end_blink else 0b00)
                    + (0b10 if green_end_blink else 0b00)
                )
                cbyte |= (0b01000000 if red else 0b00000000) + (
                    0b10000000 if green else 0b00000000
                )
            else:
                cbyte = 0b00001100 + (0b01 if red else 0b00) + (0b10 if green else 0b00)

            apdu = (
                b"\xff\x00\x40"
                + bytes([cbyte & 0xFF])
                + b"\4"
                + b"\5\3"
                + bytes([blink_count])
                + b"\0"
            )
            self.apdu_plain(apdu)

        except Exception as e:
            print("LED control error:", e)


dev = next(Acr122uSamPcscDevice.list_devices())

print("CONNECT: %s" % dev)
print("version: %s" % dev.reader_version())
print("atr: %s" % dev.get_atr().hex())
print("ats: %s" % dev.ats.hex())

# uncomment if you want to see parameters from card's selection
# dev.get_ats(True)
# dev._select()

dev.led_control(False, True, 0)

chal = sha256(b"AAA")
appid = sha256(b"BBB")
ctap1 = CTAP1(dev)
print("ctap1 version:", ctap1.get_version())

reg = ctap1.register(chal, appid)
print("u2f register:", reg)
reg.verify(appid, chal)
print("Register message verify OK")

auth = ctap1.authenticate(chal, appid, reg.key_handle)
print("u2f authenticate: ", auth)
res = auth.verify(appid, chal, reg.public_key)
print("Authenticate message verify OK")

dev.led_control()
```

## File: examples/acr1252u.py
```python
import time

from fido2.pcsc import CtapPcscDevice

# control codes:
# 3225264 - magic number!!!
# 0x42000000 + 3500 - cross platform way
C_CODE = 3225264


class Acr1252uPcscDevice(object):
    def __init__(self, pcsc_device):
        self.pcsc = pcsc_device

    def reader_version(self):
        try:
            res = self.pcsc.control_exchange(C_CODE, b"\xe0\x00\x00\x18\x00")

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == len(res) - 5:
                    strres = res[5 : 5 + reslen].decode("utf-8")
                    return strres
        except Exception as e:
            print("Get version error:", e)
        return "n/a"

    def reader_serial_number(self):
        try:
            res = self.pcsc.control_exchange(C_CODE, b"\xe0\x00\x00\x33\x00")

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == len(res) - 5:
                    strres = res[5 : 5 + reslen].decode("utf-8")
                    return strres
        except Exception as e:
            print("Get serial number error:", e)
        return "n/a"

    def led_control(self, red=False, green=False):
        try:
            cbyte = (0b01 if red else 0b00) + (0b10 if green else 0b00)
            result = self.pcsc.control_exchange(
                C_CODE, b"\xe0\x00\x00\x29\x01" + bytes([cbyte])
            )

            if len(result) > 0 and result.find(b"\xe1\x00\x00\x00") == 0:
                result_length = result[4]
                if result_length == 1:
                    ex_red = bool(result[5] & 0b01)
                    ex_green = bool(result[5] & 0b10)
                    return True, ex_red, ex_green
        except Exception as e:
            print("LED control error:", e)

        return False, False, False

    def led_status(self):
        try:
            result = self.pcsc.control_exchange(C_CODE, b"\xe0\x00\x00\x29\x00")

            if len(result) > 0 and result.find(b"\xe1\x00\x00\x00") == 0:
                result_length = result[4]
                if result_length == 1:
                    ex_red = bool(result[5] & 0b01)
                    ex_green = bool(result[5] & 0b10)
                    return True, ex_red, ex_green
        except Exception as e:
            print("LED status error:", e)

        return False, False, False

    def get_polling_settings(self):
        try:
            res = self.pcsc.control_exchange(C_CODE, b"\xe0\x00\x00\x23\x00")

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == 1:
                    return True, res[5]
        except Exception as e:
            print("Get polling settings error:", e)

        return False, 0

    def set_polling_settings(self, settings):
        try:
            res = self.pcsc.control_exchange(
                C_CODE, b"\xe0\x00\x00\x23\x01" + bytes([settings & 0xFF])
            )

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == 1:
                    return True, res[5]
        except Exception as e:
            print("Set polling settings error:", e)

        return False, 0

    def get_picc_operation_parameter(self):
        try:
            res = self.pcsc.control_exchange(C_CODE, b"\xe0\x00\x00\x20\x00")

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == 1:
                    return True, res[5]
        except Exception as e:
            print("Get PICC Operating Parameter error:", e)

        return False, 0

    def set_picc_operation_parameter(self, param):
        try:
            res = self.pcsc.control_exchange(
                C_CODE, b"\xe0\x00\x00\x20\x01" + bytes([param])
            )

            if len(res) > 0 and res.find(b"\xe1\x00\x00\x00") == 0:
                reslen = res[4]
                if reslen == 1:
                    return True, res[5]
        except Exception as e:
            print("Set PICC Operating Parameter error:", e)

        return False, 0


dev = next(CtapPcscDevice.list_devices())

print("CONNECT: %s" % dev)
pcsc_device = Acr1252uPcscDevice(dev)
if pcsc_device is not None:
    print("version: %s" % pcsc_device.reader_version())
    print("serial number: %s" % pcsc_device.reader_serial_number())
    print("")

    result, settings = pcsc_device.set_polling_settings(0x8B)
    print("write polling settings: %r 0x%x" % (result, settings))

    result, settings = pcsc_device.get_polling_settings()
    print("polling settings: %r 0x%x" % (result, settings))
    set_desc = [
        [0, "Auto PICC Polling"],
        [1, "Turn off Antenna Field if no PICC is found"],
        [2, "Turn off Antenna Field if the PICC is inactive"],
        [3, "Activate the PICC when detected"],
        [7, "Enforce ISO 14443-A Part 4"],
    ]
    for x in set_desc:
        print(x[1], "on" if settings & (1 << x[0]) else "off")
    interval_desc = [250, 500, 1000, 2500]
    print("PICC Poll Interval for PICC", interval_desc[(settings >> 4) & 0b11], "ms")
    print("")

    print(
        "PICC operation parameter: %r 0x%x" % pcsc_device.get_picc_operation_parameter()
    )
    print("")

    result, red, green = pcsc_device.led_control(True, False)
    print("led control result:", result, "red:", red, "green:", green)

    result, red, green = pcsc_device.led_status()
    print("led state result:", result, "red:", red, "green:", green)

    time.sleep(1)
    pcsc_device.led_control(False, False)
```

## File: examples/bio_enrollment.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found over USB, and attempts to enroll a new
fingerprint. This requires that a PIN is already set.

NOTE: This uses a draft bio enrollment specification which is not yet final.
Consider this highly experimental.
"""

import sys
from getpass import getpass

from fido2.ctap2 import CaptureError, Ctap2, FPBioEnrollment
from fido2.ctap2.bio import BioEnrollment
from fido2.ctap2.pin import ClientPin
from fido2.hid import CtapHidDevice

pin = None
uv = "discouraged"

for dev in CtapHidDevice.list_devices():
    try:
        ctap = Ctap2(dev)
        if BioEnrollment.is_supported(ctap.info):
            break
    except Exception:  # noqa: S112
        continue
else:
    print("No Authenticator supporting bioEnroll found")
    sys.exit(1)

if not ctap.info.options.get("clientPin"):
    print("PIN not set for the device!")
    sys.exit(1)

# Authenticate with PIN
print("Preparing to enroll a new fingerprint.")
pin = getpass("Please enter PIN: ")
client_pin = ClientPin(ctap)
pin_token = client_pin.get_pin_token(pin, ClientPin.PERMISSION.BIO_ENROLL)
bio = FPBioEnrollment(ctap, client_pin.protocol, pin_token)

print(bio.enumerate_enrollments())

# Start enrollment
enroller = bio.enroll()
template_id = None
while template_id is None:
    print("Press your fingerprint against the sensor now...")
    try:
        template_id = enroller.capture()
        print(enroller.remaining, "more scans needed.")
    except CaptureError as e:
        print(e)
bio.set_name(template_id, "Example")

print("Fingerprint registered successfully with ID:", template_id)
```

## File: examples/cred_blob.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found which supports the CredBlob extension,
creates a new credential for it with the extension enabled, and stores some data.
"""

import os
import sys

from exampleutils import get_client

from fido2.server import Fido2Server

# Locate a suitable FIDO authenticator
client, info = get_client(lambda info: "credBlob" in info.extensions)


# Prefer UV token if supported
uv = "discouraged"
if info and (info.options.get("uv") or info.options.get("bioEnroll")):
    uv = "preferred"
    print("Authenticator is configured for User Verification")


server = Fido2Server({"id": "example.com", "name": "Example RP"})
user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user,
    resident_key_requirement="required",
    user_verification=uv,
    authenticator_attachment="cross-platform",
)

# Add CredBlob extension, attach data
blob = os.urandom(32)  # 32 random bytes

# Create a credential
result = client.make_credential(
    {
        **create_options["publicKey"],
        "extensions": {"credBlob": blob},
    }
)

# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]


# CredBlob result:
if not auth_data.extensions.get("credBlob"):
    print("Credential was registered, but credBlob was NOT saved.")
    sys.exit(1)

print("New credential created, with the CredBlob extension.")

# Prepare parameters for getAssertion
request_options, state = server.authenticate_begin()

# Authenticate the credential
# Only one cred in allowCredentials, only one response.
result = client.get_assertion(
    {
        **request_options["publicKey"],
        "extensions": {"getCredBlob": True},
    }
).get_response(0)

blob_res = result.response.authenticator_data.extensions.get("credBlob")

if blob == blob_res:
    print("Authenticated, got correct blob:", blob.hex())
else:
    print(
        "Authenticated, got incorrect blob! (was %s, expected %s)"
        % (blob_res.hex(), blob.hex())
    )
    sys.exit(1)
```

## File: examples/credential.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and authenticates the credential.
This works with both FIDO 2.0 devices as well as with U2F devices.
On Windows, the native WebAuthn API will be used.
"""

from exampleutils import get_client

from fido2.server import Fido2Server

# Locate a suitable FIDO authenticator
client, info = get_client()


# Prefer UV if supported and configured
if info and (info.options.get("uv") or info.options.get("bioEnroll")):
    uv = "preferred"
    print("Authenticator supports User Verification")
else:
    uv = "discouraged"


server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")

user = {"id": b"user_id", "name": "A. User"}


# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user, user_verification=uv, authenticator_attachment="cross-platform"
)

# Create a credential
result = client.make_credential(create_options["publicKey"])

# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]

print("New credential created!")
response = result.response

print("CLIENT DATA:", response.client_data)
print("ATTESTATION OBJECT:", response.attestation_object)
print()
print("CREDENTIAL DATA:", auth_data.credential_data)


# Prepare parameters for getAssertion
request_options, state = server.authenticate_begin(credentials, user_verification=uv)

# Authenticate the credential
results = client.get_assertion(request_options["publicKey"])

# Only one cred in allowCredentials, only one response.
result = results.get_response(0)

# Complete authenticator
server.authenticate_complete(state, credentials, result)

print("Credential authenticated!")
response = result.response

print("CLIENT DATA:", response.client_data)
print()
print("AUTH DATA:", response.authenticator_data)
```

## File: examples/exampleutils.py
```python
# Copyright (c) 2024 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Utilities for common functionality used by several examples in this directory.
"""

import ctypes
from getpass import getpass

from fido2.client import DefaultClientDataCollector, Fido2Client, UserInteraction
from fido2.hid import CtapHidDevice

# Support NFC devices if we can
try:
    from fido2.pcsc import CtapPcscDevice
except ImportError:
    CtapPcscDevice = None

# Use the Windows WebAuthn API if available, and we're not running as admin
try:
    from fido2.client.windows import WindowsClient

    use_winclient = (
        WindowsClient.is_available() and not ctypes.windll.shell32.IsUserAnAdmin()
    )
except ImportError:
    use_winclient = False


# Handle user interaction via CLI prompts
class CliInteraction(UserInteraction):
    def __init__(self):
        self._pin = None

    def prompt_up(self):
        print("\nTouch your authenticator device now...\n")

    def request_pin(self, permissions, rd_id):
        if not self._pin:
            self._pin = getpass("Enter PIN: ")
        return self._pin

    def request_uv(self, permissions, rd_id):
        print("User Verification required.")
        return True


def enumerate_devices():
    for dev in CtapHidDevice.list_devices():
        yield dev
    if CtapPcscDevice:
        for dev in CtapPcscDevice.list_devices():
            yield dev


def get_client(predicate=None, **kwargs):
    """Locate a CTAP device suitable for use.

    If running on Windows as non-admin, the predicate check will be skipped and
    a webauthn.dll based client will be returned.

    Extra kwargs will be passed to the constructor of Fido2Client.

    The client will be returned, with the CTAP2 Info, if available.
    """

    client_data_collector = DefaultClientDataCollector("https://example.com")

    if use_winclient:
        return WindowsClient(client_data_collector), None

    user_interaction = kwargs.pop("user_interaction", None) or CliInteraction()

    # Locate a device
    for dev in enumerate_devices():
        # Set up a FIDO 2 client using the origin https://example.com
        client = Fido2Client(
            dev,
            client_data_collector=client_data_collector,
            user_interaction=user_interaction,
            **kwargs,
        )
        # Check if it is suitable for use
        if predicate is None or predicate(client.info):
            return client, client.info
    else:
        raise ValueError("No suitable Authenticator found!")
```

## File: examples/get_info.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to each attached FIDO device, and:
    1. If the device supports CBOR commands, perform a getInfo command.
    2. If the device supports WINK, perform the wink command.
"""

from fido2.ctap2 import Ctap2
from fido2.hid import CAPABILITY, CtapHidDevice

try:
    from fido2.pcsc import CtapPcscDevice
except ImportError:
    CtapPcscDevice = None


def enumerate_devices():
    for dev in CtapHidDevice.list_devices():
        yield dev
    if CtapPcscDevice:
        for dev in CtapPcscDevice.list_devices():
            yield dev


for dev in enumerate_devices():
    print("CONNECT: %s" % dev)
    print("Product name: %s" % dev.product_name)
    print("Serial number: %s" % dev.serial_number)
    print("CTAPHID protocol version: %d" % dev.version)

    if dev.capabilities & CAPABILITY.CBOR:
        ctap2 = Ctap2(dev)
        info = ctap2.get_info()
        print("DEVICE INFO: %s" % info)
    else:
        print("Device does not support CBOR")

    if dev.capabilities & CAPABILITY.WINK:
        dev.wink()
        print("WINK sent!")
    else:
        print("Device does not support WINK")

    dev.close()
```

## File: examples/hmac_secret.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found which supports the HmacSecret extension,
creates a new credential for it with the extension enabled, and uses it to
derive two separate secrets.

NOTE: This extension is not enabled by default as direct access to the extension
is now allowed in a browser setting. See also prf.py for an example which uses
the PRF extension which is enabled by default.
"""

import ctypes
import os
import sys

from exampleutils import CliInteraction, enumerate_devices

from fido2.client import DefaultClientDataCollector, Fido2Client
from fido2.ctap2.extensions import HmacSecretExtension
from fido2.server import Fido2Server

# Use the Windows WebAuthn API if available, and we're not running as admin
try:
    from fido2.client.windows import WindowsClient

    use_winclient = (
        WindowsClient.is_available() and not ctypes.windll.shell32.IsUserAnAdmin()
    )
except ImportError:
    use_winclient = False


uv = "discouraged"

client_data_collector = DefaultClientDataCollector("https://example.com")

if use_winclient:
    # Use the Windows WebAuthn API if available, and we're not running as admin
    # By default only the PRF extension is allowed, we need to explicitly
    # configure the client to allow hmac-secret
    client = WindowsClient(client_data_collector, allow_hmac_secret=True)
else:
    # Locate a device
    for dev in enumerate_devices():
        client = Fido2Client(
            dev,
            client_data_collector=client_data_collector,
            user_interaction=CliInteraction(),
            # By default only the PRF extension is allowed, we need to explicitly
            # configure the client to allow hmac-secret
            extensions=[HmacSecretExtension(allow_hmac_secret=True)],
        )
        if "hmac-secret" in client.info.extensions:
            break
    else:
        print("No Authenticator with the HmacSecret extension found!")
        sys.exit(1)

server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="none")
user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user,
    resident_key_requirement="discouraged",
    user_verification=uv,
    authenticator_attachment="cross-platform",
)

# Create a credential
result = client.make_credential(
    {
        **create_options["publicKey"],
        "extensions": {"hmacCreateSecret": True},
    }
)

# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]

# HmacSecret result:
if result.client_extension_results.get("hmacCreateSecret"):
    print("New credential created, with HmacSecret")
else:
    # This fails on Windows, but we might still be able to use hmac-secret even if
    # the credential wasn't made with it, so keep going
    print("Failed to create credential with HmacSecret, it might not work")

# Generate a salt for HmacSecret:
salt = os.urandom(32)
print("Authenticate with salt:", salt.hex())


# Prepare parameters for getAssertion
request_options, state = server.authenticate_begin(credentials, user_verification=uv)

# Authenticate the credential
result = client.get_assertion(
    {
        **request_options["publicKey"],
        "extensions": {"hmacGetSecret": {"salt1": salt}},
    }
)

# Only one cred in allowCredentials, only one response.
result = result.get_response(0)

output1 = result.client_extension_results.hmac_get_secret.output1
print("Authenticated, secret:", output1.hex())

# Authenticate again, using two salts to generate two secrets:

# Generate a second salt for HmacSecret:
salt2 = os.urandom(32)
print("Authenticate with second salt:", salt2.hex())

# The first salt is reused, which should result in the same secret.

result = client.get_assertion(
    {
        **request_options["publicKey"],
        "extensions": {"hmacGetSecret": {"salt1": salt, "salt2": salt2}},
    }
)

# Only one cred in allowCredentials, only one response.
result = result.get_response(0)

output = result.client_extension_results.hmac_get_secret
print("Old secret:", output.output1.hex())
print("New secret:", output.output2.hex())
```

## File: examples/large_blobs.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and authenticates the credential.
This works with both FIDO 2.0 devices as well as with U2F devices.
On Windows, the native WebAuthn API will be used.
"""

import sys

from exampleutils import get_client

from fido2.server import Fido2Server
from fido2.utils import websafe_decode, websafe_encode

# Locate a suitable FIDO authenticator
client, info = get_client(lambda info: "largeBlobKey" in info.extensions)

# LargeBlob requires UV if it is configured
uv = "discouraged"
if info.options.get("clientPin"):
    uv = "required"


server = Fido2Server({"id": "example.com", "name": "Example RP"})
user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user,
    resident_key_requirement="required",
    user_verification=uv,
    authenticator_attachment="cross-platform",
)

print("Creating a credential with LargeBlob support...")

# Create a credential
result = client.make_credential(
    {
        **create_options["publicKey"],
        # Enable largeBlob
        "extensions": {"largeBlob": {"support": "required"}},
    }
)

# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]

if auth_data.is_user_verified():
    # The WindowsClient doesn't know about authenticator config until now
    uv = "required"

if not result.client_extension_results.get("largeBlob", {}).get("supported"):
    print("Credential does not support largeBlob, failure!")
    sys.exit(1)

print("Credential created! Writing a blob...")

# Prepare parameters for getAssertion
request_options, state = server.authenticate_begin(credentials, user_verification=uv)

# Authenticate the credential
selection = client.get_assertion(
    {
        **request_options["publicKey"],
        # Write a large blob
        "extensions": {
            "largeBlob": {"write": websafe_encode(b"Here is some data to store!")}
        },
    }
)

# Only one cred in allowCredentials, only one response.
result = selection.get_response(0)
if not result.client_extension_results.get("largeBlob", {}).get("written"):
    print("Failed to write blob!")
    sys.exit(1)

print("Blob written! Reading back the blob...")

# Authenticate the credential
selection = client.get_assertion(
    {
        **request_options["publicKey"],
        # Read the blob
        "extensions": {"largeBlob": {"read": True}},
    }
)

# Only one cred in allowCredentials, only one response.
result = selection.get_response(0)
print(
    "Read blob:", websafe_decode(result.client_extension_results["largeBlob"]["blob"])
)
```

## File: examples/multi_device.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to each FIDO device found, and causes them all to blink until the user
triggers one to select it. A new credential is created for that authenticator,
and the operation is cancelled for the others.
"""

import sys
from getpass import getpass
from threading import Event, Thread

from fido2.client import (
    ClientError,
    DefaultClientDataCollector,
    Fido2Client,
    UserInteraction,
)
from fido2.hid import CtapHidDevice

# Locate a device
devs = list(CtapHidDevice.list_devices())
if not devs:
    print("No FIDO device found")
    sys.exit(1)


# Handle user interaction
class CliInteraction(UserInteraction):
    def prompt_up(self):
        print("\nTouch your authenticator device now...\n")

    def request_pin(self, permissions, rd_id):
        return getpass("Enter PIN: ")

    def request_uv(self, permissions, rd_id):
        print("User Verification required.")
        return True


cli_interaction = CliInteraction()
clients = [
    Fido2Client(
        d,
        client_data_collector=DefaultClientDataCollector("https://example.com"),
        user_interaction=cli_interaction,
    )
    for d in devs
]

# Prepare parameters for makeCredential
rp = {"id": "example.com", "name": "Example RP"}
user = {"id": b"user_id", "name": "A. User"}
challenge = b"Y2hhbGxlbmdl"
cancel = Event()
selected = None


def select(client):
    global selected
    try:
        client.selection(cancel)
        selected = client
    except ClientError as e:
        if e.code != ClientError.ERR.TIMEOUT:
            raise
        else:
            return
    cancel.set()


print("\nTouch the authenticator you wish to use...\n")

threads = []
for client in clients:
    t = Thread(target=select, args=(client,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

if cancel.is_set():
    print("Authenticator selected, making credential...")

    result = selected.make_credential(
        {
            "rp": rp,
            "user": user,
            "challenge": challenge,
            "pubKeyCredParams": [{"type": "public-key", "alg": -7}],
        },
    )

    print("New credential created!")
    response = result.response
    print("ATTESTATION OBJECT:", response.attestation_object)
    print()
    print("CREDENTIAL DATA:", response.attestation_object.auth_data.credential_data)
else:
    print("Operation timed out!")
```

## File: examples/prf.py
```python
# Copyright (c) 2024 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found which supports the PRF extension,
creates a new credential for it with the extension enabled, and uses it to
derive two separate secrets.
"""

import os

from exampleutils import get_client

from fido2.server import Fido2Server
from fido2.utils import websafe_encode

# Locate a suitable FIDO authenticator
client, _ = get_client(lambda info: "hmac-secret" in info.extensions)

uv = "discouraged"

server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="none")
user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user,
    resident_key_requirement="discouraged",
    user_verification=uv,
    authenticator_attachment="cross-platform",
)

# Create a credential
result = client.make_credential(
    {
        **create_options["publicKey"],
        "extensions": {"prf": {}},
    }
)

# Complete registration
auth_data = server.register_complete(state, result)
credential = auth_data.credential_data

# PRF result:
if result.client_extension_results.get("prf", {}).get("enabled"):
    print("New credential created, with PRF")
else:
    # This fails on Windows, but we might still be able to use prf even if
    # the credential wasn't made with it, so keep going
    print("Failed to create credential with PRF, it might not work")

print("New credential created, with the PRF extension.")

# If created with UV, keep using UV
if auth_data.is_user_verified():
    uv = "required"

# Generate a salt for PRF:
salt = websafe_encode(os.urandom(32))
print("Authenticate with salt:", salt)

# Prepare parameters for getAssertion
credentials = [credential]
request_options, state = server.authenticate_begin(credentials, user_verification=uv)

# Authenticate the credential
result = client.get_assertion(
    {
        **request_options["publicKey"],
        "extensions": {"prf": {"eval": {"first": salt}}},
    }
)

# Only one cred in allowCredentials, only one response.
response = result.get_response(0)

output1 = response.client_extension_results["prf"]["results"]["first"]
print("Authenticated, secret:", output1)

# Authenticate again, using two salts to generate two secrets.

# This time we will use evalByCredential, which can be used if there are multiple
# credentials which use different salts. Here it is not needed, but provided for
# completeness of the example.

# Generate a second salt for PRF:
salt2 = websafe_encode(os.urandom(32))
print("Authenticate with second salt:", salt2)
# The first salt is reused, which should result in the same secret.

result = client.get_assertion(
    {
        **request_options["publicKey"],
        "extensions": {
            "prf": {
                "evalByCredential": {
                    websafe_encode(credential.credential_id): {
                        "first": salt,
                        "second": salt2,
                    }
                }
            }
        },
    }
)

# Only one cred in allowCredentials, only one response.
response = result.get_response(0)

output = response.client_extension_results["prf"]["results"]
print("Old secret:", output["first"])
print("New secret:", output["second"])
```

## File: examples/resident_key.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and authenticates the credential.
This works with both FIDO 2.0 devices as well as with U2F devices.
On Windows, the native WebAuthn API will be used.
"""

from exampleutils import get_client

from fido2.server import Fido2Server

# Locate a suitable FIDO authenticator
client, info = get_client(lambda info: info.options.get("rk"))

# Prefer UV if supported and configured
uv = "discouraged"
if info and info.options.get("uv") or info.options.get("bioEnroll"):
    uv = "preferred"
    print("Authenticator is configured for User Verification")

server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")

user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user,
    resident_key_requirement="required",
    user_verification=uv,
    authenticator_attachment="cross-platform",
)

# Create a credential
result = client.make_credential(
    {
        **create_options["publicKey"],
        # This extension isn't needed, but can be used to verify that the created
        # credential uses resident key
        "extensions": {"credProps": True},
    }
)


# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]

print("New credential created!")
response = result.response

print("CLIENT DATA:", response.client_data)
print("ATTESTATION OBJECT:", response.attestation_object)
print()
print("CREDENTIAL DATA:", auth_data.credential_data)
print()
print("Credential Properties:", result.client_extension_results.get("credProps"))

# credProps:
cred_props = result.client_extension_results.get("credProps")
print("CredProps", cred_props)


# Prepare parameters for getAssertion
request_options, state = server.authenticate_begin(user_verification=uv)

# Authenticate the credential
selection = client.get_assertion(request_options["publicKey"])
result = selection.get_response(0)  # There may be multiple responses, get the first.


# Complete authenticator
server.authenticate_complete(state, credentials, result)

print("Credential authenticated!")
response = result.response

print("USER ID:", response.user_handle)
print("CLIENT DATA:", response.client_data)
print()
print("AUTHENTICATOR DATA:", response.authenticator_data)
```

## File: examples/u2f_nfc.py
```python
import sys

from fido2.ctap1 import Ctap1
from fido2.pcsc import CtapPcscDevice
from fido2.utils import sha256

dev = next(CtapPcscDevice.list_devices(), None)
if not dev:
    print("No NFC u2f device found")
    sys.exit(1)

chal = sha256(b"AAA")
appid = sha256(b"BBB")

ctap1 = Ctap1(dev)

print("version:", ctap1.get_version())

# True - make extended APDU and send it to key
# ISO 7816-3:2006. page 33, 12.1.3 Decoding conventions for command APDUs
# ISO 7816-3:2006. page 34, 12.2 Command-response pair transmission by T=0
# False - make group of short (less than 255 bytes length) APDU
# and send them to key. ISO 7816-3:2005, page 9, 5.1.1.1 Command chaining
dev.use_ext_apdu = False

reg = ctap1.register(chal, appid)
print("register:", reg)


reg.verify(appid, chal)
print("Register message verify OK")


auth = ctap1.authenticate(chal, appid, reg.key_handle)
print("authenticate result: ", auth)

res = auth.verify(appid, chal, reg.public_key)
print("Authenticate message verify OK")
```

## File: examples/verify_attestation_mds3.py
```python
# Copyright (c) 2021 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This example shows how to use the FIDO MDS to only allow authenticators for which
metadata is available.

It connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and verifies that attestation is correctly signed
and valid according to its metadata statement.

On Windows, the native WebAuthn API will be used.

NOTE: You need to retrieve a MDS3 blob to run this example.
See https://fidoalliance.org/metadata/ for more info.
"""

import sys
from base64 import b64decode

from exampleutils import get_client

from fido2.attestation import UntrustedAttestation
from fido2.mds3 import MdsAttestationVerifier, parse_blob
from fido2.server import Fido2Server

# Load the root CA used to sign the Metadata Statement blob
ca = b64decode(
    """
MIIDXzCCAkegAwIBAgILBAAAAAABIVhTCKIwDQYJKoZIhvcNAQELBQAwTDEgMB4G
A1UECxMXR2xvYmFsU2lnbiBSb290IENBIC0gUjMxEzARBgNVBAoTCkdsb2JhbFNp
Z24xEzARBgNVBAMTCkdsb2JhbFNpZ24wHhcNMDkwMzE4MTAwMDAwWhcNMjkwMzE4
MTAwMDAwWjBMMSAwHgYDVQQLExdHbG9iYWxTaWduIFJvb3QgQ0EgLSBSMzETMBEG
A1UEChMKR2xvYmFsU2lnbjETMBEGA1UEAxMKR2xvYmFsU2lnbjCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAMwldpB5BngiFvXAg7aEyiie/QV2EcWtiHL8
RgJDx7KKnQRfJMsuS+FggkbhUqsMgUdwbN1k0ev1LKMPgj0MK66X17YUhhB5uzsT
gHeMCOFJ0mpiLx9e+pZo34knlTifBtc+ycsmWQ1z3rDI6SYOgxXG71uL0gRgykmm
KPZpO/bLyCiR5Z2KYVc3rHQU3HTgOu5yLy6c+9C7v/U9AOEGM+iCK65TpjoWc4zd
QQ4gOsC0p6Hpsk+QLjJg6VfLuQSSaGjlOCZgdbKfd/+RFO+uIEn8rUAVSNECMWEZ
XriX7613t2Saer9fwRPvm2L7DWzgVGkWqQPabumDk3F2xmmFghcCAwEAAaNCMEAw
DgYDVR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFI/wS3+o
LkUkrk1Q+mOai97i3Ru8MA0GCSqGSIb3DQEBCwUAA4IBAQBLQNvAUKr+yAzv95ZU
RUm7lgAJQayzE4aGKAczymvmdLm6AC2upArT9fHxD4q/c2dKg8dEe3jgr25sbwMp
jjM5RcOO5LlXbKr8EpbsU8Yt5CRsuZRj+9xTaGdWPoO4zzUhw8lo/s7awlOqzJCK
6fBdRoyV3XpYKBovHd7NADdBj+1EbddTKJd+82cEHhXXipa0095MJ6RMG3NzdvQX
mcIfeg7jLQitChws/zyrVQ4PkX4268NXSb7hLi18YIvDQVETI53O9zJrlAGomecs
Mx86OyXShkDOOyyGeMlhLxS67ttVb9+E7gUJTb0o2HLO02JQZR7rkpeDMdmztcpH
WD9f"""
)

# Parse the MDS3 blob
if len(sys.argv) != 2:
    print("This example requires a FIDO MDS3 metadata blob, which you can get here:")
    print("https://fidoalliance.org/metadata/")
    print()
    print("USAGE: python verify_attestation_mds3.py blob.jwt")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    metadata = parse_blob(f.read(), ca)

# The verifier is used to query for data in the blob and to verify attestation.
# We could optionally pass a filter function to only allow specific authenticators.
mds = MdsAttestationVerifier(metadata)

# Locate a suitable FIDO authenticator
client, _ = get_client()

# The MDS verifier is passed to the server to verify that new credentials registered
# exist in the MDS blob, else the registration will fail.
server = Fido2Server(
    {"id": "example.com", "name": "Example RP"},
    attestation="direct",
    verify_attestation=mds,
)

user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user, user_verification="discouraged", authenticator_attachment="cross-platform"
)

# Create a credential
result = client.make_credential(create_options["publicKey"])

# Complete registration
try:
    auth_data = server.register_complete(state, result)
    print("Registration completed")

    # mds can also be used to get the metadata for the Authenticator,
    # regardless of if it was used to verify the attestation or not:
    response = result.response
    entry = mds.find_entry(response.attestation_object, response.client_data.hash)
    print("Authenticator description:", entry.metadata_statement.description)
except UntrustedAttestation:
    print("Authenticator metadata not found")
```

## File: examples/verify_attestation.py
```python
# Copyright (c) 2021 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This example shows how to use an AttestationVerifier to only allow credentials signed
by a specific CA.

It connects to the first FIDO device found (starts from USB, then looks into NFC),
creates a new credential for it, and verifies that attestation is signed by the
Yubico FIDO root CA (this will only work for Yubico devices).
On Windows, the native WebAuthn API will be used.
"""

from base64 import b64decode

from exampleutils import get_client

from fido2.attestation import AttestationVerifier
from fido2.server import Fido2Server

# Official Yubico root CA for FIDO Authenticators
YUBICO_CA = b64decode(
    """
MIIDHjCCAgagAwIBAgIEG0BT9zANBgkqhkiG9w0BAQsFADAuMSwwKgYDVQQDEyNZ
dWJpY28gVTJGIFJvb3QgQ0EgU2VyaWFsIDQ1NzIwMDYzMTAgFw0xNDA4MDEwMDAw
MDBaGA8yMDUwMDkwNDAwMDAwMFowLjEsMCoGA1UEAxMjWXViaWNvIFUyRiBSb290
IENBIFNlcmlhbCA0NTcyMDA2MzEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQC/jwYuhBVlqaiYWEMsrWFisgJ+PtM91eSrpI4TK7U53mwCIawSDHy8vUmk
5N2KAj9abvT9NP5SMS1hQi3usxoYGonXQgfO6ZXyUA9a+KAkqdFnBnlyugSeCOep
8EdZFfsaRFtMjkwz5Gcz2Py4vIYvCdMHPtwaz0bVuzneueIEz6TnQjE63Rdt2zbw
nebwTG5ZybeWSwbzy+BJ34ZHcUhPAY89yJQXuE0IzMZFcEBbPNRbWECRKgjq//qT
9nmDOFVlSRCt2wiqPSzluwn+v+suQEBsUjTGMEd25tKXXTkNW21wIWbxeSyUoTXw
LvGS6xlwQSgNpk2qXYwf8iXg7VWZAgMBAAGjQjBAMB0GA1UdDgQWBBQgIvz0bNGJ
hjgpToksyKpP9xv9oDAPBgNVHRMECDAGAQH/AgEAMA4GA1UdDwEB/wQEAwIBBjAN
BgkqhkiG9w0BAQsFAAOCAQEAjvjuOMDSa+JXFCLyBKsycXtBVZsJ4Ue3LbaEsPY4
MYN/hIQ5ZM5p7EjfcnMG4CtYkNsfNHc0AhBLdq45rnT87q/6O3vUEtNMafbhU6kt
hX7Y+9XFN9NpmYxr+ekVY5xOxi8h9JDIgoMP4VB1uS0aunL1IGqrNooL9mmFnL2k
LVVee6/VR6C5+KSTCMCWppMuJIZII2v9o4dkoZ8Y7QRjQlLfYzd3qGtKbw7xaF1U
sG/5xUb/Btwb2X2g4InpiB/yt/3CpQXpiWX/K4mBvUKiGn05ZsqeY1gx4g0xLBqc
U9psmyPzK+Vsgw2jeRQ5JlKDyqE0hebfC1tvFu0CCrJFcw==
"""
)


class YubicoAttestationVerifier(AttestationVerifier):
    """Example implementation of an AttestationVerifier.

    This simple example will attempt to verify all trust paths using the Yubico CA.
    A real implementation can use the information in the attestation result, or the
    authenticator data, to determine which CA should be used to verify the path.
    """

    def ca_lookup(self, result, auth_data):
        return YUBICO_CA


# Locate a suitable FIDO authenticator
client, _ = get_client()

server = Fido2Server(
    {"id": "example.com", "name": "Example RP"},
    attestation="direct",
    verify_attestation=YubicoAttestationVerifier(),
)

user = {"id": b"user_id", "name": "A. User"}

# Prepare parameters for makeCredential
create_options, state = server.register_begin(
    user, user_verification="discouraged", authenticator_attachment="cross-platform"
)

# Create a credential
result = client.make_credential(create_options["publicKey"])

# Complete registration
auth_data = server.register_complete(state, result)
credentials = [auth_data.credential_data]

print("New credential created, attestation verified!")
print("Yubico device AAGUID:", auth_data.credential_data.aaguid.hex())
```

## File: fido2/attestation/__init__.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from .android import AndroidSafetynetAttestation  # noqa: F401
from .apple import AppleAttestation  # noqa: F401
from .base import (  # noqa: F401
    Attestation,
    AttestationResult,
    AttestationType,
    AttestationVerifier,
    InvalidData,
    InvalidSignature,
    NoneAttestation,
    UnsupportedAttestation,
    UnsupportedType,
    UntrustedAttestation,
    verify_x509_chain,
)
from .packed import PackedAttestation  # noqa: F401
from .tpm import TpmAttestation  # noqa: F401
from .u2f import FidoU2FAttestation  # noqa: F401
```

## File: fido2/attestation/android.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import json

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.constant_time import bytes_eq

from ..cose import CoseKey
from ..utils import sha256, websafe_decode
from .base import (
    Attestation,
    AttestationResult,
    AttestationType,
    InvalidData,
    catch_builtins,
)


class AndroidSafetynetAttestation(Attestation):
    FORMAT = "android-safetynet"

    def __init__(self, allow_rooted: bool = False):
        self.allow_rooted = allow_rooted

    @catch_builtins
    def verify(self, statement, auth_data, client_data_hash):
        jwt = statement["response"]
        header, payload, sig = (websafe_decode(x) for x in jwt.split(b"."))
        data = json.loads(payload.decode("utf8"))
        if not self.allow_rooted and data["ctsProfileMatch"] is not True:
            raise InvalidData("ctsProfileMatch must be true!")
        expected_nonce = sha256(auth_data + client_data_hash)
        if not bytes_eq(expected_nonce, websafe_decode(data["nonce"])):
            raise InvalidData("Nonce does not match!")

        data = json.loads(header.decode("utf8"))
        x5c = [websafe_decode(x) for x in data["x5c"]]
        cert = x509.load_der_x509_certificate(x5c[0], default_backend())

        cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        if cn[0].value != "attest.android.com":
            raise InvalidData("Certificate not issued to attest.android.com!")

        CoseKey.for_name(data["alg"]).from_cryptography_key(cert.public_key()).verify(
            jwt.rsplit(b".", 1)[0], sig
        )
        return AttestationResult(AttestationType.BASIC, x5c)
```

## File: fido2/attestation/apple.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.constant_time import bytes_eq

from ..utils import sha256
from .base import (
    Attestation,
    AttestationResult,
    AttestationType,
    InvalidData,
    catch_builtins,
)

OID_APPLE = x509.ObjectIdentifier("1.2.840.113635.100.8.2")


class AppleAttestation(Attestation):
    FORMAT = "apple"

    @catch_builtins
    def verify(self, statement, auth_data, client_data_hash):
        x5c = statement["x5c"]
        expected_nonce = sha256(auth_data + client_data_hash)
        cert = x509.load_der_x509_certificate(x5c[0], default_backend())
        ext = cert.extensions.get_extension_for_oid(OID_APPLE)
        # Sequence of single element of octet string
        ext_nonce = ext.value.public_bytes()[6:]
        if not bytes_eq(expected_nonce, ext_nonce):
            raise InvalidData("Nonce does not match!")
        return AttestationResult(AttestationType.ANON_CA, x5c)
```

## File: fido2/attestation/base.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import IntEnum, unique
from functools import wraps
from typing import Any, Mapping, Sequence

from cryptography import x509
from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

from ..webauthn import AttestationObject, AuthenticatorData


class InvalidAttestation(Exception):
    """Base exception for attestation-related errors."""


class InvalidData(InvalidAttestation):
    """Attestation contains invalid data."""


class InvalidSignature(InvalidAttestation):
    """The signature of the attestation could not be verified."""


class UntrustedAttestation(InvalidAttestation):
    """The CA of the attestation is not trusted."""


class UnsupportedType(InvalidAttestation):
    """The attestation format is not supported."""

    def __init__(self, auth_data, fmt=None):
        super().__init__(
            f'Attestation format "{fmt}" is not supported'
            if fmt
            else "This attestation format is not supported!"
        )
        self.auth_data = auth_data
        self.fmt = fmt


@unique
class AttestationType(IntEnum):
    """Supported attestation types."""

    BASIC = 1
    SELF = 2
    ATT_CA = 3
    ANON_CA = 4
    NONE = 0


@dataclass
class AttestationResult:
    """The result of verifying an attestation."""

    attestation_type: AttestationType
    trust_path: list[bytes]


def catch_builtins(f):
    """Utility decoractor to wrap common exceptions related to InvalidData."""

    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            raise InvalidData(e)

    return inner


@catch_builtins
def verify_x509_chain(chain: list[bytes]) -> None:
    """Verifies a chain of certificates.

    Checks that the first item in the chain is signed by the next, and so on.
    The first item is the leaf, the last is the root.
    """
    certs = [x509.load_der_x509_certificate(der, default_backend()) for der in chain]
    cert = certs.pop(0)
    while certs:
        child = cert
        cert = certs.pop(0)
        pub = cert.public_key()
        try:
            if isinstance(pub, rsa.RSAPublicKey):
                assert child.signature_hash_algorithm is not None  # noqa: S101
                pub.verify(
                    child.signature,
                    child.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    child.signature_hash_algorithm,
                )
            elif isinstance(pub, ec.EllipticCurvePublicKey):
                assert child.signature_hash_algorithm is not None  # noqa: S101
                pub.verify(
                    child.signature,
                    child.tbs_certificate_bytes,
                    ec.ECDSA(child.signature_hash_algorithm),
                )
            else:
                raise ValueError("Unsupported signature key type")
        except _InvalidSignature:
            raise InvalidSignature()


class Attestation(abc.ABC):
    """Implements verification of a specific attestation type."""

    @abc.abstractmethod
    def verify(
        self,
        statement: Mapping[str, Any],
        auth_data: AuthenticatorData,
        client_data_hash: bytes,
    ) -> AttestationResult:
        """Verifies attestation statement.

        :return: An AttestationResult if successful.
        """

    @staticmethod
    def for_type(fmt: str) -> type[Attestation]:
        """Get an Attestation subclass type for the given format."""
        for cls in Attestation.__subclasses__():
            if getattr(cls, "FORMAT", None) == fmt:
                return cls

        class TypedUnsupportedAttestation(UnsupportedAttestation):
            def __init__(self):
                super().__init__(fmt)

        return TypedUnsupportedAttestation


class UnsupportedAttestation(Attestation):
    def __init__(self, fmt=None):
        self.fmt = fmt

    def verify(self, statement, auth_data, client_data_hash):
        raise UnsupportedType(auth_data, self.fmt)


class NoneAttestation(Attestation):
    FORMAT = "none"

    def verify(self, statement, auth_data, client_data_hash):
        if statement != {}:
            raise InvalidData("None Attestation requires empty statement.")
        return AttestationResult(AttestationType.NONE, [])


def _validate_cert_common(cert):
    if cert.version != x509.Version.v3:
        raise InvalidData("Attestation certificate must use version 3!")

    try:
        bc = cert.extensions.get_extension_for_class(x509.BasicConstraints)
        if bc.value.ca:
            raise InvalidData("Attestation certificate must have CA=false!")
    except x509.ExtensionNotFound:
        raise InvalidData("Attestation certificate must have Basic Constraints!")


def _default_attestations():
    return [
        cls()  # type: ignore
        for cls in Attestation.__subclasses__()
        if getattr(cls, "FORMAT", "none") != "none"
    ]


class AttestationVerifier(abc.ABC):
    """Base class for verifying attestation.

    Override the ca_lookup method to provide a trusted root certificate used
    to verify the trust path from the attestation.
    """

    def __init__(self, attestation_types: Sequence[Attestation] | None = None):
        self._attestation_types = attestation_types or _default_attestations()

    @abc.abstractmethod
    def ca_lookup(
        self, attestation_result: AttestationResult, auth_data: AuthenticatorData
    ) -> bytes | None:
        """Lookup a CA certificate to be used to verify a trust path.

        :param attestation_result: The result of the attestation
        :param auth_data: The AuthenticatorData from the registration
        """
        raise NotImplementedError()

    def verify_attestation(
        self, attestation_object: AttestationObject, client_data_hash: bytes
    ) -> None:
        """Verify attestation.

        :param attestation_object: dict containing attestation data.
        :param client_data_hash: SHA256 hash of the ClientData bytes.
        """
        att_verifier: Attestation = UnsupportedAttestation(attestation_object.fmt)
        for at in self._attestation_types:
            if getattr(at, "FORMAT", None) == attestation_object.fmt:
                att_verifier = at
                break
        # An unsupported format causes an exception to be thrown, which
        # includes the auth_data. The caller may choose to handle this case
        # and allow the registration.
        result = att_verifier.verify(
            attestation_object.att_stmt,
            attestation_object.auth_data,
            client_data_hash,
        )

        # Lookup CA to use for trust path verification
        ca = self.ca_lookup(result, attestation_object.auth_data)
        if not ca:
            raise UntrustedAttestation("No root found for Authenticator")

        # Validate the trust chain
        try:
            verify_x509_chain(result.trust_path + [ca])
        except InvalidSignature as e:
            raise UntrustedAttestation(e)

    def __call__(self, *args):
        """Allows passing an instance to Fido2Server as verify_attestation"""
        self.verify_attestation(*args)
```

## File: fido2/attestation/packed.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from cryptography import x509
from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.backends import default_backend

from ..cose import CoseKey
from .base import (
    Attestation,
    AttestationResult,
    AttestationType,
    InvalidData,
    InvalidSignature,
    _validate_cert_common,
    catch_builtins,
)

OID_AAGUID = x509.ObjectIdentifier("1.3.6.1.4.1.45724.1.1.4")


def _validate_packed_cert(cert, aaguid):
    # https://www.w3.org/TR/webauthn/#packed-attestation-cert-requirements
    _validate_cert_common(cert)

    c = cert.subject.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)
    if not c:
        raise InvalidData("Subject must have C set!")
    o = cert.subject.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)
    if not o:
        raise InvalidData("Subject must have O set!")
    ous = cert.subject.get_attributes_for_oid(x509.NameOID.ORGANIZATIONAL_UNIT_NAME)
    if not ous:
        raise InvalidData('Subject must have OU = "Authenticator Attestation"!')

    ou = ous[0]
    if ou.value != "Authenticator Attestation":
        raise InvalidData('Subject must have OU = "Authenticator Attestation"!')
    cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if not cn:
        raise InvalidData("Subject must have CN set!")

    try:
        ext = cert.extensions.get_extension_for_oid(OID_AAGUID)
        if ext.critical:
            raise InvalidData("AAGUID extension must not be marked as critical")
        ext_aaguid = ext.value.value[2:]
        if ext_aaguid != aaguid:
            raise InvalidData(
                "AAGUID in Authenticator data does not match attestation certificate!"
            )
    except x509.ExtensionNotFound:
        pass  # If missing, ignore


class PackedAttestation(Attestation):
    FORMAT = "packed"

    @catch_builtins
    def verify(self, statement, auth_data, client_data_hash):
        if "ecdaaKeyId" in statement:
            raise NotImplementedError("ECDAA not implemented")
        alg = statement["alg"]
        x5c = statement.get("x5c")
        assert auth_data.credential_data is not None  # noqa: S101
        if x5c:
            cert = x509.load_der_x509_certificate(x5c[0], default_backend())
            _validate_packed_cert(cert, auth_data.credential_data.aaguid)

            pub_key = CoseKey.for_alg(alg).from_cryptography_key(cert.public_key())
            att_type = AttestationType.BASIC
        else:
            pub_key = CoseKey.parse(auth_data.credential_data.public_key)
            if pub_key.ALGORITHM != alg:
                raise InvalidData("Wrong algorithm of public key!")
            att_type = AttestationType.SELF
        try:
            pub_key.verify(auth_data + client_data_hash, statement["sig"])
            return AttestationResult(att_type, x5c or [])
        except _InvalidSignature:
            raise InvalidSignature()
```

## File: fido2/attestation/tpm.py
```python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import struct
from dataclasses import dataclass
from enum import IntEnum, unique
from typing import TypeAlias, cast

from cryptography import x509
from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from ..cose import CoseKey
from ..utils import ByteBuffer, bytes2int
from .base import (
    Attestation,
    AttestationResult,
    AttestationType,
    InvalidData,
    InvalidSignature,
    _validate_cert_common,
    catch_builtins,
)

TPM_ALG_NULL = 0x0010
OID_AIK_CERTIFICATE = x509.ObjectIdentifier("2.23.133.8.3")


@unique
class TpmRsaScheme(IntEnum):
    RSASSA = 0x0014
    RSAPSS = 0x0016
    OAEP = 0x0017
    RSAES = 0x0015


@unique
class TpmAlgAsym(IntEnum):
    RSA = 0x0001
    ECC = 0x0023


@unique
class TpmAlgHash(IntEnum):
    SHA1 = 0x0004
    SHA256 = 0x000B
    SHA384 = 0x000C
    SHA512 = 0x000D

    def _hash_alg(self) -> hashes.HashAlgorithm:
        if self == TpmAlgHash.SHA1:
            return hashes.SHA1()  # noqa: S303
        elif self == TpmAlgHash.SHA256:
            return hashes.SHA256()
        elif self == TpmAlgHash.SHA384:
            return hashes.SHA384()
        elif self == TpmAlgHash.SHA512:
            return hashes.SHA512()

        raise NotImplementedError(f"_hash_alg is not implemented for {self!r}")


@dataclass
class TpmsCertifyInfo:
    name: bytes
    qualified_name: bytes


TPM_GENERATED_VALUE = b"\xffTCG"
TPM_ST_ATTEST_CERTIFY = b"\x80\x17"


@dataclass
class TpmAttestationFormat:
    """the signature data is defined by [TPMv2-Part2] Section 10.12.8 (TPMS_ATTEST)
    as:
      TPM_GENERATED_VALUE (0xff544347 aka "\xffTCG")
      TPMI_ST_ATTEST - always TPM_ST_ATTEST_CERTIFY (0x8017)
        because signing procedure defines it should call TPM_Certify
        [TPMv2-Part3] Section 18.2
      TPM2B_NAME
        size (uint16)
        name (size long)
      TPM2B_DATA
        size (uint16)
        name (size long)
      TPMS_CLOCK_INFO
        clock (uint64)
        resetCount (uint32)
        restartCount (uint32)
        safe (byte) 1 yes, 0 no
      firmwareVersion uint64
      attested TPMS_CERTIFY_INFO (because TPM_ST_ATTEST_CERTIFY)
        name TPM2B_NAME
        qualified_name TPM2B_NAME
    See:
      https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
      https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-3-Commands-01.38.pdf
    """

    name: bytes
    data: bytes
    clock_info: tuple[int, int, int, bool]
    firmware_version: int
    attested: TpmsCertifyInfo

    @classmethod
    def parse(cls, data: bytes) -> TpmAttestationFormat:
        reader = ByteBuffer(data)
        generated_value = reader.read(4)

        # Verify that magic is set to TPM_GENERATED_VALUE.
        # see https://w3c.github.io/webauthn/#sctn-tpm-attestation
        #     verification procedure
        if generated_value != TPM_GENERATED_VALUE:
            raise ValueError("generated value field is invalid")

        # Verify that type is set to TPM_ST_ATTEST_CERTIFY.
        # see https://w3c.github.io/webauthn/#sctn-tpm-attestation
        #     verification procedure
        tpmi_st_attest = reader.read(2)
        if tpmi_st_attest != TPM_ST_ATTEST_CERTIFY:
            raise ValueError("tpmi_st_attest field is invalid")

        try:
            name = reader.read(reader.unpack("!H"))
            data = reader.read(reader.unpack("!H"))

            clock = reader.unpack("!Q")
            reset_count = reader.unpack("!L")
            restart_count = reader.unpack("!L")
            safe_value = reader.unpack("B")
            if safe_value not in (0, 1):
                raise ValueError(f"invalid value 0x{safe_value:x} for boolean")
            safe = safe_value == 1

            firmware_version = reader.unpack("!Q")

            attested_name = reader.read(reader.unpack("!H"))
            attested_qualified_name = reader.read(reader.unpack("!H"))
        except struct.error as e:
            raise ValueError(e)

        return cls(
            name=name,
            data=data,
            clock_info=(clock, reset_count, restart_count, safe),
            firmware_version=firmware_version,
            attested=TpmsCertifyInfo(
                name=attested_name, qualified_name=attested_qualified_name
            ),
        )


@dataclass
class TpmsRsaParms:
    """Parse TPMS_RSA_PARMS struct

    See:
    https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    section 12.2.3.5
    """

    symmetric: int
    scheme: int
    key_bits: int
    exponent: int

    @classmethod
    def parse(cls, reader, attributes):
        symmetric = reader.unpack("!H")

        restricted_decryption = attributes & (
            ATTRIBUTES.RESTRICTED | ATTRIBUTES.DECRYPT
        )
        is_restricted_decryption_key = restricted_decryption == (
            ATTRIBUTES.DECRYPT | ATTRIBUTES.RESTRICTED
        )
        if not is_restricted_decryption_key and symmetric != TPM_ALG_NULL:
            # if the key is not a restricted decryption key, this field
            # shall be set to TPM_ALG_NULL.
            raise ValueError("symmetric is expected to be NULL")
        # Otherwise should be set to a supported symmetric algorithm, keysize and mode
        # TODO(baloo): Should we have non-null value here, do we expect more data?

        scheme = reader.unpack("!H")

        restricted_sign = attributes & (ATTRIBUTES.RESTRICTED | ATTRIBUTES.SIGN_ENCRYPT)
        is_unrestricted_signing_key = restricted_sign == ATTRIBUTES.SIGN_ENCRYPT
        if is_unrestricted_signing_key and scheme not in (
            TPM_ALG_NULL,
            TpmRsaScheme.RSASSA,
            TpmRsaScheme.RSAPSS,
        ):
            raise ValueError(
                "key is an unrestricted signing key, scheme is "
                "expected to be TPM_ALG_RSAPSS, TPM_ALG_RSASSA, "
                "or TPM_ALG_NULL"
            )

        is_restricted_signing_key = restricted_sign == (
            ATTRIBUTES.RESTRICTED | ATTRIBUTES.SIGN_ENCRYPT
        )
        if is_restricted_signing_key and scheme not in (
            TpmRsaScheme.RSASSA,
            TpmRsaScheme.RSAPSS,
        ):
            raise ValueError(
                "key is a restricted signing key, scheme is "
                "expected to be TPM_ALG_RSAPSS, or TPM_ALG_RSASSA"
            )

        is_unrestricted_decryption_key = restricted_decryption == ATTRIBUTES.DECRYPT
        if is_unrestricted_decryption_key and scheme not in (
            TpmRsaScheme.OAEP,
            TpmRsaScheme.RSAES,
            TPM_ALG_NULL,
        ):
            raise ValueError(
                "key is an unrestricted decryption key, scheme is "
                "expected to be TPM_ALG_RSAES, TPM_ALG_OAEP, or "
                "TPM_ALG_NULL"
            )

        if is_restricted_decryption_key and scheme not in (TPM_ALG_NULL,):
            raise ValueError(
                "key is an restricted decryption key, scheme is "
                "expected to be TPM_ALG_NULL"
            )

        key_bits = reader.unpack("!H")
        exponent = reader.unpack("!L")
        if exponent == 0:
            # When  zero,  indicates  that  the  exponent  is  the  default  of 2^16 + 1
            exponent = (2**16) + 1

        return cls(symmetric, scheme, key_bits, exponent)


class Tpm2bPublicKeyRsa(bytes):
    @classmethod
    def parse(cls, reader: ByteBuffer) -> Tpm2bPublicKeyRsa:
        return cls(reader.read(reader.unpack("!H")))


@unique
class TpmEccCurve(IntEnum):
    """TPM_ECC_CURVE
    https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    section 6.4
    """

    NONE = 0x0000
    NIST_P192 = 0x0001
    NIST_P224 = 0x0002
    NIST_P256 = 0x0003
    NIST_P384 = 0x0004
    NIST_P521 = 0x0005
    BN_P256 = 0x0010
    BN_P638 = 0x0011
    SM2_P256 = 0x0020

    def to_curve(self) -> ec.EllipticCurve:
        if self == TpmEccCurve.NONE:
            raise ValueError("No such curve")
        elif self == TpmEccCurve.NIST_P192:
            return ec.SECP192R1()
        elif self == TpmEccCurve.NIST_P224:
            return ec.SECP224R1()
        elif self == TpmEccCurve.NIST_P256:
            return ec.SECP256R1()
        elif self == TpmEccCurve.NIST_P384:
            return ec.SECP384R1()
        elif self == TpmEccCurve.NIST_P521:
            return ec.SECP521R1()

        raise ValueError("curve is not supported", self)


@unique
class TpmiAlgKdf(IntEnum):
    """TPMI_ALG_KDF
    https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    section 9.28
    """

    NULL = TPM_ALG_NULL
    KDF1_SP800_56A = 0x0020
    KDF2 = 0x0021
    KDF1_SP800_108 = 0x0022


@dataclass
class TpmsEccParms:
    symmetric: int
    scheme: int
    curve_id: TpmEccCurve
    kdf: TpmiAlgKdf

    @classmethod
    def parse(cls, reader: ByteBuffer) -> TpmsEccParms:
        symmetric = reader.unpack("!H")
        scheme = reader.unpack("!H")
        if symmetric != TPM_ALG_NULL:
            raise ValueError("symmetric is expected to be NULL")
        if scheme != TPM_ALG_NULL:
            raise ValueError("scheme is expected to be NULL")

        curve_id = TpmEccCurve(reader.unpack("!H"))
        kdf_scheme = TpmiAlgKdf(reader.unpack("!H"))

        return cls(symmetric, scheme, curve_id, kdf_scheme)


@dataclass
class TpmsEccPoint:
    """TPMS_ECC_POINT
    https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    Section 11.2.5.2
    """

    x: bytes
    y: bytes

    @classmethod
    def parse(cls, reader: ByteBuffer) -> TpmsEccPoint:
        x = reader.read(reader.unpack("!H"))
        y = reader.read(reader.unpack("!H"))

        return cls(x, y)


@unique
class ATTRIBUTES(IntEnum):
    """Object attributes
    see section 8.3
      https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    """

    FIXED_TPM = 1 << 1
    ST_CLEAR = 1 << 2
    FIXED_PARENT = 1 << 4
    SENSITIVE_DATA_ORIGIN = 1 << 5
    USER_WITH_AUTH = 1 << 6
    ADMIN_WITH_POLICY = 1 << 7
    NO_DA = 1 << 10
    ENCRYPTED_DUPLICATION = 1 << 11
    RESTRICTED = 1 << 16
    DECRYPT = 1 << 17
    SIGN_ENCRYPT = 1 << 18

    SHALL_BE_ZERO = (
        (1 << 0)  # 0 Reserved
        | (1 << 3)  # 3 Reserved
        | (0x3 << 8)  # 9:8 Reserved
        | (0xF << 12)  # 15:12 Reserved
        | ((0xFFFFFFFF << 19) & (2**32 - 1))  # 31:19 Reserved
    )


_PublicKey: TypeAlias = rsa.RSAPublicKey | ec.EllipticCurvePublicKey
_Parameters = TpmsRsaParms | TpmsEccParms
_Unique = Tpm2bPublicKeyRsa | TpmsEccPoint


@dataclass
class TpmPublicFormat:
    """the public area structure is defined by [TPMv2-Part2] Section 12.2.4
    (TPMT_PUBLIC)
    as:
      TPMI_ALG_PUBLIC - type
      TPMI_ALG_HASH - nameAlg
        or + to indicate TPM_ALG_NULL
      TPMA_OBJECT - objectAttributes
      TPM2B_DIGEST - authPolicy
      TPMU_PUBLIC_PARMS - type parameters
      TPMU_PUBLIC_ID - uniq
    See:
      https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
    """

    sign_alg: TpmAlgAsym
    name_alg: TpmAlgHash
    attributes: int
    auth_policy: bytes
    parameters: _Parameters
    unique: _Unique
    data: bytes

    @classmethod
    def parse(cls, data: bytes) -> TpmPublicFormat:
        reader = ByteBuffer(data)
        sign_alg = TpmAlgAsym(reader.unpack("!H"))
        name_alg = TpmAlgHash(reader.unpack("!H"))

        attributes = reader.unpack("!L")
        if attributes & ATTRIBUTES.SHALL_BE_ZERO != 0:
            raise ValueError(f"attributes is not formated correctly: 0x{attributes:x}")

        auth_policy = reader.read(reader.unpack("!H"))

        if sign_alg == TpmAlgAsym.RSA:
            parameters: _Parameters = TpmsRsaParms.parse(reader, attributes)
            unique: _Unique = Tpm2bPublicKeyRsa.parse(reader)
        elif sign_alg == TpmAlgAsym.ECC:
            parameters = TpmsEccParms.parse(reader)
            unique = TpmsEccPoint.parse(reader)
        else:
            raise NotImplementedError(f"sign alg {sign_alg:x} is not supported")

        rest = reader.read()
        if len(rest) != 0:
            raise ValueError("there should not be any data left in buffer")

        return cls(
            sign_alg, name_alg, attributes, auth_policy, parameters, unique, data
        )

    def public_key(self) -> _PublicKey:
        if self.sign_alg == TpmAlgAsym.RSA:
            exponent = cast(TpmsRsaParms, self.parameters).exponent
            modulus = bytes2int(cast(Tpm2bPublicKeyRsa, self.unique))
            return rsa.RSAPublicNumbers(exponent, modulus).public_key(default_backend())
        elif self.sign_alg == TpmAlgAsym.ECC:
            unique = cast(TpmsEccPoint, self.unique)
            return ec.EllipticCurvePublicNumbers(
                bytes2int(unique.x),
                bytes2int(unique.y),
                cast(TpmsEccParms, self.parameters).curve_id.to_curve(),
            ).public_key(default_backend())

        raise NotImplementedError(f"public_key not implemented for {self.sign_alg!r}")

    def name(self) -> bytes:
        """
        Computing Entity Names

        see:
          https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-1-Architecture-01.38.pdf
        section 16 Names

        Name ≔ nameAlg || HnameAlg (handle→nvPublicArea)
          where
            nameAlg algorithm used to compute Name
            HnameAlg hash using the nameAlg parameter in the NV Index location
                     associated with handle
            nvPublicArea contents of the TPMS_NV_PUBLIC associated with handle
        """
        output = struct.pack("!H", self.name_alg)

        digest = hashes.Hash(self.name_alg._hash_alg(), backend=default_backend())
        digest.update(self.data)
        output += digest.finalize()

        return output


def _validate_tpm_cert(cert):
    # https://www.w3.org/TR/webauthn/#tpm-cert-requirements
    _validate_cert_common(cert)

    s = cert.subject.get_attributes_for_oid(x509.NameOID)
    if s:
        raise InvalidData("Certificate should not have Subject")

    s = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    if not s:
        raise InvalidData("Certificate should have SubjectAlternativeName")
    ext = cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage)
    has_aik = [x == OID_AIK_CERTIFICATE for x in ext.value]
    if True not in has_aik:
        raise InvalidData(
            'Extended key usage MUST contain the "joint-iso-itu-t(2) '
            "internationalorganizations(23) 133 tcg-kp(8) "
            'tcg-kp-AIKCertificate(3)" OID.'
        )


class TpmAttestation(Attestation):
    FORMAT = "tpm"

    @catch_builtins
    def verify(self, statement, auth_data, client_data_hash):
        if "ecdaaKeyId" in statement:
            raise NotImplementedError("ECDAA not implemented")
        alg = statement["alg"]
        x5c = statement["x5c"]
        cert_info = statement["certInfo"]
        cert = x509.load_der_x509_certificate(x5c[0], default_backend())
        _validate_tpm_cert(cert)

        pub_key = CoseKey.for_alg(alg).from_cryptography_key(cert.public_key())

        try:
            pub_area = TpmPublicFormat.parse(statement["pubArea"])
        except Exception as e:
            raise InvalidData("unable to parse pubArea", e)

        # Verify that the public key specified by the parameters and unique
        # fields of pubArea is identical to the credentialPublicKey in the
        # attestedCredentialData in authenticatorData.
        assert auth_data.credential_data is not None  # noqa: S101
        if (
            auth_data.credential_data.public_key.from_cryptography_key(
                pub_area.public_key()
            )
            != auth_data.credential_data.public_key
        ):
            raise InvalidSignature(
                "attestation pubArea does not match attestedCredentialData"
            )

        try:
            # TpmAttestationFormat.parse is reponsible for:
            #   Verify that magic is set to TPM_GENERATED_VALUE.
            #   Verify that type is set to TPM_ST_ATTEST_CERTIFY.
            tpm = TpmAttestationFormat.parse(cert_info)

            # Verify that extraData is set to the hash of attToBeSigned
            # using the hash algorithm employed in "alg".
            att_to_be_signed = auth_data + client_data_hash
            hash_alg = pub_key._HASH_ALG  # type: ignore
            digest = hashes.Hash(hash_alg, backend=default_backend())
            digest.update(att_to_be_signed)
            data = digest.finalize()

            if tpm.data != data:
                raise InvalidSignature(
                    "attestation does not sign for authData and ClientData"
                )

            # Verify that attested contains a TPMS_CERTIFY_INFO structure as
            # specified in [TPMv2-Part2] section 10.12.3, whose name field
            # contains a valid Name for pubArea, as computed using the
            # algorithm in the nameAlg field of pubArea using the procedure
            # specified in [TPMv2-Part1] section 16.
            # [TPMv2-Part2]:
            # https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-2-Structures-01.38.pdf
            # [TPMv2-Part1]:
            # https://www.trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-1-Architecture-01.38.pdf
            if tpm.attested.name != pub_area.name():
                raise InvalidData(
                    "TPMS_CERTIFY_INFO does not include a valid name for pubArea"
                )

            pub_key.verify(cert_info, statement["sig"])
            return AttestationResult(AttestationType.ATT_CA, x5c)
        except _InvalidSignature:
            raise InvalidSignature("signature of certInfo does not match")
```

## File: fido2/attestation/u2f.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from cryptography import x509
from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.backends import default_backend

from ..cose import ES256
from .base import (
    Attestation,
    AttestationResult,
    AttestationType,
    InvalidSignature,
    catch_builtins,
)


class FidoU2FAttestation(Attestation):
    FORMAT = "fido-u2f"

    @catch_builtins
    def verify(self, statement, auth_data, client_data_hash):
        cd = auth_data.credential_data
        assert cd is not None  # noqa: S101
        pk = b"\x04" + cd.public_key[-2] + cd.public_key[-3]
        x5c = statement["x5c"]
        FidoU2FAttestation.verify_signature(
            auth_data.rp_id_hash,
            client_data_hash,
            cd.credential_id,
            pk,
            x5c[0],
            statement["sig"],
        )
        return AttestationResult(AttestationType.BASIC, x5c)

    @staticmethod
    def verify_signature(
        app_param, client_param, key_handle, public_key, cert_bytes, signature
    ):
        m = b"\0" + app_param + client_param + key_handle + public_key
        cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
        try:
            ES256.from_cryptography_key(cert.public_key()).verify(m, signature)
        except _InvalidSignature:
            raise InvalidSignature()
```

## File: fido2/client/__init__.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
import logging
from dataclasses import replace
from enum import IntEnum, unique
from threading import Event, Timer
from typing import Any, Callable, Mapping, Sequence, overload
from urllib.parse import urlparse

from ..cose import ES256
from ..ctap import CtapDevice, CtapError
from ..ctap1 import APDU, ApduError, Ctap1
from ..ctap2 import AssertionResponse, Ctap2, Info
from ..ctap2.extensions import (
    _DEFAULT_EXTENSIONS,
    AuthenticationExtensionProcessor,
    Ctap2Extension,
    RegistrationExtensionProcessor,
)
from ..ctap2.pin import ClientPin, PinProtocol
from ..hid import STATUS
from ..rpid import verify_rp_id
from ..utils import sha256
from ..webauthn import (
    Aaguid,
    AttestationConveyancePreference,
    AttestationObject,
    AuthenticationExtensionsClientOutputs,
    AuthenticationResponse,
    AuthenticatorAssertionResponse,
    AuthenticatorAttachment,
    AuthenticatorAttestationResponse,
    AuthenticatorSelectionCriteria,
    CollectedClientData,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialType,
    RegistrationResponse,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    _as_cbor,
)

logger = logging.getLogger(__name__)


class ClientError(Exception):
    """Base error raised by clients."""

    @unique
    class ERR(IntEnum):
        """Error codes for ClientError."""

        OTHER_ERROR = 1
        BAD_REQUEST = 2
        CONFIGURATION_UNSUPPORTED = 3
        DEVICE_INELIGIBLE = 4
        TIMEOUT = 5

        def __call__(self, cause=None):
            return ClientError(self, cause)

    def __init__(self, code, cause=None):
        self.code = ClientError.ERR(code)
        self.cause = cause

    def __repr__(self):
        r = "Client error: {0} - {0.name}".format(self.code)
        if self.cause:
            r += f" (cause: {self.cause})"
        return r


def _ctap2client_err(e, err_cls=ClientError):
    if e.code in [CtapError.ERR.CREDENTIAL_EXCLUDED, CtapError.ERR.NO_CREDENTIALS]:
        ce = ClientError.ERR.DEVICE_INELIGIBLE
    elif e.code in [
        CtapError.ERR.KEEPALIVE_CANCEL,
        CtapError.ERR.ACTION_TIMEOUT,
        CtapError.ERR.USER_ACTION_TIMEOUT,
    ]:
        ce = ClientError.ERR.TIMEOUT
    elif e.code in [
        CtapError.ERR.UNSUPPORTED_ALGORITHM,
        CtapError.ERR.UNSUPPORTED_OPTION,
        CtapError.ERR.KEY_STORE_FULL,
    ]:
        ce = ClientError.ERR.CONFIGURATION_UNSUPPORTED
    elif e.code in [
        CtapError.ERR.INVALID_COMMAND,
        CtapError.ERR.CBOR_UNEXPECTED_TYPE,
        CtapError.ERR.INVALID_CBOR,
        CtapError.ERR.MISSING_PARAMETER,
        CtapError.ERR.INVALID_OPTION,
        CtapError.ERR.PUAT_REQUIRED,
        CtapError.ERR.PIN_INVALID,
        CtapError.ERR.PIN_BLOCKED,
        CtapError.ERR.PIN_NOT_SET,
        CtapError.ERR.PIN_POLICY_VIOLATION,
        CtapError.ERR.PIN_TOKEN_EXPIRED,
        CtapError.ERR.PIN_AUTH_INVALID,
        CtapError.ERR.PIN_AUTH_BLOCKED,
        CtapError.ERR.REQUEST_TOO_LARGE,
        CtapError.ERR.OPERATION_DENIED,
    ]:
        ce = ClientError.ERR.BAD_REQUEST
    else:
        ce = ClientError.ERR.OTHER_ERROR

    return err_cls(ce, e)


class PinRequiredError(ClientError):
    """Raised when a call cannot be completed without providing PIN."""

    def __init__(
        self, code=ClientError.ERR.BAD_REQUEST, cause="PIN required but not provided"
    ):
        super().__init__(code, cause)


def _call_polling(poll_delay, event, on_keepalive, func, *args, **kwargs):
    event = event or Event()
    while not event.is_set():
        try:
            return func(*args, **kwargs)
        except ApduError as e:
            if e.code == APDU.USE_NOT_SATISFIED:
                if on_keepalive:
                    on_keepalive(STATUS.UPNEEDED)
                    on_keepalive = None
                event.wait(poll_delay)
            else:
                raise ClientError.ERR.OTHER_ERROR(e)
        except CtapError as e:
            raise _ctap2client_err(e)
    raise ClientError.ERR.TIMEOUT()


class AssertionSelection:
    """GetAssertion result holding one or more assertions.

    Since multiple assertions may be retured by Fido2Client.get_assertion, this result
    is returned which can be used to select a specific response to get.
    """

    def __init__(
        self,
        client_data: CollectedClientData,
        assertions: Sequence[AssertionResponse],
        extension_results: Mapping[str, Any] = {},
    ):
        self._client_data = client_data
        self._assertions = assertions
        self._extension_results = extension_results

    def get_assertions(self) -> Sequence[AssertionResponse]:
        """Get the raw AssertionResponses available to inspect before selecting one."""
        return self._assertions

    def _get_extension_results(self, assertion: AssertionResponse) -> Mapping[str, Any]:
        return self._extension_results

    def get_response(self, index: int) -> AuthenticationResponse:
        """Get a single response."""
        assertion = self._assertions[index]

        return AuthenticationResponse(
            raw_id=assertion.credential["id"],
            response=AuthenticatorAssertionResponse(
                client_data=self._client_data,
                authenticator_data=assertion.auth_data,
                signature=assertion.signature,
                user_handle=assertion.user["id"] if assertion.user else None,
            ),
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            client_extension_results=AuthenticationExtensionsClientOutputs(
                self._get_extension_results(assertion)
            ),
            type=PublicKeyCredentialType.PUBLIC_KEY,
        )


class WebAuthnClient(abc.ABC):
    """Base class for a WebAuthn client, supporting registration and authentication."""

    @abc.abstractmethod
    def make_credential(
        self,
        options: PublicKeyCredentialCreationOptions,
        event: Event | None = None,
    ) -> RegistrationResponse:
        """Creates a credential.

        :param options: PublicKeyCredentialCreationOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_assertion(
        self,
        options: PublicKeyCredentialRequestOptions,
        event: Event | None = None,
    ) -> AssertionSelection:
        """Get an assertion.

        :param options: PublicKeyCredentialRequestOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """
        raise NotImplementedError()


class UserInteraction:
    """Provides user interaction to the Client.

    Users of Fido2Client should subclass this to implement asking the user to perform
    specific actions, such as entering a PIN or touching their"""

    def prompt_up(self) -> None:
        """Called when the authenticator is awaiting a user presence check."""
        logger.info("User Presence check required.")

    def request_pin(
        self, permissions: ClientPin.PERMISSION, rp_id: str | None
    ) -> str | None:
        """Called when the client requires a PIN from the user.

        Should return a PIN, or None/Empty to cancel."""
        logger.info("PIN requested, but UserInteraction does not support it.")
        return None

    def request_uv(self, permissions: ClientPin.PERMISSION, rp_id: str | None) -> bool:
        """Called when the client is about to request UV from the user.

        Should return True if allowed, or False to cancel."""
        logger.info("User Verification requested.")
        return True


class ClientDataCollector(abc.ABC):
    """Provides client data and logic to the Client.

    Users should subclass this to implement custom behavior for determining the origin,
    validating the RP ID, and providing client data for a request.
    """

    @abc.abstractmethod
    def collect_client_data(
        self,
        options: PublicKeyCredentialCreationOptions | PublicKeyCredentialRequestOptions,
    ) -> tuple[CollectedClientData, str]:
        """Called when the client is preparing a request.

        Should return a CollectedClientData object with the client data for the request,
        as well as the RP ID of the credential.
        """


class DefaultClientDataCollector(ClientDataCollector):
    """Default implementation of ClientDataProvider.

    This implementation uses a fixed origin, it can be subclassed to customize specific
    behavior.
    """

    def __init__(self, origin: str, verify: Callable[[str, str], bool] = verify_rp_id):
        self._origin = origin
        self._verify = verify

    def get_rp_id(
        self,
        options: PublicKeyCredentialCreationOptions | PublicKeyCredentialRequestOptions,
        origin: str,
    ) -> str:
        """Get the RP ID for the given options and origin."""
        if isinstance(options, PublicKeyCredentialCreationOptions):
            rp_id = options.rp.id
        elif isinstance(options, PublicKeyCredentialRequestOptions):
            rp_id = options.rp_id
        else:
            raise ValueError("Invalid options type.")

        if rp_id is None:
            url = urlparse(origin)
            if url.scheme != "https" or not url.netloc:
                raise ClientError.ERR.BAD_REQUEST(
                    "RP ID required for non-https origin."
                )
            return url.netloc
        else:
            return rp_id

    def verify_rp_id(self, rp_id: str, origin: str) -> None:
        """Verify the RP ID for the given origin."""
        try:
            if self._verify(rp_id, origin):
                return
        except Exception:  # noqa: S110
            pass  # Fall through to ClientError
        raise ClientError.ERR.BAD_REQUEST()

    def get_request_type(self, options) -> str:
        """Get the request type for the given options."""
        if isinstance(options, PublicKeyCredentialCreationOptions):
            return CollectedClientData.TYPE.CREATE
        elif isinstance(options, PublicKeyCredentialRequestOptions):
            return CollectedClientData.TYPE.GET
        else:
            raise ValueError("Invalid options type.")

    def collect_client_data(self, options):
        # Get the effective RP ID from the request options, falling back to the origin
        rp_id = self.get_rp_id(options, self._origin)
        # Validate that the RP ID is valid for the given origin
        self.verify_rp_id(rp_id, self._origin)

        # Construct the client data
        return (
            CollectedClientData.create(
                type=self.get_request_type(options),
                origin=self._origin,
                challenge=options.challenge,
            ),
            rp_id,
        )


def _user_keepalive(user_interaction):
    def on_keepalive(status):
        if status == STATUS.UPNEEDED:  # Waiting for touch
            user_interaction.prompt_up()

    return on_keepalive


class _ClientBackend(abc.ABC):
    info: Info

    @abc.abstractmethod
    def selection(self, event: Event | None) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def do_make_credential(
        self,
        options: PublicKeyCredentialCreationOptions,
        client_data: CollectedClientData,
        rp_id: str,
        enterprise_rpid_list: Sequence[str] | None,
        event: Event,
    ) -> RegistrationResponse:
        raise NotImplementedError()

    @abc.abstractmethod
    def do_get_assertion(
        self,
        options: PublicKeyCredentialRequestOptions,
        client_data: CollectedClientData,
        rp_id: str,
        event: Event,
    ) -> AssertionSelection:
        raise NotImplementedError()


class _Ctap1ClientBackend(_ClientBackend):
    def __init__(self, device: CtapDevice, user_interaction: UserInteraction):
        self.ctap1 = Ctap1(device)
        self.info = Info(versions=["U2F_V2"], extensions=[], aaguid=Aaguid.NONE)
        self._poll_delay = 0.25
        self._on_keepalive = _user_keepalive(user_interaction)

    def selection(self, event):
        _call_polling(
            self._poll_delay,
            event,
            None,
            self.ctap1.register,
            b"\0" * 32,
            b"\0" * 32,
        )

    def do_make_credential(
        self,
        options,
        client_data,
        rp_id,
        enterprise_rpid_list,
        event,
    ):
        key_params = options.pub_key_cred_params
        exclude_list = options.exclude_credentials
        selection = options.authenticator_selection or AuthenticatorSelectionCriteria()
        rk = selection.require_resident_key
        user_verification = selection.user_verification

        if (
            rk
            or user_verification == UserVerificationRequirement.REQUIRED
            or ES256.ALGORITHM not in [p.alg for p in key_params]
            or options.attestation == AttestationConveyancePreference.ENTERPRISE
        ):
            raise CtapError(CtapError.ERR.UNSUPPORTED_OPTION)

        app_param = sha256(rp_id.encode())

        dummy_param = b"\0" * 32
        for cred in exclude_list or []:
            key_handle = cred.id
            try:
                self.ctap1.authenticate(dummy_param, app_param, key_handle, True)
                raise ClientError.ERR.OTHER_ERROR()  # Shouldn't happen
            except ApduError as e:
                if e.code == APDU.USE_NOT_SATISFIED:
                    _call_polling(
                        self._poll_delay,
                        event,
                        self._on_keepalive,
                        self.ctap1.register,
                        dummy_param,
                        dummy_param,
                    )
                    raise ClientError.ERR.DEVICE_INELIGIBLE()

        att_obj = AttestationObject.from_ctap1(
            app_param,
            _call_polling(
                self._poll_delay,
                event,
                self._on_keepalive,
                self.ctap1.register,
                client_data.hash,
                app_param,
            ),
        )
        credential = att_obj.auth_data.credential_data
        assert credential is not None  # noqa: S101

        return RegistrationResponse(
            raw_id=credential.credential_id,
            response=AuthenticatorAttestationResponse(
                client_data=client_data, attestation_object=att_obj
            ),
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            client_extension_results=AuthenticationExtensionsClientOutputs({}),
            type=PublicKeyCredentialType.PUBLIC_KEY,
        )

    def do_get_assertion(
        self,
        options,
        client_data,
        rp_id,
        event,
    ):
        allow_list = options.allow_credentials
        user_verification = options.user_verification

        if user_verification == UserVerificationRequirement.REQUIRED or not allow_list:
            raise CtapError(CtapError.ERR.UNSUPPORTED_OPTION)

        app_param = sha256(rp_id.encode())
        client_param = client_data.hash
        for cred in allow_list:
            try:
                auth_resp = _call_polling(
                    self._poll_delay,
                    event,
                    self._on_keepalive,
                    self.ctap1.authenticate,
                    client_param,
                    app_param,
                    cred.id,
                )
                assertions = [
                    AssertionResponse.from_ctap1(app_param, _as_cbor(cred), auth_resp)
                ]
                return AssertionSelection(client_data, assertions)
            except ClientError as e:
                if e.code == ClientError.ERR.TIMEOUT:
                    raise  # Other errors are ignored so we move to the next.
        raise ClientError.ERR.DEVICE_INELIGIBLE()


class _Ctap2ClientAssertionSelection(AssertionSelection):
    def __init__(
        self,
        client_data: CollectedClientData,
        assertions: Sequence[AssertionResponse],
        extensions: Sequence[AuthenticationExtensionProcessor],
        pin_token: bytes | None,
    ):
        super().__init__(client_data, assertions)
        self._extensions = extensions
        self._pin_token = pin_token

    def _get_extension_results(self, assertion):
        # Process extension outputs
        extension_outputs = {}
        try:
            for ext in self._extensions:
                output = ext.prepare_outputs(assertion, self._pin_token)
                if output:
                    extension_outputs.update(output)
        except ValueError as e:
            raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(e)
        return extension_outputs


@overload
def _cbor_list(values: Sequence) -> list: ...


@overload
def _cbor_list(values: None) -> None: ...


def _cbor_list(values):
    if not values:
        return None
    return [_as_cbor(v) for v in values]


class _Ctap2ClientBackend(_ClientBackend):
    def __init__(
        self,
        device: CtapDevice,
        user_interaction: UserInteraction,
        extensions: Sequence[Ctap2Extension],
    ):
        self.ctap2 = Ctap2(device)
        self.info = self.ctap2.info
        self._extensions = extensions
        self.user_interaction = user_interaction

    def _filter_creds(
        self, rp_id, cred_list, pin_protocol, pin_token, event, on_keepalive
    ):
        # Use fresh info
        info = self.ctap2.get_info()

        # Filter out credential IDs which are too long
        max_len = info.max_cred_id_length
        if max_len:
            cred_list = [c for c in cred_list if len(c.id) <= max_len]

        client_data_hash = b"\0" * 32
        if pin_token:
            pin_auth = pin_protocol.authenticate(pin_token, client_data_hash)
            version = pin_protocol.VERSION
        else:
            pin_auth = None
            version = None

        max_creds = info.max_creds_in_list or 1
        while cred_list:
            chunk = cred_list[:max_creds]
            try:
                assertions = self.ctap2.get_assertions(
                    rp_id,
                    client_data_hash,
                    _cbor_list(chunk),
                    None,
                    {"up": False},
                    pin_auth,
                    version,
                    event=event,
                    on_keepalive=on_keepalive,
                )
                if len(chunk) == 1:
                    # Credential ID might be omitted from assertions
                    return chunk[0]
                else:
                    return PublicKeyCredentialDescriptor(**assertions[0].credential)
            except CtapError as e:
                match e.code:
                    case CtapError.ERR.REQUEST_TOO_LARGE if max_creds > 1:
                        # Message is too large, try smaller chunks
                        max_creds -= 1
                    case CtapError.ERR.NO_CREDENTIALS:
                        # All creds in chunk are discarded
                        cred_list = cred_list[max_creds:]
                    case _:
                        raise

        # No matches found
        return None

    def selection(self, event):
        if "FIDO_2_1" in self.ctap2.info.versions:
            self.ctap2.selection(event=event)
        else:
            # Selection not supported, make dummy credential instead
            try:
                self.ctap2.make_credential(
                    b"\0" * 32,
                    {"id": "example.com", "name": "example.com"},
                    {"id": b"dummy", "name": "dummy"},
                    [{"type": "public-key", "alg": -7}],
                    pin_uv_param=b"",
                    event=event,
                )
            except CtapError as e:
                if e.code in (
                    CtapError.ERR.PIN_NOT_SET,
                    CtapError.ERR.PIN_INVALID,
                    CtapError.ERR.PIN_AUTH_INVALID,
                ):
                    return
                raise

    def _should_use_uv(self, info, user_verification, permissions):
        uv_supported = any(k in info.options for k in ("uv", "clientPin", "bioEnroll"))
        uv_configured = any(
            info.options.get(k) for k in ("uv", "clientPin", "bioEnroll")
        )
        mc = ClientPin.PERMISSION.MAKE_CREDENTIAL & permissions != 0
        additional_perms = permissions & ~(
            ClientPin.PERMISSION.MAKE_CREDENTIAL | ClientPin.PERMISSION.GET_ASSERTION
        )

        if (
            user_verification == UserVerificationRequirement.REQUIRED
            or (
                user_verification in (UserVerificationRequirement.PREFERRED, None)
                and uv_supported
            )
            or info.options.get("alwaysUv")
        ):
            if not uv_configured:
                raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(
                    "User verification not configured/supported"
                )
            return True
        elif mc and uv_configured and not info.options.get("makeCredUvNotRqd"):
            return True
        elif uv_configured and additional_perms:
            return True
        return False

    def _get_token(
        self,
        info,
        client_pin,
        permissions,
        rp_id,
        event,
        on_keepalive,
        allow_internal_uv,
        allow_uv,
    ):
        # Prefer UV
        if allow_uv and info.options.get("uv"):
            if ClientPin.is_token_supported(info):
                if self.user_interaction.request_uv(permissions, rp_id):
                    return client_pin.get_uv_token(
                        permissions, rp_id, event, on_keepalive
                    )
            elif allow_internal_uv:
                if self.user_interaction.request_uv(permissions, rp_id):
                    return None  # No token, use uv=True

        # PIN if UV not supported/allowed.
        if info.options.get("clientPin"):
            pin = self.user_interaction.request_pin(permissions, rp_id)
            if pin:
                return client_pin.get_pin_token(pin, permissions, rp_id)
            raise PinRequiredError()

        # Client PIN not configured.
        raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(
            "User verification not configured"
        )

    def _get_auth_params(
        self,
        pin_protocol,
        rp_id,
        user_verification,
        permissions,
        allow_uv,
        event,
        on_keepalive,
    ):
        info = self.ctap2.get_info()

        pin_token = None
        internal_uv = False
        if self._should_use_uv(info, user_verification, permissions):
            client_pin = ClientPin(self.ctap2, pin_protocol)
            allow_internal_uv = (
                permissions
                & ~(
                    ClientPin.PERMISSION.MAKE_CREDENTIAL
                    | ClientPin.PERMISSION.GET_ASSERTION
                )
                == 0
            )
            pin_token = self._get_token(
                info,
                client_pin,
                permissions,
                rp_id,
                event,
                on_keepalive,
                allow_internal_uv,
                allow_uv,
            )
            if not pin_token:
                internal_uv = True
        return pin_token, internal_uv

    def do_make_credential(
        self,
        options,
        client_data,
        rp_id,
        enterprise_rpid_list,
        event,
    ):
        user = options.user
        key_params = options.pub_key_cred_params
        exclude_list = options.exclude_credentials
        selection = options.authenticator_selection or AuthenticatorSelectionCriteria()
        user_verification = selection.user_verification

        on_keepalive = _user_keepalive(self.user_interaction)
        info = self.ctap2.get_info()

        # Handle enterprise attestation
        enterprise_attestation = None
        if options.attestation == AttestationConveyancePreference.ENTERPRISE:
            if info.options.get("ep"):
                if enterprise_rpid_list is not None:
                    # Platform facilitated
                    if rp_id in enterprise_rpid_list:
                        enterprise_attestation = 2
                else:
                    # Vendor facilitated
                    enterprise_attestation = 1

        # Negotiate PIN/UV protocol version
        for proto in ClientPin.PROTOCOLS:
            if proto.VERSION in info.pin_uv_protocols:
                pin_protocol: PinProtocol | None = proto()
                break
        else:
            pin_protocol = None

        used_extensions: list[RegistrationExtensionProcessor] = []
        allow_uv = True

        def _do_make():
            # Gather UV permissions
            permissions = ClientPin.PERMISSION.MAKE_CREDENTIAL
            if exclude_list:
                # We need this for filtering the exclude_list
                permissions |= ClientPin.PERMISSION.GET_ASSERTION

            # Initialize extensions and add extension permissions
            used_extensions.clear()
            for e in self._extensions:
                ext = e.make_credential(self.ctap2, options, pin_protocol)
                if ext:
                    used_extensions.append(ext)
                    permissions |= ext.permissions

            # Handle auth
            pin_token, internal_uv = self._get_auth_params(
                pin_protocol,
                rp_id,
                user_verification,
                permissions,
                allow_uv,
                event,
                on_keepalive,
            )

            if exclude_list:
                exclude_cred = self._filter_creds(
                    rp_id, exclude_list, pin_protocol, pin_token, event, on_keepalive
                )
                # We know the request will fail if exclude_cred is not None here
                # BUT DO NOT FAIL EARLY! We still need to prompt for UP, so we keep
                # processing the request
            else:
                exclude_cred = None

            # Process extensions
            extension_inputs = {}
            try:
                for ext in used_extensions:
                    auth_input = ext.prepare_inputs(pin_token)
                    if auth_input:
                        extension_inputs.update(auth_input)
            except ValueError as e:
                raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(e)

            can_rk = info.options.get("rk")
            rk = selection.resident_key == ResidentKeyRequirement.REQUIRED or (
                selection.resident_key == ResidentKeyRequirement.PREFERRED and can_rk
            )

            if not (rk or internal_uv):
                opts = None
            else:
                opts = {}
                if rk:
                    if not can_rk:
                        raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(
                            "Resident key not supported"
                        )
                    opts["rk"] = True
                if internal_uv:
                    opts["uv"] = True

            # Calculate pin_auth
            client_data_hash = client_data.hash
            if pin_protocol and pin_token:
                pin_auth: tuple[bytes | None, int | None] = (
                    pin_protocol.authenticate(pin_token, client_data_hash),
                    pin_protocol.VERSION,
                )
            else:
                pin_auth = (None, None)

            # Perform make credential
            return (
                self.ctap2.make_credential(
                    client_data_hash,
                    _as_cbor(replace(options.rp, id=rp_id)),
                    _as_cbor(user),
                    _cbor_list(key_params),
                    [_as_cbor(exclude_cred)] if exclude_cred else None,
                    extension_inputs or None,
                    opts,
                    *pin_auth,
                    enterprise_attestation,
                    event=event,
                    on_keepalive=on_keepalive,
                ),
                pin_token,
            )

        dev = self.ctap2.device
        reconnected = False
        while True:
            try:
                att_resp, pin_token = _do_make()
                break
            except CtapError as e:
                # The Authenticator may still require UV, try again
                if (
                    e.code == CtapError.ERR.PUAT_REQUIRED
                    and user_verification == UserVerificationRequirement.DISCOURAGED
                ):
                    user_verification = UserVerificationRequirement.REQUIRED
                    continue
                # UV may be blocked, try again (once) with PIN
                if e.code == CtapError.ERR.UV_BLOCKED and allow_uv:
                    allow_uv = False
                    continue
                # NFC may require reconnect
                connect = getattr(dev, "connect", None)
                if (
                    e.code == CtapError.ERR.PIN_AUTH_BLOCKED
                    and connect
                    and not reconnected
                ):
                    dev.close()
                    connect()
                    reconnected = True  # We only want to try this once
                    continue
                raise

        # Process extension outputs
        extension_outputs = {}
        try:
            for ext in used_extensions:
                output = ext.prepare_outputs(att_resp, pin_token)
                if output is not None:
                    extension_outputs.update(output)
        except ValueError as e:
            raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(e)

        att_obj = AttestationObject.create(
            att_resp.fmt, att_resp.auth_data, att_resp.att_stmt
        )

        credential = att_obj.auth_data.credential_data
        assert credential is not None  # noqa: S101

        return RegistrationResponse(
            raw_id=credential.credential_id,
            response=AuthenticatorAttestationResponse(
                client_data=client_data, attestation_object=att_obj
            ),
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            client_extension_results=AuthenticationExtensionsClientOutputs(
                extension_outputs
            ),
            type=PublicKeyCredentialType.PUBLIC_KEY,
        )

    def do_get_assertion(
        self,
        options,
        client_data,
        rp_id,
        event,
    ):
        rp_id = options.rp_id
        allow_list = options.allow_credentials
        user_verification = options.user_verification

        on_keepalive = _user_keepalive(self.user_interaction)

        # Negotiate PIN/UV protocol version
        for proto in ClientPin.PROTOCOLS:
            if proto.VERSION in self.info.pin_uv_protocols:
                pin_protocol: PinProtocol | None = proto()
                break
        else:
            pin_protocol = None

        allow_uv = True

        def _do_auth():
            # Gather UV permissions
            permissions = ClientPin.PERMISSION.GET_ASSERTION

            # Initialize extensions and add extension permissions
            used_extensions = []
            for e in self._extensions:
                ext = e.get_assertion(self.ctap2, options, pin_protocol)
                if ext:
                    used_extensions.append(ext)
                    permissions |= ext.permissions

            # Handle auth
            pin_token, internal_uv = self._get_auth_params(
                pin_protocol,
                rp_id,
                user_verification,
                permissions,
                allow_uv,
                event,
                on_keepalive,
            )

            if allow_list:
                selected_cred = self._filter_creds(
                    rp_id, allow_list, pin_protocol, pin_token, event, on_keepalive
                )
                # We know the request will fail if selected_cred is None here
                # BUT DO NOT FAIL EARLY! We still need to prompt for UP, so we keep
                # processing the request
            else:
                selected_cred = None

            # Process extensions
            extension_inputs = {}
            try:
                for ext in used_extensions:
                    inputs = ext.prepare_inputs(selected_cred, pin_token)
                    if inputs:
                        extension_inputs.update(inputs)
            except ValueError as e:
                raise ClientError.ERR.CONFIGURATION_UNSUPPORTED(e)

            opts = {"uv": True} if internal_uv else None

            # Calculate pin_auth
            client_data_hash = client_data.hash
            if pin_protocol and pin_token:
                pin_auth: tuple[bytes | None, int | None] = (
                    pin_protocol.authenticate(pin_token, client_data_hash),
                    pin_protocol.VERSION,
                )
            else:
                pin_auth = (None, None)

            if allow_list and not selected_cred:
                # We still need to send a dummy value if there was an allow_list
                # but no matches were found:
                selected_cred = PublicKeyCredentialDescriptor(
                    type=allow_list[0].type, id=b"\0"
                )

            # Perform get assertion
            assertions = self.ctap2.get_assertions(
                rp_id,
                client_data_hash,
                [_as_cbor(selected_cred)] if selected_cred else None,
                extension_inputs or None,
                opts,
                *pin_auth,
                event=event,
                on_keepalive=on_keepalive,
            )

            return _Ctap2ClientAssertionSelection(
                client_data, assertions, used_extensions, pin_token
            )

        dev = self.ctap2.device
        reconnected = False
        while True:
            try:
                return _do_auth()
            except CtapError as e:
                # The Authenticator may still require UV, try again
                if (
                    e.code == CtapError.ERR.PUAT_REQUIRED
                    and user_verification == UserVerificationRequirement.DISCOURAGED
                ):
                    user_verification = UserVerificationRequirement.REQUIRED
                    continue
                # UV may be blocked, try again (once) with PIN
                if e.code == CtapError.ERR.UV_BLOCKED and allow_uv:
                    allow_uv = False
                    continue
                # NFC may require reconnect
                connect = getattr(dev, "connect", None)
                if (
                    e.code == CtapError.ERR.PIN_AUTH_BLOCKED
                    and connect
                    and not reconnected
                ):
                    dev.close()
                    connect()
                    reconnected = True  # We only want to try this once
                    continue
                raise


class Fido2Client(WebAuthnClient):
    """WebAuthn-like client implementation.

    The client allows registration and authentication of WebAuthn credentials against
    an Authenticator using CTAP (1 or 2).

    :param device: CtapDevice to use.
    :param str origin: The origin to use.
    :param verify: Function to verify an RP ID for a given origin.
    """

    def __init__(
        self,
        device: CtapDevice,
        client_data_collector: ClientDataCollector,
        user_interaction: UserInteraction = UserInteraction(),
        extensions: Sequence[Ctap2Extension] = _DEFAULT_EXTENSIONS,
    ):
        self._client_data_collector = client_data_collector

        # TODO: Decide how to configure this list.
        self._enterprise_rpid_list: Sequence[str] | None = None

        try:
            self._backend: _ClientBackend = _Ctap2ClientBackend(
                device, user_interaction, extensions
            )
        except (ValueError, CtapError):
            self._backend = _Ctap1ClientBackend(device, user_interaction)

    @property
    def info(self) -> Info:
        return self._backend.info

    def selection(self, event: Event | None = None) -> None:
        try:
            self._backend.selection(event)
        except CtapError as e:
            raise _ctap2client_err(e)

    def make_credential(
        self,
        options: PublicKeyCredentialCreationOptions,
        event: Event | None = None,
    ) -> RegistrationResponse:
        """Creates a credential.

        :param options: PublicKeyCredentialCreationOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """

        options = PublicKeyCredentialCreationOptions.from_dict(options)
        event = event or Event()
        if options.timeout:
            timer = Timer(options.timeout / 1000, event.set)
            timer.daemon = True
            timer.start()
        else:
            timer = None

        # Gather client data, RP ID from client
        client_data, rp_id = self._client_data_collector.collect_client_data(options)
        logger.debug(f"Register a new credential for RP ID: {rp_id}")

        try:
            return self._backend.do_make_credential(
                options,
                client_data,
                rp_id,
                self._enterprise_rpid_list,
                event,
            )
        except CtapError as e:
            raise _ctap2client_err(e)
        finally:
            if timer:
                timer.cancel()

    def get_assertion(
        self,
        options: PublicKeyCredentialRequestOptions,
        event: Event | None = None,
    ) -> AssertionSelection:
        """Get an assertion.

        :param options: PublicKeyCredentialRequestOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """

        options = PublicKeyCredentialRequestOptions.from_dict(options)
        event = event or Event()
        if options.timeout:
            timer = Timer(options.timeout / 1000, event.set)
            timer.daemon = True
            timer.start()
        else:
            timer = None

        # Gather client data, RP ID from client
        client_data, rp_id = self._client_data_collector.collect_client_data(options)
        logger.debug(f"Assert a credential for RP ID: {rp_id}")

        try:
            return self._backend.do_get_assertion(
                options,
                client_data,
                rp_id,
                event,
            )
        except CtapError as e:
            raise _ctap2client_err(e)
        finally:
            if timer:
                timer.cancel()
```

## File: fido2/client/win_api.py
```python
# Copyright (c) 2019 Onica Group LLC.
# Modified work Copyright 2019 Yubico.
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Structs based on Microsoft's WebAuthN API.
https://github.com/microsoft/webauthn

Definitions taken from https://github.com/microsoft/webauthn/blob/master/webauthn.h
"""

# With the ctypes.Structure a lot of the property names
# will be invalid, and when creating the __init__ methods
# we do not need to call super() for the Structure class
#
# pylint: disable=invalid-name, super-init-not-called, too-few-public-methods

from __future__ import annotations

import ctypes
from ctypes import LibraryLoader, WinDLL  # type: ignore
from ctypes.wintypes import BOOL, DWORD, HWND, LONG, LPCWSTR, WORD
from enum import IntEnum, unique
from typing import Any, Mapping, Sequence

# Not implemented: Platform credentials support, listing of built-in authenticators


windll = LibraryLoader(WinDLL)


PBYTE = ctypes.POINTER(ctypes.c_ubyte)  # Different from wintypes.PBYTE, which is signed
PCWSTR = ctypes.c_wchar_p
PVOID = ctypes.c_void_p


class BytesProperty:
    """Property for structs storing byte arrays as DWORD + PBYTE.

    Allows for easy reading/writing to struct fields using Python bytes objects.
    """

    def __init__(self, name: str):
        self.cbName = "cb" + name
        self.pbName = "pb" + name

    def __get__(self, instance, owner):
        return bytes(
            bytearray(getattr(instance, self.pbName)[: getattr(instance, self.cbName)])
        )

    def __set__(self, instance, value: bytes | None):
        ln = len(value) if value else 0
        buffer = ctypes.create_string_buffer(value) if value else 0
        setattr(instance, self.cbName, ln)
        setattr(instance, self.pbName, ctypes.cast(buffer, PBYTE))


class GUID(ctypes.Structure):
    """GUID Type in C++."""

    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]

    def __str__(self):
        return "{%08X-%04X-%04X-%04X-%012X}" % (
            self.Data1,
            self.Data2,
            self.Data3,
            self.Data4[0] * 256 + self.Data4[1],
            self.Data4[2] * (256**5)
            + self.Data4[3] * (256**4)
            + self.Data4[4] * (256**3)
            + self.Data4[5] * (256**2)
            + self.Data4[6] * 256
            + self.Data4[7],
        )


class _FromString:
    @classmethod
    def from_string(cls, value: str):
        return getattr(cls, value.upper().replace("-", "_"))


@unique
class WebAuthNUserVerificationRequirement(_FromString, IntEnum):
    """Maps to WEBAUTHN_USER_VERIFICATION_REQUIREMENT_*."""

    ANY = 0
    REQUIRED = 1
    PREFERRED = 2
    DISCOURAGED = 3


@unique
class WebAuthNAttestationConveyancePreference(_FromString, IntEnum):
    """Maps to WEBAUTHN_ATTESTATION_CONVEYANCE_PREFERENCE_*."""

    ANY = 0
    NONE = 1
    INDIRECT = 2
    DIRECT = 3


@unique
class WebAuthNAuthenticatorAttachment(_FromString, IntEnum):
    """Maps to WEBAUTHN_AUTHENTICATOR_ATTACHMENT_*."""

    ANY = 0
    PLATFORM = 1
    CROSS_PLATFORM = 2
    CROSS_PLATFORM_U2F_V2 = 3


@unique
class WebAuthNCTAPTransport(_FromString, IntEnum):
    """Maps to WEBAUTHN_CTAP_TRANSPORT_*."""

    ANY = 0x00000000
    USB = 0x00000001
    NFC = 0x00000002
    BLE = 0x00000004
    TEST = 0x00000008
    INTERNAL = 0x00000010
    HYBRID = 0x00000020
    SMART_CARD = 0x00000040
    FLAGS_MASK = 0x0000007F


@unique
class WebAuthNEnterpriseAttestation(_FromString, IntEnum):
    """Maps to WEBAUTHN_ENTERPRISE_ATTESTATION_*."""

    NONE = 0
    VENDOR_FACILITATED = 1
    PLATFORM_MANAGED = 2


@unique
class WebAuthNLargeBlobSupport(_FromString, IntEnum):
    """Maps to WEBAUTHN_LARGE_BLOB_SUPPORT_*."""

    NONE = 0
    REQUIRED = 1
    PREFERRED = 2


@unique
class WebAuthNLargeBlobOperation(_FromString, IntEnum):
    """Maps to WEBAUTHN_LARGE_BLOB_OPERATION_*."""

    NONE = 0
    GET = 1
    SET = 2
    DELETE = 3


@unique
class WebAuthNUserVerification(_FromString, IntEnum):
    """Maps to WEBAUTHN_USER_VERIFICATION_*."""

    ANY = 0
    OPTIONAL = 1
    OPTIONAL_WITH_CREDENTIAL_ID_LIST = 2
    REQUIRED = 3


class WebAuthNCoseCredentialParameter(ctypes.Structure):
    """Maps to WEBAUTHN_COSE_CREDENTIAL_PARAMETER Struct.

    :param cred_params: Dict of Credential parameters.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("pwszCredentialType", LPCWSTR),
        ("lAlg", LONG),
    ]

    def __init__(self, cred_params: Mapping[str, Any]):
        self.dwVersion = get_version(self.__class__.__name__)
        self.pwszCredentialType = cred_params["type"]
        self.lAlg = cred_params["alg"]


class WebAuthNCoseCredentialParameters(ctypes.Structure):
    """Maps to WEBAUTHN_COSE_CREDENTIAL_PARAMETERS Struct.

    :param params: List of Credential parameter dicts.
    """

    _fields_ = [
        ("cCredentialParameters", DWORD),
        ("pCredentialParameters", ctypes.POINTER(WebAuthNCoseCredentialParameter)),
    ]

    def __init__(self, params: Sequence[Mapping[str, Any]]):
        self.cCredentialParameters = len(params)
        self.pCredentialParameters = (WebAuthNCoseCredentialParameter * len(params))(
            *(WebAuthNCoseCredentialParameter(param) for param in params)
        )


class WebAuthNClientData(ctypes.Structure):
    """Maps to WEBAUTHN_CLIENT_DATA Struct.

    :param client_data_json: ClientData serialized as JSON bytes.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbClientDataJSON", DWORD),
        ("pbClientDataJSON", PBYTE),
        ("pwszHashAlgId", LPCWSTR),
    ]

    client_data_json = BytesProperty("ClientDataJSON")

    def __init__(self, client_data_json: bytes):
        self.dwVersion = get_version(self.__class__.__name__)
        self.client_data_json = client_data_json
        self.pwszHashAlgId = "SHA-256"


class WebAuthNRpEntityInformation(ctypes.Structure):
    """Maps to WEBAUTHN_RP_ENTITY_INFORMATION Struct.

    :param rp: Dict of RP information.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("pwszId", PCWSTR),
        ("pwszName", PCWSTR),
        ("pwszIcon", PCWSTR),
    ]

    def __init__(self, rp: Mapping[str, Any]):
        self.dwVersion = get_version(self.__class__.__name__)
        self.pwszId = rp["id"]
        self.pwszName = rp["name"]
        self.pwszIcon = rp.get("icon")


class WebAuthNUserEntityInformation(ctypes.Structure):
    """Maps to WEBAUTHN_USER_ENTITY_INFORMATION Struct.

    :param user: Dict of User information.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbId", DWORD),
        ("pbId", PBYTE),
        ("pwszName", PCWSTR),
        ("pwszIcon", PCWSTR),
        ("pwszDisplayName", PCWSTR),
    ]

    id = BytesProperty("Id")

    def __init__(self, user: Mapping[str, Any]):
        self.dwVersion = get_version(self.__class__.__name__)
        self.id = user["id"]
        self.pwszName = user["name"]
        self.pwszIcon = user.get("icon")
        self.pwszDisplayName = user.get("displayName")


class WebAuthNCredentialEx(ctypes.Structure):
    """Maps to WEBAUTHN_CREDENTIAL_EX Struct.

    :param cred: Dict of Credential Descriptor data.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbId", DWORD),
        ("pbId", PBYTE),
        ("pwszCredentialType", LPCWSTR),
        ("dwTransports", DWORD),
    ]

    id = BytesProperty("Id")

    def __init__(self, cred: Mapping[str, Any]):
        self.dwVersion = get_version(self.__class__.__name__)
        self.id = cred["id"]
        self.pwszCredentialType = cred["type"]
        self.dwTransports = WebAuthNCTAPTransport[cred.get("transport", "ANY")]


class WebAuthNCredentialList(ctypes.Structure):
    """Maps to WEBAUTHN_CREDENTIAL_LIST Struct.

    :param credentials: List of dict of Credential Descriptor data.
    """

    _fields_ = [
        ("cCredentials", DWORD),
        ("ppCredentials", ctypes.POINTER(ctypes.POINTER(WebAuthNCredentialEx))),
    ]

    def __init__(self, credentials: Sequence[Mapping[str, Any]]):
        self.cCredentials = len(credentials)
        self.ppCredentials = (ctypes.POINTER(WebAuthNCredentialEx) * len(credentials))(
            *(ctypes.pointer(WebAuthNCredentialEx(cred)) for cred in credentials)
        )


class WebAuthNHmacSecretSalt(ctypes.Structure):
    _fields_ = [
        ("cbFirst", DWORD),
        ("pbFirst", PBYTE),
        ("cbSecond", DWORD),
        ("pbSecond", PBYTE),
    ]

    first = BytesProperty("First")
    second = BytesProperty("Second")

    def __init__(self, first: bytes, second: bytes | None = None):
        self.first = first
        self.second = second


class WebAuthNCredWithHmacSecretSalt(ctypes.Structure):
    _fields_ = [
        ("cbCredID", DWORD),
        ("pbCredID", PBYTE),
        ("pHmacSecretSalt", ctypes.POINTER(WebAuthNHmacSecretSalt)),
    ]

    cred_id = BytesProperty("CredID")

    def __init__(self, cred_id: bytes, salt: WebAuthNHmacSecretSalt):
        self.cred_id = cred_id
        self.pHmacSecretSalt = ctypes.pointer(salt)


class WebAuthNHmacSecretSaltValues(ctypes.Structure):
    _fields_ = [
        ("pGlobalHmacSalt", ctypes.POINTER(WebAuthNHmacSecretSalt)),
        ("cCredWithHmacSecretSaltList", DWORD),
        ("pCredWithHmacSecretSaltList", ctypes.POINTER(WebAuthNCredWithHmacSecretSalt)),
    ]

    def __init__(
        self,
        global_salt: WebAuthNHmacSecretSalt | None,
        credential_salts: Sequence[WebAuthNCredWithHmacSecretSalt] = [],
    ):
        if global_salt:
            self.pGlobalHmacSalt = ctypes.pointer(global_salt)

        self.cCredWithHmacSecretSaltList = len(credential_salts)
        self.pCredWithHmacSecretSaltList = (
            WebAuthNCredWithHmacSecretSalt * len(credential_salts)
        )(*credential_salts)


class WebAuthNCredProtectExtensionIn(ctypes.Structure):
    """Maps to WEBAUTHN_CRED_PROTECT_EXTENSION_IN Struct."""

    _fields_ = [
        ("dwCredProtect", DWORD),
        ("bRequireCredProtect", BOOL),
    ]

    def __init__(
        self, cred_protect: WebAuthNUserVerification, require_cred_protect: bool
    ):
        self.dwCredProtect = cred_protect
        self.bRequireCredProtect = require_cred_protect


class WebAuthNCredBlobExtension(ctypes.Structure):
    _fields_ = [
        ("cbCredBlob", DWORD),
        ("pbCredBlob", PBYTE),
    ]

    cred_blob = BytesProperty("CredBlob")

    def __init__(self, blob: bytes):
        self.cred_blob = blob


class WebAuthNExtension(ctypes.Structure):
    """Maps to WEBAUTHN_EXTENSION Struct."""

    _fields_ = [
        ("pwszExtensionIdentifier", LPCWSTR),
        ("cbExtension", DWORD),
        ("pvExtension", PVOID),
    ]

    def __init__(self, identifier: str, value: Any):
        self.pwszExtensionIdentifier = identifier
        self.cbExtension = ctypes.sizeof(value)
        self.pvExtension = ctypes.cast(ctypes.pointer(value), PVOID)


class WebAuthNExtensions(ctypes.Structure):
    """Maps to WEBAUTHN_EXTENSIONS Struct."""

    _fields_ = [
        ("cExtensions", DWORD),
        ("pExtensions", ctypes.POINTER(WebAuthNExtension)),
    ]

    def __init__(self, extensions: Sequence[WebAuthNExtension]):
        self.cExtensions = len(extensions)
        self.pExtensions = (WebAuthNExtension * len(extensions))(*extensions)


class WebAuthNCredential(ctypes.Structure):
    """Maps to WEBAUTHN_CREDENTIAL Struct.

    :param cred: Dict of Credential Descriptor data.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbId", DWORD),
        ("pbId", PBYTE),
        ("pwszCredentialType", LPCWSTR),
    ]

    id = BytesProperty("Id")

    def __init__(self, cred: Mapping[str, Any]):
        self.id = cred["id"]
        self.pwszCredentialType = cred["type"]


class WebAuthNCredentials(ctypes.Structure):
    """Maps to WEBAUTHN_CREDENTIALS Struct.

    :param credentials: List of dict of Credential Descriptor data.
    """

    _fields_ = [
        ("cCredentials", DWORD),
        ("pCredentials", ctypes.POINTER(WebAuthNCredential)),
    ]

    def __init__(self, credentials: Sequence[Mapping[str, Any]]):
        self.cCredentials = len(credentials)
        self.pCredentials = (WebAuthNCredential * len(credentials))(
            *(WebAuthNCredential(cred) for cred in credentials)
        )


class CtapCborHybridStorageLinkedData(ctypes.Structure):
    """Maps to CTAPCBOR_HYBRID_STORAGE_LINKED_DATA Struct."""

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbContactId", DWORD),
        ("pbContactId", PBYTE),
        ("cbLinkId", DWORD),
        ("pbLinkId", PBYTE),
        ("cbLinkSecret", DWORD),
        ("pbLinkSecret", PBYTE),
        ("cbPublicKey", DWORD),
        ("pbPublicKey", PBYTE),
        ("pwszAuthenticatorName", PCWSTR),
        ("wEncodedTunnelServerDomain", WORD),
    ]  # TODO

    contact_id = BytesProperty("ContactId")
    link_id = BytesProperty("LinkId")
    link_secret = BytesProperty("LinkSecret")
    public_key = BytesProperty("PublicKey")


class WebAuthNGetAssertionOptions(ctypes.Structure):
    """Maps to WEBAUTHN_AUTHENTICATOR_GET_ASSERTION_OPTIONS Struct.

    :param timeout: Time that the operation is expected to complete within.
        This is used as guidance, and can be overridden by the platform.
    :param attachment: Platform vs Cross-Platform
        Authenticators.
    :param uv_requirement: User Verification Requirement.
    :param credentials: Allowed Credentials List.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("dwTimeoutMilliseconds", DWORD),
        ("CredentialList", WebAuthNCredentials),
        ("Extensions", WebAuthNExtensions),
        ("dwAuthenticatorAttachment", DWORD),
        ("dwUserVerificationRequirement", DWORD),
        ("dwFlags", DWORD),
        # Version 2 additions
        ("pwszU2fAppId", PCWSTR),
        ("pbU2fAppId", ctypes.POINTER(BOOL)),
        # Version 3 additions
        ("pCancellationId", ctypes.POINTER(GUID)),
        # Version 4 additions
        ("pAllowCredentialList", ctypes.POINTER(WebAuthNCredentialList)),
        # Version 5 additions
        ("dwCredLargeBlobOperation", DWORD),
        ("cbCredLargeBlob", DWORD),
        ("pbCredLargeBlob", PBYTE),
        # Version 6 additions
        ("pHmacSecretSaltValues", ctypes.POINTER(WebAuthNHmacSecretSaltValues)),
        ("bBrowserInPrivateMode", BOOL),
        # Version 7 additions
        ("pLinkedDevice", ctypes.POINTER(CtapCborHybridStorageLinkedData)),
        ("bAutoFill", BOOL),
        ("cbJsonExt", DWORD),
        ("pbJsonExt", PBYTE),
        # Version 8 additions
        ("cCredentialHints", DWORD),
        ("ppwszCredentialHints", ctypes.POINTER(PCWSTR)),
        # Version 9 additions
        ("pwszRemoteWebOrigin", PCWSTR),
        ("cbPublicKeyCredentialRequestOptionsJSON", DWORD),
        ("pbPublicKeyCredentialRequestOptionsJSON", PBYTE),
        ("cbAuthenticatorId", DWORD),
        ("pbAuthenticatorId", PBYTE),
    ]

    cred_large_blob = BytesProperty("CredLargeBlob")
    json_ext = BytesProperty("JsonExt")
    public_key_credential_request_options_json = BytesProperty(
        "PublicKeyCredentialRequestOptionsJSON"
    )
    authenticator_id = BytesProperty("AuthenticatorId")

    def __init__(
        self,
        timeout: int = 0,
        attachment: int = WebAuthNAuthenticatorAttachment.ANY,
        uv_requirement: int = WebAuthNUserVerificationRequirement.DISCOURAGED,
        credentials: Sequence[Mapping[str, Any]] = [],
        cancellationId: GUID | None = None,
        cred_large_blob_operation: int = WebAuthNLargeBlobOperation.NONE,
        cred_large_blob: bytes | None = None,
        hmac_secret_salts: WebAuthNHmacSecretSaltValues | None = None,
        extensions: Sequence[WebAuthNExtension] = [],
        flags: int = 0,
        u2f_appid: str | None = None,
        u2f_appid_used: BOOL | None = None,
        credential_hints: Sequence[str] | None = None,
        remote_web_origin: str | None = None,
        public_key_credential_request_options_json: bytes | None = None,
        authenticator_id: bytes | None = None,
    ):
        self.dwVersion = get_version(self.__class__.__name__)
        self.dwTimeoutMilliseconds = timeout
        self.dwAuthenticatorAttachment = attachment
        self.dwUserVerificationRequirement = uv_requirement
        self.dwFlags = flags

        if extensions:
            self.Extensions = WebAuthNExtensions(extensions)

        if self.dwVersion >= 2:
            self.pwszU2fAppId = u2f_appid
            if u2f_appid_used is not None:
                self.pbU2fAppId = ctypes.pointer(u2f_appid_used)

        if self.dwVersion >= 3 and cancellationId:
            self.pCancellationId = ctypes.pointer(cancellationId)

        if self.dwVersion >= 4:
            clist = WebAuthNCredentialList(credentials)
            self.pAllowCredentialList = ctypes.pointer(clist)
        else:
            self.CredentialList = WebAuthNCredentials(credentials)

        if self.dwVersion >= 5:
            self.dwCredLargeBlobOperation = cred_large_blob_operation
            self.cred_large_blob = cred_large_blob

        if self.dwVersion >= 6 and hmac_secret_salts:
            self.pHmacSecretSaltValues = ctypes.pointer(hmac_secret_salts)

        if self.dwVersion >= 8 and credential_hints:
            self.cCredentialHints = len(credential_hints)
            # Keep array alive by storing on instance
            self._credential_hints_array = (PCWSTR * len(credential_hints))(
                *credential_hints
            )
            self.ppwszCredentialHints = self._credential_hints_array

        if self.dwVersion >= 9:
            self.pwszRemoteWebOrigin = remote_web_origin
            self.public_key_credential_request_options_json = (
                public_key_credential_request_options_json
            )
            self.authenticator_id = authenticator_id


class WebAuthNAssertion(ctypes.Structure):
    """Maps to WEBAUTHN_ASSERTION Struct."""

    _fields_ = [
        ("dwVersion", DWORD),
        ("cbAuthenticatorData", DWORD),
        ("pbAuthenticatorData", PBYTE),
        ("cbSignature", DWORD),
        ("pbSignature", PBYTE),
        ("Credential", WebAuthNCredential),
        ("cbUserId", DWORD),
        ("pbUserId", PBYTE),
        # Version 2 additions
        ("Extensions", WebAuthNExtensions),
        ("cbCredLargeBlob", DWORD),
        ("pbCredLargeBlob", PBYTE),
        ("dwCredLargeBlobStatus", DWORD),
        # Version 3 additions
        ("pHmacSecret", ctypes.POINTER(WebAuthNHmacSecretSalt)),
        # Version 4 additions
        ("dwUsedTransports", DWORD),
        # Version 5 additions
        ("cbUnsignedExtensionOutputs", DWORD),
        ("pbUnsignedExtensionOutputs", PBYTE),
        # Version 6 additions
        ("cbClientDataJSON", DWORD),
        ("pbClientDataJSON", PBYTE),
        ("cbAuthenticationResponseJSON", DWORD),
        ("pbAuthenticationResponseJSON", PBYTE),
    ]

    auth_data = BytesProperty("AuthenticatorData")
    signature = BytesProperty("Signature")
    user_id = BytesProperty("UserId")
    cred_large_blob = BytesProperty("CredLargeBlob")
    unsigned_extension_outputs = BytesProperty("UnsignedExtensionOutputs")
    client_data_json = BytesProperty("ClientDataJSON")
    authentication_response_json = BytesProperty("AuthenticationResponseJSON")

    def __del__(self):
        WEBAUTHN.WebAuthNFreeAssertion(ctypes.byref(self))


class WebAuthNMakeCredentialOptions(ctypes.Structure):
    """maps to WEBAUTHN_AUTHENTICATOR_MAKE_CREDENTIAL_OPTIONS Struct.

    :param timeout: Time that the operation is expected to complete within.This
        is used as guidance, and can be overridden by the platform.
    :param require_resident_key: Require key to be resident or not.
    :param attachment: Platform vs Cross-Platform
        Authenticators.
    :param user_verification_requirement: User
        Verification Requirement.
    :param attestation_convoyence:
        Attestation Conveyance Preference.
    :param credentials: Credentials used for exclusion.
    """

    _fields_ = [
        ("dwVersion", DWORD),
        ("dwTimeoutMilliseconds", DWORD),
        ("CredentialList", WebAuthNCredentials),
        ("Extensions", WebAuthNExtensions),
        ("dwAuthenticatorAttachment", DWORD),
        ("bRequireResidentKey", BOOL),
        ("dwUserVerificationRequirement", DWORD),
        ("dwAttestationConveyancePreference", DWORD),
        ("dwFlags", DWORD),
        # Version 2 additions
        ("pCancellationId", ctypes.POINTER(GUID)),
        # Version 3 additions
        ("pExcludeCredentialList", ctypes.POINTER(WebAuthNCredentialList)),
        # Version 4 additions
        ("dwEnterpriseAttestation", DWORD),
        ("dwLargeBlobSupport", DWORD),
        ("bPreferResidentKey", BOOL),
        # Version 5 additions
        ("bBrowserInPrivateMode", BOOL),
        # Version 6 additions
        ("bEnablePrf", BOOL),
        # Version 7 additions
        ("pLinkedDevice", ctypes.POINTER(CtapCborHybridStorageLinkedData)),
        ("cbJsonExt", DWORD),
        ("pbJsonExt", PBYTE),
        # Version 8 additions
        ("pPRFGlobalEval", ctypes.POINTER(WebAuthNHmacSecretSalt)),
        ("cCredentialHints", DWORD),
        ("ppwszCredentialHints", ctypes.POINTER(PCWSTR)),
        ("bThirdPartyPayment", BOOL),
        # Version 9 additions
        ("pwszRemoteWebOrigin", PCWSTR),
        ("cbPublicKeyCredentialCreationOptionsJSON", DWORD),
        ("pbPublicKeyCredentialCreationOptionsJSON", PBYTE),
        ("cbAuthenticatorId", DWORD),
        ("pbAuthenticatorId", PBYTE),
    ]

    json_ext = BytesProperty("JsonExt")
    public_key_credential_creation_options_json = BytesProperty(
        "PublicKeyCredentialCreationOptionsJSON"
    )
    authenticator_id = BytesProperty("AuthenticatorId")

    def __init__(
        self,
        timeout: int = 0,
        require_resident_key: bool = False,
        attachment: int = WebAuthNAuthenticatorAttachment.ANY,
        uv_requirement: int = WebAuthNUserVerificationRequirement.DISCOURAGED,
        attestation_convoyence: int = WebAuthNAttestationConveyancePreference.ANY,
        credentials: Sequence[Mapping[str, Any]] = [],
        cancellationId: GUID | None = None,
        enterprise_attestation: int = WebAuthNEnterpriseAttestation.NONE,
        large_blob_support: int = WebAuthNLargeBlobSupport.NONE,
        prefer_resident_key: bool = False,
        enable_prf: bool = False,
        extensions: Sequence[WebAuthNExtension] = [],
        prf_global_eval: WebAuthNHmacSecretSalt | None = None,
        credential_hints: Sequence[str] | None = None,
        third_party_payment: bool = False,
        remote_web_origin: str | None = None,
        public_key_credential_creation_options_json: bytes | None = None,
        authenticator_id: bytes | None = None,
    ):
        self.dwVersion = get_version(self.__class__.__name__)
        self.dwTimeoutMilliseconds = timeout
        self.bRequireResidentKey = require_resident_key
        self.dwAuthenticatorAttachment = attachment
        self.dwUserVerificationRequirement = uv_requirement
        self.dwAttestationConveyancePreference = attestation_convoyence

        if extensions:
            self.Extensions = WebAuthNExtensions(extensions)

        if self.dwVersion >= 2 and cancellationId:
            self.pCancellationId = ctypes.pointer(cancellationId)

        if self.dwVersion >= 3:
            self.pExcludeCredentialList = ctypes.pointer(
                WebAuthNCredentialList(credentials)
            )
        else:
            self.CredentialList = WebAuthNCredentials(credentials)

        if self.dwVersion >= 4:
            self.dwEnterpriseAttestation = enterprise_attestation
            self.dwLargeBlobSupport = large_blob_support
            self.bPreferResidentKey = prefer_resident_key

        if self.dwVersion >= 6:
            self.bEnablePrf = enable_prf

        if self.dwVersion >= 8:
            if prf_global_eval is not None:
                self.pPRFGlobalEval = ctypes.pointer(prf_global_eval)
            if credential_hints:
                self.cCredentialHints = len(credential_hints)
                self._credential_hints_array = (PCWSTR * len(credential_hints))(
                    *credential_hints
                )
                self.ppwszCredentialHints = self._credential_hints_array
            self.bThirdPartyPayment = third_party_payment

        if self.dwVersion >= 9:
            self.pwszRemoteWebOrigin = remote_web_origin
            self.public_key_credential_creation_options_json = (
                public_key_credential_creation_options_json
            )
            self.authenticator_id = authenticator_id


class WebAuthNCredentialAttestation(ctypes.Structure):
    """Maps to WEBAUTHN_CREDENTIAL_ATTESTATION Struct."""

    _fields_ = [
        ("dwVersion", DWORD),
        ("pwszFormatType", LPCWSTR),
        ("cbAuthenticatorData", DWORD),
        ("pbAuthenticatorData", PBYTE),
        ("cbAttestation", DWORD),
        ("pbAttestation", PBYTE),
        ("dwAttestationDecodeType", DWORD),
        ("pvAttestationDecode", PBYTE),
        ("cbAttestationObject", DWORD),
        ("pbAttestationObject", PBYTE),
        ("cbCredentialId", DWORD),
        ("pbCredentialId", PBYTE),
        # Version 2 additions
        ("Extensions", WebAuthNExtensions),
        # Version 3 additions
        ("dwUsedTransport", DWORD),
        # Version 4 additions
        ("bEpAtt", BOOL),
        ("bLargeBlobSupported", BOOL),
        ("bResidentKey", BOOL),
        # Version 5 additions
        ("bPrfEnabled", BOOL),
        # Version 6 additions
        ("cbUnsignedExtensionOutputs", DWORD),
        ("pbUnsignedExtensionOutputs", PBYTE),
        # Version 7 additions
        ("pHmacSecret", ctypes.POINTER(WebAuthNHmacSecretSalt)),
        ("bThirdPartyPayment", BOOL),
        # Version 8 additions
        ("dwTransports", DWORD),
        ("cbClientDataJSON", DWORD),
        ("pbClientDataJSON", PBYTE),
        ("cbRegistrationResponseJSON", DWORD),
        ("pbRegistrationResponseJSON", PBYTE),
    ]

    auth_data = BytesProperty("AuthenticatorData")
    attestation = BytesProperty("Attestation")
    attestation_object = BytesProperty("AttestationObject")
    credential_id = BytesProperty("CredentialId")
    unsigned_extension_outputs = BytesProperty("UnsignedExtensionOutputs")
    client_data_json = BytesProperty("ClientDataJSON")
    registration_response_json = BytesProperty("RegistrationResponseJSON")

    def __del__(self):
        WEBAUTHN.WebAuthNFreeCredentialAttestation(ctypes.byref(self))


HRESULT = ctypes.HRESULT  # type: ignore
WEBAUTHN = windll.webauthn  # type: ignore
WEBAUTHN_API_VERSION = WEBAUTHN.WebAuthNGetApiVersionNumber()

WEBAUTHN.WebAuthNIsUserVerifyingPlatformAuthenticatorAvailable.argtypes = [
    ctypes.POINTER(ctypes.c_bool)
]
WEBAUTHN.WebAuthNIsUserVerifyingPlatformAuthenticatorAvailable.restype = HRESULT

WEBAUTHN.WebAuthNAuthenticatorMakeCredential.argtypes = [
    HWND,
    ctypes.POINTER(WebAuthNRpEntityInformation),
    ctypes.POINTER(WebAuthNUserEntityInformation),
    ctypes.POINTER(WebAuthNCoseCredentialParameters),
    ctypes.POINTER(WebAuthNClientData),
    ctypes.POINTER(WebAuthNMakeCredentialOptions),
    ctypes.POINTER(ctypes.POINTER(WebAuthNCredentialAttestation)),
]
WEBAUTHN.WebAuthNAuthenticatorMakeCredential.restype = HRESULT

WEBAUTHN.WebAuthNAuthenticatorGetAssertion.argtypes = [
    HWND,
    LPCWSTR,
    ctypes.POINTER(WebAuthNClientData),
    ctypes.POINTER(WebAuthNGetAssertionOptions),
    ctypes.POINTER(ctypes.POINTER(WebAuthNAssertion)),
]
WEBAUTHN.WebAuthNAuthenticatorGetAssertion.restype = HRESULT

WEBAUTHN.WebAuthNFreeCredentialAttestation.argtypes = [
    ctypes.POINTER(WebAuthNCredentialAttestation)
]
WEBAUTHN.WebAuthNFreeAssertion.argtypes = [ctypes.POINTER(WebAuthNAssertion)]

WEBAUTHN.WebAuthNGetCancellationId.argtypes = [ctypes.POINTER(GUID)]
WEBAUTHN.WebAuthNGetCancellationId.restype = HRESULT

WEBAUTHN.WebAuthNCancelCurrentOperation.argtypes = [ctypes.POINTER(GUID)]
WEBAUTHN.WebAuthNCancelCurrentOperation.restype = HRESULT

WEBAUTHN.WebAuthNGetErrorName.argtypes = [HRESULT]
WEBAUTHN.WebAuthNGetErrorName.restype = PCWSTR


WEBAUTHN_STRUCT_VERSIONS: Mapping[int, Mapping[str, int]] = {
    1: {
        "WebAuthNRpEntityInformation": 1,
        "WebAuthNUserEntityInformation": 1,
        "WebAuthNClientData": 1,
        "WebAuthNCoseCredentialParameter": 1,
        "WebAuthNCredential": 1,
        "WebAuthNCredentialEx": 1,
        "WebAuthNMakeCredentialOptions": 3,
        "WebAuthNGetAssertionOptions": 4,
        "WebAuthNCommonAttestation": 1,
        "WebAuthNCredentialAttestation": 3,
        "WebAuthNAssertion": 1,
    },
    2: {},
    3: {
        "WebAuthNMakeCredentialOptions": 4,
        "WebAuthNGetAssertionOptions": 5,
        "WebAuthNCredentialAttestation": 4,
        "WebAuthNAssertion": 2,
    },
    4: {
        "WebAuthNMakeCredentialOptions": 5,
        "WebAuthNGetAssertionOptions": 6,
        "WebAuthNAssertion": 3,
        "WebAuthNCredentialDetails": 1,  # Not implemented
    },
    5: {
        "WebAuthNCredentialDetails": 2,
    },
    6: {
        "WebAuthNMakeCredentialOptions": 6,
        "WebAuthNCredentialAttestation": 5,
        "WebAuthNAssertion": 4,
    },
    7: {
        "WebAuthNMakeCredentialOptions": 7,
        "WebAuthNGetAssertionOptions": 7,
        "WebAuthNCredentialAttestation": 6,
        "WebAuthNAssertion": 5,
    },
    8: {
        "WebAuthNMakeCredentialOptions": 8,
        "WebAuthNCredentialDetails": 3,
        "WebAuthNCredentialAttestation": 7,
        "WebAuthNGetAssertionOptions": 8,
    },
    9: {
        "WebAuthNMakeCredentialOptions": 9,
        "WebAuthNGetAssertionOptions": 9,
        "WebAuthNAssertion": 6,
        "WebAuthNCredentialDetails": 4,
        "WebAuthNCredentialAttestation": 8,
        "WebAuthNAuthenticatorDetails": 1,  # Not implemented
    },
}


def get_version(class_name: str) -> int:
    """Get version of struct.

    :param str class_name: Struct class name.
    :returns: Version of Struct to use.
    :rtype: int
    """
    for api_version in range(WEBAUTHN_API_VERSION, 0, -1):
        if (
            api_version in WEBAUTHN_STRUCT_VERSIONS
            and class_name in WEBAUTHN_STRUCT_VERSIONS[api_version]
        ):
            return WEBAUTHN_STRUCT_VERSIONS[api_version][class_name]
    raise ValueError("Unknown class name")
```

## File: fido2/client/windows.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import ctypes
import logging
from threading import Thread
from typing import Any, Mapping, Sequence, cast

from ..ctap2 import AssertionResponse
from ..ctap2.extensions import (
    AuthenticatorExtensionsLargeBlobInputs,
    AuthenticatorExtensionsLargeBlobOutputs,
    AuthenticatorExtensionsPRFInputs,
    AuthenticatorExtensionsPRFOutputs,
    CredentialPropertiesOutput,
    HMACGetSecretInput,
    HMACGetSecretOutput,
)
from ..utils import _JsonDataObject, websafe_decode
from ..webauthn import (
    AttestationConveyancePreference,
    AttestationObject,
    AuthenticationExtensionsClientOutputs,
    AuthenticatorAttachment,
    AuthenticatorAttestationResponse,
    AuthenticatorData,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialType,
    RegistrationResponse,
    ResidentKeyRequirement,
    _as_cbor,
)
from . import (
    AssertionSelection,
    ClientDataCollector,
    ClientError,
    WebAuthnClient,
    _cbor_list,
)
from .win_api import (
    BOOL,
    GUID,
    WEBAUTHN,
    WEBAUTHN_API_VERSION,
    WebAuthNAssertion,
    WebAuthNAttestationConveyancePreference,
    WebAuthNAuthenticatorAttachment,
    WebAuthNClientData,
    WebAuthNCoseCredentialParameters,
    WebAuthNCredBlobExtension,
    WebAuthNCredentialAttestation,
    WebAuthNCredProtectExtensionIn,
    WebAuthNCredWithHmacSecretSalt,
    WebAuthNEnterpriseAttestation,
    WebAuthNExtension,
    WebAuthNGetAssertionOptions,
    WebAuthNHmacSecretSalt,
    WebAuthNHmacSecretSaltValues,
    WebAuthNLargeBlobOperation,
    WebAuthNLargeBlobSupport,
    WebAuthNMakeCredentialOptions,
    WebAuthNRpEntityInformation,
    WebAuthNUserEntityInformation,
    WebAuthNUserVerification,
    WebAuthNUserVerificationRequirement,
    windll,
)

logger = logging.getLogger(__name__)

_extension_output_types: dict[str, type[_JsonDataObject]] = {
    "hmacGetSecret": HMACGetSecretOutput,
    "prf": AuthenticatorExtensionsPRFOutputs,
    "largeBlob": AuthenticatorExtensionsLargeBlobOutputs,
    "credProps": CredentialPropertiesOutput,
}


def _wrap_ext(key, value):
    if key in _extension_output_types:
        return _extension_output_types[key].from_dict(value)
    return value


class CancelThread(Thread):
    def __init__(self, event):
        super().__init__()
        self.daemon = True
        self._completed = False
        self.event = event
        self.guid = GUID()
        WEBAUTHN.WebAuthNGetCancellationId(ctypes.byref(self.guid))

    def run(self):
        self.event.wait()
        if not self._completed:
            WEBAUTHN.WebAuthNCancelCurrentOperation(ctypes.byref(self.guid))

    def complete(self):
        self._completed = True
        self.event.set()
        self.join()


class WindowsClient(WebAuthnClient):
    """Fido2Client-like class using the Windows WebAuthn API.

    Note: This class only works on Windows 10 19H1 or later. This is also when Windows
    started restricting access to FIDO devices, causing the standard client classes to
    require admin priveleges to run (unlike this one).

    :param str origin: The origin to use.
    :param verify: Function to verify an RP ID for a given origin.
    :param ctypes.wintypes.HWND handle: (optional) Window reference to use.
    """

    def __init__(
        self,
        client_data_collector: ClientDataCollector,
        handle=None,
        allow_hmac_secret=False,
    ):
        self.handle = handle or windll.user32.GetForegroundWindow()
        self._client_data_collector = client_data_collector

        self._allow_hmac_secret = allow_hmac_secret

        # TODO: Decide how to configure this list.
        self._enterprise_rpid_list: Sequence[str] | None = None

    @staticmethod
    def is_available() -> bool:
        return WEBAUTHN_API_VERSION > 0

    def make_credential(self, options, event=None):
        """Create a credential using Windows WebAuthN APIs.

        :param options: PublicKeyCredentialCreationOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """

        options = PublicKeyCredentialCreationOptions.from_dict(options)

        # Gather client data, RP ID from client
        client_data, rp_id = self._client_data_collector.collect_client_data(options)
        logger.debug(f"Register a new credential for RP ID: {rp_id}")

        selection = options.authenticator_selection or AuthenticatorSelectionCriteria()
        resident_key = selection.resident_key or ResidentKeyRequirement.DISCOURAGED

        enterprise_attestation = WebAuthNEnterpriseAttestation.NONE
        if options.attestation == AttestationConveyancePreference.ENTERPRISE:
            attestation = WebAuthNAttestationConveyancePreference.ANY
            if self._enterprise_rpid_list is not None:
                # Platform facilitated
                if options.rp.id in self._enterprise_rpid_list:
                    enterprise_attestation = (
                        WebAuthNEnterpriseAttestation.PLATFORM_MANAGED
                    )
            else:
                # Vendor facilitated
                enterprise_attestation = (
                    WebAuthNEnterpriseAttestation.VENDOR_FACILITATED
                )
        else:
            attestation = WebAuthNAttestationConveyancePreference.from_string(
                options.attestation or "none"
            )

        win_extensions = []
        large_blob_support = WebAuthNLargeBlobSupport.NONE
        enable_prf = False
        hmac_salts = None
        if options.extensions:
            if "credentialProtectionPolicy" in options.extensions:
                win_extensions.append(
                    WebAuthNExtension(
                        "credProtect",
                        WebAuthNCredProtectExtensionIn(
                            WebAuthNUserVerification.from_string(
                                options.extensions["credentialProtectionPolicy"]
                            ),
                            options.extensions.get(
                                "enforceCredentialProtectionPolicy", False
                            ),
                        ),
                    )
                )
            if "credBlob" in options.extensions:
                win_extensions.append(
                    WebAuthNExtension(
                        "credBlob",
                        WebAuthNCredBlobExtension(options.extensions["credBlob"]),
                    )
                )
            if "largeBlob" in options.extensions:
                large_blob_support = WebAuthNLargeBlobSupport.from_string(
                    options.extensions["largeBlob"].get("support", "none")
                )
            if options.extensions.get("minPinLength", True):
                win_extensions.append(WebAuthNExtension("minPinLength", BOOL(True)))
            prf = AuthenticatorExtensionsPRFInputs.from_dict(
                cast(Mapping | None, options.extensions.get("prf"))
            )
            if prf:
                enable_prf = True
                win_extensions.append(WebAuthNExtension("hmac-secret", BOOL(True)))
                if prf.eval:
                    hmac_salts = WebAuthNHmacSecretSalt(prf.eval.first, prf.eval.second)
            elif "hmacCreateSecret" in options.extensions and self._allow_hmac_secret:
                win_extensions.append(WebAuthNExtension("hmac-secret", BOOL(True)))
                hmac_get_secret = HMACGetSecretInput.from_dict(
                    cast(Mapping | None, options.extensions.get("hmacGetSecret"))
                )
                if hmac_get_secret:
                    hmac_salts = WebAuthNHmacSecretSalt(
                        hmac_get_secret.salt1, hmac_get_secret.salt2
                    )

        if event:
            timer = CancelThread(event)
            timer.start()
        else:
            timer = None

        attestation_pointer = ctypes.POINTER(WebAuthNCredentialAttestation)()
        try:
            WEBAUTHN.WebAuthNAuthenticatorMakeCredential(
                self.handle,
                ctypes.byref(WebAuthNRpEntityInformation(_as_cbor(options.rp))),
                ctypes.byref(WebAuthNUserEntityInformation(_as_cbor(options.user))),
                ctypes.byref(
                    WebAuthNCoseCredentialParameters(
                        _cbor_list(options.pub_key_cred_params)
                    )
                ),
                ctypes.byref(WebAuthNClientData(client_data)),
                ctypes.byref(
                    WebAuthNMakeCredentialOptions(
                        options.timeout or 0,
                        resident_key == ResidentKeyRequirement.REQUIRED,
                        WebAuthNAuthenticatorAttachment.from_string(
                            selection.authenticator_attachment or "any"
                        ),
                        WebAuthNUserVerificationRequirement.from_string(
                            selection.user_verification or "discouraged"
                        ),
                        attestation,
                        _cbor_list(options.exclude_credentials) or [],
                        timer.guid if timer else None,
                        enterprise_attestation,
                        large_blob_support,
                        resident_key == ResidentKeyRequirement.PREFERRED,
                        enable_prf,
                        win_extensions,
                        hmac_salts,
                        options.hints,
                    )
                ),
                ctypes.byref(attestation_pointer),
            )
        except OSError as e:
            raise ClientError.ERR.OTHER_ERROR(e)

        if timer:
            # TODO: Avoid setting event?
            timer.complete()

        obj = attestation_pointer.contents
        att_obj = AttestationObject(obj.attestation_object)

        extension_outputs: dict[str, Any] = {}
        if options.extensions:
            extensions_out = att_obj.auth_data.extensions or {}
            if obj.dwVersion >= 4 and options.extensions.get("credProps"):
                extension_outputs["credProps"] = {"rk": bool(obj.bResidentKey)}
            if "hmac-secret" in extensions_out:
                if obj.dwVersion >= 7:
                    secret = obj.pHmacSecret.contents
                    secrets = (secret.first, secret.second)
                else:
                    secrets = None
                if enable_prf:
                    extension_outputs["prf"] = {
                        "enabled": extensions_out["hmac-secret"]
                    }
                    if secrets:
                        results = {"first": secrets[0]}
                        if secrets[1]:
                            results["second"] = secrets[1]
                        extension_outputs["prf"]["results"] = results
                else:
                    extension_outputs["hmacCreateSecret"] = extensions_out[
                        "hmac-secret"
                    ]
                    if secrets:
                        results = {"output1": secrets[0]}
                        if secrets[1]:
                            results["output2"] = secrets[1]
                        extension_outputs["hmacGetSecret"] = results
            if obj.dwVersion >= 4 and "largeBlob" in options.extensions:
                extension_outputs["largeBlob"] = {
                    "supported": bool(obj.bLargeBlobSupported)
                }

        logger.info("New credential registered")

        credential = att_obj.auth_data.credential_data
        assert credential is not None  # noqa: S101

        return RegistrationResponse(
            raw_id=credential.credential_id,
            response=AuthenticatorAttestationResponse(
                client_data=client_data, attestation_object=att_obj
            ),
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            client_extension_results=AuthenticationExtensionsClientOutputs(
                {k: _wrap_ext(k, v) for k, v in extension_outputs.items()}
            ),
            type=PublicKeyCredentialType.PUBLIC_KEY,
        )

    def get_assertion(self, options, event=None):
        """Get assertion using Windows WebAuthN APIs.

        :param options: PublicKeyCredentialRequestOptions data.
        :param threading.Event event: (optional) Signal to abort the operation.
        """

        options = PublicKeyCredentialRequestOptions.from_dict(options)

        # Gather client data, RP ID from client
        client_data, rp_id = self._client_data_collector.collect_client_data(options)
        logger.debug(f"Assert a credential for RP ID: {rp_id}")

        attachment = WebAuthNAuthenticatorAttachment.ANY
        for hint in options.hints or []:
            match hint:
                case "security-key":
                    attachment = WebAuthNAuthenticatorAttachment.CROSS_PLATFORM
                case "client-device":
                    attachment = WebAuthNAuthenticatorAttachment.PLATFORM
                case _:
                    continue
            break

        flags = 0
        large_blob = None
        large_blob_operation = WebAuthNLargeBlobOperation.NONE
        hmac_secret_salts = None
        win_extensions = []
        u2f_appid = None
        u2f_appid_used = BOOL(False)
        if options.extensions:
            if options.extensions.get("appid"):
                u2f_appid = options.extensions["appid"]
            if options.extensions.get("getCredBlob"):
                win_extensions.append(WebAuthNExtension("credBlob", BOOL(True)))
            lg_blob = AuthenticatorExtensionsLargeBlobInputs.from_dict(
                cast(Mapping | None, options.extensions.get("largeBlob"))
            )
            if lg_blob:
                if lg_blob.read:
                    large_blob_operation = WebAuthNLargeBlobOperation.GET
                else:
                    large_blob = lg_blob.write
                    large_blob_operation = WebAuthNLargeBlobOperation.SET

            prf = AuthenticatorExtensionsPRFInputs.from_dict(
                cast(Mapping | None, options.extensions.get("prf"))
            )
            if prf:
                cred_salts = prf.eval_by_credential or {}
                hmac_secret_salts = WebAuthNHmacSecretSaltValues(
                    (
                        WebAuthNHmacSecretSalt(prf.eval.first, prf.eval.second)
                        if prf.eval
                        else None
                    ),
                    [
                        WebAuthNCredWithHmacSecretSalt(
                            websafe_decode(cred_id),
                            WebAuthNHmacSecretSalt(salts.first, salts.second),
                        )
                        for cred_id, salts in cred_salts.items()
                    ],
                )
            elif "hmacGetSecret" in options.extensions and self._allow_hmac_secret:
                flags |= 0x00100000
                salts = HMACGetSecretInput.from_dict(
                    cast(Mapping, options.extensions["hmacGetSecret"])
                )
                hmac_secret_salts = WebAuthNHmacSecretSaltValues(
                    WebAuthNHmacSecretSalt(salts.salt1, salts.salt2)
                )

        if event:
            timer = CancelThread(event)
            timer.start()
        else:
            timer = None

        assertion_pointer = ctypes.POINTER(WebAuthNAssertion)()
        try:
            WEBAUTHN.WebAuthNAuthenticatorGetAssertion(
                self.handle,
                options.rp_id,
                ctypes.byref(WebAuthNClientData(client_data)),
                ctypes.byref(
                    WebAuthNGetAssertionOptions(
                        options.timeout or 0,
                        attachment,
                        WebAuthNUserVerificationRequirement.from_string(
                            options.user_verification or "discouraged"
                        ),
                        _cbor_list(options.allow_credentials) or [],
                        timer.guid if timer else None,
                        large_blob_operation,
                        large_blob,
                        hmac_secret_salts,
                        win_extensions,
                        flags,
                        u2f_appid,
                        u2f_appid_used,
                        options.hints,
                    )
                ),
                ctypes.byref(assertion_pointer),
            )
        except OSError as e:
            raise ClientError.ERR.OTHER_ERROR(e)

        if timer:
            # TODO: Avoid setting event?
            timer.complete()

        obj = assertion_pointer.contents
        auth_data = AuthenticatorData(obj.auth_data)

        extension_outputs: dict[str, Any] = {}

        if obj.dwVersion >= 2 and u2f_appid:
            extension_outputs["appid"] = bool(u2f_appid_used.value)

        if options.extensions:
            if obj.dwVersion >= 3 and hmac_secret_salts:
                secret = obj.pHmacSecret.contents
                if "prf" in options.extensions:
                    result = {"first": secret.first}
                    if secret.second:
                        result["second"] = secret.second
                    extension_outputs["prf"] = {"results": result}
                else:
                    result = {"output1": secret.first}
                    if secret.second:
                        result["output2"] = secret.second
                    extension_outputs["hmacGetSecret"] = result
            if obj.dwVersion >= 2 and obj.dwCredLargeBlobStatus != 0:
                if options.extensions["largeBlob"].get("read", False):
                    extension_outputs["largeBlob"] = {"blob": obj.cred_large_blob}
                else:
                    extension_outputs["largeBlob"] = {
                        "written": obj.dwCredLargeBlobStatus == 1
                    }

        credential = {
            "type": obj.Credential.pwszCredentialType,
            "id": obj.Credential.id,
        }
        return AssertionSelection(
            client_data,
            [
                AssertionResponse(
                    credential=credential,
                    auth_data=auth_data,
                    signature=obj.signature,
                    user={"id": obj.user_id} if obj.user_id else None,
                )
            ],
            {k: _wrap_ext(k, v) for k, v in extension_outputs.items()},
        )
```

## File: fido2/ctap2/__init__.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from .base import (  # noqa
    Ctap2,
    Info,
    AttestationResponse,
    AssertionResponse,
)

from .pin import ClientPin, PinProtocolV1, PinProtocolV2  # noqa
from .credman import CredentialManagement  # noqa
from .bio import FPBioEnrollment, CaptureError  # noqa
from .blob import LargeBlobs  # noqa
from .config import Config  # noqa
```

## File: fido2/ctap2/base.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import struct
from dataclasses import Field, dataclass, field, fields
from enum import IntEnum, unique
from threading import Event
from typing import Any, Callable, Mapping

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from .. import cbor
from ..cose import CoseKey
from ..ctap import CtapDevice, CtapError
from ..hid import CAPABILITY, CTAPHID
from ..utils import _DataClassMapping
from ..webauthn import Aaguid, AuthenticatorData

logger = logging.getLogger(__name__)


def args(*params) -> dict[int, Any]:
    """Constructs a dict from a list of arguments for sending a CBOR command.
    None elements will be omitted.

    :param params: Arguments, in order, to add to the command.
    :return: The input parameters as a dict.
    """
    return {i: v for i, v in enumerate(params, 1) if v is not None}


class _CborDataObject(_DataClassMapping[int]):
    @classmethod
    def _get_field_key(cls, field: Field) -> int:
        return fields(cls).index(field) + 1  # type: ignore


@dataclass(eq=False, frozen=True)
class Info(_CborDataObject):
    """Binary CBOR encoded response data returned by the CTAP2 GET_INFO command.

    See:
    https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html#authenticatorGetInfo
    for descriptions of these fields.

    Note that while many fields are optional when returned by the authenticator,
    this dataclass uses defaults to represent a missing value such as empty lists
    or dicts, or the integer value 0. These are used rather than None for omitted
    values as long as this can be done without introducing any practical ambiguity.
    This also means that several of these fields may have a 0 value even if the
    specification states that they should be non-zero when returned from the
    authenticator.

    :param _: The binary content of the Info data.
    """

    versions: list[str]
    extensions: list[str] = field(default_factory=list)
    aaguid: Aaguid = Aaguid.NONE
    options: dict[str, bool] = field(default_factory=dict)
    max_msg_size: int = 1024
    pin_uv_protocols: list[int] = field(default_factory=list)
    max_creds_in_list: int = 0
    max_cred_id_length: int = 0
    transports: list[str] = field(default_factory=list)
    algorithms: list[dict[str, Any]] = field(default_factory=list)
    max_large_blob: int = 0
    force_pin_change: bool = False
    min_pin_length: int = 4
    firmware_version: int = 0
    max_cred_blob_length: int = 0
    max_rpids_for_min_pin: int = 0
    preferred_platform_uv_attempts: int = 0
    uv_modality: int = 0
    certifications: dict = field(default_factory=dict)
    remaining_disc_creds: int | None = None
    vendor_prototype_config_commands: list[int] = field(default_factory=list)
    attestation_formats: list[str] = field(default_factory=lambda: ["packed"])
    uv_count_since_pin: int | None = None
    long_touch_for_reset: bool = False
    enc_identifier: bytes | None = None
    transports_for_reset: list[str] = field(default_factory=list)
    pin_complexity_policy: bool | None = None
    pin_complexity_policy_url: bytes | None = None
    max_pin_length: int = 63

    def get_identifier(self, pin_token: bytes) -> bytes | None:
        """Decrypt the device identifier using a persistent PUAT."""
        if not self.enc_identifier:
            return None

        iv, ct = self.enc_identifier[:16], self.enc_identifier[16:]
        be = default_backend()
        secret = HKDF(
            algorithm=hashes.SHA256(),
            length=16,
            salt=b"\0" * 32,
            info=b"encIdentifier",
            backend=be,
        ).derive(pin_token)

        dec = Cipher(algorithms.AES(secret), modes.CBC(iv), be).decryptor()
        return dec.update(ct) + dec.finalize()


@dataclass(eq=False, frozen=True)
class AttestationResponse(_CborDataObject):
    """Binary CBOR encoded attestation object.

    :param _: The binary representation of the attestation object.
    :ivar fmt: The type of attestation used.
    :ivar auth_data: The attested authenticator data.
    :ivar att_stmt: The attestation statement.
    :ivar ep_att: Whether an enterprise attestation was returned for this credential.
    :ivar large_blob_key: The largeBlobKey for the credential, if requested.
    :ivar unsigned_extension_outputs: Any unsigned outputs of extensions.
    """

    fmt: str
    auth_data: AuthenticatorData
    att_stmt: dict[str, Any]
    ep_att: bool | None = None
    large_blob_key: bytes | None = None
    unsigned_extension_outputs: dict[str, Any] = field(default_factory=dict)


@dataclass(eq=False, frozen=True)
class AssertionResponse(_CborDataObject):
    """Binary CBOR encoded assertion response.

    :param _: The binary representation of the assertion response.
    :ivar credential: The credential used for the assertion.
    :ivar auth_data: The authenticator data part of the response.
    :ivar signature: The digital signature of the assertion.
    :ivar user: The user data of the credential.
    :ivar number_of_credentials: The total number of responses available
        (only set for the first response, if > 1).
    """

    credential: Mapping[str, Any]
    auth_data: AuthenticatorData
    signature: bytes
    user: dict[str, Any] | None = None
    number_of_credentials: int | None = None
    user_selected: bool | None = None
    large_blob_key: bytes | None = None

    def verify(self, client_param: bytes, public_key: CoseKey):
        """Verify the digital signature of the response with regard to the
        client_param, using the given public key.

        :param client_param: SHA256 hash of the ClientData used for the request.
        :param public_key: The public key of the credential, to verify.
        """
        public_key.verify(self.auth_data + client_param, self.signature)

    @classmethod
    def from_ctap1(
        cls, app_param: bytes, credential: Mapping[str, Any], authentication
    ) -> "AssertionResponse":
        """Create an AssertionResponse from a CTAP1 SignatureData instance.

        :param app_param: SHA256 hash of the RP ID used for the CTAP1 request.
        :param credential: Credential used for the CTAP1 request (from the
            allowList).
        :param authentication: The CTAP1 signature data.
        :return: The assertion response.
        """
        return cls(
            credential=credential,
            auth_data=AuthenticatorData.create(
                app_param,
                authentication.user_presence & AuthenticatorData.FLAG.UP,
                authentication.counter,
            ),
            signature=authentication.signature,
        )


class Ctap2:
    """Implementation of the CTAP2 specification.

    :param device: A CtapHidDevice handle supporting CTAP2.
    :param strict_cbor: Validate that CBOR returned from the Authenticator is
        canonical, defaults to True.
    """

    @unique
    class CMD(IntEnum):
        MAKE_CREDENTIAL = 0x01
        GET_ASSERTION = 0x02
        GET_INFO = 0x04
        CLIENT_PIN = 0x06
        RESET = 0x07
        GET_NEXT_ASSERTION = 0x08
        BIO_ENROLLMENT = 0x09
        CREDENTIAL_MGMT = 0x0A
        SELECTION = 0x0B
        LARGE_BLOBS = 0x0C
        CONFIG = 0x0D

        BIO_ENROLLMENT_PRE = 0x40
        CREDENTIAL_MGMT_PRE = 0x41

    def __init__(self, device: CtapDevice, strict_cbor: bool = True):
        if not device.capabilities & CAPABILITY.CBOR:
            raise ValueError("Device does not support CTAP2.")
        self.device = device
        self._strict_cbor = strict_cbor
        self._max_msg_size = 1024  # For initial get_info call
        self._info = self.get_info()
        self._max_msg_size = self._info.max_msg_size

    @property
    def info(self) -> Info:
        """Get a cached Info object which can be used to determine capabilities.

        :rtype: Info
        :return: The response of calling GetAuthenticatorInfo.
        """
        return self._info

    def send_cbor(
        self,
        cmd: int,
        data: Mapping[int, Any] | None = None,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> Mapping[int, Any]:
        """Sends a CBOR message to the device, and waits for a response.

        :param cmd: The command byte of the request.
        :param data: The payload to send (to be CBOR encoded).
        :param event: Optional threading.Event used to cancel the request.
        :param on_keepalive: Optional function called when keep-alive is sent by
            the authenticator.
        """
        request = struct.pack(">B", cmd)
        if data is not None:
            request += cbor.encode(data)
        if len(request) > self._max_msg_size:
            raise CtapError(CtapError.ERR.REQUEST_TOO_LARGE)
        response = self.device.call(CTAPHID.CBOR, request, event, on_keepalive)
        status = response[0]
        if status != 0x00:
            raise CtapError(status)
        enc = response[1:]
        if not enc:
            return {}
        decoded = cbor.decode(enc)
        if self._strict_cbor:
            expected = cbor.encode(decoded)
            if expected != enc:
                raise ValueError(
                    "Non-canonical CBOR from Authenticator.\n"
                    f"Got: {enc.hex()}\nExpected: {expected.hex()}"
                )
        if isinstance(decoded, Mapping):
            return decoded
        raise TypeError("Decoded value of wrong type")

    def get_info(self) -> Info:
        """CTAP2 getInfo command.

        :return: Information about the authenticator.
        """
        return Info.from_dict(self.send_cbor(Ctap2.CMD.GET_INFO))

    def client_pin(
        self,
        pin_uv_protocol: int,
        sub_cmd: int,
        key_agreement: Mapping[int, Any] | None = None,
        pin_uv_param: bytes | None = None,
        new_pin_enc: bytes | None = None,
        pin_hash_enc: bytes | None = None,
        permissions: int | None = None,
        permissions_rpid: str | None = None,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> Mapping[int, Any]:
        """CTAP2 clientPin command, used for various PIN operations.

        This method is not intended to be called directly. It is intended to be used by
        an instance of the PinProtocolV1 class.

        :param pin_uv_protocol: The PIN/UV protocol version to use.
        :param sub_cmd: A clientPin sub command.
        :param key_agreement: The keyAgreement parameter.
        :param pin_uv_param: The pinAuth parameter.
        :param new_pin_enc: The newPinEnc parameter.
        :param pin_hash_enc: The pinHashEnc parameter.
        :param permissions: The permissions parameter.
        :param permissions_rpid: The permissions RPID parameter.
        :param event: Optional threading.Event used to cancel the request.
        :param on_keepalive: Optional callback function to handle keep-alive
            messages from the authenticator.
        :return: The response of the command, decoded.
        """
        return self.send_cbor(
            Ctap2.CMD.CLIENT_PIN,
            args(
                pin_uv_protocol,
                sub_cmd,
                key_agreement,
                pin_uv_param,
                new_pin_enc,
                pin_hash_enc,
                None,
                None,
                permissions,
                permissions_rpid,
            ),
            event=event,
            on_keepalive=on_keepalive,
        )

    def reset(
        self,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> None:
        """CTAP2 reset command, erases all credentials and PIN.

        :param event: Optional threading.Event object used to cancel the request.
        :param on_keepalive: Optional callback function to handle keep-alive
            messages from the authenticator.
        """
        self.send_cbor(Ctap2.CMD.RESET, event=event, on_keepalive=on_keepalive)
        logger.info("Reset completed - All data erased")

    def make_credential(
        self,
        client_data_hash: bytes,
        rp: Mapping[str, Any],
        user: Mapping[str, Any],
        key_params: list[Mapping[str, Any]],
        exclude_list: list[Mapping[str, Any]] | None = None,
        extensions: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
        pin_uv_param: bytes | None = None,
        pin_uv_protocol: int | None = None,
        enterprise_attestation: int | None = None,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> AttestationResponse:
        """CTAP2 makeCredential operation.

        :param client_data_hash: SHA256 hash of the ClientData.
        :param rp: PublicKeyCredentialRpEntity parameters.
        :param user: PublicKeyCredentialUserEntity parameters.
        :param key_params: List of acceptable credential types.
        :param exclude_list: Optional list of PublicKeyCredentialDescriptors.
        :param extensions: Optional dict of extensions.
        :param options: Optional dict of options.
        :param pin_uv_param: Optional PIN/UV auth parameter.
        :param pin_uv_protocol: The version of PIN/UV protocol used, if any.
        :param enterprise_attestation: Whether or not to request Enterprise Attestation.
        :param event: Optional threading.Event used to cancel the request.
        :param on_keepalive: Optional callback function to handle keep-alive
            messages from the authenticator.
        :return: The new credential.
        """
        logger.debug("Calling CTAP2 make_credential")
        return AttestationResponse.from_dict(
            self.send_cbor(
                Ctap2.CMD.MAKE_CREDENTIAL,
                args(
                    client_data_hash,
                    rp,
                    user,
                    key_params,
                    exclude_list,
                    extensions,
                    options,
                    pin_uv_param,
                    pin_uv_protocol,
                    enterprise_attestation,
                ),
                event=event,
                on_keepalive=on_keepalive,
            )
        )

    def get_assertion(
        self,
        rp_id: str,
        client_data_hash: bytes,
        allow_list: list[Mapping[str, Any]] | None = None,
        extensions: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
        pin_uv_param: bytes | None = None,
        pin_uv_protocol: int | None = None,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> AssertionResponse:
        """CTAP2 getAssertion command.

        :param rp_id: The RP ID of the credential.
        :param client_data_hash: SHA256 hash of the ClientData used.
        :param allow_list: Optional list of PublicKeyCredentialDescriptors.
        :param extensions: Optional dict of extensions.
        :param options: Optional dict of options.
        :param pin_uv_param: Optional PIN/UV auth parameter.
        :param pin_uv_protocol: The version of PIN/UV protocol used, if any.
        :param event: Optional threading.Event used to cancel the request.
        :param on_keepalive: Optional callback function to handle keep-alive messages
            from the authenticator.
        :return: The new assertion.
        """
        logger.debug("Calling CTAP2 get_assertion")
        return AssertionResponse.from_dict(
            self.send_cbor(
                Ctap2.CMD.GET_ASSERTION,
                args(
                    rp_id,
                    client_data_hash,
                    allow_list,
                    extensions,
                    options,
                    pin_uv_param,
                    pin_uv_protocol,
                ),
                event=event,
                on_keepalive=on_keepalive,
            )
        )

    def get_next_assertion(self) -> AssertionResponse:
        """CTAP2 getNextAssertion command.

        :return: The next available assertion response.
        """
        return AssertionResponse.from_dict(self.send_cbor(Ctap2.CMD.GET_NEXT_ASSERTION))

    def get_assertions(self, *args, **kwargs) -> list[AssertionResponse]:
        """Convenience method to get list of assertions.

        See get_assertion and get_next_assertion for details.
        """
        first = self.get_assertion(*args, **kwargs)
        rest = [
            self.get_next_assertion()
            for _ in range(1, first.number_of_credentials or 1)
        ]
        return [first] + rest

    def credential_mgmt(
        self,
        sub_cmd: int,
        sub_cmd_params: Mapping[int, Any] | None = None,
        pin_uv_protocol: int | None = None,
        pin_uv_param: bytes | None = None,
    ) -> Mapping[int, Any]:
        """CTAP2 credentialManagement command, used to manage resident
        credentials.

        NOTE: This implements the current draft version of the CTAP2 specification and
        should be considered highly experimental.

        This method is not intended to be called directly. It is intended to be used by
        an instance of the CredentialManagement class.

        :param sub_cmd: A CredentialManagement sub command.
        :param sub_cmd_params: Sub command specific parameters.
        :param pin_uv_protocol: PIN/UV auth protocol version used.
        :param pin_uv_param: PIN/UV Auth parameter.
        """
        if "credMgmt" in self.info.options:
            cmd = Ctap2.CMD.CREDENTIAL_MGMT
        elif "credentialMgmtPreview" in self.info.options:
            cmd = Ctap2.CMD.CREDENTIAL_MGMT_PRE
        else:
            raise ValueError(
                "Credential Management not supported by this Authenticator"
            )
        return self.send_cbor(
            cmd,
            args(sub_cmd, sub_cmd_params, pin_uv_protocol, pin_uv_param),
        )

    def bio_enrollment(
        self,
        modality: int | None = None,
        sub_cmd: int | None = None,
        sub_cmd_params: Mapping[int, Any] | None = None,
        pin_uv_protocol: int | None = None,
        pin_uv_param: bytes | None = None,
        get_modality: bool | None = None,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> Mapping[int, Any]:
        """CTAP2 bio enrollment command. Used to provision/enumerate/delete bio
        enrollments in the authenticator.

        NOTE: This implements the current draft version of the CTAP2 specification and
        should be considered highly experimental.

        This method is not intended to be called directly. It is intended to be used by
        an instance of the BioEnrollment class.

        :param modality: The user verification modality being used.
        :param sub_cmd: A BioEnrollment sub command.
        :param sub_cmd_params: Sub command specific parameters.
        :param pin_uv_protocol: PIN/UV protocol version used.
        :param pin_uv_param: PIN/UV auth param.
        :param get_modality: Get the user verification type modality.
        """
        if "bioEnroll" in self.info.options:
            cmd = Ctap2.CMD.BIO_ENROLLMENT
        elif "userVerificationMgmtPreview" in self.info.options:
            cmd = Ctap2.CMD.BIO_ENROLLMENT_PRE
        else:
            raise ValueError("Authenticator does not support Bio Enroll")
        return self.send_cbor(
            cmd,
            args(
                modality,
                sub_cmd,
                sub_cmd_params,
                pin_uv_protocol,
                pin_uv_param,
                get_modality,
            ),
            event=event,
            on_keepalive=on_keepalive,
        )

    def selection(
        self,
        *,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> None:
        """CTAP2 authenticator selection command.

        This command allows the platform to let a user select a certain authenticator
        by asking for user presence.

        :param event: Optional threading.Event used to cancel the request.
        :param on_keepalive: Optional callback function to handle keep-alive messages
            from the authenticator.
        """
        self.send_cbor(Ctap2.CMD.SELECTION, event=event, on_keepalive=on_keepalive)

    def large_blobs(
        self,
        offset: int,
        get: int | None = None,
        set: bytes | None = None,
        length: int | None = None,
        pin_uv_param: bytes | None = None,
        pin_uv_protocol: int | None = None,
    ) -> Mapping[int, Any]:
        """CTAP2 authenticator large blobs command.

        This command is used to read and write the large blob array.

        This method is not intended to be called directly. It is intended to be used by
        an instance of the LargeBlobs class.

        :param offset: The offset of where to start reading/writing data.
        :param get: Optional (max) length of data to read.
        :param set: Optional data to write.
        :param length: Length of the payload in set.
        :param pin_uv_protocol: PIN/UV protocol version used.
        :param pin_uv_param: PIN/UV auth param.
        """
        return self.send_cbor(
            Ctap2.CMD.LARGE_BLOBS,
            args(get, set, offset, length, pin_uv_param, pin_uv_protocol),
        )

    def config(
        self,
        sub_cmd: int,
        sub_cmd_params: Mapping[int, Any] | None = None,
        pin_uv_protocol: int | None = None,
        pin_uv_param: bytes | None = None,
    ) -> Mapping[int, Any]:
        """CTAP2 authenticator config command.

        This command is used to configure various authenticator features through the
        use of its subcommands.

        This method is not intended to be called directly. It is intended to be used by
        an instance of the Config class.

        :param sub_cmd: A Config sub command.
        :param sub_cmd_params: Sub command specific parameters.
        :param pin_uv_protocol: PIN/UV auth protocol version used.
        :param pin_uv_param: PIN/UV Auth parameter.
        """
        return self.send_cbor(
            Ctap2.CMD.CONFIG,
            args(sub_cmd, sub_cmd_params, pin_uv_protocol, pin_uv_param),
        )
```

## File: fido2/ctap2/bio.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import struct
from enum import IntEnum, unique
from threading import Event
from typing import Any, Callable, Mapping

from .. import cbor
from ..ctap import CtapError
from .base import Ctap2, Info
from .pin import PinProtocol

logger = logging.getLogger(__name__)


class BioEnrollment:
    @unique
    class RESULT(IntEnum):
        MODALITY = 0x01
        FINGERPRINT_KIND = 0x02
        MAX_SAMPLES_REQUIRED = 0x03
        TEMPLATE_ID = 0x04
        LAST_SAMPLE_STATUS = 0x05
        REMAINING_SAMPLES = 0x06
        TEMPLATE_INFOS = 0x07
        MAX_TEMPLATE_FRIENDLY_NAME = 0x08

    @unique
    class TEMPLATE_INFO(IntEnum):
        ID = 0x01
        NAME = 0x02

    @unique
    class MODALITY(IntEnum):
        FINGERPRINT = 0x01

    @staticmethod
    def is_supported(info: Info) -> bool:
        if "bioEnroll" in info.options:
            return True
        # We also support the Prototype command
        if (
            "FIDO_2_1_PRE" in info.versions
            and "userVerificationMgmtPreview" in info.options
        ):
            return True
        return False

    def __init__(self, ctap: Ctap2, modality: MODALITY):
        if not self.is_supported(ctap.info):
            raise ValueError("Authenticator does not support BioEnroll")

        self.ctap = ctap
        self.modality = self.get_modality()
        if modality != self.modality:
            raise ValueError(f"Device does not support {modality:s}")

    def get_modality(self) -> int:
        """Get bio modality.

        :return: The type of modality supported by the authenticator.
        """
        return self.ctap.bio_enrollment(get_modality=True)[
            BioEnrollment.RESULT.MODALITY
        ]


class CaptureError(Exception):
    def __init__(self, code: int):
        self.code = code
        super().__init__(f"Fingerprint capture error: {code}")


class FPEnrollmentContext:
    """Helper object to perform fingerprint enrollment.

    :param bio: An instance of FPBioEnrollment.
    :param timeout: Optional timeout for fingerprint captures (ms).
    :ivar remaining: The number of (estimated) remaining samples needed.
    :ivar template_id: The ID of the new template (only available after the initial
        sample has been captured).
    """

    def __init__(self, bio: "FPBioEnrollment", timeout: int | None = None):
        self._bio = bio
        self.timeout = timeout
        self.template_id: bytes | None = None
        self.remaining: int | None = None

    def capture(
        self,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> bytes | None:
        """Capture a fingerprint sample.

        This call will block for up to timeout milliseconds (or indefinitely, if
        timeout not specified) waiting for the user to scan their fingerprint to
        collect one sample.

        :return: None, if more samples are needed, or the template ID if enrollment is
            completed.
        """
        if self.template_id is None:
            self.template_id, status, self.remaining = self._bio.enroll_begin(
                self.timeout, event, on_keepalive
            )
        else:
            status, self.remaining = self._bio.enroll_capture_next(
                self.template_id, self.timeout, event, on_keepalive
            )
        if status != FPBioEnrollment.FEEDBACK.FP_GOOD:
            raise CaptureError(status)
        if self.remaining == 0:
            return self.template_id
        return None

    def cancel(self) -> None:
        """Cancels ongoing enrollment."""
        self._bio.enroll_cancel()
        self.template_id = None


class FPBioEnrollment(BioEnrollment):
    """Implementation of the bio enrollment API.

    NOTE: The get_fingerprint_sensor_info method does not require authentication, and
    can be used by setting pin_uv_protocol and pin_uv_token to None.

    :param ctap: An instance of a CTAP2 object.
    :param pin_uv_protocol: The PIN/UV protocol version used.
    :param pin_uv_token: A valid PIN/UV Auth Token for the current CTAP session.
    """

    @unique
    class CMD(IntEnum):
        ENROLL_BEGIN = 0x01
        ENROLL_CAPTURE_NEXT = 0x02
        ENROLL_CANCEL = 0x03
        ENUMERATE_ENROLLMENTS = 0x04
        SET_NAME = 0x05
        REMOVE_ENROLLMENT = 0x06
        GET_SENSOR_INFO = 0x07

    @unique
    class PARAM(IntEnum):
        TEMPLATE_ID = 0x01
        TEMPLATE_NAME = 0x02
        TIMEOUT_MS = 0x03

    @unique
    class FEEDBACK(IntEnum):
        FP_GOOD = 0x00
        FP_TOO_HIGH = 0x01
        FP_TOO_LOW = 0x02
        FP_TOO_LEFT = 0x03
        FP_TOO_RIGHT = 0x04
        FP_TOO_FAST = 0x05
        FP_TOO_SLOW = 0x06
        FP_POOR_QUALITY = 0x07
        FP_TOO_SKEWED = 0x08
        FP_TOO_SHORT = 0x09
        FP_MERGE_FAILURE = 0x0A
        FP_EXISTS = 0x0B
        FP_DATABASE_FULL = 0x0C
        NO_USER_ACTIVITY = 0x0D
        NO_UP_TRANSITION = 0x0E

        def __str__(self):
            return f"0x{self.value:02X} - {self.name}"

    def __init__(self, ctap: Ctap2, pin_uv_protocol: PinProtocol, pin_uv_token: bytes):
        super().__init__(ctap, BioEnrollment.MODALITY.FINGERPRINT)
        self.pin_uv_protocol = pin_uv_protocol
        self.pin_uv_token = pin_uv_token

    def _call(self, sub_cmd, params=None, auth=True, event=None, on_keepalive=None):
        kwargs = {
            "modality": self.modality,
            "sub_cmd": sub_cmd,
            "sub_cmd_params": params,
            "event": event,
            "on_keepalive": on_keepalive,
        }
        if auth:
            msg = struct.pack(">BB", self.modality, sub_cmd)
            if params is not None:
                msg += cbor.encode(params)
            kwargs["pin_uv_protocol"] = self.pin_uv_protocol.VERSION
            kwargs["pin_uv_param"] = self.pin_uv_protocol.authenticate(
                self.pin_uv_token, msg
            )
        return self.ctap.bio_enrollment(**kwargs)

    def get_fingerprint_sensor_info(self) -> Mapping[int, Any]:
        """Get fingerprint sensor info.

        :return: A dict containing FINGERPRINT_KIND and MAX_SAMPLES_REQUIRES.
        """
        return self._call(FPBioEnrollment.CMD.GET_SENSOR_INFO, auth=False)

    def enroll_begin(
        self,
        timeout: int | None = None,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> tuple[bytes, FPBioEnrollment.FEEDBACK, int]:
        """Start fingerprint enrollment.

        Starts the process of enrolling a new fingerprint, and will wait for the user
        to scan their fingerprint once to provide an initial sample.

        :param timeout: Optional timeout in milliseconds.
        :return: A tuple containing the new template ID, the sample status, and the
            number of samples remaining to complete the enrollment.
        """
        logger.debug(f"Starting fingerprint enrollment (timeout={timeout})")
        result = self._call(
            FPBioEnrollment.CMD.ENROLL_BEGIN,
            (
                {FPBioEnrollment.PARAM.TIMEOUT_MS: timeout}
                if timeout is not None
                else None
            ),
            event=event,
            on_keepalive=on_keepalive,
        )
        logger.debug(f"Sample capture result: {result}")
        return (
            result[BioEnrollment.RESULT.TEMPLATE_ID],
            FPBioEnrollment.FEEDBACK(result[BioEnrollment.RESULT.LAST_SAMPLE_STATUS]),
            result[BioEnrollment.RESULT.REMAINING_SAMPLES],
        )

    def enroll_capture_next(
        self,
        template_id: bytes,
        timeout: int | None = None,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> tuple[FPBioEnrollment.FEEDBACK, int]:
        """Continue fingerprint enrollment.

        Continues enrolling a new fingerprint and will wait for the user to scan their
        fingerpring once to provide a new sample.
        Once the number of samples remaining is 0, the enrollment is completed.

        :param template_id: The template ID returned by a call to `enroll_begin`.
        :param timeout: Optional timeout in milliseconds.
        :return: A tuple containing the sample status, and the number of samples
            remaining to complete the enrollment.
        """
        logger.debug(f"Capturing next sample with (timeout={timeout})")
        params: dict[int, Any] = {FPBioEnrollment.PARAM.TEMPLATE_ID: template_id}
        if timeout is not None:
            params[FPBioEnrollment.PARAM.TIMEOUT_MS] = timeout
        result = self._call(
            FPBioEnrollment.CMD.ENROLL_CAPTURE_NEXT,
            params,
            event=event,
            on_keepalive=on_keepalive,
        )
        logger.debug(f"Sample capture result: {result}")
        return (
            FPBioEnrollment.FEEDBACK(result[BioEnrollment.RESULT.LAST_SAMPLE_STATUS]),
            result[BioEnrollment.RESULT.REMAINING_SAMPLES],
        )

    def enroll_cancel(self) -> None:
        """Cancel any ongoing fingerprint enrollment."""
        logger.debug("Cancelling fingerprint enrollment.")
        self._call(FPBioEnrollment.CMD.ENROLL_CANCEL, auth=False)

    def enroll(self, timeout: int | None = None) -> FPEnrollmentContext:
        """Convenience wrapper for doing fingerprint enrollment.

        See FPEnrollmentContext for details.
        :return: An initialized FPEnrollmentContext.
        """
        return FPEnrollmentContext(self, timeout)

    def enumerate_enrollments(self) -> Mapping[bytes, str | None]:
        """Get a dict of enrolled fingerprint templates which maps template ID's to
        their friendly names.

        :return: A dict of enrolled template_id -> name pairs.
        """
        try:
            return {
                t[BioEnrollment.TEMPLATE_INFO.ID]: t[BioEnrollment.TEMPLATE_INFO.NAME]
                for t in self._call(FPBioEnrollment.CMD.ENUMERATE_ENROLLMENTS)[
                    BioEnrollment.RESULT.TEMPLATE_INFOS
                ]
            }
        except CtapError as e:
            if e.code == CtapError.ERR.INVALID_OPTION:
                return {}
            raise

    def set_name(self, template_id: bytes, name: str) -> None:
        """Set/Change the friendly name of a previously enrolled fingerprint template.

        :param template_id: The ID of the template to change.
        :param name: A friendly name to give the template.
        """
        logger.debug(f"Changing name of template: {template_id.hex()} to {name}")
        self._call(
            FPBioEnrollment.CMD.SET_NAME,
            {
                BioEnrollment.TEMPLATE_INFO.ID: template_id,
                BioEnrollment.TEMPLATE_INFO.NAME: name,
            },
        )
        logger.info("Fingerprint template renamed")

    def remove_enrollment(self, template_id: bytes) -> None:
        """Remove a previously enrolled fingerprint template.

        :param template_id: The Id of the template to remove.
        """
        logger.debug(f"Deleting template: {template_id.hex()}")
        self._call(
            FPBioEnrollment.CMD.REMOVE_ENROLLMENT,
            {BioEnrollment.TEMPLATE_INFO.ID: template_id},
        )
        logger.info("Fingerprint template deleted")
```

## File: fido2/ctap2/blob.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import os
import struct
import zlib
from typing import Any, Mapping, Sequence, cast

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .. import cbor
from ..utils import sha256
from .base import Ctap2, Info
from .pin import PinProtocol, _PinUv


def _compress(data):
    o = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    return o.compress(data) + o.flush()


def _decompress(data):
    o = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
    return o.decompress(data) + o.flush()


def _lb_ad(orig_size):
    return b"blob" + struct.pack("<Q", orig_size)


def _lb_pack(key, data):
    orig_size = len(data)
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(nonce, _compress(data), _lb_ad(orig_size))

    return {
        1: ciphertext,
        2: nonce,
        3: orig_size,
    }


def _lb_unpack(key, entry):
    try:
        ciphertext = entry[1]
        nonce = entry[2]
        orig_size = entry[3]
        aesgcm = AESGCM(key)
        compressed = aesgcm.decrypt(nonce, ciphertext, _lb_ad(orig_size))
        return compressed, orig_size
    except (TypeError, IndexError, KeyError):
        raise ValueError("Invalid entry")
    except InvalidTag:
        raise ValueError("Wrong key")


class LargeBlobs:
    """Implementation of the CTAP2.1 Large Blobs API.

    Getting a largeBlobKey for a credential is done via the LargeBlobKey extension.

    :param ctap: An instance of a CTAP2 object.
    :param pin_uv_protocol: An instance of a PinUvAuthProtocol.
    :param pin_uv_token: A valid PIN/UV Auth Token for the current CTAP session.
    """

    @staticmethod
    def is_supported(info: Info) -> bool:
        return info.options.get("largeBlobs") is True

    def __init__(
        self,
        ctap: Ctap2,
        pin_uv_protocol: PinProtocol | None = None,
        pin_uv_token: bytes | None = None,
    ):
        if not self.is_supported(ctap.info):
            raise ValueError("Authenticator does not support LargeBlobs")

        self.ctap = ctap
        self.max_fragment_length = self.ctap.info.max_msg_size - 64
        self.pin_uv = (
            _PinUv(pin_uv_protocol, pin_uv_token)
            if pin_uv_protocol and pin_uv_token
            else None
        )

    def read_blob_array(self) -> Sequence[Mapping[int, Any]]:
        """Gets the entire contents of the Large Blobs array.

        :return: The CBOR decoded list of Large Blobs.
        """
        offset = 0
        buf = b""
        while True:
            fragment = self.ctap.large_blobs(offset, get=self.max_fragment_length)[1]
            buf += fragment
            if len(fragment) < self.max_fragment_length:
                break
            offset += self.max_fragment_length

        data, check = buf[:-16], buf[-16:]
        if check != sha256(data)[:-16]:
            return []
        return cast(Sequence[Mapping[int, Any]], cbor.decode(data))

    def write_blob_array(self, blob_array: Sequence[Mapping[int, Any]]) -> None:
        """Writes the entire Large Blobs array.

        :param blob_array: A list to write to the Authenticator.
        """
        if not isinstance(blob_array, list):
            raise TypeError("large-blob array must be a list")

        data = cbor.encode(blob_array)
        data += sha256(data)[:16]
        offset = 0
        size = len(data)

        while offset < size:
            ln = min(size - offset, self.max_fragment_length)
            _set = data[offset : offset + ln]

            if self.pin_uv:
                msg = (
                    b"\xff" * 32
                    + b"\x0c\x00"
                    + struct.pack("<I", offset)
                    + sha256(_set)
                )
                pin_uv_protocol = self.pin_uv.protocol.VERSION
                pin_uv_param = self.pin_uv.protocol.authenticate(self.pin_uv.token, msg)
            else:
                pin_uv_param = None
                pin_uv_protocol = None

            self.ctap.large_blobs(
                offset,
                set=_set,
                length=size if offset == 0 else None,
                pin_uv_protocol=pin_uv_protocol,
                pin_uv_param=pin_uv_param,
            )

            offset += ln

    def get_blob(self, large_blob_key: bytes) -> bytes | None:
        """Gets the Large Blob stored for a single credential.

        :param large_blob_key: The largeBlobKey for the credential, or None.
        :returns: The decrypted and deflated value stored for the credential.
        """
        for entry in self.read_blob_array():
            try:
                compressed, orig_size = _lb_unpack(large_blob_key, entry)
                decompressed = _decompress(compressed)
                if len(decompressed) == orig_size:
                    return decompressed
            except (ValueError, zlib.error):
                continue
        return None

    def put_blob(self, large_blob_key: bytes, data: bytes | None) -> None:
        """Stores a Large Blob for a single credential.

        Any existing entries for the same credential will be replaced.

        :param large_blob_key: The largeBlobKey for the credential.
        :param data: The data to compress, encrypt and store.
        """
        modified = data is not None
        entries = []

        for entry in self.read_blob_array():
            try:
                _lb_unpack(large_blob_key, entry)
                modified = True
            except ValueError:
                entries.append(entry)

        if data is not None:
            entries.append(_lb_pack(large_blob_key, data))

        if modified:
            self.write_blob_array(entries)

    def delete_blob(self, large_blob_key: bytes) -> None:
        """Deletes any Large Blob(s) stored for a single credential.

        :param large_blob_key: The largeBlobKey for the credential.
        """
        self.put_blob(large_blob_key, None)
```

## File: fido2/ctap2/config.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import struct
from enum import IntEnum, unique
from typing import Any

from .. import cbor
from .base import Ctap2, Info
from .pin import PinProtocol, _PinUv


class Config:
    """Implementation of the CTAP2.1 Authenticator Config API.

    :param ctap: An instance of a CTAP2 object.
    :param pin_uv_protocol: An instance of a PinUvAuthProtocol.
    :param pin_uv_token: A valid PIN/UV Auth Token for the current CTAP session.
    """

    @unique
    class CMD(IntEnum):
        ENABLE_ENTERPRISE_ATT = 0x01
        TOGGLE_ALWAYS_UV = 0x02
        SET_MIN_PIN_LENGTH = 0x03
        VENDOR_PROTOTYPE = 0xFF

    @unique
    class PARAM(IntEnum):
        NEW_MIN_PIN_LENGTH = 0x01
        MIN_PIN_LENGTH_RPIDS = 0x02
        FORCE_CHANGE_PIN = 0x03

    @staticmethod
    def is_supported(info: Info) -> bool:
        return info.options.get("authnrCfg") is True

    def __init__(
        self,
        ctap: Ctap2,
        pin_uv_protocol: PinProtocol | None = None,
        pin_uv_token: bytes | None = None,
    ):
        if not self.is_supported(ctap.info):
            raise ValueError("Authenticator does not support Config")

        self.ctap = ctap
        self.pin_uv = (
            _PinUv(pin_uv_protocol, pin_uv_token)
            if pin_uv_protocol and pin_uv_token
            else None
        )

    def _call(self, sub_cmd, params=None):
        if self.pin_uv:
            msg = b"\xff" * 32 + b"\x0d" + struct.pack("<B", sub_cmd)
            if params is not None:
                msg += cbor.encode(params)
            pin_uv_protocol = self.pin_uv.protocol.VERSION
            pin_uv_param = self.pin_uv.protocol.authenticate(self.pin_uv.token, msg)
        else:
            pin_uv_protocol = None
            pin_uv_param = None
        return self.ctap.config(sub_cmd, params, pin_uv_protocol, pin_uv_param)

    def enable_enterprise_attestation(self) -> None:
        """Enables Enterprise Attestation.

        If already enabled, this command is ignored.
        """
        self._call(Config.CMD.ENABLE_ENTERPRISE_ATT)

    def toggle_always_uv(self) -> None:
        """Toggle the alwaysUV setting.

        When true, the Authenticator always requires UV for credential assertion.
        """
        self._call(Config.CMD.TOGGLE_ALWAYS_UV)

    def set_min_pin_length(
        self,
        min_pin_length: int | None = None,
        rp_ids: list[str] | None = None,
        force_change_pin: bool = False,
    ) -> None:
        """Set the minimum PIN length allowed when setting/changing the PIN.

        :param min_pin_length: The minimum PIN length the Authenticator should allow.
        :param rp_ids: A list of RP IDs which should be allowed to get the current
            minimum PIN length.
        :param force_change_pin: True if the Authenticator should enforce changing the
            PIN before the next use.
        """
        params: dict[int, Any] = {Config.PARAM.FORCE_CHANGE_PIN: force_change_pin}
        if min_pin_length is not None:
            params[Config.PARAM.NEW_MIN_PIN_LENGTH] = min_pin_length
        if rp_ids is not None:
            params[Config.PARAM.MIN_PIN_LENGTH_RPIDS] = rp_ids
        self._call(Config.CMD.SET_MIN_PIN_LENGTH, params)
```

## File: fido2/ctap2/credman.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import struct
from enum import IntEnum, unique
from typing import Any, Mapping, Sequence

from .. import cbor
from ..ctap import CtapError
from ..webauthn import (
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialUserEntity,
    _as_cbor,
)
from .base import Ctap2, Info
from .pin import PinProtocol, _PinUv

logger = logging.getLogger(__name__)


class CredentialManagement:
    """Implementation of a draft specification of the Credential Management API.
    WARNING: This specification is not final and this class is likely to change.

    :param ctap: An instance of a CTAP2 object.
    :param pin_uv_protocol: An instance of a PinUvAuthProtocol.
    :param pin_uv_token: A valid PIN/UV Auth Token for the current CTAP session.
    """

    @unique
    class CMD(IntEnum):
        GET_CREDS_METADATA = 0x01
        ENUMERATE_RPS_BEGIN = 0x02
        ENUMERATE_RPS_NEXT = 0x03
        ENUMERATE_CREDS_BEGIN = 0x04
        ENUMERATE_CREDS_NEXT = 0x05
        DELETE_CREDENTIAL = 0x06
        UPDATE_USER_INFO = 0x07

    @unique
    class PARAM(IntEnum):
        RP_ID_HASH = 0x01
        CREDENTIAL_ID = 0x02
        USER = 0x03

    @unique
    class RESULT(IntEnum):
        EXISTING_CRED_COUNT = 0x01
        MAX_REMAINING_COUNT = 0x02
        RP = 0x03
        RP_ID_HASH = 0x04
        TOTAL_RPS = 0x05
        USER = 0x06
        CREDENTIAL_ID = 0x07
        PUBLIC_KEY = 0x08
        TOTAL_CREDENTIALS = 0x09
        CRED_PROTECT = 0x0A
        LARGE_BLOB_KEY = 0x0B

    @staticmethod
    def is_supported(info: Info) -> bool:
        if info.options.get("credMgmt"):
            return True
        # We also support the Prototype command
        if "FIDO_2_1_PRE" in info.versions and "credentialMgmtPreview" in info.options:
            return True
        return False

    @staticmethod
    def is_update_supported(info: Info) -> bool:
        # Not supported in credentialMgmtPreview
        return bool(info.options.get("credMgmt"))

    @staticmethod
    def is_readonly_supported(info: Info) -> bool:
        return bool(info.options.get("perCredMgmtRO"))

    def __init__(
        self,
        ctap: Ctap2,
        pin_uv_protocol: PinProtocol,
        pin_uv_token: bytes,
    ):
        if not self.is_supported(ctap.info):
            raise ValueError("Authenticator does not support Credential Management")

        self.ctap = ctap
        self.pin_uv = _PinUv(pin_uv_protocol, pin_uv_token)

    def _call(self, sub_cmd, params=None, auth=True):
        kwargs = {"sub_cmd": sub_cmd, "sub_cmd_params": params}
        if auth:
            msg = struct.pack(">B", sub_cmd)
            if params is not None:
                msg += cbor.encode(params)
            kwargs["pin_uv_protocol"] = self.pin_uv.protocol.VERSION
            kwargs["pin_uv_param"] = self.pin_uv.protocol.authenticate(
                self.pin_uv.token, msg
            )
        return self.ctap.credential_mgmt(**kwargs)

    def get_metadata(self) -> Mapping[int, Any]:
        """Get credentials metadata.

        This returns the existing resident credentials count, and the max
        possible number of remaining resident credentials (the actual number of
        remaining credentials may depend on algorithm choice, etc).

        :return: A dict containing EXISTING_CRED_COUNT, and MAX_REMAINING_COUNT.
        """
        return self._call(CredentialManagement.CMD.GET_CREDS_METADATA)

    def enumerate_rps_begin(self) -> Mapping[int, Any]:
        """Start enumeration of RP entities of resident credentials.

        This will begin enumeration of stored RP entities, returning the first
        entity, as well as a count of the total number of entities stored.

        :return: A dict containing RP, RP_ID_HASH, and TOTAL_RPS.
        """
        return self._call(CredentialManagement.CMD.ENUMERATE_RPS_BEGIN)

    def enumerate_rps_next(self) -> Mapping[int, Any]:
        """Get the next RP entity stored.

        This continues enumeration of stored RP entities, returning the next
        entity.

        :return: A dict containing RP, and RP_ID_HASH.
        """
        return self._call(CredentialManagement.CMD.ENUMERATE_RPS_NEXT, auth=False)

    def enumerate_rps(self) -> Sequence[Mapping[int, Any]]:
        """Convenience method to enumerate all RPs.

        See enumerate_rps_begin and enumerate_rps_next for details.
        """
        try:
            first = self.enumerate_rps_begin()
        except CtapError as e:
            if e.code == CtapError.ERR.NO_CREDENTIALS:
                return []
            raise  # Other error
        n_rps = first[CredentialManagement.RESULT.TOTAL_RPS]
        if n_rps == 0:
            return []
        rest = [self.enumerate_rps_next() for _ in range(1, n_rps)]
        return [first] + rest

    def enumerate_creds_begin(self, rp_id_hash: bytes) -> Mapping[int, Any]:
        """Start enumeration of resident credentials.

        This will begin enumeration of resident credentials for a given RP,
        returning the first credential, as well as a count of the total number
        of resident credentials stored for the given RP.

        :param rp_id_hash: SHA256 hash of the RP ID.
        :return: A dict containing USER, CREDENTIAL_ID, PUBLIC_KEY, and
            TOTAL_CREDENTIALS.
        """
        return self._call(
            CredentialManagement.CMD.ENUMERATE_CREDS_BEGIN,
            {CredentialManagement.PARAM.RP_ID_HASH: rp_id_hash},
        )

    def enumerate_creds_next(self) -> Mapping[int, Any]:
        """Get the next resident credential stored.

        This continues enumeration of resident credentials, returning the next
        credential.

        :return: A dict containing USER, CREDENTIAL_ID, and PUBLIC_KEY.
        """
        return self._call(CredentialManagement.CMD.ENUMERATE_CREDS_NEXT, auth=False)

    def enumerate_creds(self, *args, **kwargs) -> Sequence[Mapping[int, Any]]:
        """Convenience method to enumerate all resident credentials for an RP.

        See enumerate_creds_begin and enumerate_creds_next for details.
        """
        try:
            first = self.enumerate_creds_begin(*args, **kwargs)
        except CtapError as e:
            if e.code == CtapError.ERR.NO_CREDENTIALS:
                return []
            raise  # Other error
        rest = [
            self.enumerate_creds_next()
            for _ in range(
                1, first.get(CredentialManagement.RESULT.TOTAL_CREDENTIALS, 1)
            )
        ]
        return [first] + rest

    def delete_cred(self, cred_id: PublicKeyCredentialDescriptor) -> None:
        """Delete a resident credential.

        :param cred_id: The PublicKeyCredentialDescriptor of the credential to delete.
        """
        cred_id = PublicKeyCredentialDescriptor.from_dict(cred_id)
        logger.debug(f"Deleting credential with ID: {cred_id}")
        self._call(
            CredentialManagement.CMD.DELETE_CREDENTIAL,
            {CredentialManagement.PARAM.CREDENTIAL_ID: _as_cbor(cred_id)},
        )
        logger.info("Credential deleted")

    def update_user_info(
        self,
        cred_id: PublicKeyCredentialDescriptor,
        user_info: PublicKeyCredentialUserEntity,
    ) -> None:
        """Update the user entity of a resident key.

        :param cred_id: The PublicKeyCredentialDescriptor of the credential to update.
        :param user_info: The user info update.
        """
        if not CredentialManagement.is_update_supported(self.ctap.info):
            raise ValueError("Authenticator does not support update_user_info")

        cred_id = PublicKeyCredentialDescriptor.from_dict(cred_id)
        user_info = PublicKeyCredentialUserEntity.from_dict(user_info)
        logger.debug(f"Updating credential: {cred_id} with user info: {user_info}")
        self._call(
            CredentialManagement.CMD.UPDATE_USER_INFO,
            {
                CredentialManagement.PARAM.CREDENTIAL_ID: _as_cbor(cred_id),
                CredentialManagement.PARAM.USER: _as_cbor(user_info),
            },
        )
        logger.info("Credential user info updated")
```

## File: fido2/ctap2/extensions.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Mapping, cast

from ..utils import _JsonDataObject, sha256, websafe_encode
from ..webauthn import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
    ResidentKeyRequirement,
)
from .base import AssertionResponse, AttestationResponse, Ctap2
from .blob import LargeBlobs
from .pin import ClientPin, PinProtocol


class ExtensionProcessor(abc.ABC):
    """Base class for CTAP2 extension processing.

    See: :class:`RegistrationExtensionProcessor` and
    :class:`AuthenticationExtensionProcessor`.
    """

    def __init__(
        self,
        permissions: ClientPin.PERMISSION = ClientPin.PERMISSION(0),
        inputs: dict[str, Any] | None = None,
        outputs: dict[str, Any] | None = None,
    ):
        self.permissions = permissions
        self._inputs = inputs
        self._outputs = outputs


class RegistrationExtensionProcessor(ExtensionProcessor):
    """Processing state for a CTAP2 extension, for single use.

    The ExtensionProcessor holds state and logic for client processing of an extension,
    for a registration (MakeCredential) call.

    :param permissions: PinUvAuthToken permissions required by the extension.
    :param inputs: Default authenticator inputs, if prepare_inputs is not overridden.
    :param outputs: Default client outputs, if prepare_outputs is not overridden.
    """

    def prepare_inputs(self, pin_token: bytes | None) -> dict[str, Any] | None:
        "Prepare authenticator extension inputs, to be passed to the Authenenticator."
        return self._inputs

    def prepare_outputs(
        self,
        response: AttestationResponse,
        pin_token: bytes | None,
    ) -> dict[str, Any] | None:
        "Prepare client extension outputs, to be returned to the caller."
        return self._outputs


class AuthenticationExtensionProcessor(ExtensionProcessor):
    """Processing state for a CTAP2 extension, for single use.

    The ExtensionProcessor holds state and logic for client processing of an extension,
    for an authentication (GetAssertion) call.

    :param permissions: PinUvAuthToken permissions required by the extension.
    :param inputs: Default authenticator inputs, if prepare_inputs is not overridden.
    :param outputs: Default client outputs, if prepare_outputs is not overridden.
    """

    def prepare_inputs(
        self,
        selected: PublicKeyCredentialDescriptor | None,
        pin_token: bytes | None,
    ) -> dict[str, Any] | None:
        "Prepare authenticator extension inputs, to be passed to the Authenenticator."
        return self._inputs

    def prepare_outputs(
        self,
        response: AssertionResponse,
        pin_token: bytes | None,
    ) -> dict[str, Any] | None:
        "Prepare client extension outputs, to be returned to the caller."
        return self._outputs


class Ctap2Extension(abc.ABC):
    """Base class for CTAP2 extensions.

    As of python-fido2 1.2 these instances can be used for multiple requests and
    should be invoked via the make_credential and get_assertion methods.
    Subclasses are instantiated for a single request, if the Authenticator supports
    the extension.
    """

    @abc.abstractmethod
    def is_supported(self, ctap: Ctap2) -> bool:
        """Whether or not the extension is supported by the authenticator."""

    def make_credential(
        self,
        ctap: Ctap2,
        options: PublicKeyCredentialCreationOptions,
        pin_protocol: PinProtocol | None,
    ) -> RegistrationExtensionProcessor | None:
        """Start client extension processing for registration."""
        return None

    def get_assertion(
        self,
        ctap: Ctap2,
        options: PublicKeyCredentialRequestOptions,
        pin_protocol: PinProtocol | None,
    ) -> AuthenticationExtensionProcessor | None:
        """Start client extension processing for authentication."""
        return None


@dataclass(eq=False, frozen=True)
class HMACGetSecretInput(_JsonDataObject):
    """Client inputs for hmac-secret."""

    salt1: bytes
    salt2: bytes | None = None


@dataclass(eq=False, frozen=True)
class HMACGetSecretOutput(_JsonDataObject):
    """Client outputs for hmac-secret."""

    output1: bytes
    output2: bytes | None = None


def _prf_salt(secret):
    return sha256(b"WebAuthn PRF\0" + secret)


@dataclass(eq=False, frozen=True)
class AuthenticatorExtensionsPRFValues(_JsonDataObject):
    """Salt values for use with prf."""

    first: bytes
    second: bytes | None = None


@dataclass(eq=False, frozen=True)
class AuthenticatorExtensionsPRFInputs(_JsonDataObject):
    """Client inputs for prf."""

    eval: AuthenticatorExtensionsPRFValues | None = None
    eval_by_credential: Mapping[str, AuthenticatorExtensionsPRFValues] | None = None


@dataclass(eq=False, frozen=True)
class AuthenticatorExtensionsPRFOutputs(_JsonDataObject):
    """Client outputs for prf."""

    enabled: bool | None = None
    results: AuthenticatorExtensionsPRFValues | None = None


def _hmac_prepare_salts(allow_list, selected, prf, hmac):
    if prf:
        secrets = prf.eval
        by_creds = prf.eval_by_credential
        if by_creds:
            # Make sure all keys are valid IDs from allow_credentials
            if not allow_list:
                raise ValueError("evalByCredentials requires allowCredentials")
            ids = {websafe_encode(c.id) for c in allow_list}
            if not ids.issuperset(by_creds):
                raise ValueError("evalByCredentials contains invalid key")
            if selected:
                key = websafe_encode(selected.id)
                if key in by_creds:
                    secrets = by_creds[key]

        if not secrets:
            return

        salts = (
            _prf_salt(secrets.first),
            (_prf_salt(secrets.second) if secrets.second is not None else b""),
        )
    elif hmac:
        salts = hmac.salt1, hmac.salt2 or b""
    else:
        return

    if not (
        len(salts[0]) == HmacSecretExtension.SALT_LEN
        and (not salts[1] or len(salts[1]) == HmacSecretExtension.SALT_LEN)
    ):
        raise ValueError("Invalid salt length")

    return salts


def _hmac_format_outputs(enabled, decrypted, prf):
    output1 = decrypted[: HmacSecretExtension.SALT_LEN] if decrypted else None
    output2 = decrypted[HmacSecretExtension.SALT_LEN :] if decrypted else None

    if prf:
        result = AuthenticatorExtensionsPRFOutputs(
            enabled=enabled,
            results=(
                AuthenticatorExtensionsPRFValues(output1, output2) if output1 else None
            ),
        )
        # If result has no content, don't add an entry for it
        return {"prf": result} if result else None
    else:
        outputs = {}
        if enabled is not None:
            outputs["hmacCreateSecret"] = enabled
        if output1:
            outputs["hmacGetSecret"] = HMACGetSecretOutput(output1, output2)
        return outputs or None


class HmacSecretExtension(Ctap2Extension):
    """
    Implements the Pseudo-random function (prf) and the hmac-secret CTAP2 extensions.

    The hmac-secret extension is not directly available to clients by default, instead
    the prf extension is used.

    https://www.w3.org/TR/webauthn-3/#prf-extension

    https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#sctn-hmac-secret-extension

    :param allow_hmac_secret: Set to True to allow hmac-secret, in addition to prf.
    """

    NAME = "hmac-secret"
    MC_NAME = "hmac-secret-mc"
    SALT_LEN = 32

    def __init__(self, allow_hmac_secret=False):
        self._allow_hmac_secret = allow_hmac_secret

    def is_supported(self, ctap):
        return self.NAME in ctap.info.extensions

    def make_credential(self, ctap, options, pin_protocol):
        c_inputs = options.extensions or {}
        prf = c_inputs.get("prf") is not None
        hmac = self._allow_hmac_secret and c_inputs.get("hmacCreateSecret") is True
        if pin_protocol and self.is_supported(ctap) and (prf or hmac):
            inputs: dict[str, Any] = {HmacSecretExtension.NAME: True}
            shared_secret = None
            if self.MC_NAME in ctap.info.extensions:
                prf_salts = AuthenticatorExtensionsPRFInputs.from_dict(
                    cast(Mapping | None, c_inputs.get("prf"))
                )
                hmac_salts = (
                    HMACGetSecretInput.from_dict(
                        cast(Mapping | None, c_inputs.get("hmacGetSecret"))
                    )
                    if hmac
                    else None
                )
                salts = _hmac_prepare_salts(None, None, prf_salts, hmac_salts)
                if salts:
                    client_pin = ClientPin(ctap, pin_protocol)
                    key_agreement, shared_secret = client_pin._get_shared_secret()
                    salt_enc = pin_protocol.encrypt(shared_secret, salts[0] + salts[1])
                    salt_auth = pin_protocol.authenticate(shared_secret, salt_enc)
                    inputs[HmacSecretExtension.MC_NAME] = {
                        1: key_agreement,
                        2: salt_enc,
                        3: salt_auth,
                        4: pin_protocol.VERSION,
                    }

            class Processor(RegistrationExtensionProcessor):
                def prepare_inputs(self, pin_token):
                    return inputs

                def prepare_outputs(self, response, pin_token):
                    extensions = response.auth_data.extensions or {}
                    enabled = extensions.get(HmacSecretExtension.NAME, False)
                    value = extensions.get(HmacSecretExtension.MC_NAME)
                    decrypted = (
                        pin_protocol.decrypt(shared_secret, value)
                        if value and shared_secret
                        else None
                    )
                    return _hmac_format_outputs(enabled, decrypted, prf)

            return Processor()

    def get_assertion(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        prf = AuthenticatorExtensionsPRFInputs.from_dict(
            cast(Mapping | None, inputs.get("prf"))
        )
        hmac = (
            HMACGetSecretInput.from_dict(
                cast(Mapping | None, inputs.get("hmacGetSecret"))
            )
            if self._allow_hmac_secret
            else None
        )

        if pin_protocol and self.is_supported(ctap) and (prf or hmac):
            client_pin = ClientPin(ctap, pin_protocol)
            key_agreement, shared_secret = client_pin._get_shared_secret()

            class Processing(AuthenticationExtensionProcessor):
                def prepare_inputs(self, selected, pin_token):
                    salts = _hmac_prepare_salts(
                        options.allow_credentials, selected, prf, hmac
                    )
                    if not salts:
                        return

                    salt_enc = pin_protocol.encrypt(shared_secret, salts[0] + salts[1])
                    salt_auth = pin_protocol.authenticate(shared_secret, salt_enc)

                    return {
                        HmacSecretExtension.NAME: {
                            1: key_agreement,
                            2: salt_enc,
                            3: salt_auth,
                            4: pin_protocol.VERSION,
                        }
                    }

                def prepare_outputs(self, response, pin_token):
                    extensions = response.auth_data.extensions or {}
                    value = extensions.get(HmacSecretExtension.NAME)
                    decrypted = (
                        pin_protocol.decrypt(shared_secret, value) if value else None
                    )
                    return _hmac_format_outputs(None, decrypted, prf)

            return Processing()


@dataclass(eq=False, frozen=True)
class AuthenticatorExtensionsLargeBlobInputs(_JsonDataObject):
    """Client inputs for largeBlob."""

    support: str | None = None
    read: bool | None = None
    write: bytes | None = None


@dataclass(eq=False, frozen=True)
class AuthenticatorExtensionsLargeBlobOutputs(_JsonDataObject):
    """Client outputs for largeBlob."""

    supported: bool | None = None
    blob: bytes | None = None
    written: bool | None = None


class LargeBlobExtension(Ctap2Extension):
    """
    Implements the Large Blob storage (largeBlob) WebAuthn extension.

    https://www.w3.org/TR/webauthn-3/#sctn-large-blob-extension
    """

    NAME = "largeBlobKey"

    def is_supported(self, ctap):
        return self.NAME in ctap.info.extensions and ctap.info.options.get(
            "largeBlobs", False
        )

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        data = AuthenticatorExtensionsLargeBlobInputs.from_dict(
            cast(Mapping | None, inputs.get("largeBlob"))
        )
        if data:
            if data.read or data.write:
                raise ValueError("Invalid set of parameters")
            if data.support == "required" and not self.is_supported(ctap):
                raise ValueError("Authenticator does not support large blob storage")

            class Processor(RegistrationExtensionProcessor):
                def prepare_inputs(self, pin_token):
                    return {LargeBlobExtension.NAME: True}

                def prepare_outputs(self, response, pin_token):
                    return {
                        "largeBlob": AuthenticatorExtensionsLargeBlobOutputs(
                            supported=response.large_blob_key is not None
                        )
                    }

            return Processor()

    def get_assertion(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        data = AuthenticatorExtensionsLargeBlobInputs.from_dict(
            cast(Mapping | None, inputs.get("largeBlob"))
        )
        if data:
            if data.support or (data.read and data.write):
                raise ValueError("Invalid set of parameters")
            if not self.is_supported(ctap):
                raise ValueError("Authenticator does not support large blob storage")

            class Processor(AuthenticationExtensionProcessor):
                def prepare_outputs(self, response, pin_token):
                    assert data is not None  # noqa: S101 needed for mypy
                    blob_key = response.large_blob_key
                    if blob_key:
                        if data.read:
                            large_blobs = LargeBlobs(ctap)
                            blob = large_blobs.get_blob(blob_key)
                            return {
                                "largeBlob": AuthenticatorExtensionsLargeBlobOutputs(
                                    blob=blob
                                )
                            }
                        elif data.write:
                            large_blobs = LargeBlobs(ctap, pin_protocol, pin_token)
                            large_blobs.put_blob(blob_key, data.write)
                            return {
                                "largeBlob": AuthenticatorExtensionsLargeBlobOutputs(
                                    written=True
                                )
                            }

            return Processor(
                (
                    ClientPin.PERMISSION.LARGE_BLOB_WRITE
                    if data.write
                    else ClientPin.PERMISSION(0)
                ),
                inputs={LargeBlobExtension.NAME: True},
            )


class CredBlobExtension(Ctap2Extension):
    """
    Implements the Credential Blob (credBlob) CTAP2 extension.

    https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#sctn-credBlob-extension
    """

    NAME = "credBlob"

    def is_supported(self, ctap):
        return self.NAME in ctap.info.extensions

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        if self.is_supported(ctap):
            blob = inputs.get("credBlob")
            assert ctap.info.max_cred_blob_length is not None  # noqa: S101
            if blob and len(blob) <= ctap.info.max_cred_blob_length:
                return RegistrationExtensionProcessor(inputs={self.NAME: blob})

    def get_assertion(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        if self.is_supported(ctap) and inputs.get("getCredBlob") is True:
            return AuthenticationExtensionProcessor(inputs={self.NAME: True})


class CredProtectExtension(Ctap2Extension):
    """
    Implements the Credential Protection CTAP2 extension.

    https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#sctn-credProtect-extension
    """

    @unique
    class POLICY(Enum):
        OPTIONAL = "userVerificationOptional"
        OPTIONAL_WITH_LIST = "userVerificationOptionalWithCredentialIDList"
        REQUIRED = "userVerificationRequired"

    NAME = "credProtect"

    def is_supported(self, ctap):
        return self.NAME in ctap.info.extensions

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        policy = inputs.get("credentialProtectionPolicy")
        if policy:
            index = list(CredProtectExtension.POLICY).index(
                CredProtectExtension.POLICY(policy)
            )
            enforce = inputs.get("enforceCredentialProtectionPolicy", False)
            if enforce and not self.is_supported(ctap) and index > 0:
                raise ValueError("Authenticator does not support Credential Protection")

            return RegistrationExtensionProcessor(inputs={self.NAME: index + 1})


class MinPinLengthExtension(Ctap2Extension):
    """
    Implements the Minimum PIN Length (minPinLength) CTAP2 extension.

    https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#sctn-minpinlength-extension
    """

    NAME = "minPinLength"

    def is_supported(self, ctap):
        # NB: There is no key in the extensions field.
        return "setMinPINLength" in ctap.info.options

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        if self.is_supported(ctap) and inputs.get(self.NAME) is True:
            return RegistrationExtensionProcessor(inputs={self.NAME: True})


@dataclass(eq=False, frozen=True)
class CredentialPropertiesOutput(_JsonDataObject):
    """Client outputs for credProps."""

    rk: bool | None = None


class CredPropsExtension(Ctap2Extension):
    """
    Implements the Credential Properties (credProps) WebAuthn extension.

    https://www.w3.org/TR/webauthn-3/#sctn-authenticator-credential-properties-extension
    """

    NAME = "credProps"

    def is_supported(self, ctap):
        # NB: There is no key in the extensions field.
        return True

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        if inputs.get(self.NAME) is True:
            selection = (
                options.authenticator_selection or AuthenticatorSelectionCriteria()
            )
            rk = selection.resident_key == ResidentKeyRequirement.REQUIRED or (
                selection.resident_key == ResidentKeyRequirement.PREFERRED
                and ctap.info.options.get("rk")
            )

            return RegistrationExtensionProcessor(
                outputs={self.NAME: CredentialPropertiesOutput(rk=rk)}
            )


@dataclass(eq=False, frozen=True)
class PaymentCurrencyAmount(_JsonDataObject):
    currency: str
    value: str


@dataclass(eq=False, frozen=True)
class PaymentCredentialInstrument(_JsonDataObject):
    display_name: str
    icon: str
    icon_must_be_shown: bool = True


@dataclass(eq=False, frozen=True)
class AuthenticationExtensionsPaymentInputs(_JsonDataObject):
    """Client inputs for payment."""

    is_payment: bool | None = None
    rp_id: str | None = None
    top_origin: str | None = None
    payee_name: str | None = None
    payee_origin: str | None = None
    total: PaymentCurrencyAmount | None = None
    instrument: PaymentCredentialInstrument | None = None


class ThirdPartyPaymentExtension(Ctap2Extension):
    """
    Implements the Third Party Payment (thirdPartyPayment) CTAP2.2 extension.

    https://fidoalliance.org/specs/fido-v2.2-ps-20250228/fido-client-to-authenticator-protocol-v2.2-ps-20250228.html#sctn-thirdPartyPayment-extension

    Note that most of the processing for the WebAuthn extension needs to be done by the
    client, see:
    https://www.w3.org/TR/secure-payment-confirmation/#sctn-collectedclientpaymentdata-dictionary

    As such, this extension is not included in the default extensions list, and should
    not be used without a client that supports the WebAuthn payment extension.
    """

    NAME = "thirdPartyPayment"

    def is_supported(self, ctap):
        return self.NAME in ctap.info.extensions

    def make_credential(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        data = AuthenticationExtensionsPaymentInputs.from_dict(
            cast(Mapping | None, inputs.get("payment"))
        )
        if self.is_supported(ctap) and data and data.is_payment:
            return RegistrationExtensionProcessor(inputs={self.NAME: True})

    def get_assertion(self, ctap, options, pin_protocol):
        inputs = options.extensions or {}
        data = AuthenticationExtensionsPaymentInputs.from_dict(
            cast(Mapping | None, inputs.get("payment"))
        )
        if self.is_supported(ctap) and data and data.is_payment:
            return AuthenticationExtensionProcessor(inputs={self.NAME: True})


_DEFAULT_EXTENSIONS = [
    HmacSecretExtension(),
    LargeBlobExtension(),
    CredBlobExtension(),
    CredProtectExtension(),
    MinPinLengthExtension(),
    CredPropsExtension(),
]
```

## File: fido2/ctap2/pin.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
import logging
import os
from dataclasses import dataclass
from enum import IntEnum, IntFlag, unique
from threading import Event
from typing import Any, Callable, ClassVar, Mapping

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from ..cose import CoseKey
from ..utils import bytes2int, hmac_sha256, int2bytes, sha256
from .base import Ctap2

logger = logging.getLogger(__name__)


def _pad_pin(pin: str) -> bytes:
    if not isinstance(pin, str):
        raise ValueError(f"PIN of wrong type, expecting {str}")
    if len(pin) < 4:
        raise ValueError("PIN must be >= 4 characters")
    pin_padded = pin.encode().ljust(64, b"\0")
    pin_padded += b"\0" * (-(len(pin_padded) - 16) % 16)
    if len(pin_padded) > 255:
        raise ValueError("PIN must be <= 255 bytes")
    return pin_padded


class PinProtocol(abc.ABC):
    VERSION: ClassVar[int]

    @abc.abstractmethod
    def encapsulate(self, peer_cose_key: CoseKey) -> tuple[Mapping[int, Any], bytes]:
        """Generates an encapsulation of the public key.
        Returns the message to transmit and the shared secret.
        """

    @abc.abstractmethod
    def encrypt(self, key: bytes, plaintext: bytes) -> bytes:
        """Encrypts data"""

    @abc.abstractmethod
    def decrypt(self, key: bytes, ciphertext: bytes) -> bytes:
        """Decrypts encrypted data"""

    @abc.abstractmethod
    def authenticate(self, key: bytes, message: bytes) -> bytes:
        """Computes a MAC of the given message."""

    @abc.abstractmethod
    def validate_token(self, token: bytes) -> bytes:
        """Validates that a token is well-formed.
        Returns the token, or if invalid, raises a ValueError.
        """


@dataclass
class _PinUv:
    protocol: PinProtocol
    token: bytes


class PinProtocolV1(PinProtocol):
    """Implementation of the CTAP2 PIN/UV protocol v1.

    :param ctap: An instance of a CTAP2 object.
    :cvar VERSION: The version number of the PIV/UV protocol.
    :cvar IV: An all-zero IV used for some cryptographic operations.
    """

    VERSION = 1
    IV = b"\x00" * 16

    def kdf(self, z: bytes) -> bytes:
        return sha256(z)

    def encapsulate(self, peer_cose_key):
        be = default_backend()
        sk = ec.generate_private_key(ec.SECP256R1(), be)
        pn = sk.public_key().public_numbers()
        key_agreement = {
            1: 2,
            3: -25,  # Per the spec, "although this is NOT the algorithm actually used"
            -1: 1,
            -2: int2bytes(pn.x, 32),
            -3: int2bytes(pn.y, 32),
        }

        x = bytes2int(peer_cose_key[-2])
        y = bytes2int(peer_cose_key[-3])
        pk = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key(be)
        shared_secret = self.kdf(sk.exchange(ec.ECDH(), pk))  # x-coordinate, 32b
        return key_agreement, shared_secret

    def _get_cipher_v1(self, secret):
        be = default_backend()
        return Cipher(algorithms.AES(secret), modes.CBC(PinProtocolV1.IV), be)

    def encrypt(self, key, plaintext):
        cipher = self._get_cipher_v1(key)
        enc = cipher.encryptor()
        return enc.update(plaintext) + enc.finalize()

    def decrypt(self, key, ciphertext):
        cipher = self._get_cipher_v1(key)
        dec = cipher.decryptor()
        return dec.update(ciphertext) + dec.finalize()

    def authenticate(self, key, message):
        return hmac_sha256(key, message)[:16]

    def validate_token(self, token):
        if len(token) not in (16, 32):
            raise ValueError("PIN/UV token must be 16 or 32 bytes")
        return token


class PinProtocolV2(PinProtocolV1):
    """Implementation of the CTAP2 PIN/UV protocol v2.

    :param ctap: An instance of a CTAP2 object.
    :cvar VERSION: The version number of the PIV/UV protocol.
    :cvar IV: An all-zero IV used for some cryptographic operations.
    """

    VERSION = 2
    HKDF_SALT = b"\x00" * 32
    HKDF_INFO_HMAC = b"CTAP2 HMAC key"
    HKDF_INFO_AES = b"CTAP2 AES key"

    def kdf(self, z):
        be = default_backend()
        hmac_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=PinProtocolV2.HKDF_SALT,
            info=PinProtocolV2.HKDF_INFO_HMAC,
            backend=be,
        ).derive(z)
        aes_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=PinProtocolV2.HKDF_SALT,
            info=PinProtocolV2.HKDF_INFO_AES,
            backend=be,
        ).derive(z)
        return hmac_key + aes_key

    def _get_cipher_v2(self, secret, iv):
        be = default_backend()
        return Cipher(algorithms.AES(secret), modes.CBC(iv), be)

    def encrypt(self, key, plaintext):
        aes_key = key[32:]
        iv = os.urandom(16)

        cipher = self._get_cipher_v2(aes_key, iv)
        enc = cipher.encryptor()
        return iv + enc.update(plaintext) + enc.finalize()

    def decrypt(self, key, ciphertext):
        aes_key = key[32:]
        iv, ciphertext = ciphertext[:16], ciphertext[16:]
        cipher = self._get_cipher_v2(aes_key, iv)
        dec = cipher.decryptor()
        return dec.update(ciphertext) + dec.finalize()

    def authenticate(self, key, message):
        hmac_key = key[:32]
        return hmac_sha256(hmac_key, message)

    def validate_token(self, token):
        if len(token) != 32:
            raise ValueError("PIN/UV token must be 32 bytes")
        return token


class ClientPin:
    """Implementation of the CTAP2 Client PIN API.

    :param ctap: An instance of a CTAP2 object.
    :param protocol: An optional instance of a PinUvAuthProtocol object. If None is
        provided then the latest protocol supported by both library and Authenticator
        will be used.
    """

    PROTOCOLS = [PinProtocolV2, PinProtocolV1]

    @unique
    class CMD(IntEnum):
        GET_PIN_RETRIES = 0x01
        GET_KEY_AGREEMENT = 0x02
        SET_PIN = 0x03
        CHANGE_PIN = 0x04
        GET_TOKEN_USING_PIN_LEGACY = 0x05
        GET_TOKEN_USING_UV = 0x06
        GET_UV_RETRIES = 0x07
        GET_TOKEN_USING_PIN = 0x09

    @unique
    class RESULT(IntEnum):
        KEY_AGREEMENT = 0x01
        PIN_UV_TOKEN = 0x02
        PIN_RETRIES = 0x03
        POWER_CYCLE_STATE = 0x04
        UV_RETRIES = 0x05

    @unique
    class PERMISSION(IntFlag):
        MAKE_CREDENTIAL = 0x01
        GET_ASSERTION = 0x02
        CREDENTIAL_MGMT = 0x04
        BIO_ENROLL = 0x08
        LARGE_BLOB_WRITE = 0x10
        AUTHENTICATOR_CFG = 0x20
        PERSISTENT_CREDENTIAL_MGMT = 0x40

    @staticmethod
    def is_supported(info):
        """Checks if ClientPin functionality is supported.

        Note that the ClientPin function is still usable without support for client
        PIN functionality, as UV token may still be supported.
        """
        return "clientPin" in info.options

    @staticmethod
    def is_token_supported(info):
        """Checks if pinUvAuthToken is supported."""
        return info.options.get("pinUvAuthToken") is True

    def __init__(self, ctap: Ctap2, protocol: PinProtocol | None = None):
        self.ctap = ctap
        if protocol is None:
            for proto in ClientPin.PROTOCOLS:
                if proto.VERSION in ctap.info.pin_uv_protocols:
                    self.protocol: PinProtocol = proto()
                    break
            else:
                raise ValueError("No compatible PIN/UV protocols supported!")
        else:
            self.protocol = protocol

    def _get_shared_secret(self):
        resp = self.ctap.client_pin(
            self.protocol.VERSION, ClientPin.CMD.GET_KEY_AGREEMENT
        )
        pk = resp[ClientPin.RESULT.KEY_AGREEMENT]

        return self.protocol.encapsulate(pk)

    def get_pin_token(
        self,
        pin: str,
        permissions: ClientPin.PERMISSION | None = None,
        permissions_rpid: str | None = None,
    ) -> bytes:
        """Get a PIN/UV token from the authenticator using PIN.

        :param pin: The PIN of the authenticator.
        :param permissions: The permissions to associate with the token.
        :param permissions_rpid: The permissions RPID to associate with the token.
        :return: A PIN/UV token.
        """
        if not ClientPin.is_supported(self.ctap.info):
            raise ValueError("Authenticator does not support get_pin_token")

        key_agreement, shared_secret = self._get_shared_secret()

        pin_hash = sha256(pin.encode())[:16]
        pin_hash_enc = self.protocol.encrypt(shared_secret, pin_hash)

        if ClientPin.is_token_supported(self.ctap.info) and permissions:
            cmd = ClientPin.CMD.GET_TOKEN_USING_PIN
        else:
            cmd = ClientPin.CMD.GET_TOKEN_USING_PIN_LEGACY
            # Ignore permissions if not supported
            permissions = None
            permissions_rpid = None

        resp = self.ctap.client_pin(
            self.protocol.VERSION,
            cmd,
            key_agreement=key_agreement,
            pin_hash_enc=pin_hash_enc,
            permissions=permissions,
            permissions_rpid=permissions_rpid,
        )
        pin_token_enc = resp[ClientPin.RESULT.PIN_UV_TOKEN]
        logger.debug(f"Got PIN token for permissions: {permissions}")
        return self.protocol.validate_token(
            self.protocol.decrypt(shared_secret, pin_token_enc)
        )

    def get_uv_token(
        self,
        permissions: ClientPin.PERMISSION | None = None,
        permissions_rpid: str | None = None,
        event: Event | None = None,
        on_keepalive: Callable[[int], None] | None = None,
    ) -> bytes:
        """Get a PIN/UV token from the authenticator using built-in UV.

        :param permissions: The permissions to associate with the token.
        :param permissions_rpid: The permissions RPID to associate with the token.
        :param event: An optional threading.Event which can be used to cancel
            the invocation.
        :param on_keepalive: An optional callback to handle keep-alive messages
            from the authenticator. The function is only called once for
            consecutive keep-alive messages with the same status.
        :return: A PIN/UV token.
        """
        if not ClientPin.is_token_supported(self.ctap.info):
            raise ValueError("Authenticator does not support get_uv_token")

        key_agreement, shared_secret = self._get_shared_secret()

        resp = self.ctap.client_pin(
            self.protocol.VERSION,
            ClientPin.CMD.GET_TOKEN_USING_UV,
            key_agreement=key_agreement,
            permissions=permissions,
            permissions_rpid=permissions_rpid,
            event=event,
            on_keepalive=on_keepalive,
        )

        pin_token_enc = resp[ClientPin.RESULT.PIN_UV_TOKEN]
        logger.debug(f"Got UV token for permissions: {permissions}")
        return self.protocol.validate_token(
            self.protocol.decrypt(shared_secret, pin_token_enc)
        )

    def get_pin_retries(self) -> tuple[int, int | None]:
        """Get the number of PIN retries remaining.

        :return: A tuple of the number of PIN attempts remaining until the
        authenticator is locked, and the power cycle state, if available.
        """
        resp = self.ctap.client_pin(
            self.protocol.VERSION, ClientPin.CMD.GET_PIN_RETRIES
        )
        return (
            resp[ClientPin.RESULT.PIN_RETRIES],
            resp.get(ClientPin.RESULT.POWER_CYCLE_STATE),
        )

    def get_uv_retries(self) -> int:
        """Get the number of UV retries remaining.

        :return: A tuple of the number of UV attempts remaining until the
        authenticator is locked, and the power cycle state, if available.
        """
        resp = self.ctap.client_pin(self.protocol.VERSION, ClientPin.CMD.GET_UV_RETRIES)
        return resp[ClientPin.RESULT.UV_RETRIES]

    def set_pin(self, pin: str) -> None:
        """Set the PIN of the autenticator.

        This only works when no PIN is set. To change the PIN when set, use
        change_pin.

        :param pin: A PIN to set.
        """
        if not ClientPin.is_supported(self.ctap.info):
            raise ValueError("Authenticator does not support ClientPin")

        key_agreement, shared_secret = self._get_shared_secret()

        pin_enc = self.protocol.encrypt(shared_secret, _pad_pin(pin))
        pin_uv_param = self.protocol.authenticate(shared_secret, pin_enc)
        self.ctap.client_pin(
            self.protocol.VERSION,
            ClientPin.CMD.SET_PIN,
            key_agreement=key_agreement,
            new_pin_enc=pin_enc,
            pin_uv_param=pin_uv_param,
        )
        logger.info("PIN has been set")

    def change_pin(self, old_pin: str, new_pin: str) -> None:
        """Change the PIN of the authenticator.

        This only works when a PIN is already set. If no PIN is set, use
        set_pin.

        :param old_pin: The currently set PIN.
        :param new_pin: The new PIN to set.
        """
        if not ClientPin.is_supported(self.ctap.info):
            raise ValueError("Authenticator does not support ClientPin")

        key_agreement, shared_secret = self._get_shared_secret()

        pin_hash = sha256(old_pin.encode())[:16]
        pin_hash_enc = self.protocol.encrypt(shared_secret, pin_hash)
        new_pin_enc = self.protocol.encrypt(shared_secret, _pad_pin(new_pin))
        pin_uv_param = self.protocol.authenticate(
            shared_secret, new_pin_enc + pin_hash_enc
        )
        self.ctap.client_pin(
            self.protocol.VERSION,
            ClientPin.CMD.CHANGE_PIN,
            key_agreement=key_agreement,
            pin_hash_enc=pin_hash_enc,
            new_pin_enc=new_pin_enc,
            pin_uv_param=pin_uv_param,
        )
        logger.info("PIN has been changed")
```

## File: fido2/hid/__init__.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import os
import struct
import sys
from enum import IntEnum, IntFlag, unique
from threading import Event
from typing import Callable, Iterator

from ..ctap import STATUS, CtapDevice, CtapError
from ..utils import LOG_LEVEL_TRAFFIC
from .base import CtapHidConnection, HidDescriptor

logger = logging.getLogger(__name__)


if sys.platform == "linux":
    from . import linux as backend
elif sys.platform == "win32":
    from . import windows as backend
elif sys.platform == "darwin":
    from . import macos as backend
elif sys.platform == "freebsd":
    from . import freebsd as backend
elif sys.platform == "netbsd":
    from . import netbsd as backend
elif sys.platform == "openbsd":
    from . import openbsd as backend
else:
    raise Exception("Unsupported platform")


list_descriptors = backend.list_descriptors
get_descriptor = backend.get_descriptor
open_connection = backend.open_connection


class ConnectionFailure(Exception):
    """The CTAP connection failed or returned an invalid response."""


@unique
class CTAPHID(IntEnum):
    PING = 0x01
    MSG = 0x03
    LOCK = 0x04
    INIT = 0x06
    WINK = 0x08
    CBOR = 0x10
    CANCEL = 0x11

    ERROR = 0x3F
    KEEPALIVE = 0x3B

    VENDOR_FIRST = 0x40


@unique
class CAPABILITY(IntFlag):
    WINK = 0x01
    LOCK = 0x02  # Not used
    CBOR = 0x04
    NMSG = 0x08

    def supported(self, flags: CAPABILITY) -> bool:
        return bool(flags & self)


TYPE_INIT = 0x80


class CtapHidDevice(CtapDevice):
    """
    CtapDevice implementation using the HID transport.

    :cvar descriptor: Device descriptor.
    """

    def __init__(self, descriptor: HidDescriptor, connection: CtapHidConnection):
        self.descriptor = descriptor
        self._packet_size = descriptor.report_size_out
        self._connection = connection

        nonce = os.urandom(8)
        self._channel_id = 0xFFFFFFFF
        response = self.call(CTAPHID.INIT, nonce)
        r_nonce, response = response[:8], response[8:]
        if r_nonce != nonce:
            raise ConnectionFailure("Wrong nonce")
        (
            self._channel_id,
            self._u2fhid_version,
            v1,
            v2,
            v3,
            self._capabilities,
        ) = struct.unpack_from(">IBBBBB", response)
        self._device_version = (v1, v2, v3)

    def __repr__(self):
        return f"CtapHidDevice({self.descriptor.path!r})"

    @property
    def version(self) -> int:
        """CTAP HID protocol version."""
        return self._u2fhid_version

    @property
    def device_version(self) -> tuple[int, int, int]:
        """Device version number."""
        return self._device_version

    @property
    def capabilities(self) -> int:
        """Capabilities supported by the device."""
        return self._capabilities

    @property
    def product_name(self) -> str | None:
        """Product name of device."""
        return self.descriptor.product_name

    @property
    def serial_number(self) -> str | None:
        """Serial number of device."""
        return self.descriptor.serial_number

    def _send_cancel(self):
        packet = struct.pack(">IB", self._channel_id, TYPE_INIT | CTAPHID.CANCEL).ljust(
            self._packet_size, b"\0"
        )
        logger.log(LOG_LEVEL_TRAFFIC, "SEND: %s", packet.hex())
        self._connection.write_packet(packet)

    def call(
        self,
        cmd: int,
        data: bytes = b"",
        event: Event | None = None,
        on_keepalive: Callable[[STATUS], None] | None = None,
    ) -> bytes:
        event = event or Event()

        while True:
            try:
                return self._do_call(cmd, data, event, on_keepalive)
            except CtapError as e:
                if e.code == CtapError.ERR.CHANNEL_BUSY:
                    if not event.wait(0.1):
                        logger.warning("CTAP channel busy, trying again...")
                        continue  # Keep retrying on BUSY while not cancelled
                raise

    def _do_call(self, cmd, data, event, on_keepalive):
        remaining = data
        seq = 0

        # Send request
        header = struct.pack(">IBH", self._channel_id, TYPE_INIT | cmd, len(remaining))
        while remaining or seq == 0:
            size = min(len(remaining), self._packet_size - len(header))
            body, remaining = remaining[:size], remaining[size:]
            packet = header + body
            logger.log(LOG_LEVEL_TRAFFIC, "SEND: %s", packet.hex())
            self._connection.write_packet(packet.ljust(self._packet_size, b"\0"))
            header = struct.pack(">IB", self._channel_id, 0x7F & seq)
            seq += 1

        try:
            # Read response
            seq = 0
            r_len = 0
            response = b""
            last_ka = None
            while True:
                if event.is_set():
                    # Cancel
                    logger.debug("Sending cancel...")
                    self._send_cancel()

                recv = self._connection.read_packet()
                logger.log(LOG_LEVEL_TRAFFIC, "RECV: %s", recv.hex())

                r_channel = struct.unpack_from(">I", recv)[0]
                recv = recv[4:]
                if r_channel != self._channel_id:
                    raise ConnectionFailure("Wrong channel")

                if not response:  # Initialization packet
                    r_cmd, r_len = struct.unpack_from(">BH", recv)
                    recv = recv[3:]
                    if r_cmd == TYPE_INIT | cmd:
                        pass  # first data packet
                    elif r_cmd == TYPE_INIT | CTAPHID.KEEPALIVE:
                        try:
                            ka_status = STATUS(struct.unpack_from(">B", recv)[0])
                            logger.debug(f"Got keepalive status: {ka_status:02x}")
                        except ValueError:
                            raise ConnectionFailure("Invalid keepalive status")
                        if on_keepalive and ka_status != last_ka:
                            last_ka = ka_status
                            on_keepalive(ka_status)
                        continue
                    elif r_cmd == TYPE_INIT | CTAPHID.ERROR:
                        raise CtapError(struct.unpack_from(">B", recv)[0])
                    else:
                        raise CtapError(CtapError.ERR.INVALID_COMMAND)
                else:  # Continuation packet
                    r_seq = struct.unpack_from(">B", recv)[0]
                    recv = recv[1:]
                    if r_seq != seq:
                        raise ConnectionFailure("Wrong sequence number")
                    seq += 1

                response += recv
                if len(response) >= r_len:
                    break

            return response[:r_len]
        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt, cancelling...")
            self._send_cancel()

            raise

    def wink(self) -> None:
        """Causes the authenticator to blink."""
        self.call(CTAPHID.WINK)

    def ping(self, msg: bytes = b"Hello FIDO") -> bytes:
        """Sends data to the authenticator, which echoes it back.

        :param msg: The data to send.
        :return: The response from the authenticator.
        """
        return self.call(CTAPHID.PING, msg)

    def lock(self, lock_time: int = 10) -> None:
        """Locks the channel."""
        self.call(CTAPHID.LOCK, struct.pack(">B", lock_time))

    def close(self) -> None:
        self._connection.close()

    @classmethod
    def list_devices(cls) -> Iterator[CtapHidDevice]:
        for d in list_descriptors():
            yield cls(d, open_connection(d))


def list_devices() -> Iterator[CtapHidDevice]:
    return CtapHidDevice.list_devices()


def open_device(path) -> CtapHidDevice:
    descriptor = get_descriptor(path)
    return CtapHidDevice(descriptor, open_connection(descriptor))
```

## File: fido2/hid/base.py
```python
# Copyright (c) 2020 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
import os
import struct
from dataclasses import dataclass

FIDO_USAGE_PAGE = 0xF1D0
FIDO_USAGE = 0x1


@dataclass
class HidDescriptor:
    path: str | bytes
    vid: int
    pid: int
    report_size_in: int
    report_size_out: int
    product_name: str | None
    serial_number: str | None


class CtapHidConnection(abc.ABC):
    @abc.abstractmethod
    def read_packet(self) -> bytes:
        """Reads a CTAP HID packet"""

    @abc.abstractmethod
    def write_packet(self, data: bytes) -> None:
        """Writes a CTAP HID packet"""

    @abc.abstractmethod
    def close(self) -> None:
        """Closes the connection"""


class FileCtapHidConnection(CtapHidConnection):
    """Basic CtapHidConnection implementation which uses a path to a file descriptor"""

    def __init__(self, descriptor):
        self.handle = os.open(descriptor.path, os.O_RDWR)
        self.descriptor = descriptor

    def close(self):
        os.close(self.handle)

    def write_packet(self, data):
        if os.write(self.handle, data) != len(data):
            raise OSError("failed to write entire packet")

    def read_packet(self):
        return os.read(self.handle, self.descriptor.report_size_in)


REPORT_DESCRIPTOR_KEY_MASK = 0xFC
SIZE_MASK = ~REPORT_DESCRIPTOR_KEY_MASK
OUTPUT_ITEM = 0x90
INPUT_ITEM = 0x80
COLLECTION_ITEM = 0xA0
REPORT_COUNT = 0x94
REPORT_SIZE = 0x74
USAGE_PAGE = 0x04
USAGE = 0x08


def parse_report_descriptor(data: bytes) -> tuple[int, int]:
    # Parse report descriptor data
    usage, usage_page = None, None
    max_input_size, max_output_size = None, None
    report_count, report_size = None, None
    remaining = 4
    while data and remaining:
        head, data = struct.unpack_from(">B", data)[0], data[1:]
        key, size = REPORT_DESCRIPTOR_KEY_MASK & head, SIZE_MASK & head
        value = struct.unpack_from("<I", data[:size].ljust(4, b"\0"))[0]
        data = data[size:]

        if report_count is not None and report_size is not None:
            if key == INPUT_ITEM:
                if max_input_size is None:
                    max_input_size = report_count * report_size // 8
                    report_count, report_size = None, None
                    remaining -= 1
            elif key == OUTPUT_ITEM:
                if max_output_size is None:
                    max_output_size = report_count * report_size // 8
                    report_count, report_size = None, None
                    remaining -= 1
        if key == USAGE_PAGE:
            if not usage_page:
                usage_page = value
                remaining -= 1
        elif key == USAGE:
            if not usage:
                usage = value
                remaining -= 1
        elif key == REPORT_COUNT:
            if not report_count:
                report_count = value
        elif key == REPORT_SIZE:
            if not report_size:
                report_size = value

    if not remaining and usage_page == FIDO_USAGE_PAGE and usage == FIDO_USAGE:
        return max_input_size, max_output_size  # type: ignore

    raise ValueError("Not a FIDO device")
```

## File: fido2/hid/freebsd.py
```python
# Original work Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified work Copyright 2020 Yubico AB. All Rights Reserved.
# This file, with modifications, is licensed under the above Apache License.

# FreeBSD HID driver.
#
# There are two options to access UHID on FreeBSD:
#
# hidraw(4) - New method, not enabled by default
#             on FreeBSD 13.x and earlier
# uhid(4) - Classic method, default option on
#           FreeBSD 13.x and earlier
#
# hidraw is available since FreeBSD 13 and can be activated by adding
# `hw.usb.usbhid.enable="1"` to `/boot/loader.conf`. The actual kernel
# module is loaded with `kldload hidraw`.

from __future__ import annotations

import ctypes
import fcntl
import glob
import logging
import os
import re
import struct
import sys
from array import array
from ctypes.util import find_library
from dataclasses import dataclass

from .base import FileCtapHidConnection, HidDescriptor, parse_report_descriptor

# Don't typecheck this file on Windows
assert sys.platform != "win32"  # noqa: S101

logger = logging.getLogger(__name__)


devdir = "/dev/"

vendor_re = re.compile("vendor=(0x[0-9a-fA-F]+)")
product_re = re.compile("product=(0x[0-9a-fA-F]+)")
sernum_re = re.compile('sernum="([^"]+)')

libc = ctypes.CDLL(find_library("c"))

# /usr/include/dev/usb/usb_ioctl.h
USB_GET_REPORT_DESC = 0xC0205515

# /usr/include/dev/hid/hidraw.h>
HIDIOCGRAWINFO = 0x40085520
HIDIOCGRDESC = 0x2000551F
HIDIOCGRDESCSIZE = 0x4004551E
HIDIOCGRAWNAME_128 = 0x40805521
HIDIOCGRAWUNIQ_64 = 0x40405525


class usb_gen_descriptor(ctypes.Structure):
    _fields_ = [
        (
            "ugd_data",
            ctypes.c_void_p,
        ),  # TODO: check what COMPAT_32BIT in C header means
        ("ugd_lang_id", ctypes.c_uint16),
        ("ugd_maxlen", ctypes.c_uint16),
        ("ugd_actlen", ctypes.c_uint16),
        ("ugd_offset", ctypes.c_uint16),
        ("ugd_config_index", ctypes.c_uint8),
        ("ugd_string_index", ctypes.c_uint8),
        ("ugd_iface_index", ctypes.c_uint8),
        ("ugd_altif_index", ctypes.c_uint8),
        ("ugd_endpt_index", ctypes.c_uint8),
        ("ugd_report_type", ctypes.c_uint8),
        ("reserved", ctypes.c_uint8 * 8),
    ]


class HidrawCtapHidConnection(FileCtapHidConnection):
    def write_packet(self, data):
        # Prepend the report ID
        super(HidrawCtapHidConnection, self).write_packet(b"\0" + data)


def open_connection(descriptor):
    if descriptor.path.find(devdir + "hidraw") == 0:
        return HidrawCtapHidConnection(descriptor)
    else:
        return FileCtapHidConnection(descriptor)


def _get_report_data(fd, report_type):
    data = ctypes.create_string_buffer(4096)
    desc = usb_gen_descriptor(
        ugd_data=ctypes.addressof(data),
        ugd_maxlen=ctypes.sizeof(data),
        ugd_report_type=report_type,
    )
    ret = libc.ioctl(fd, USB_GET_REPORT_DESC, ctypes.byref(desc))
    if ret != 0:
        raise ValueError("ioctl failed")
    return data.raw[: desc.ugd_actlen]


def _read_descriptor(vid, pid, name, serial, path):
    fd = os.open(path, os.O_RDONLY)
    data = _get_report_data(fd, 3)
    os.close(fd)
    max_in_size, max_out_size = parse_report_descriptor(data)
    return HidDescriptor(path, vid, pid, max_in_size, max_out_size, name, serial)


@dataclass
class _UhidDevice:
    name: str
    path: str
    vendor_id: int | None = None
    product_id: int | None = None
    serial_number: str | None = None
    product_desc: str | None = None


def _enumerate():
    for uhid in glob.glob(devdir + "uhid?*"):
        index = uhid[len(devdir) + len("uhid") :]
        if not index.isdigit():
            continue

        pnpinfo = ("dev.uhid." + index + ".%pnpinfo").encode()
        desc = ("dev.uhid." + index + ".%desc").encode()

        ovalue = ctypes.create_string_buffer(1024)
        olen = ctypes.c_size_t(ctypes.sizeof(ovalue))
        key = ctypes.c_char_p(pnpinfo)
        retval = libc.sysctlbyname(key, ovalue, ctypes.byref(olen), None, None)
        if retval != 0:
            continue

        dev_name = uhid[len(devdir) :]
        dev_path = uhid

        value = ovalue.value[: olen.value].decode()
        m = vendor_re.search(value)
        dev_vendor_id = int(m.group(1), 16) if m else None

        m = product_re.search(value)
        dev_product_id = int(m.group(1), 16) if m else None

        m = sernum_re.search(value)
        dev_serial_number = m.group(1) if m else None

        key = ctypes.c_char_p(desc)
        retval = libc.sysctlbyname(key, ovalue, ctypes.byref(olen), None, None)
        if retval == 0:
            dev_product_desc = ovalue.value[: olen.value].decode() or None
        else:
            dev_product_desc = None

        yield _UhidDevice(
            dev_name,
            dev_path,
            dev_vendor_id,
            dev_product_id,
            dev_serial_number,
            dev_product_desc,
        )


def get_hidraw_descriptor(path):
    with open(path, "rb") as f:
        # Read VID, PID
        buf = array("B", [0] * (4 + 2 + 2))
        fcntl.ioctl(f, HIDIOCGRAWINFO, buf, True)
        _, vid, pid = struct.unpack("<IHH", buf)

        # FreeBSD's hidraw(4) does not return string length for
        # HIDIOCGRAWNAME and HIDIOCGRAWUNIQ, see https://reviews.freebsd.org/D35233

        # Read product
        buf = array("B", [0] * 129)
        fcntl.ioctl(f, HIDIOCGRAWNAME_128, buf, True)
        length = buf.index(0) + 1  # emulate ioctl return value
        name = bytearray(buf[: (length - 1)]).decode("utf-8") if length > 1 else None

        # Read unique ID
        try:
            buf = array("B", [0] * 65)
            fcntl.ioctl(f, HIDIOCGRAWUNIQ_64, buf, True)
            length = buf.index(0) + 1  # emulate ioctl return value
            serial = (
                bytearray(buf[: (length - 1)]).decode("utf-8") if length > 1 else None
            )
        except OSError:
            serial = None

        # Read report descriptor
        buf = array("B", [0] * 4)
        fcntl.ioctl(f, HIDIOCGRDESCSIZE, buf, True)
        size = struct.unpack("<I", buf)[0]
        buf += array("B", [0] * size)
        fcntl.ioctl(f, HIDIOCGRDESC, buf, True)

    data = bytes(buf[4:])
    max_in_size, max_out_size = parse_report_descriptor(data)
    return HidDescriptor(path, vid, pid, max_in_size, max_out_size, name, serial)


def get_descriptor(path):
    if path.find(devdir + "hidraw") == 0:
        return get_hidraw_descriptor(path)

    for dev in _enumerate():
        if dev.path == path:
            return _read_descriptor(
                dev.vendor_id, dev.product_id, dev.name, dev.serial_number, dev.path
            )
    raise ValueError("Device not found")


# Cache for continuously failing devices
_failed_cache: set[str] = set()


def list_descriptors():
    stale = set(_failed_cache)
    descriptors = []
    for hidraw in glob.glob(devdir + "hidraw?*"):
        stale.discard(hidraw)
        try:
            descriptors.append(get_descriptor(hidraw))
        except ValueError:
            pass  # Not a CTAP device, ignore
        except Exception:
            if hidraw not in _failed_cache:
                logger.debug("Failed opening device %s", hidraw, exc_info=True)
                _failed_cache.add(hidraw)

    if not descriptors:
        for dev in _enumerate():
            stale.discard(dev.path)
            try:
                descriptors.append(
                    _read_descriptor(
                        dev.vendor_id,
                        dev.product_id,
                        dev.name,
                        dev.serial_number,
                        dev.path,
                    )
                )
            except ValueError:
                pass  # Not a CTAP device, ignore
            except Exception:
                if dev.path not in _failed_cache:
                    logger.debug(
                        "Failed opening HID device %s", dev.path, exc_info=True
                    )
                    _failed_cache.add(dev.path)

    # Remove entries from the cache that were not seen
    _failed_cache.difference_update(stale)

    return descriptors
```

## File: fido2/hid/linux.py
```python
# Original work Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified work Copyright 2020 Yubico AB. All Rights Reserved.
# This file, with modifications, is licensed under the above Apache License.

from __future__ import annotations

import fcntl
import glob
import logging
import struct
import sys
from array import array

from .base import FileCtapHidConnection, HidDescriptor, parse_report_descriptor

# Don't typecheck this file on Windows
assert sys.platform != "win32"  # noqa: S101

logger = logging.getLogger(__name__)

# hidraw.h
HIDIOCGRAWINFO = 0x80084803
HIDIOCGRDESCSIZE = 0x80044801
HIDIOCGRDESC = 0x90044802
HIDIOCGRAWNAME = 0x90044804
HIDIOCGRAWUNIQ = 0x90044808


class LinuxCtapHidConnection(FileCtapHidConnection):
    def write_packet(self, data):
        # Prepend the report ID
        super().write_packet(b"\0" + data)


def open_connection(descriptor):
    return LinuxCtapHidConnection(descriptor)


def get_descriptor(path):
    with open(path, "rb") as f:
        # Read VID, PID
        buf = array("B", [0] * (4 + 2 + 2))
        fcntl.ioctl(f, HIDIOCGRAWINFO, buf, True)
        _, vid, pid = struct.unpack("<IHH", buf)

        # Read product
        buf = array("B", [0] * 128)
        length = fcntl.ioctl(f, HIDIOCGRAWNAME, buf, True)
        name = bytearray(buf[: (length - 1)]).decode("utf-8") if length > 1 else None

        # Read unique ID
        try:
            buf = array("B", [0] * 64)
            length = fcntl.ioctl(f, HIDIOCGRAWUNIQ, buf, True)
            serial = (
                bytearray(buf[: (length - 1)]).decode("utf-8") if length > 1 else None
            )
        except OSError:
            serial = None

        # Read report descriptor
        buf = array("B", [0] * 4)
        fcntl.ioctl(f, HIDIOCGRDESCSIZE, buf, True)
        size = struct.unpack("<I", buf)[0]
        buf += array("B", [0] * size)
        fcntl.ioctl(f, HIDIOCGRDESC, buf, True)

    data = bytes(buf[4:])
    max_in_size, max_out_size = parse_report_descriptor(data)
    return HidDescriptor(path, vid, pid, max_in_size, max_out_size, name, serial)


# Cache for continuously failing devices
_failed_cache: set[str] = set()


def list_descriptors():
    stale = set(_failed_cache)
    devices = []
    for hidraw in glob.glob("/dev/hidraw*"):
        stale.discard(hidraw)
        try:
            devices.append(get_descriptor(hidraw))
        except ValueError:
            pass  # Not a CTAP device, ignore.
        except Exception:
            if hidraw not in _failed_cache:
                logger.debug("Failed opening device %s", hidraw, exc_info=True)
                _failed_cache.add(hidraw)

    # Remove entries from the cache that were not seen
    _failed_cache.difference_update(stale)

    return devices
```

## File: fido2/hid/macos.py
```python
# Original work Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified work Copyright 2020 Yubico AB. All Rights Reserved.
# This file, with modifications, is licensed under the above Apache License.

from __future__ import annotations

import ctypes
import ctypes.util
import logging
import threading
from queue import Empty, Queue

from .base import FIDO_USAGE, FIDO_USAGE_PAGE, CtapHidConnection, HidDescriptor

logger = logging.getLogger(__name__)

# Constants

HID_DEVICE_PROPERTY_VENDOR_ID = b"VendorID"
HID_DEVICE_PROPERTY_PRODUCT_ID = b"ProductID"
HID_DEVICE_PROPERTY_PRODUCT = b"Product"
HID_DEVICE_PROPERTY_SERIAL_NUMBER = b"SerialNumber"
HID_DEVICE_PROPERTY_PRIMARY_USAGE = b"PrimaryUsage"
HID_DEVICE_PROPERTY_PRIMARY_USAGE_PAGE = b"PrimaryUsagePage"
HID_DEVICE_PROPERTY_MAX_INPUT_REPORT_SIZE = b"MaxInputReportSize"
HID_DEVICE_PROPERTY_MAX_OUTPUT_REPORT_SIZE = b"MaxOutputReportSize"
HID_DEVICE_PROPERTY_REPORT_ID = b"ReportID"


# Declare C types
class _CFType(ctypes.Structure):
    pass


class _CFString(_CFType):
    pass


class _CFSet(_CFType):
    pass


class _IOHIDManager(_CFType):
    pass


class _IOHIDDevice(_CFType):
    pass


class _CFRunLoop(_CFType):
    pass


class _CFAllocator(_CFType):
    pass


CF_SET_REF = ctypes.POINTER(_CFSet)
CF_STRING_REF = ctypes.POINTER(_CFString)
CF_TYPE_REF = ctypes.POINTER(_CFType)
CF_RUN_LOOP_REF = ctypes.POINTER(_CFRunLoop)
CF_RUN_LOOP_RUN_RESULT = ctypes.c_int32
CF_ALLOCATOR_REF = ctypes.POINTER(_CFAllocator)
CF_DICTIONARY_REF = ctypes.c_void_p
CF_MUTABLE_DICTIONARY_REF = ctypes.c_void_p
CF_TYPE_ID = ctypes.c_ulong
CF_INDEX = ctypes.c_long
CF_TIME_INTERVAL = ctypes.c_double
CF_STRING_ENCODING = ctypes.c_uint32
CF_STRING_BUILTIN_ENCODINGS_UTF8 = 134217984
IO_RETURN = ctypes.c_uint
IO_HID_REPORT_TYPE = ctypes.c_uint
IO_OPTION_BITS = ctypes.c_uint
IO_OBJECT_T = ctypes.c_uint
MACH_PORT_T = ctypes.c_uint
IO_SERVICE_T = IO_OBJECT_T
IO_REGISTRY_ENTRY_T = IO_OBJECT_T

IO_HID_MANAGER_REF = ctypes.POINTER(_IOHIDManager)
IO_HID_DEVICE_REF = ctypes.POINTER(_IOHIDDevice)

IO_HID_REPORT_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.py_object,
    IO_RETURN,
    ctypes.c_void_p,
    IO_HID_REPORT_TYPE,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    CF_INDEX,
)
IO_HID_CALLBACK = ctypes.CFUNCTYPE(None, ctypes.py_object, IO_RETURN, ctypes.c_void_p)

# Define C constants
K_CF_NUMBER_SINT32_TYPE = 3
K_CF_ALLOCATOR_DEFAULT = None

K_IO_MASTER_PORT_DEFAULT = 0
K_IO_HID_REPORT_TYPE_OUTPUT = 1
K_IO_RETURN_SUCCESS = 0

K_CF_RUN_LOOP_RUN_STOPPED = 2
K_CF_RUN_LOOP_RUN_TIMED_OUT = 3
K_CF_RUN_LOOP_RUN_HANDLED_SOURCE = 4

# Load relevant libraries
# NOTE: find_library doesn't currently work on Big Sur, requiring the hardcoded paths
iokit = ctypes.cdll.LoadLibrary(
    ctypes.util.find_library("IOKit")
    or "/System/Library/Frameworks/IOKit.framework/IOKit"
)
cf = ctypes.cdll.LoadLibrary(
    ctypes.util.find_library("CoreFoundation")
    or "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
)

# Exported constants
K_CF_RUNLOOP_DEFAULT_MODE = CF_STRING_REF.in_dll(cf, "kCFRunLoopDefaultMode")

# Declare C function prototypes
cf.CFSetGetValues.restype = None
cf.CFSetGetValues.argtypes = [CF_SET_REF, ctypes.POINTER(ctypes.c_void_p)]
cf.CFStringCreateWithCString.restype = CF_STRING_REF
cf.CFStringCreateWithCString.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_uint32,
]
cf.CFStringGetCString.restype = ctypes.c_bool
cf.CFStringGetCString.argtypes = [
    CF_TYPE_REF,
    ctypes.c_char_p,
    CF_INDEX,
    CF_STRING_ENCODING,
]
cf.CFGetTypeID.restype = CF_TYPE_ID
cf.CFGetTypeID.argtypes = [CF_TYPE_REF]
cf.CFNumberGetTypeID.restype = CF_TYPE_ID
cf.CFStringGetTypeID.restype = CF_TYPE_ID
cf.CFNumberGetValue.restype = ctypes.c_int
cf.CFRunLoopGetCurrent.restype = CF_RUN_LOOP_REF
cf.CFRunLoopGetCurrent.argtypes = []
cf.CFRunLoopRunInMode.restype = CF_RUN_LOOP_RUN_RESULT
cf.CFRunLoopRunInMode.argtypes = [CF_STRING_REF, CF_TIME_INTERVAL, ctypes.c_bool]
cf.CFRelease.restype = IO_RETURN
cf.CFRelease.argtypes = [CF_TYPE_REF]

iokit.IOObjectRelease.argtypes = [IO_OBJECT_T]

iokit.IOHIDManagerCreate.restype = IO_HID_MANAGER_REF
iokit.IOHIDManagerCreate.argtypes = [CF_ALLOCATOR_REF, IO_OPTION_BITS]
iokit.IOHIDManagerCopyDevices.restype = CF_SET_REF
iokit.IOHIDManagerCopyDevices.argtypes = [IO_HID_MANAGER_REF]
iokit.IOHIDManagerSetDeviceMatching.restype = None
iokit.IOHIDManagerSetDeviceMatching.argtypes = [IO_HID_MANAGER_REF, CF_TYPE_REF]

iokit.IORegistryEntryIDMatching.restype = CF_MUTABLE_DICTIONARY_REF
iokit.IORegistryEntryIDMatching.argtypes = [ctypes.c_uint64]
iokit.IORegistryEntryGetRegistryEntryID.restype = IO_RETURN
iokit.IORegistryEntryGetRegistryEntryID.argtypes = [
    IO_REGISTRY_ENTRY_T,
    ctypes.POINTER(ctypes.c_uint64),
]

iokit.IOHIDDeviceCreate.restype = IO_HID_DEVICE_REF
iokit.IOHIDDeviceCreate.argtypes = [CF_ALLOCATOR_REF, IO_SERVICE_T]
iokit.IOHIDDeviceClose.restype = IO_RETURN
iokit.IOHIDDeviceClose.argtypes = [IO_HID_DEVICE_REF, ctypes.c_uint32]
iokit.IOHIDDeviceScheduleWithRunLoop.restype = None
iokit.IOHIDDeviceScheduleWithRunLoop.argtypes = [
    IO_HID_DEVICE_REF,
    CF_RUN_LOOP_REF,
    CF_STRING_REF,
]
iokit.IOHIDDeviceUnscheduleFromRunLoop.restype = None
iokit.IOHIDDeviceUnscheduleFromRunLoop.argtypes = [
    IO_HID_DEVICE_REF,
    CF_RUN_LOOP_REF,
    CF_STRING_REF,
]
iokit.IOHIDDeviceGetProperty.restype = CF_TYPE_REF
iokit.IOHIDDeviceGetProperty.argtypes = [IO_HID_DEVICE_REF, CF_STRING_REF]
iokit.IOHIDDeviceSetReport.restype = IO_RETURN
iokit.IOHIDDeviceSetReport.argtypes = [
    IO_HID_DEVICE_REF,
    IO_HID_REPORT_TYPE,
    CF_INDEX,
    ctypes.c_void_p,
    CF_INDEX,
]
iokit.IOServiceGetMatchingService.restype = IO_SERVICE_T
iokit.IOServiceGetMatchingService.argtypes = [MACH_PORT_T, CF_DICTIONARY_REF]


def _hid_read_callback(
    read_queue, result, sender, report_type, report_id, report, report_length
):
    """Handles incoming IN report from HID device."""
    del result, sender, report_type, report_id  # Unused by the callback function

    read_queue.put(ctypes.string_at(report, report_length))


# C wrapper around ReadCallback()
# Declared in this scope so it doesn't get GC-ed
REGISTERED_READ_CALLBACK = IO_HID_REPORT_CALLBACK(_hid_read_callback)


def _hid_removal_callback(hid_device, result, sender):
    del result, sender
    cf.CFRunLoopStop(hid_device.run_loop_ref)


REMOVAL_CALLBACK = IO_HID_CALLBACK(_hid_removal_callback)


def _dev_read_thread(hid_device):
    """Binds a device to the thread's run loop, then starts the run loop.

    Args:
    hid_device: The MacOsHidDevice object

    The HID manager requires a run loop to handle Report reads. This thread
    function serves that purpose.
    """

    # Schedule device events with run loop
    hid_device.run_loop_ref = cf.CFRunLoopGetCurrent()
    if not hid_device.run_loop_ref:
        logger.error("Failed to get current run loop")
        return

    iokit.IOHIDDeviceScheduleWithRunLoop(
        hid_device.handle, hid_device.run_loop_ref, K_CF_RUNLOOP_DEFAULT_MODE
    )

    iokit.IOHIDDeviceRegisterRemovalCallback(
        hid_device.handle, REMOVAL_CALLBACK, ctypes.py_object(hid_device)
    )

    max_retries = 2  # Maximum number of run loop retries
    retries = 0

    while retries < max_retries:
        # Run the run loop
        run_loop_run_result = cf.CFRunLoopRunInMode(
            K_CF_RUNLOOP_DEFAULT_MODE,
            4,
            True,  # Timeout in seconds
        )  # Return after source handled

        received_data = not hid_device.read_queue.empty()
        if run_loop_run_result == K_CF_RUN_LOOP_RUN_HANDLED_SOURCE:
            if received_data:
                # Return when data has been received
                break
            else:
                # Retry running the run loop if data has not been received yet
                logger.debug("Read queue empty after HANDLE_SOURCE, attempting retry")
                retries += 1
        else:
            # log any unexpected run loop exit
            logger.error("Unexpected run loop exit code: %d", run_loop_run_result)
            break

    # Unschedule from run loop
    iokit.IOHIDDeviceUnscheduleFromRunLoop(
        hid_device.handle, hid_device.run_loop_ref, K_CF_RUNLOOP_DEFAULT_MODE
    )


class MacCtapHidConnection(CtapHidConnection):
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.handle = _handle_from_path(descriptor.path)

        # Open device
        result = iokit.IOHIDDeviceOpen(self.handle, 0)
        if result != K_IO_RETURN_SUCCESS:
            raise OSError(f"Failed to open device for communication: {result}")

        # Create read queue
        self.read_queue: Queue = Queue()

        # Create and start read thread
        self.run_loop_ref = None

        # Register read callback
        self.in_report_buffer = (ctypes.c_uint8 * descriptor.report_size_in)()
        iokit.IOHIDDeviceRegisterInputReportCallback(
            self.handle,
            self.in_report_buffer,
            self.descriptor.report_size_in,
            REGISTERED_READ_CALLBACK,
            ctypes.py_object(self.read_queue),
        )

    def close(self):
        iokit.IOHIDDeviceRegisterInputReportCallback(
            self.handle,
            self.in_report_buffer,
            self.descriptor.report_size_in,
            ctypes.cast(0, IO_HID_REPORT_CALLBACK),
            None,
        )

    def write_packet(self, data):
        result = iokit.IOHIDDeviceSetReport(
            self.handle,
            K_IO_HID_REPORT_TYPE_OUTPUT,
            0,
            data,
            len(data),
        )

        # Non-zero status indicates failure
        if result != K_IO_RETURN_SUCCESS:
            raise OSError(f"Failed to write report to device: {result}")

    def read_packet(self):
        try:
            return self.read_queue.get(False)
        except Empty:
            read_thread = threading.Thread(target=_dev_read_thread, args=(self,))
            read_thread.start()
            read_thread.join()
            try:
                return self.read_queue.get(False)
            except Empty:
                raise OSError("Failed reading a response")


def get_int_property(dev, key):
    """Reads int property from the HID device."""
    cf_key = cf.CFStringCreateWithCString(None, key, 0)
    type_ref = iokit.IOHIDDeviceGetProperty(dev, cf_key)
    cf.CFRelease(cf_key)
    if not type_ref:
        raise ValueError(f"Property '{key}' not found")

    if cf.CFGetTypeID(type_ref) != cf.CFNumberGetTypeID():
        raise OSError(f"Expected number type, got {cf.CFGetTypeID(type_ref)}")

    out = ctypes.c_int32()
    if not cf.CFNumberGetValue(type_ref, K_CF_NUMBER_SINT32_TYPE, ctypes.byref(out)):
        raise OSError(f"Failed to read property '{key}'")

    return out.value


def get_string_property(dev, key):
    """Reads string property from the HID device."""
    cf_key = cf.CFStringCreateWithCString(None, key, 0)
    type_ref = iokit.IOHIDDeviceGetProperty(dev, cf_key)
    cf.CFRelease(cf_key)
    if not type_ref:
        return None

    if cf.CFGetTypeID(type_ref) != cf.CFStringGetTypeID():
        raise OSError(f"Expected string type, got {cf.CFGetTypeID(type_ref)}")

    out = ctypes.create_string_buffer(128)
    ret = cf.CFStringGetCString(
        type_ref, out, ctypes.sizeof(out), CF_STRING_BUILTIN_ENCODINGS_UTF8
    )
    if not ret:
        return None

    try:
        return out.value.decode("utf-8") or None
    except UnicodeDecodeError:
        return None


def get_device_id(handle):
    """Obtains the unique IORegistry entry ID for the device.

    Args:
    handle: reference to the device

    Returns:
    A unique ID for the device, obtained from the IO Registry
    """
    # Obtain device entry ID from IO Registry
    io_service_obj = iokit.IOHIDDeviceGetService(handle)
    entry_id = ctypes.c_uint64()
    result = iokit.IORegistryEntryGetRegistryEntryID(
        io_service_obj, ctypes.byref(entry_id)
    )
    if result != K_IO_RETURN_SUCCESS:
        raise OSError(f"Failed to obtain IORegistry entry ID: {result}")

    return entry_id.value


def _handle_from_path(path):
    # Resolve the path to device handle
    entry_id = ctypes.c_uint64(int(path))
    matching_dict = iokit.IORegistryEntryIDMatching(entry_id)
    device_entry = iokit.IOServiceGetMatchingService(
        K_IO_MASTER_PORT_DEFAULT, matching_dict
    )
    if not device_entry:
        raise OSError(f"Device ID {path} does not match any HID device on the system")

    return iokit.IOHIDDeviceCreate(K_CF_ALLOCATOR_DEFAULT, device_entry)


def open_connection(descriptor):
    return MacCtapHidConnection(descriptor)


def _get_descriptor_from_handle(handle):
    usage_page = get_int_property(handle, HID_DEVICE_PROPERTY_PRIMARY_USAGE_PAGE)
    usage = get_int_property(handle, HID_DEVICE_PROPERTY_PRIMARY_USAGE)
    if usage_page == FIDO_USAGE_PAGE and usage == FIDO_USAGE:
        device_id = get_device_id(handle)
        vid = get_int_property(handle, HID_DEVICE_PROPERTY_VENDOR_ID)
        pid = get_int_property(handle, HID_DEVICE_PROPERTY_PRODUCT_ID)
        product = get_string_property(handle, HID_DEVICE_PROPERTY_PRODUCT)
        serial = get_string_property(handle, HID_DEVICE_PROPERTY_SERIAL_NUMBER)
        size_in = get_int_property(handle, HID_DEVICE_PROPERTY_MAX_INPUT_REPORT_SIZE)
        size_out = get_int_property(handle, HID_DEVICE_PROPERTY_MAX_OUTPUT_REPORT_SIZE)
        return HidDescriptor(
            str(device_id), vid, pid, size_in, size_out, product, serial
        )
    raise ValueError("Not a CTAP device")


def get_descriptor(path):
    return _get_descriptor_from_handle(_handle_from_path(path))


def list_descriptors():
    # Init a HID manager
    hid_mgr = iokit.IOHIDManagerCreate(None, 0)
    if not hid_mgr:
        raise OSError("Unable to obtain HID manager reference")
    try:
        iokit.IOHIDManagerSetDeviceMatching(hid_mgr, None)

        # Get devices from HID manager
        device_set_ref = iokit.IOHIDManagerCopyDevices(hid_mgr)
        if not device_set_ref:
            raise OSError("Failed to obtain devices from HID manager")
        try:
            num = iokit.CFSetGetCount(device_set_ref)
            devices = (IO_HID_DEVICE_REF * num)()
            iokit.CFSetGetValues(device_set_ref, devices)

            # Retrieve and build descriptor dictionaries for each device
            descriptors = []
            for handle in devices:
                try:
                    descriptor = _get_descriptor_from_handle(handle)
                    descriptors.append(descriptor)
                except ValueError:
                    continue  # Not a CTAP device, ignore it
            return descriptors
        finally:
            cf.CFRelease(device_set_ref)
    finally:
        cf.CFRelease(hid_mgr)
```

## File: fido2/hid/netbsd.py
```python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implements raw HID interface on NetBSD."""

from __future__ import absolute_import

import errno
import logging
import os
import select
import struct
import sys
from ctypes import (
    Structure,
    c_char,
    c_int,
    c_ubyte,
    c_uint8,
    c_uint16,
    c_uint32,
)

from . import base

# Don't typecheck this file on Windows
assert sys.platform != "win32"  # noqa: S101

from fcntl import ioctl  # noqa: E402

logger = logging.getLogger(__name__)


USB_MAX_DEVNAMELEN = 16
USB_MAX_DEVNAMES = 4
USB_MAX_STRING_LEN = 128
USB_MAX_ENCODED_STRING_LEN = USB_MAX_STRING_LEN * 3


class usb_ctl_report_desc(Structure):
    _fields_ = [
        ("ucrd_size", c_int),
        ("ucrd_data", c_ubyte * 1024),
    ]


class usb_device_info(Structure):
    _fields_ = [
        ("udi_bus", c_uint8),
        ("udi_addr", c_uint8),
        ("udi_pad0", c_uint8 * 2),
        ("udi_cookie", c_uint32),
        ("udi_product", c_char * USB_MAX_ENCODED_STRING_LEN),
        ("udi_vendor", c_char * USB_MAX_ENCODED_STRING_LEN),
        ("udi_release", c_char * 8),
        ("udi_serial", c_char * USB_MAX_ENCODED_STRING_LEN),
        ("udi_productNo", c_uint16),
        ("udi_vendorNo", c_uint16),
        ("udi_releaseNo", c_uint16),
        ("udi_class", c_uint8),
        ("udi_subclass", c_uint8),
        ("udi_protocol", c_uint8),
        ("udi_config", c_uint8),
        ("udi_speed", c_uint8),
        ("udi_pad1", c_uint8),
        ("udi_power", c_int),
        ("udi_nports", c_int),
        ("udi_devnames", c_char * USB_MAX_DEVNAMES * USB_MAX_DEVNAMELEN),
        ("udi_ports", c_uint8 * 16),
    ]


USB_GET_DEVICE_INFO = 0x44F45570  # _IOR('U', 112, struct usb_device_info)
USB_GET_REPORT_DESC = 0x44045515  # _IOR('U', 21, struct usb_ctl_report_desc)
USB_HID_SET_RAW = 0x80046802  # _IOW('h', 2, int)


# Cache for continuously failing devices
# XXX not thread-safe
_failed_cache: set[str] = set()


def list_descriptors():
    stale = set(_failed_cache)
    descriptors = []

    for i in range(100):
        path = "/dev/uhid%d" % (i,)
        stale.discard(path)
        try:
            desc = get_descriptor(path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                break
            if path not in _failed_cache:
                logger.debug("Failed opening FIDO device %s", path, exc_info=True)
                _failed_cache.add(path)
            continue
        except Exception:
            if path not in _failed_cache:
                logger.debug("Failed opening FIDO device %s", path, exc_info=True)
                _failed_cache.add(path)
            continue
        descriptors.append(desc)

    _failed_cache.difference_update(stale)
    return descriptors


def get_descriptor(path):
    fd = None
    try:
        fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC)
        devinfo = usb_device_info()
        ioctl(fd, USB_GET_DEVICE_INFO, devinfo)
        ucrd = usb_ctl_report_desc()
        ioctl(fd, USB_GET_REPORT_DESC, ucrd)
        report_desc = bytes(ucrd.ucrd_data[: ucrd.ucrd_size])
        maxin, maxout = base.parse_report_descriptor(report_desc)
        vid = devinfo.udi_vendorNo
        pid = devinfo.udi_productNo
        try:
            name = devinfo.udi_product.decode("utf-8")
        except UnicodeDecodeError:
            name = None
        try:
            serial = devinfo.udi_serial.decode("utf-8")
        except UnicodeDecodeError:
            serial = None
        return base.HidDescriptor(path, vid, pid, maxin, maxout, name, serial)
    finally:
        if fd is not None:
            os.close(fd)


def open_connection(descriptor):
    return NetBSDCtapHidConnection(descriptor)


class NetBSDCtapHidConnection(base.FileCtapHidConnection):
    def __init__(self, descriptor):
        # XXX racy -- device can change identity now that it has been
        # closed
        super().__init__(descriptor)
        try:
            ioctl(self.handle, USB_HID_SET_RAW, struct.pack("@i", 1))
            ping = bytearray(64)
            ping[0:7] = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0x81, 0, 1])
            for i in range(10):
                self.write_packet(bytes(ping))
                poll = select.poll()
                poll.register(self.handle, select.POLLIN)
                if poll.poll(100):
                    self.read_packet()
                    break
            else:
                raise Exception("u2f ping timeout")
        except Exception:
            self.close()
            raise
```

## File: fido2/hid/openbsd.py
```python
# Original work Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified work Copyright 2020 Yubico AB. All Rights Reserved.
# This file, with modifications, is licensed under the above Apache License.

from __future__ import annotations

import fcntl
import logging
import os
import os.path
import select
import sys
from ctypes import Structure, c_char, c_int, c_uint8, c_uint16, c_uint32

from .base import FileCtapHidConnection, HidDescriptor

# Don't typecheck this file on Windows
assert sys.platform != "win32"  # noqa: S101

logger = logging.getLogger(__name__)

# /usr/include/dev/usb/usb.h
USB_GET_DEVICEINFO = 0x421C5570
USB_MAX_STRING_LEN = 127
USB_MAX_DEVNAMES = 4
USB_MAX_DEVNAMELEN = 16

FIDO_DEVS = "/dev/fido"
MAX_U2F_HIDLEN = 64


class UsbDeviceInfo(Structure):
    _fields_ = [
        ("udi_bus", c_uint8),
        ("udi_addr", c_uint8),
        ("udi_product", c_char * USB_MAX_STRING_LEN),
        ("udi_vendor", c_char * USB_MAX_STRING_LEN),
        ("udi_release", c_char * 8),
        ("udi_productNo", c_uint16),
        ("udi_vendorNo", c_uint16),
        ("udi_releaseNo", c_uint16),
        ("udi_class", c_uint8),
        ("udi_subclass", c_uint8),
        ("udi_protocol", c_uint8),
        ("udi_config", c_uint8),
        ("udi_speed", c_uint8),
        ("udi_power", c_int),
        ("udi_nports", c_int),
        ("udi_devnames", c_char * USB_MAX_DEVNAMELEN * USB_MAX_DEVNAMES),
        ("udi_ports", c_uint32 * 16),
        ("udi_serial", c_char * USB_MAX_STRING_LEN),
    ]


class OpenBsdCtapHidConnection(FileCtapHidConnection):
    def __init__(self, descriptor):
        super().__init__(descriptor)
        try:
            self._terrible_ping_kludge()
        except Exception:
            self.close()
            raise

    def _terrible_ping_kludge(self):
        # This is pulled from
        # https://github.com/Yubico/libfido2/blob/da24193aa901086960f8d31b60d930ebef21f7a2/src/hid_openbsd.c#L128
        for _ in range(4):
            # 1 byte ping
            data = b"\xff\xff\xff\xff\x81\0\1".ljust(
                self.descriptor.report_size_out, b"\0"
            )

            poll = select.poll()
            poll.register(self.handle, select.POLLIN)

            self.write_packet(data)

            poll.poll(100)
            data = self.read_packet()


def open_connection(descriptor):
    return OpenBsdCtapHidConnection(descriptor)


def get_descriptor(path):
    f = os.open(path, os.O_RDONLY)

    dev_info = UsbDeviceInfo()

    try:
        fcntl.ioctl(f, USB_GET_DEVICEINFO, dev_info)  # type: ignore
    finally:
        os.close(f)

    vid = int(dev_info.udi_vendorNo)
    pid = int(dev_info.udi_productNo)
    name = dev_info.udi_product.decode("utf-8") or None
    serial = dev_info.udi_serial.decode("utf-8") or None

    return HidDescriptor(path, vid, pid, MAX_U2F_HIDLEN, MAX_U2F_HIDLEN, name, serial)


# Cache for continuously failing devices
_failed_cache: set[str] = set()


def list_descriptors():
    stale = set(_failed_cache)
    descriptors = []
    for dev in os.listdir(FIDO_DEVS):
        path = os.path.join(FIDO_DEVS, dev)
        stale.discard(path)
        try:
            descriptors.append(get_descriptor(path))
        except Exception:
            if path not in _failed_cache:
                logger.debug("Failed opening FIDO device %s", path, exc_info=True)
                _failed_cache.add(path)
    return descriptors
```

## File: fido2/hid/windows.py
```python
# Original work Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified work Copyright 2020 Yubico AB. All Rights Reserved.
# This file, with modifications, is licensed under the above Apache License.

from __future__ import annotations

import ctypes
import logging
import platform
import sys
from typing import cast

from .base import FIDO_USAGE, FIDO_USAGE_PAGE, CtapHidConnection, HidDescriptor

# Only typecheck this file on Windows
assert sys.platform == "win32"  # noqa: S101
from ctypes import LibraryLoader, WinDLL, WinError, wintypes  # noqa: E402

logger = logging.getLogger(__name__)


# Load relevant DLLs
windll = LibraryLoader(WinDLL)
hid = windll.Hid
setupapi = windll.SetupAPI
kernel32 = windll.Kernel32


# Various structs that are used in the Windows APIs we call
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]


# On Windows, SetupAPI.h packs structures differently in 64bit and
# 32bit mode.  In 64-bit mode, the structures are packed on 8 byte
# boundaries, while in 32-bit mode, they are packed on 1 byte boundaries.
# This is important to get right for some API calls that fill out these
# structures.
if platform.architecture()[0] == "64bit":
    SETUPAPI_PACK = 8
elif platform.architecture()[0] == "32bit":
    SETUPAPI_PACK = 1
else:
    raise OSError(f"Unknown architecture: {platform.architecture()[0]}")


class DeviceInterfaceData(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("InterfaceClassGuid", GUID),
        ("Flags", wintypes.DWORD),
        ("Reserved", ctypes.POINTER(ctypes.c_ulong)),
    ]
    _pack_ = SETUPAPI_PACK


class DeviceInterfaceDetailData(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD), ("DevicePath", ctypes.c_byte * 1)]
    _pack_ = SETUPAPI_PACK


class HidAttributes(ctypes.Structure):
    _fields_ = [
        ("Size", ctypes.c_ulong),
        ("VendorID", ctypes.c_ushort),
        ("ProductID", ctypes.c_ushort),
        ("VersionNumber", ctypes.c_ushort),
    ]


class HidCapabilities(ctypes.Structure):
    _fields_ = [
        ("Usage", ctypes.c_ushort),
        ("UsagePage", ctypes.c_ushort),
        ("InputReportByteLength", ctypes.c_ushort),
        ("OutputReportByteLength", ctypes.c_ushort),
        ("FeatureReportByteLength", ctypes.c_ushort),
        ("Reserved", ctypes.c_ushort * 17),
        ("NotUsed", ctypes.c_ushort * 10),
    ]


# Various void* aliases for readability.
HDEVINFO = ctypes.c_void_p
HANDLE = ctypes.c_void_p
PHIDP_PREPARSED_DATA = ctypes.c_void_p  # pylint: disable=invalid-name

# This is a HANDLE.
# INVALID_HANDLE_VALUE = 0xFFFFFFFF
INVALID_HANDLE_VALUE = (1 << 8 * ctypes.sizeof(ctypes.c_void_p)) - 1

# Status codes
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 0x03
NTSTATUS = ctypes.c_long
HIDP_STATUS_SUCCESS = 0x00110000

# CreateFile Flags
GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000

DIGCF_DEVICEINTERFACE = 0x10
DIGCF_PRESENT = 0x02

# Function signatures
hid.HidD_GetHidGuid.restype = None
hid.HidD_GetHidGuid.argtypes = [ctypes.POINTER(GUID)]
hid.HidD_GetAttributes.restype = wintypes.BOOLEAN
hid.HidD_GetAttributes.argtypes = [HANDLE, ctypes.POINTER(HidAttributes)]
hid.HidD_GetPreparsedData.restype = wintypes.BOOLEAN
hid.HidD_GetPreparsedData.argtypes = [HANDLE, ctypes.POINTER(PHIDP_PREPARSED_DATA)]
hid.HidD_FreePreparsedData.restype = wintypes.BOOLEAN
hid.HidD_FreePreparsedData.argtypes = [PHIDP_PREPARSED_DATA]
hid.HidD_GetProductString.restype = wintypes.BOOLEAN
hid.HidD_GetProductString.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_ulong]
hid.HidD_GetSerialNumberString.restype = wintypes.BOOLEAN
hid.HidD_GetSerialNumberString.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_ulong]
hid.HidP_GetCaps.restype = NTSTATUS
hid.HidP_GetCaps.argtypes = [PHIDP_PREPARSED_DATA, ctypes.POINTER(HidCapabilities)]


hid.HidD_GetFeature.restype = wintypes.BOOL
hid.HidD_GetFeature.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_ulong]
hid.HidD_SetFeature.restype = wintypes.BOOL
hid.HidD_SetFeature.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_ulong]

setupapi.SetupDiGetClassDevsA.argtypes = [
    ctypes.POINTER(GUID),
    ctypes.c_char_p,
    wintypes.HWND,
    wintypes.DWORD,
]
setupapi.SetupDiGetClassDevsA.restype = HDEVINFO
setupapi.SetupDiEnumDeviceInterfaces.restype = wintypes.BOOL
setupapi.SetupDiEnumDeviceInterfaces.argtypes = [
    HDEVINFO,
    ctypes.c_void_p,
    ctypes.POINTER(GUID),
    wintypes.DWORD,
    ctypes.POINTER(DeviceInterfaceData),
]
setupapi.SetupDiGetDeviceInterfaceDetailA.restype = wintypes.BOOL
setupapi.SetupDiGetDeviceInterfaceDetailA.argtypes = [
    HDEVINFO,
    ctypes.POINTER(DeviceInterfaceData),
    ctypes.POINTER(DeviceInterfaceDetailData),
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
]
setupapi.SetupDiDestroyDeviceInfoList.restype = wintypes.BOOL
setupapi.SetupDiDestroyDeviceInfoList.argtypes = [
    HDEVINFO,
]

kernel32.CreateFileA.restype = HANDLE
kernel32.CreateFileA.argtypes = [
    ctypes.c_char_p,
    wintypes.DWORD,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.DWORD,
    wintypes.DWORD,
    HANDLE,
]
kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [HANDLE]


class WinCtapHidConnection(CtapHidConnection):
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.handle = kernel32.CreateFileA(
            descriptor.path,
            GENERIC_WRITE | GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            0,
            None,
        )
        if self.handle == INVALID_HANDLE_VALUE:
            raise WinError()

    def close(self):
        kernel32.CloseHandle(self.handle)

    def write_packet(self, data):
        out = b"\0" + data  # Prepend report ID
        num_written = wintypes.DWORD()
        ret = kernel32.WriteFile(
            self.handle, out, len(out), ctypes.byref(num_written), None
        )
        if not ret:
            raise WinError()
        if num_written.value != len(out):
            raise OSError(
                "Failed to write complete packet.  "
                + "Expected %d, but got %d" % (len(out), num_written.value)
            )

    def read_packet(self):
        buf = ctypes.create_string_buffer(self.descriptor.report_size_in + 1)
        num_read = wintypes.DWORD()
        ret = kernel32.ReadFile(
            self.handle, buf, len(buf), ctypes.byref(num_read), None
        )
        if not ret:
            raise WinError()

        if num_read.value != self.descriptor.report_size_in + 1:
            raise OSError("Failed to read full length report from device.")

        return buf.raw[1:]  # Strip report ID


def get_vid_pid(device):
    attributes = HidAttributes()
    result = hid.HidD_GetAttributes(device, ctypes.byref(attributes))
    if not result:
        raise WinError()

    return attributes.VendorID, attributes.ProductID


def get_product_name(device):
    buf = ctypes.create_unicode_buffer(128)

    result = hid.HidD_GetProductString(device, buf, ctypes.c_ulong(ctypes.sizeof(buf)))
    if not result:
        return None

    return buf.value


def get_serial(device):
    buf = ctypes.create_unicode_buffer(128)

    result = hid.HidD_GetSerialNumberString(
        device, buf, ctypes.c_ulong(ctypes.sizeof(buf))
    )
    if not result:
        return None

    return buf.value


def get_descriptor(path):
    device = kernel32.CreateFileA(
        path,
        0,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )
    if device == INVALID_HANDLE_VALUE:
        raise WinError()
    try:
        preparsed_data = PHIDP_PREPARSED_DATA(0)
        ret = hid.HidD_GetPreparsedData(device, ctypes.byref(preparsed_data))
        if not ret:
            raise WinError()

        try:
            caps = HidCapabilities()
            ret = hid.HidP_GetCaps(preparsed_data, ctypes.byref(caps))

            if ret != HIDP_STATUS_SUCCESS:
                raise WinError()

            if caps.UsagePage == FIDO_USAGE_PAGE and caps.Usage == FIDO_USAGE:
                vid, pid = get_vid_pid(device)
                product_name = get_product_name(device)
                serial = get_serial(device)
                # Sizes here include 1-byte report ID, which we need to remove.
                size_in = caps.InputReportByteLength - 1
                size_out = caps.OutputReportByteLength - 1
                return HidDescriptor(
                    path, vid, pid, size_in, size_out, product_name, serial
                )
            raise ValueError("Not a CTAP device")

        finally:
            hid.HidD_FreePreparsedData(preparsed_data)
    finally:
        kernel32.CloseHandle(device)


def open_connection(descriptor):
    return WinCtapHidConnection(descriptor)


_SKIP = cast(HidDescriptor, object())
_descriptor_cache: dict[bytes, HidDescriptor] = {}


def list_descriptors():
    stale = set(_descriptor_cache)
    descriptors = []

    hid_guid = GUID()
    hid.HidD_GetHidGuid(ctypes.byref(hid_guid))

    collection = setupapi.SetupDiGetClassDevsA(
        ctypes.byref(hid_guid), None, None, DIGCF_DEVICEINTERFACE | DIGCF_PRESENT
    )
    try:
        index = 0
        interface_info = DeviceInterfaceData()
        interface_info.cbSize = ctypes.sizeof(DeviceInterfaceData)

        while True:
            result = setupapi.SetupDiEnumDeviceInterfaces(
                collection,
                0,
                ctypes.byref(hid_guid),
                index,
                ctypes.byref(interface_info),
            )
            index += 1
            if not result:
                break

            dw_detail_len = wintypes.DWORD()
            result = setupapi.SetupDiGetDeviceInterfaceDetailA(
                collection,
                ctypes.byref(interface_info),
                None,
                0,
                ctypes.byref(dw_detail_len),
                None,
            )
            if result:
                raise WinError()

            detail_len = dw_detail_len.value
            if detail_len == 0:
                # skip this device, some kind of error
                continue

            buf = ctypes.create_string_buffer(detail_len)
            interface_detail = DeviceInterfaceDetailData.from_buffer(buf)
            interface_detail.cbSize = ctypes.sizeof(DeviceInterfaceDetailData)

            result = setupapi.SetupDiGetDeviceInterfaceDetailA(
                collection,
                ctypes.byref(interface_info),
                ctypes.byref(interface_detail),
                detail_len,
                None,
                None,
            )
            if not result:
                raise WinError()

            path = ctypes.string_at(interface_detail.DevicePath)
            stale.discard(path)

            # Check if path already cached
            desc = _descriptor_cache.get(path)
            if desc:
                if desc is not _SKIP:
                    descriptors.append(desc)
                continue

            try:
                descriptor = get_descriptor(path)
                _descriptor_cache[path] = descriptor
                descriptors.append(descriptor)
                continue
            except ValueError:
                pass  # Not a CTAP device
            except Exception:
                logger.debug(
                    "Failed reading HID descriptor for %s", path, exc_info=True
                )
            _descriptor_cache[path] = _SKIP
    finally:
        setupapi.SetupDiDestroyDeviceInfoList(collection)

    # Remove entries from the cache that were not seen
    for path in stale:
        del _descriptor_cache[path]

    return descriptors
```

## File: fido2/__init__.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
```

## File: fido2/cbor.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
Minimal CBOR implementation supporting a subset of functionality and types
required for FIDO 2 CTAP.

Use the :func:`encode`, :func:`decode` and :func:`decode_from` functions to encode
and decode objects to/from CBOR.
"""

from __future__ import annotations

import struct
from typing import Any, Callable, Mapping, Sequence

CborType = int | bool | str | bytes | Sequence[Any] | Mapping[Any, Any]


def _dump_int(data: int, mt: int = 0) -> bytes:
    if data < 0:
        mt = 1
        data = -1 - data

    mt = mt << 5
    if data <= 23:
        args: Any = (">B", mt | data)
    elif data <= 0xFF:
        args = (">BB", mt | 24, data)
    elif data <= 0xFFFF:
        args = (">BH", mt | 25, data)
    elif data <= 0xFFFFFFFF:
        args = (">BI", mt | 26, data)
    else:
        args = (">BQ", mt | 27, data)
    return struct.pack(*args)


def _dump_bool(data: bool) -> bytes:
    return b"\xf5" if data else b"\xf4"


def _dump_list(data: Sequence[CborType]) -> bytes:
    return _dump_int(len(data), mt=4) + b"".join([encode(x) for x in data])


def _sort_keys(entry):
    key = entry[0]
    return key[0], len(key), key


def _dump_dict(data: Mapping[CborType, CborType]) -> bytes:
    items = [(encode(k), encode(v)) for k, v in data.items()]
    items.sort(key=_sort_keys)
    return _dump_int(len(items), mt=5) + b"".join([k + v for (k, v) in items])


def _dump_bytes(data: bytes) -> bytes:
    return _dump_int(len(data), mt=2) + data


def _dump_text(data: str) -> bytes:
    data_bytes = data.encode("utf8")
    return _dump_int(len(data_bytes), mt=3) + data_bytes


_SERIALIZERS: Sequence[tuple[type, Callable[[Any], bytes]]] = [
    (bool, _dump_bool),
    (int, _dump_int),
    (str, _dump_text),
    (bytes, _dump_bytes),
    (Mapping, _dump_dict),
    (Sequence, _dump_list),
]


def _load_int(ai: int, data: bytes) -> tuple[int, bytes]:
    if ai < 24:
        return ai, data
    elif ai == 24:
        return data[0], data[1:]
    elif ai == 25:
        return struct.unpack_from(">H", data)[0], data[2:]
    elif ai == 26:
        return struct.unpack_from(">I", data)[0], data[4:]
    elif ai == 27:
        return struct.unpack_from(">Q", data)[0], data[8:]
    raise ValueError("Invalid additional information")


def _load_nint(ai: int, data: bytes) -> tuple[int, bytes]:
    val, rest = _load_int(ai, data)
    return -1 - val, rest


def _load_bool(ai: int, data: bytes) -> tuple[bool, bytes]:
    return ai == 21, data


def _load_bytes(ai: int, data: bytes) -> tuple[bytes, bytes]:
    ln, data = _load_int(ai, data)
    return data[:ln], data[ln:]


def _load_text(ai: int, data: bytes) -> tuple[str, bytes]:
    enc, rest = _load_bytes(ai, data)
    return enc.decode("utf8"), rest


def _load_array(ai: int, data: bytes) -> tuple[Sequence[CborType], bytes]:
    ln, data = _load_int(ai, data)
    values = []
    for i in range(ln):
        val, data = decode_from(data)
        values.append(val)
    return values, data


def _load_map(ai: int, data: bytes) -> tuple[Mapping[CborType, CborType], bytes]:
    ln, data = _load_int(ai, data)
    values = {}
    for i in range(ln):
        k, data = decode_from(data)
        v, data = decode_from(data)
        values[k] = v
    return values, data


_DESERIALIZERS = {
    0: _load_int,
    1: _load_nint,
    2: _load_bytes,
    3: _load_text,
    4: _load_array,
    5: _load_map,
    7: _load_bool,
}


def encode(data: CborType) -> bytes:
    """Encodes data to a CBOR byte string."""
    for k, v in _SERIALIZERS:
        if isinstance(data, k):
            return v(data)
    raise ValueError(f"Unsupported value: {data!r}")


def decode_from(data: bytes) -> tuple[Any, bytes]:
    """Decodes a CBOR-encoded value from the start of a byte string.

    Additional data after a valid CBOR object is returned as well.

    :return: The decoded object, and any remaining data."""
    fb = data[0]
    return _DESERIALIZERS[fb >> 5](fb & 0b11111, data[1:])


def decode(data) -> CborType:
    """Decodes data from a CBOR-encoded byte string.

    Also validates that no extra data follows the encoded object.
    """
    value, rest = decode_from(data)
    if rest != b"":
        raise ValueError("Extraneous data")
    return value
```

## File: fido2/cose.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Sequence, TypeVar

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed448, ed25519, padding, rsa

from .utils import bytes2int, int2bytes

if TYPE_CHECKING:
    # This type isn't available on cryptography <40.
    from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes


class CoseKey(dict):
    """A COSE formatted public key.

    :param _: The COSE key paramters.
    :cvar ALGORITHM: COSE algorithm identifier.
    """

    ALGORITHM: int = None  # type: ignore

    def verify(self, message: bytes, signature: bytes) -> None:
        """Validates a digital signature over a given message.

        :param message: The message which was signed.
        :param signature: The signature to check.
        """
        raise NotImplementedError("Signature verification not supported.")

    @classmethod
    def from_cryptography_key(
        cls: type[T_CoseKey], public_key: PublicKeyTypes
    ) -> T_CoseKey:
        """Converts a PublicKey object from Cryptography into a COSE key.

        :param public_key: Either an EC or RSA public key.
        :return: A CoseKey.
        """
        raise NotImplementedError("Creation from cryptography not supported.")

    @staticmethod
    def for_alg(alg: int) -> type[CoseKey]:
        """Get a subclass of CoseKey corresponding to an algorithm identifier.

        :param alg: The COSE identifier of the algorithm.
        :return: A CoseKey.
        """

        def find_subclass(base_cls: type[CoseKey]) -> type[CoseKey] | None:
            for cls in base_cls.__subclasses__():
                if cls.ALGORITHM == alg:
                    return cls
                subresult = find_subclass(cls)
                if subresult:
                    return subresult
            return None

        return find_subclass(CoseKey) or UnsupportedKey

    @staticmethod
    def for_name(name: str) -> type[CoseKey]:
        """Get a subclass of CoseKey corresponding to an algorithm identifier.

        :param alg: The COSE identifier of the algorithm.
        :return: A CoseKey.
        """

        def find_subclass(base_cls: type[CoseKey]) -> type[CoseKey] | None:
            for cls in base_cls.__subclasses__():
                if cls.__name__ == name:
                    return cls
                subresult = find_subclass(cls)
                if subresult:
                    return subresult
            return None

        return find_subclass(CoseKey) or UnsupportedKey

    @staticmethod
    def parse(cose: Mapping[int, Any]) -> CoseKey:
        """Create a CoseKey from a dict"""
        alg = cose.get(3)
        if not alg:
            raise ValueError("COSE alg identifier must be provided.")
        return CoseKey.for_alg(alg)(cose)

    @staticmethod
    def supported_algorithms() -> Sequence[int]:
        """Get a list of all supported algorithm identifiers"""
        algs: Sequence[type[CoseKey]] = [
            ES256,
            EdDSA,
            ES384,
            ES512,
            PS256,
            RS256,
            ES256K,
        ]
        return [cls.ALGORITHM for cls in algs]


T_CoseKey = TypeVar("T_CoseKey", bound=CoseKey)


class UnsupportedKey(CoseKey):
    """A COSE key with an unsupported algorithm."""


class ES256(CoseKey):
    ALGORITHM = -7
    _HASH_ALG = hashes.SHA256()

    def verify(self, message, signature):
        if self[-1] != 1:
            raise ValueError("Unsupported elliptic curve")
        ec.EllipticCurvePublicNumbers(
            bytes2int(self[-2]), bytes2int(self[-3]), ec.SECP256R1()
        ).public_key(default_backend()).verify(
            signature, message, ec.ECDSA(self._HASH_ALG)
        )

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ec.EllipticCurvePublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls(
            {
                1: 2,
                3: cls.ALGORITHM,
                -1: 1,
                -2: int2bytes(pn.x, 32),
                -3: int2bytes(pn.y, 32),
            }
        )

    @classmethod
    def from_ctap1(cls, data):
        """Creates an ES256 key from a CTAP1 formatted public key byte string.

        :param data: A 65 byte SECP256R1 public key.
        :return: A ES256 key.
        """
        return cls({1: 2, 3: cls.ALGORITHM, -1: 1, -2: data[1:33], -3: data[33:65]})


class ESP256(ES256):
    # See: https://www.ietf.org/archive/id/draft-ietf-jose-fully-specified-algorithms-10.html#name-elliptic-curve-digital-sign  # noqa:E501
    ALGORITHM = -9


class ES384(CoseKey):
    ALGORITHM = -35
    _HASH_ALG = hashes.SHA384()

    def verify(self, message, signature):
        if self[-1] != 2:
            raise ValueError("Unsupported elliptic curve")
        ec.EllipticCurvePublicNumbers(
            bytes2int(self[-2]), bytes2int(self[-3]), ec.SECP384R1()
        ).public_key(default_backend()).verify(
            signature, message, ec.ECDSA(self._HASH_ALG)
        )

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ec.EllipticCurvePublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls(
            {
                1: 2,
                3: cls.ALGORITHM,
                -1: 2,
                -2: int2bytes(pn.x, 48),
                -3: int2bytes(pn.y, 48),
            }
        )


class ESP384(ES384):
    # See: https://www.ietf.org/archive/id/draft-ietf-jose-fully-specified-algorithms-12.html#name-elliptic-curve-digital-sign  # noqa:E501
    ALGORITHM = -51


class ES512(CoseKey):
    ALGORITHM = -36
    _HASH_ALG = hashes.SHA512()

    def verify(self, message, signature):
        if self[-1] != 3:
            raise ValueError("Unsupported elliptic curve")
        ec.EllipticCurvePublicNumbers(
            bytes2int(self[-2]), bytes2int(self[-3]), ec.SECP521R1()
        ).public_key(default_backend()).verify(
            signature, message, ec.ECDSA(self._HASH_ALG)
        )

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ec.EllipticCurvePublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls(
            {
                1: 2,
                3: cls.ALGORITHM,
                -1: 3,
                -2: int2bytes(pn.x, 66),
                -3: int2bytes(pn.y, 66),
            }
        )


class ESP512(ES512):
    # See: https://www.ietf.org/archive/id/draft-ietf-jose-fully-specified-algorithms-12.html#name-elliptic-curve-digital-sign  # noqa:E501
    ALGORITHM = -52


class RS256(CoseKey):
    ALGORITHM = -257
    _HASH_ALG = hashes.SHA256()

    def verify(self, message, signature):
        rsa.RSAPublicNumbers(bytes2int(self[-2]), bytes2int(self[-1])).public_key(
            default_backend()
        ).verify(signature, message, padding.PKCS1v15(), self._HASH_ALG)

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, rsa.RSAPublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls({1: 3, 3: cls.ALGORITHM, -1: int2bytes(pn.n), -2: int2bytes(pn.e)})


class PS256(CoseKey):
    ALGORITHM = -37
    _HASH_ALG = hashes.SHA256()

    def verify(self, message, signature):
        rsa.RSAPublicNumbers(bytes2int(self[-2]), bytes2int(self[-1])).public_key(
            default_backend()
        ).verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(self._HASH_ALG), salt_length=padding.PSS.MAX_LENGTH
            ),
            self._HASH_ALG,
        )

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, rsa.RSAPublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls({1: 3, 3: cls.ALGORITHM, -1: int2bytes(pn.n), -2: int2bytes(pn.e)})


class EdDSA(CoseKey):
    ALGORITHM = -8

    def verify(self, message, signature):
        if self[-1] != 6:
            raise ValueError("Unsupported elliptic curve")
        ed25519.Ed25519PublicKey.from_public_bytes(self[-2]).verify(signature, message)

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ed25519.Ed25519PublicKey)  # noqa: S101
        return cls(
            {
                1: 1,
                3: cls.ALGORITHM,
                -1: 6,
                -2: public_key.public_bytes(
                    serialization.Encoding.Raw, serialization.PublicFormat.Raw
                ),
            }
        )


class Ed25519(EdDSA):
    # See: https://www.ietf.org/archive/id/draft-ietf-jose-fully-specified-algorithms-12.html#name-edwards-curve-digital-signa  # noqa:E501
    ALGORITHM = -19


class Ed448(CoseKey):
    # See: https://www.ietf.org/archive/id/draft-ietf-jose-fully-specified-algorithms-12.html#name-edwards-curve-digital-signa  # noqa:E501
    ALGORITHM = -53

    def verify(self, message, signature):
        if self[-1] != 7:
            raise ValueError("Unsupported elliptic curve")
        ed448.Ed448PublicKey.from_public_bytes(self[-2]).verify(signature, message)

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ed448.Ed448PublicKey)  # noqa: S101
        return cls(
            {
                1: 1,
                3: cls.ALGORITHM,
                -1: 7,
                -2: public_key.public_bytes(
                    serialization.Encoding.Raw, serialization.PublicFormat.Raw
                ),
            }
        )


class RS1(CoseKey):
    ALGORITHM = -65535
    _HASH_ALG = hashes.SHA1()  # noqa: S303

    def verify(self, message, signature):
        rsa.RSAPublicNumbers(bytes2int(self[-2]), bytes2int(self[-1])).public_key(
            default_backend()
        ).verify(signature, message, padding.PKCS1v15(), self._HASH_ALG)

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, rsa.RSAPublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls({1: 3, 3: cls.ALGORITHM, -1: int2bytes(pn.n), -2: int2bytes(pn.e)})


class ES256K(CoseKey):
    ALGORITHM = -47
    _HASH_ALG = hashes.SHA256()

    def verify(self, message, signature):
        if self[-1] != 8:
            raise ValueError("Unsupported elliptic curve")
        ec.EllipticCurvePublicNumbers(
            bytes2int(self[-2]), bytes2int(self[-3]), ec.SECP256K1()
        ).public_key(default_backend()).verify(
            signature, message, ec.ECDSA(self._HASH_ALG)
        )

    @classmethod
    def from_cryptography_key(cls, public_key):
        assert isinstance(public_key, ec.EllipticCurvePublicKey)  # noqa: S101
        pn = public_key.public_numbers()
        return cls(
            {
                1: 2,
                3: cls.ALGORITHM,
                -1: 8,
                -2: int2bytes(pn.x, 32),
                -3: int2bytes(pn.y, 32),
            }
        )
```

## File: fido2/ctap.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import abc
from enum import IntEnum, unique
from threading import Event
from typing import Callable, Iterator


@unique
class STATUS(IntEnum):
    """Status code for CTAP keep-alive message."""

    PROCESSING = 1
    UPNEEDED = 2


class CtapDevice(abc.ABC):
    """
    CTAP-capable device.

    Subclasses of this should implement :func:`call`, as well as :func:`list_devices`,
    which should return a generator over discoverable devices.
    """

    @property
    @abc.abstractmethod
    def capabilities(self) -> int:
        """Get device capabilities"""

    @abc.abstractmethod
    def call(
        self,
        cmd: int,
        data: bytes = b"",
        event: Event | None = None,
        on_keepalive: Callable[[STATUS], None] | None = None,
    ) -> bytes:
        """Sends a command to the authenticator, and reads the response.

        :param cmd: The integer value of the command.
        :param data: The payload of the command.
        :param event: An optional threading.Event which can be used to cancel
            the invocation.
        :param on_keepalive: An optional callback to handle keep-alive messages
            from the authenticator. The function is only called once for
            consecutive keep-alive messages with the same status.
        :return: The response from the authenticator.
        """

    def close(self) -> None:
        """Close the device, releasing any held resources."""

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.close()

    @classmethod
    @abc.abstractmethod
    def list_devices(cls) -> Iterator[CtapDevice]:
        """Generates instances of cls for discoverable devices."""


class CtapError(Exception):
    """Error returned from the Authenticator when a command fails."""

    class UNKNOWN_ERR(int):
        """CTAP error status code that is not recognized."""

        name = "UNKNOWN_ERR"

        @property
        def value(self) -> int:
            return int(self)

        def __repr__(self):
            return "<ERR.UNKNOWN: %d>" % self

        def __str__(self):
            return f"0x{self:02X} - UNKNOWN"

    @unique
    class ERR(IntEnum):
        """CTAP status codes.

        https://fidoalliance.org/specs/fido-v2.1-rd-20201208/fido-client-to-authenticator-protocol-v2.1-rd-20201208.html#error-responses
        """

        SUCCESS = 0x00
        INVALID_COMMAND = 0x01
        INVALID_PARAMETER = 0x02
        INVALID_LENGTH = 0x03
        INVALID_SEQ = 0x04
        TIMEOUT = 0x05
        CHANNEL_BUSY = 0x06
        LOCK_REQUIRED = 0x0A
        INVALID_CHANNEL = 0x0B
        CBOR_UNEXPECTED_TYPE = 0x11
        INVALID_CBOR = 0x12
        MISSING_PARAMETER = 0x14
        LIMIT_EXCEEDED = 0x15
        # UNSUPPORTED_EXTENSION = 0x16  # No longer in spec
        FP_DATABASE_FULL = 0x17
        LARGE_BLOB_STORAGE_FULL = 0x18
        CREDENTIAL_EXCLUDED = 0x19
        PROCESSING = 0x21
        INVALID_CREDENTIAL = 0x22
        USER_ACTION_PENDING = 0x23
        OPERATION_PENDING = 0x24
        NO_OPERATIONS = 0x25
        UNSUPPORTED_ALGORITHM = 0x26
        OPERATION_DENIED = 0x27
        KEY_STORE_FULL = 0x28
        # NOT_BUSY = 0x29  # No longer in spec
        # NO_OPERATION_PENDING = 0x2A  # No longer in spec
        UNSUPPORTED_OPTION = 0x2B
        INVALID_OPTION = 0x2C
        KEEPALIVE_CANCEL = 0x2D
        NO_CREDENTIALS = 0x2E
        USER_ACTION_TIMEOUT = 0x2F
        NOT_ALLOWED = 0x30
        PIN_INVALID = 0x31
        PIN_BLOCKED = 0x32
        PIN_AUTH_INVALID = 0x33
        PIN_AUTH_BLOCKED = 0x34
        PIN_NOT_SET = 0x35
        PUAT_REQUIRED = 0x36
        PIN_POLICY_VIOLATION = 0x37
        PIN_TOKEN_EXPIRED = 0x38
        REQUEST_TOO_LARGE = 0x39
        ACTION_TIMEOUT = 0x3A
        UP_REQUIRED = 0x3B
        UV_BLOCKED = 0x3C
        INTEGRITY_FAILURE = 0x3D
        INVALID_SUBCOMMAND = 0x3E
        UV_INVALID = 0x3F
        UNAUTHORIZED_PERMISSION = 0x40
        OTHER = 0x7F
        SPEC_LAST = 0xDF
        EXTENSION_FIRST = 0xE0
        EXTENSION_LAST = 0xEF
        VENDOR_FIRST = 0xF0
        VENDOR_LAST = 0xFF

        def __str__(self):
            return f"0x{self.value:02X} - {self.name}"

    def __init__(self, code: int):
        try:
            self.code = CtapError.ERR(code)
        except ValueError:
            self.code = CtapError.UNKNOWN_ERR(code)  # type: ignore
        super().__init__(f"CTAP error: {self.code}")
```

## File: fido2/ctap1.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import struct
from dataclasses import dataclass
from enum import IntEnum, unique

from .attestation import FidoU2FAttestation
from .cose import ES256
from .ctap import CtapDevice
from .hid import CTAPHID
from .utils import ByteBuffer, bytes2int, websafe_decode, websafe_encode


@unique
class APDU(IntEnum):
    """APDU response codes."""

    OK = 0x9000
    USE_NOT_SATISFIED = 0x6985
    WRONG_DATA = 0x6A80


class ApduError(Exception):
    """An Exception thrown when a response APDU doesn't have an OK (0x9000)
    status.

    :param code: APDU response code.
    :param data: APDU response body.

    """

    def __init__(self, code: int, data: bytes = b""):
        self.code = code
        self.data = data

    def __repr__(self):
        return f"APDU error: 0x{self.code:04X} {len(self.data):d} bytes of data"


@dataclass(init=False)
class RegistrationData(bytes):
    """Binary response data for a CTAP1 registration.

    :param _: The binary contents of the response data.
    :ivar public_key: Binary representation of the credential public key.
    :ivar key_handle: Binary key handle of the credential.
    :ivar certificate: Attestation certificate of the authenticator, DER
        encoded.
    :ivar signature: Attestation signature.
    """

    public_key: bytes
    key_handle: bytes
    certificate: bytes
    signature: bytes

    def __init__(self, _: bytes):
        super().__init__()

        reader = ByteBuffer(self)
        if reader.unpack("B") != 0x05:
            raise ValueError("Reserved byte != 0x05")

        self.public_key = reader.read(65)
        self.key_handle = reader.read(reader.unpack("B"))

        cert_buf = reader.read(2)  # Tag and first length byte
        cert_len = cert_buf[1]
        if cert_len > 0x80:  # Multi-byte length
            n_bytes = cert_len - 0x80
            len_bytes = reader.read(n_bytes)
            cert_buf += len_bytes
            cert_len = bytes2int(len_bytes)
        self.certificate = cert_buf + reader.read(cert_len)
        self.signature = reader.read()

    @property
    def b64(self) -> str:
        """Websafe base64 encoded string of the RegistrationData."""
        return websafe_encode(self)

    def verify(self, app_param: bytes, client_param: bytes) -> None:
        """Verify the included signature with regard to the given app and client
        params.

        :param app_param: SHA256 hash of the app ID used for the request.
        :param client_param: SHA256 hash of the ClientData used for the request.
        """
        FidoU2FAttestation.verify_signature(
            app_param,
            client_param,
            self.key_handle,
            self.public_key,
            self.certificate,
            self.signature,
        )

    @classmethod
    def from_b64(cls, data: str) -> RegistrationData:
        """Parse a RegistrationData from a websafe base64 encoded string.

        :param data: Websafe base64 encoded string.
        :return: The decoded and parsed RegistrationData.
        """
        return cls(websafe_decode(data))


@dataclass(init=False)
class SignatureData(bytes):
    """Binary response data for a CTAP1 authentication.

    :param _: The binary contents of the response data.
    :ivar user_presence: User presence byte.
    :ivar counter: Signature counter.
    :ivar signature: Cryptographic signature.
    """

    user_presence: int
    counter: int
    signature: bytes

    def __init__(self, _: bytes):
        super().__init__()

        reader = ByteBuffer(self)
        self.user_presence = reader.unpack("B")
        self.counter = reader.unpack(">I")
        self.signature = reader.read()

    @property
    def b64(self) -> str:
        """str: Websafe base64 encoded string of the SignatureData."""
        return websafe_encode(self)

    def verify(self, app_param: bytes, client_param: bytes, public_key: bytes) -> None:
        """Verify the included signature with regard to the given app and client
        params, using the given public key.

        :param app_param: SHA256 hash of the app ID used for the request.
        :param client_param: SHA256 hash of the ClientData used for the request.
        :param public_key: Binary representation of the credential public key.
        """
        m = app_param + self[:5] + client_param
        ES256.from_ctap1(public_key).verify(m, self.signature)

    @classmethod
    def from_b64(cls, data: str) -> SignatureData:
        """Parse a SignatureData from a websafe base64 encoded string.

        :param data: Websafe base64 encoded string.
        :return: The decoded and parsed SignatureData.
        """
        return cls(websafe_decode(data))


class Ctap1:
    """Implementation of the CTAP1 specification.

    :param device: A CtapHidDevice handle supporting CTAP1.
    """

    @unique
    class INS(IntEnum):
        REGISTER = 0x01
        AUTHENTICATE = 0x02
        VERSION = 0x03

    def __init__(self, device: CtapDevice):
        self.device = device

    def send_apdu(
        self, cla: int = 0, ins: int = 0, p1: int = 0, p2: int = 0, data: bytes = b""
    ) -> bytes:
        """Packs and sends an APDU for use in CTAP1 commands.
        This is a low-level method mainly used internally. Avoid calling it
        directly if possible, and use the get_version, register, and
        authenticate methods if possible instead.

        :param cla: The CLA parameter of the request.
        :param ins: The INS parameter of the request.
        :param p1: The P1 parameter of the request.
        :param p2: The P2 parameter of the request.
        :param data: The body of the request.
        :return: The response APDU data of a successful request.
        :raise: ApduError
        """
        apdu = struct.pack(">BBBBBH", cla, ins, p1, p2, 0, len(data)) + data + b"\0\0"

        response = self.device.call(CTAPHID.MSG, apdu)
        status = struct.unpack(">H", response[-2:])[0]
        data = response[:-2]
        if status != APDU.OK:
            raise ApduError(status, data)
        return data

    def get_version(self) -> str:
        """Get the U2F version implemented by the authenticator.
        The only version specified is "U2F_V2".

        :return: A U2F version string.
        """
        return self.send_apdu(ins=Ctap1.INS.VERSION).decode()

    def register(self, client_param: bytes, app_param: bytes) -> RegistrationData:
        """Register a new U2F credential.

        :param client_param: SHA256 hash of the ClientData used for the request.
        :param app_param: SHA256 hash of the app ID used for the request.
        :return: The registration response from the authenticator.
        """
        data = client_param + app_param
        response = self.send_apdu(ins=Ctap1.INS.REGISTER, data=data)
        return RegistrationData(response)

    def authenticate(
        self,
        client_param: bytes,
        app_param: bytes,
        key_handle: bytes,
        check_only: bool = False,
    ) -> SignatureData:
        """Authenticate a previously registered credential.

        :param client_param: SHA256 hash of the ClientData used for the request.
        :param app_param: SHA256 hash of the app ID used for the request.
        :param key_handle: The binary key handle of the credential.
        :param check_only: True to send a "check-only" request, which is used to
            determine if a key handle is known.
        :return: The authentication response from the authenticator.
        """
        data = (
            client_param + app_param + struct.pack(">B", len(key_handle)) + key_handle
        )
        p1 = 0x07 if check_only else 0x03
        response = self.send_apdu(ins=Ctap1.INS.AUTHENTICATE, p1=p1, data=data)
        return SignatureData(response)
```

## File: fido2/features.py
```python
# Copyright (c) 2022 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import warnings


class FeatureNotEnabledError(Exception):
    pass


class _Feature:
    def __init__(self, name: str, desc: str):
        self._enabled: bool | None = None
        self._name = name
        self._desc = desc

    @property
    def enabled(self) -> bool:
        self.warn()
        return self._enabled is True

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if self._enabled is not None:
            raise ValueError(
                f"{self._name} has already been configured with {self._enabled}"
            )
        self._enabled = value

    def require(self, state=True) -> None:
        if self._enabled != state:
            self.warn()
            raise FeatureNotEnabledError(
                f"Usage requires {self._name}.enabled = {state}"
            )

    def warn(self) -> None:
        if self._enabled is None:
            warnings.warn(
                f"""Deprecated use of {self._name}.

You are using deprecated functionality which will change in the next major version of
python-fido2. You can opt-in to use the new functionality now by adding the following
to your code somewhere where it gets executed prior to using the affected functionality:

  import fido2.features
  fido2.features.{self._name}.enabled = True

To silence this warning but retain the current behavior, instead set enabled to False:
  fido2.features.{self._name}.enabled = False

{self._desc}
            """,
                DeprecationWarning,
            )
```

## File: fido2/mds3.py
```python
# Copyright (c) 2022 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import json
import logging
from base64 import b64decode, b64encode
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, unique
from typing import Any, Callable, Mapping, Sequence

from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .attestation import (
    Attestation,
    AttestationVerifier,
    UntrustedAttestation,
    verify_x509_chain,
)
from .cose import CoseKey
from .utils import _JsonDataObject, websafe_decode
from .webauthn import Aaguid, AttestationObject

logger = logging.getLogger(__name__)


@dataclass(eq=False, frozen=True)
class Version(_JsonDataObject):
    major: int
    minor: int


@dataclass(eq=False, frozen=True)
class RogueListEntry(_JsonDataObject):
    sk: bytes
    date: int


@dataclass(eq=False, frozen=True)
class BiometricStatusReport(_JsonDataObject):
    cert_level: int
    modality: str
    effective_date: int
    certification_descriptor: str
    certificate_number: str
    certification_policy_version: str
    certification_requirements_version: str


@dataclass(eq=False, frozen=True)
class CodeAccuracyDescriptor(_JsonDataObject):
    base: int
    min_length: int
    max_retries: int | None = None
    block_slowdown: int | None = None


@dataclass(eq=False, frozen=True)
class BiometricAccuracyDescriptor(_JsonDataObject):
    self_attested_frr: float | None = field(
        default=None, metadata=dict(name="selfAttestedFRR")
    )
    self_attested_far: float | None = field(
        default=None, metadata=dict(name="selfAttestedFAR")
    )
    max_templates: int | None = None
    max_retries: int | None = None
    block_slowdown: int | None = None


@dataclass(eq=False, frozen=True)
class PatternAccuracyDescriptor(_JsonDataObject):
    min_complexity: int
    max_retries: int | None = None
    block_slowdown: int | None = None


@dataclass(eq=False, frozen=True)
class VerificationMethodDescriptor(_JsonDataObject):
    user_verification_method: str | None = None
    ca_desc: CodeAccuracyDescriptor | None = None
    ba_desc: BiometricAccuracyDescriptor | None = None
    pa_desc: PatternAccuracyDescriptor | None = None


@dataclass(eq=False, frozen=True)
class RgbPaletteEntry(_JsonDataObject):
    r: int
    g: int
    b: int


@dataclass(eq=False, frozen=True)
class DisplayPngCharacteristicsDescriptor(_JsonDataObject):
    width: int
    height: int
    bit_depth: int
    color_type: int
    compression: int
    filter: int
    interlace: int
    plte: Sequence[RgbPaletteEntry] | None = None


@dataclass(eq=False, frozen=True)
class EcdaaTrustAnchor(_JsonDataObject):
    x: str = field(metadata=dict(name="X"))
    y: str = field(metadata=dict(name="Y"))
    c: str
    sx: str
    sy: str
    g1_curve: str = field(metadata=dict(name="G1Curve"))


@unique
class AuthenticatorStatus(str, Enum):
    """Status of an Authenticator."""

    NOT_FIDO_CERTIFIED = "NOT_FIDO_CERTIFIED"
    FIDO_CERTIFIED = "FIDO_CERTIFIED"
    USER_VERIFICATION_BYPASS = "USER_VERIFICATION_BYPASS"
    ATTESTATION_KEY_COMPROMISE = "ATTESTATION_KEY_COMPROMISE"
    USER_KEY_REMOTE_COMPROMISE = "USER_KEY_REMOTE_COMPROMISE"
    USER_KEY_PHYSICAL_COMPROMISE = "USER_KEY_PHYSICAL_COMPROMISE"
    UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    REVOKED = "REVOKED"
    SELF_ASSERTION_SUBMITTED = "SELF_ASSERTION_SUBMITTED"
    FIDO_CERTIFIED_L1 = "FIDO_CERTIFIED_L1"
    FIDO_CERTIFIED_L1plus = "FIDO_CERTIFIED_L1plus"
    FIDO_CERTIFIED_L2 = "FIDO_CERTIFIED_L2"
    FIDO_CERTIFIED_L2plus = "FIDO_CERTIFIED_L2plus"
    FIDO_CERTIFIED_L3 = "FIDO_CERTIFIED_L3"
    FIDO_CERTIFIED_L3plus = "FIDO_CERTIFIED_L3plus"


@dataclass(eq=False, frozen=True)
class StatusReport(_JsonDataObject):
    status: AuthenticatorStatus
    effective_date: date | None = field(
        metadata=dict(
            deserialize=date.fromisoformat,
            serialize=lambda x: x.isoformat(),
        ),
        default=None,
    )
    authenticator_version: int | None = None
    certificate: bytes | None = field(
        metadata=dict(deserialize=b64decode, serialize=lambda x: b64encode(x).decode()),
        default=None,
    )
    url: str | None = None
    certification_descriptor: str | None = None
    certificate_number: str | None = None
    certification_policy_version: str | None = None
    certification_requirements_version: str | None = None


@dataclass(eq=False, frozen=True)
class ExtensionDescriptor(_JsonDataObject):
    fail_if_unknown: bool = field(metadata=dict(name="fail_if_unknown"))
    id: str
    tag: int | None = None
    data: str | None = None


@dataclass(eq=False, frozen=True)
class MetadataStatement(_JsonDataObject):
    description: str
    authenticator_version: int
    schema: int
    upv: Sequence[Version]
    attestation_types: Sequence[str]
    user_verification_details: Sequence[Sequence[VerificationMethodDescriptor]] = field(
        metadata=dict(serialize=lambda xss: [[dict(x) for x in xs] for xs in xss])
    )
    key_protection: Sequence[str]
    matcher_protection: Sequence[str]
    attachment_hint: Sequence[str]
    tc_display: Sequence[str]
    attestation_root_certificates: Sequence[bytes] = field(
        metadata=dict(
            deserialize=lambda xs: [b64decode(x) for x in xs],
            serialize=lambda xs: [b64encode(x).decode() for x in xs],
        )
    )
    legal_header: str | None = None
    aaid: str | None = None
    aaguid: Aaguid | None = field(
        metadata=dict(
            deserialize=Aaguid.parse,
            serialize=lambda x: str(x),
        ),
        default=None,
    )
    attestation_certificate_key_identifiers: Sequence[bytes] | None = field(
        metadata=dict(
            deserialize=lambda xs: [bytes.fromhex(x) for x in xs],
            serialize=lambda xs: [x.hex() for x in xs],
        ),
        default=None,
    )
    alternative_descriptions: Mapping[str, str] | None = None
    protocol_family: str | None = None
    authentication_algorithms: Sequence[str] | None = None
    public_key_alg_and_encodings: Sequence[str] | None = None
    is_key_restricted: bool | None = None
    is_fresh_user_verification_required: bool | None = None
    crypto_strength: int | None = None
    operating_env: str | None = None
    tc_display_content_type: str | None = None
    tc_display_png_characteristics: (
        Sequence[DisplayPngCharacteristicsDescriptor] | None
    ) = field(
        metadata=dict(name="tcDisplayPNGCharacteristics"),
        default=None,
    )
    ecdaa_trust_anchors: Sequence[EcdaaTrustAnchor] | None = None
    icon: str | None = None
    supported_extensions: Sequence[ExtensionDescriptor] | None = None
    authenticator_get_info: Mapping[str, Any] | None = None


@dataclass(eq=False, frozen=True)
class MetadataBlobPayloadEntry(_JsonDataObject):
    status_reports: Sequence[StatusReport]
    time_of_last_status_change: date = field(
        metadata=dict(
            deserialize=date.fromisoformat,
            serialize=lambda x: x.isoformat(),
        )
    )
    aaid: str | None = None
    aaguid: Aaguid | None = field(
        metadata=dict(
            deserialize=Aaguid.parse,
            serialize=lambda x: str(x),
        ),
        default=None,
    )
    attestation_certificate_key_identifiers: Sequence[bytes] | None = field(
        metadata=dict(
            deserialize=lambda xs: [bytes.fromhex(x) for x in xs],
            serialize=lambda xs: [x.hex() for x in xs],
        ),
        default=None,
    )
    metadata_statement: MetadataStatement | None = None
    biometric_status_reports: Sequence[BiometricStatusReport] | None = None
    rogue_list_url: str | None = field(metadata=dict(name="rogueListURL"), default=None)
    rogue_list_hash: bytes | None = field(
        metadata=dict(
            deserialize=bytes.fromhex,
            serialize=lambda x: x.hex(),
        ),
        default=None,
    )


@dataclass(eq=False, frozen=True)
class MetadataBlobPayload(_JsonDataObject):
    legal_header: str
    no: int
    next_update: date = field(
        metadata=dict(
            deserialize=date.fromisoformat,
            serialize=lambda x: x.isoformat(),
        )
    )
    entries: Sequence[MetadataBlobPayloadEntry]


EntryFilter = Callable[[MetadataBlobPayloadEntry], bool]
LookupFilter = Callable[[MetadataBlobPayloadEntry, Sequence[bytes]], bool]


def filter_revoked(entry: MetadataBlobPayloadEntry) -> bool:
    """Filters out any revoked metadata entry.

    This filter will remove any metadata entry which has a status_report with
    the REVOKED status.
    """
    return not any(
        r.status == AuthenticatorStatus.REVOKED for r in entry.status_reports
    )


def filter_attestation_key_compromised(
    entry: MetadataBlobPayloadEntry, certificate_chain: Sequence[bytes]
) -> bool:
    """Denies any attestation that has a compromised attestation key.

    This filter checks the status reports of a metadata entry and ensures the
    attestation isn't signed by a key which is marked as compromised.
    """
    for r in entry.status_reports:
        if r.status == AuthenticatorStatus.ATTESTATION_KEY_COMPROMISE:
            if r.certificate in certificate_chain:
                return False
    return True


_last_entry: ContextVar[MetadataBlobPayloadEntry | None] = ContextVar("_last_entry")


class MdsAttestationVerifier(AttestationVerifier):
    """MDS3 implementation of an AttestationVerifier.

    The entry_filter is an optional predicate used to filter which metadata entries to
    include in the lookup for verification. By default, a filter that removes any
    entries that have a status report indicating the authenticator is REVOKED is used.
    See: filter_revoked

    The attestation_filter is an optional predicate used to filter metadata entries
    while performing attestation validation, and may take into account the
    Authenticators attestation trust_chain. By default, a filter that will fail any
    verification that has a trust_chain where one of the certificates is marked as
    compromised by the metadata statement is used.
    See: filter_attestation_key_compromised

    NOTE: The attestation_filter is not used when calling find_entry_by_aaguid nor
    find_entry_by_chain as no attestation is being verified!

    Setting either filter (including setting it to None) will replace it, removing
    the default behavior.

    :param blob: The MetadataBlobPayload to query for device metadata.
    :param entry_filter: An optional filter to exclude entries from lookup.
    :param attestation_filter: An optional filter to fail verification for a given
        attestation.
    :param attestation_types: A list of Attestation types to support.
    """

    def __init__(
        self,
        blob: MetadataBlobPayload,
        entry_filter: EntryFilter | None = filter_revoked,
        attestation_filter: LookupFilter | None = filter_attestation_key_compromised,
        attestation_types: Sequence[Attestation] | None = None,
    ):
        super().__init__(attestation_types)
        self._attestation_filter = attestation_filter or (
            lambda a, b: True
        )  # No-op for None

        entries = (
            [e for e in blob.entries if entry_filter(e)]
            if entry_filter
            else blob.entries
        )
        self._aaguid_table = {e.aaguid: e for e in entries if e.aaguid}
        self._ski_table = {
            ski: e
            for e in entries
            for ski in e.attestation_certificate_key_identifiers or []
        }

    def find_entry_by_aaguid(self, aaguid: Aaguid) -> MetadataBlobPayloadEntry | None:
        """Find an entry by AAGUID.

        Returns a MetadataBlobPayloadEntry with a matching aaguid field, if found.
        This method does not take the attestation_filter into account.
        """
        return self._aaguid_table.get(aaguid)

    def find_entry_by_chain(
        self, certificate_chain: Sequence[bytes]
    ) -> MetadataBlobPayloadEntry | None:
        """Find an entry by trust chain.

        Returns a MetadataBlobPayloadEntry containing an
        attestationCertificateKeyIdentifier which matches one of the certificates in the
        given chain, if found.
        This method does not take the attestation_filter into account.
        """
        for der in certificate_chain:
            cert = x509.load_der_x509_certificate(der, default_backend())
            ski = x509.SubjectKeyIdentifier.from_public_key(cert.public_key()).digest
            if ski in self._ski_table:
                return self._ski_table[ski]
        return None

    def ca_lookup(self, attestation_result, auth_data):
        assert auth_data.credential_data is not None  # noqa: S101
        aaguid = auth_data.credential_data.aaguid
        if aaguid:
            logging.debug(f"Using AAGUID: {aaguid} to look up metadata")
            entry = self.find_entry_by_aaguid(aaguid)
        else:
            logging.debug("Using trust_path chain to look up metadata")
            entry = self.find_entry_by_chain(attestation_result.trust_path)

        if entry:
            logging.debug(f"Found entry: {entry}")

            # Check attestation filter
            if not self._attestation_filter(entry, attestation_result.trust_path):
                logging.debug("Matched entry did not pass attestation filter")
                return None

            # Figure out which root to use
            if not entry.metadata_statement:
                logging.warning(
                    "Matched entry has no metadata_statement, can't validate!"
                )
                return None

            issuer = x509.load_der_x509_certificate(
                attestation_result.trust_path[-1], default_backend()
            ).issuer

            for root in entry.metadata_statement.attestation_root_certificates:
                subject = x509.load_der_x509_certificate(
                    root, default_backend()
                ).subject
                if subject == issuer:
                    _last_entry.set(entry)
                    return root
            logger.info(f"No attestation root matching subject: {issuer}")
        return None

    def find_entry(
        self, attestation_object: AttestationObject, client_data_hash: bytes
    ) -> MetadataBlobPayloadEntry | None:
        """Lookup a Metadata entry based on an Attestation.

        Returns the first Metadata entry matching the given attestation and verifies it,
        including checking it against the attestation_filter.
        """
        token = _last_entry.set(None)
        try:
            self.verify_attestation(attestation_object, client_data_hash)
            return _last_entry.get()
        except UntrustedAttestation:
            return None
        finally:
            _last_entry.reset(token)


def parse_blob(blob: bytes, trust_root: bytes | None) -> MetadataBlobPayload:
    """Parse a FIDO MDS3 blob and verifies its signature.

    See https://fidoalliance.org/metadata/ for details on obtaining the blob, as well as
    the CA certificate used to sign it.

    The resulting MetadataBlobPayload can be used to lookup metadata entries for
    specific Authenticators, or used with the MdsAttestationVerifier to verify that the
    attestation from a WebAuthn registration is valid and included in the metadata blob.

    NOTE: If trust_root is None, the signature of the blob will NOT be verified!
    """
    message, signature_b64 = blob.rsplit(b".", 1)
    signature = websafe_decode(signature_b64)
    header, payload = (json.loads(websafe_decode(x)) for x in message.split(b"."))

    if trust_root is not None:
        # Verify trust chain
        chain = [b64decode(c) for c in header.get("x5c", [])]
        chain += [trust_root]
        verify_x509_chain(chain)

        # Verify blob signature using leaf
        leaf = x509.load_der_x509_certificate(chain[0], default_backend())
        public_key = CoseKey.for_name(header["alg"]).from_cryptography_key(
            leaf.public_key()
        )
        public_key.verify(message, signature)
    else:
        logger.warning(
            "Parsing MDS blob without trust anchor, CONTENT IS NOT VERIFIED!"
        )

    return MetadataBlobPayload.from_dict(payload)
```

## File: fido2/payment.py
```python
# Copyright (c) 2025 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from dataclasses import dataclass

from .client import DefaultClientDataCollector
from .ctap2.extensions import (
    AuthenticationExtensionsPaymentInputs,
    PaymentCredentialInstrument,
    PaymentCurrencyAmount,
)
from .utils import _JsonDataObject
from .webauthn import (
    AuthenticatorAttachment,
    CollectedClientData,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

"""
Implements client and server functionality for the WebAuthn "payment" extension.

https://www.w3.org/TR/secure-payment-confirmation/#sctn-payment-extension-registration
"""


@dataclass(eq=False, frozen=True, kw_only=True)
class CollectedClientAdditionalPaymentData(_JsonDataObject):
    rp_id: str
    top_origin: str
    payee_name: str | None = None
    payee_origin: str | None = None
    total: PaymentCurrencyAmount
    instrument: PaymentCredentialInstrument


@dataclass(init=False, frozen=True, kw_only=True)
class CollectedClientPaymentData(CollectedClientData):
    payment: CollectedClientAdditionalPaymentData

    def __init__(self, serialized: bytes):
        super().__init__(serialized)

        payment = CollectedClientAdditionalPaymentData.from_dict(self._data["payment"])
        object.__setattr__(self, "payment", payment)

    @classmethod
    def create(
        cls,
        type: str,
        challenge: bytes | str,
        origin: str,
        cross_origin: bool = False,
        **kwargs,
    ) -> CollectedClientData:
        return super().create(
            type=type,
            challenge=challenge,
            origin=origin,
            cross_origin=cross_origin,
            payment=dict(kwargs.pop("payment")),
            **kwargs,
        )


class PaymentClientDataCollector(DefaultClientDataCollector):
    """ClientDataCollector for the WebAuthn "payment" extension.

    This class can be used together with the CTAP2 "thirdPartyPayment" extension to
    enable third-party payment confirmation. It collects the necessary client data and
    validates the options provided by the client.
    """

    def collect_client_data(self, options):
        # Get the effective RP ID from the request options, falling back to the origin
        rp_id = self.get_rp_id(options, self._origin)
        inputs = options.extensions or {}
        data = AuthenticationExtensionsPaymentInputs.from_dict(inputs.get("payment"))
        if data and data.is_payment:
            if isinstance(options, PublicKeyCredentialCreationOptions):
                sel = options.authenticator_selection
                if (
                    not sel
                    or sel.authenticator_attachment
                    not in (
                        AuthenticatorAttachment.PLATFORM,
                        # This is against the spec, but we need cross-platform
                        AuthenticatorAttachment.CROSS_PLATFORM,
                    )
                    or sel.resident_key
                    not in (
                        ResidentKeyRequirement.REQUIRED,
                        ResidentKeyRequirement.PREFERRED,
                    )
                    or sel.user_verification != UserVerificationRequirement.REQUIRED
                ):
                    raise ValueError("Invalid options for payment extension")
            elif isinstance(options, PublicKeyCredentialRequestOptions):
                # NOTE: We skip RP ID validation, as per the spec
                return (
                    CollectedClientPaymentData.create(
                        type="payment.get",
                        origin=self._origin,
                        challenge=options.challenge,
                        payment=CollectedClientAdditionalPaymentData(
                            rp_id=data.rp_id,
                            top_origin=data.top_origin,
                            payee_name=data.payee_name,
                            payee_origin=data.payee_origin,
                            total=data.total,
                            instrument=data.instrument,
                        ),
                    ),
                    rp_id,
                )

        # Validate that the RP ID is valid for the given origin
        self.verify_rp_id(rp_id, self._origin)
        return super().collect_client_data(options)
```

## File: fido2/pcsc.py
```python
# Copyright (c) 2019 Yubico AB
# Copyright (c) 2019 Oleg Moiseenko
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import struct
from threading import Event
from typing import Callable, Iterator

from smartcard import System
from smartcard.CardConnection import CardConnection
from smartcard.pcsc.PCSCExceptions import ListReadersException

from .ctap import STATUS, CtapDevice, CtapError
from .hid import CAPABILITY, CTAPHID
from .utils import LOG_LEVEL_TRAFFIC

AID_FIDO = b"\xa0\x00\x00\x06\x47\x2f\x00\x01"
SW_SUCCESS = (0x90, 0x00)
SW_UPDATE = (0x91, 0x00)
SW1_MORE_DATA = 0x61


logger = logging.getLogger(__name__)


class CtapPcscDevice(CtapDevice):
    """
    CtapDevice implementation using pyscard (PCSC).

    This class is intended for use with NFC readers.
    """

    def __init__(self, connection: CardConnection, name: str):
        self._name = name
        self._capabilities = CAPABILITY(0)
        self.use_ext_apdu = False
        self.use_nfcctap_getresponse = True
        self._conn = connection
        self.connect()

        try:  # Probe for CTAP2 by calling GET_INFO
            self.call(CTAPHID.CBOR, b"\x04")
            self._capabilities |= CAPABILITY.CBOR
        except CtapError:
            if not self._capabilities:
                raise ValueError("Unsupported device")

    def connect(self):
        self._conn.connect()
        self._select()

    def __repr__(self):
        return f"CtapPcscDevice({self._name})"

    @property
    def version(self) -> int:
        """CTAPHID protocol version."""
        return 2 if CAPABILITY.CBOR in self._capabilities else 1

    @property
    def capabilities(self) -> CAPABILITY:
        """Capabilities supported by the device."""
        return self._capabilities

    @property
    def product_name(self) -> str | None:
        """Product name of device."""
        return None

    @property
    def serial_number(self) -> int | None:
        """Serial number of device."""
        return None

    def get_atr(self) -> bytes:
        """Get the ATR/ATS of the connected card."""
        return bytes(self._conn.getATR() or b"")

    def apdu_exchange(
        self, apdu: bytes, protocol: int | None = None
    ) -> tuple[bytes, int, int]:
        """Exchange data with smart card.

        :param apdu: byte string. data to exchange with card
        :return: byte string. response from card
        """

        logger.log(LOG_LEVEL_TRAFFIC, "SEND: %s", apdu.hex())
        resp, sw1, sw2 = self._conn.transmit(list(apdu), protocol)
        response = bytes(resp)
        logger.log(LOG_LEVEL_TRAFFIC, "RECV: %s SW=%02X%02X", response.hex(), sw1, sw2)

        return response, sw1, sw2

    def control_exchange(self, control_code: int, control_data: bytes = b"") -> bytes:
        """Sends control sequence to reader's driver.

        :param control_code: int. code to send to reader driver.
        :param control_data: byte string. data to send to driver
        :return: byte string. response
        """

        logger.log(LOG_LEVEL_TRAFFIC, "Send control: %s", control_data.hex())
        response = self._conn.control(control_code, list(control_data))
        response = bytes(response)
        logger.log(LOG_LEVEL_TRAFFIC, "Control response: %s", response.hex())

        return response

    def _select(self) -> None:
        apdu = b"\x00\xa4\x04\x00" + struct.pack("!B", len(AID_FIDO)) + AID_FIDO
        resp, sw1, sw2 = self._chained_apdu_exchange(apdu)
        if (sw1, sw2) != SW_SUCCESS:
            raise ValueError("FIDO applet selection failure.")
        if resp == b"U2F_V2":
            self._capabilities |= CAPABILITY.NMSG

    def _chain_apdus(
        self, cla: int, ins: int, p1: int, p2: int, data: bytes = b""
    ) -> tuple[bytes, int, int]:
        if self.use_ext_apdu:
            header = struct.pack("!BBBBBH", cla, ins, p1, p2, 0x00, len(data))
            resp, sw1, sw2 = self.apdu_exchange(header + data)
            return resp, sw1, sw2
        else:
            while len(data) > 250:
                to_send, data = data[:250], data[250:]
                header = struct.pack("!BBBBB", 0x10 | cla, ins, p1, p2, len(to_send))
                resp, sw1, sw2 = self.apdu_exchange(header + to_send)
                if (sw1, sw2) != SW_SUCCESS:
                    return resp, sw1, sw2
            apdu = struct.pack("!BBBB", cla, ins, p1, p2)
            if data:
                apdu += struct.pack("!B", len(data)) + data
            resp, sw1, sw2 = self.apdu_exchange(apdu + b"\x00")
            while sw1 == SW1_MORE_DATA:
                apdu = b"\x00\xc0\x00\x00" + struct.pack("!B", sw2)  # sw2 == le
                lres, sw1, sw2 = self.apdu_exchange(apdu)
                resp += lres
            return resp, sw1, sw2

    def _chained_apdu_exchange(self, apdu: bytes) -> tuple[bytes, int, int]:
        if len(apdu) >= 7 and apdu[4] == 0:
            # Extended APDU
            data_len = struct.unpack("!H", apdu[5:7])[0]
            data = apdu[7 : 7 + data_len]
        elif len(apdu) == 4:
            data = b""
        else:
            # Short APDU
            data_len = apdu[4]
            data = apdu[5 : 5 + data_len]
        (cla, ins, p1, p2) = apdu[:4]

        return self._chain_apdus(cla, ins, p1, p2, data)

    def _call_apdu(self, apdu: bytes) -> bytes:
        resp, sw1, sw2 = self._chained_apdu_exchange(apdu)
        return resp + struct.pack("!BB", sw1, sw2)

    def _call_cbor(
        self,
        data: bytes = b"",
        event: Event | None = None,
        on_keepalive: Callable[[STATUS], None] | None = None,
    ) -> bytes:
        event = event or Event()

        # NFCCTAP_MSG
        p1 = 0x80 if self.use_nfcctap_getresponse else 0x00
        resp, sw1, sw2 = self._chain_apdus(0x80, 0x10, p1, 0x00, data)
        last_ka = None

        # NFCCTAP_GETRESPONSE
        p1 = 0x00
        try:
            while (sw1, sw2) == SW_UPDATE:
                ka_status = STATUS(resp[0])
                if on_keepalive and last_ka != ka_status:
                    last_ka = ka_status
                    on_keepalive(ka_status)

                if event.wait(0.1):
                    p1 = 0x11  # cancel
                resp, sw1, sw2 = self._chain_apdus(0x80, 0x11, p1, 0x00)
        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt, cancelling...")
            self._chain_apdus(0x80, 0x11, 0x11, 0x00)

            raise

        if (sw1, sw2) != SW_SUCCESS:
            raise CtapError(CtapError.ERR.OTHER)  # TODO: Map from SW error

        return resp

    def call(
        self,
        cmd: int,
        data: bytes = b"",
        event: Event | None = None,
        on_keepalive: Callable[[STATUS], None] | None = None,
    ) -> bytes:
        if cmd == CTAPHID.CBOR:
            return self._call_cbor(data, event, on_keepalive)
        elif cmd == CTAPHID.MSG:
            return self._call_apdu(data)
        else:
            raise CtapError(CtapError.ERR.INVALID_COMMAND)

    def close(self) -> None:
        self._conn.disconnect()

    @classmethod
    def list_devices(cls, name: str = "") -> Iterator[CtapPcscDevice]:
        for reader in _list_readers():
            if name in reader.name:
                try:
                    yield cls(reader.createConnection(), reader.name)
                except Exception as e:
                    logger.debug("Error %r", e)


def _list_readers():
    try:
        return System.readers()
    except ListReadersException as e:
        # If the PCSC system has restarted the context might be stale, try
        # forcing a new context (This happens on Windows if the last reader is
        # removed):
        try:
            from smartcard.pcsc.PCSCContext import PCSCContext  # type: ignore

            PCSCContext.instance = None
            return System.readers()
        except ImportError:
            # As of pyscard 2.2.2 the PCSCContext singleton has been removed
            raise e
```

## File: fido2/rpid.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
These functions validate RP_ID and APP_ID according to simplified TLD+1 rules,
using a bundled copy of the public suffix list fetched from:

  https://publicsuffix.org/list/public_suffix_list.dat

Advanced APP_ID values pointing to JSON files containing valid facets are not
supported by this implementation.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

tld_fname = os.path.join(os.path.dirname(__file__), "public_suffix_list.dat")
with open(tld_fname, "rb") as f:
    suffixes = [
        entry
        for entry in (line.decode("utf8").strip() for line in f.readlines())
        if entry and not entry.startswith("//")
    ]


def verify_rp_id(rp_id: str, origin: str) -> bool:
    """Checks if a Webauthn RP ID is usable for a given origin.

    :param rp_id: The RP ID to validate.
    :param origin: The origin of the request.
    :return: True if the RP ID is usable by the origin, False if not.
    """
    if not rp_id:
        return False

    url = urlparse(origin)
    host = url.hostname
    # Note that Webauthn requires a secure context, i.e. an origin with https scheme.
    # However, most browsers also treat http://localhost as a secure context. See
    # https://groups.google.com/a/chromium.org/g/blink-dev/c/RC9dSw-O3fE/m/E3_0XaT0BAAJ
    if (
        url.scheme != "https"
        and (url.scheme, host) != ("http", "localhost")
        and not (url.scheme == "http" and host and host.endswith(".localhost"))
    ):
        return False
    if host == rp_id:
        return True
    if host and host.endswith("." + rp_id) and rp_id not in suffixes:
        return True
    return False
```

## File: fido2/server.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Mapping, Sequence

from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.primitives import constant_time

from .cose import CoseKey
from .rpid import verify_rp_id
from .utils import websafe_decode, websafe_encode
from .webauthn import (
    AttestationConveyancePreference,
    AttestationObject,
    AttestedCredentialData,
    AuthenticationResponse,
    AuthenticatorAttachment,
    AuthenticatorData,
    AuthenticatorSelectionCriteria,
    CollectedClientData,
    CredentialCreationOptions,
    CredentialRequestOptions,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialType,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

logger = logging.getLogger(__name__)


VerifyAttestation = Callable[[AttestationObject, bytes], None]
VerifyOrigin = Callable[[str], bool]


def _verify_origin_for_rp(rp_id: str) -> VerifyOrigin:
    return lambda o: verify_rp_id(rp_id, o)


def _validata_challenge(challenge: bytes | None) -> bytes:
    if challenge is None:
        challenge = os.urandom(32)
    else:
        if not isinstance(challenge, bytes):
            raise TypeError("Custom challenge must be of type 'bytes'.")
        if len(challenge) < 16:
            raise ValueError("Custom challenge length must be >= 16.")
    return challenge


def to_descriptor(
    credential: AttestedCredentialData, transports=None
) -> PublicKeyCredentialDescriptor:
    """Converts an AttestedCredentialData to a PublicKeyCredentialDescriptor.

    :param credential: AttestedCredentialData containing the credential ID to use.
    :param transports: Optional list of AuthenticatorTransport strings to add to the
        descriptor.
    :return: A descriptor of the credential, for use with register_begin or
        authenticate_begin.
    :rtype: PublicKeyCredentialDescriptor
    """
    return PublicKeyCredentialDescriptor(
        type=PublicKeyCredentialType.PUBLIC_KEY,
        id=credential.credential_id,
        transports=transports,
    )


def _wrap_credentials(
    creds: Sequence[AttestedCredentialData | PublicKeyCredentialDescriptor] | None,
) -> Sequence[PublicKeyCredentialDescriptor] | None:
    if creds is None:
        return None
    return [
        (
            to_descriptor(c)
            if isinstance(c, AttestedCredentialData)
            else PublicKeyCredentialDescriptor.from_dict(c)
        )
        for c in creds
    ]


def _ignore_attestation(
    attestation_object: AttestationObject, client_data_hash: bytes
) -> None:
    """Ignore attestation."""


class Fido2Server:
    """FIDO2 server.

    :param rp: Relying party data as `PublicKeyCredentialRpEntity` instance.
    :param attestation: (optional) Requirement on authenticator attestation.
    :param verify_origin: (optional) Alternative function to validate an origin.
    :param verify_attestation: (optional) function to validate attestation, which is
        invoked with attestation_object and client_data_hash. It should return nothing
        and raise an exception on failure. By default, attestation is ignored.
        Attestation is also ignored if `attestation` is set to `none`.
    """

    def __init__(
        self,
        rp: PublicKeyCredentialRpEntity,
        attestation: AttestationConveyancePreference | None = None,
        verify_origin: VerifyOrigin | None = None,
        verify_attestation: VerifyAttestation | None = None,
    ):
        self.rp = PublicKeyCredentialRpEntity.from_dict(rp)
        assert self.rp.id is not None  # noqa: S101
        self._verify = verify_origin or _verify_origin_for_rp(self.rp.id)
        self.timeout = None
        self.attestation = AttestationConveyancePreference(attestation)
        self.allowed_algorithms = [
            PublicKeyCredentialParameters(
                type=PublicKeyCredentialType.PUBLIC_KEY, alg=alg
            )
            for alg in CoseKey.supported_algorithms()
        ]
        self._verify_attestation = verify_attestation or _ignore_attestation
        logger.debug(f"Fido2Server initialized for RP: {self.rp}")

    def register_begin(
        self,
        user: PublicKeyCredentialUserEntity,
        credentials: (
            Sequence[AttestedCredentialData | PublicKeyCredentialDescriptor] | None
        ) = None,
        resident_key_requirement: ResidentKeyRequirement | None = None,
        user_verification: UserVerificationRequirement | None = None,
        authenticator_attachment: AuthenticatorAttachment | None = None,
        challenge: bytes | None = None,
        extensions=None,
    ) -> tuple[CredentialCreationOptions, Any]:
        """Return a PublicKeyCredentialCreationOptions registration object and
        the internal state dictionary that needs to be passed as is to the
        corresponding `register_complete` call.

        :param user: The dict containing the user data.
        :param credentials: The list of previously registered credentials, these can be
            of type AttestedCredentialData, or PublicKeyCredentialDescriptor.
        :param resident_key_requirement: The desired RESIDENT_KEY_REQUIREMENT level.
        :param user_verification: The desired USER_VERIFICATION level.
        :param authenticator_attachment: The desired AUTHENTICATOR_ATTACHMENT
            or None to not provide a preference (and get both types).
        :param challenge: A custom challenge to sign and verify or None to use
            OS-specific random bytes.
        :return: Registration data, internal state."""
        if not self.allowed_algorithms:
            raise ValueError("Server has no allowed algorithms.")

        challenge = _validata_challenge(challenge)
        descriptors = _wrap_credentials(credentials)
        state = self._make_internal_state(challenge, user_verification)
        logger.debug(
            "Starting new registration, existing credentials: "
            + ", ".join(d.id.hex() for d in descriptors or [])
        )

        return (
            CredentialCreationOptions(
                public_key=PublicKeyCredentialCreationOptions(
                    rp=self.rp,
                    user=PublicKeyCredentialUserEntity.from_dict(user),
                    challenge=challenge,
                    pub_key_cred_params=self.allowed_algorithms,
                    timeout=self.timeout,
                    exclude_credentials=descriptors,
                    authenticator_selection=(
                        AuthenticatorSelectionCriteria(
                            authenticator_attachment=authenticator_attachment,
                            resident_key=resident_key_requirement,
                            user_verification=user_verification,
                        )
                        if any(
                            (
                                authenticator_attachment,
                                resident_key_requirement,
                                user_verification,
                            )
                        )
                        else None
                    ),
                    attestation=self.attestation,
                    extensions=extensions,
                )
            ),
            state,
        )

    def register_complete(
        self,
        state,
        response: RegistrationResponse | Mapping[str, Any],
    ) -> AuthenticatorData:
        """Verify the correctness of the registration data received from
        the client.

        :param state: The state data returned by the corresponding
            `register_begin`.
        :param response: The registration response from the client.
        :return: The authenticator data
        """
        registration = RegistrationResponse.from_dict(response)
        client_data = registration.response.client_data
        attestation_object = registration.response.attestation_object

        if client_data.type != CollectedClientData.TYPE.CREATE:
            raise ValueError("Incorrect type in CollectedClientData.")
        if not self._verify(client_data.origin):
            raise ValueError("Invalid origin in CollectedClientData.")
        if not constant_time.bytes_eq(
            websafe_decode(state["challenge"]), client_data.challenge
        ):
            raise ValueError("Wrong challenge in response.")
        if not constant_time.bytes_eq(
            self.rp.id_hash or b"", attestation_object.auth_data.rp_id_hash
        ):
            raise ValueError("Wrong RP ID hash in response.")
        if not attestation_object.auth_data.is_user_present():
            raise ValueError("User Present flag not set.")

        if (
            state["user_verification"] == UserVerificationRequirement.REQUIRED
            and not attestation_object.auth_data.is_user_verified()
        ):
            raise ValueError(
                "User verification required, but User Verified flag not set."
            )

        if self.attestation not in (None, AttestationConveyancePreference.NONE):
            logger.debug(f"Verifying attestation of type {attestation_object.fmt}")
            self._verify_attestation(attestation_object, client_data.hash)
        # We simply ignore attestation if self.attestation == 'none', as not all
        # clients strip the attestation.

        auth_data = attestation_object.auth_data
        assert auth_data.credential_data is not None  # noqa: S101
        logger.info(
            "New credential registered: "
            + auth_data.credential_data.credential_id.hex()
        )
        return auth_data

    def authenticate_begin(
        self,
        credentials: (
            Sequence[AttestedCredentialData | PublicKeyCredentialDescriptor] | None
        ) = None,
        user_verification: UserVerificationRequirement | None = None,
        challenge: bytes | None = None,
        extensions=None,
    ) -> tuple[CredentialRequestOptions, Any]:
        """Return a PublicKeyCredentialRequestOptions assertion object and the internal
        state dictionary that needs to be passed as is to the corresponding
        `authenticate_complete` call.

        :param credentials: The list of previously registered credentials, these can be
            of type AttestedCredentialData, or PublicKeyCredentialDescriptor.
        :param user_verification: The desired USER_VERIFICATION level.
        :param challenge: A custom challenge to sign and verify or None to use
            OS-specific random bytes.
        :return: Assertion data, internal state."""
        challenge = _validata_challenge(challenge)
        descriptors = _wrap_credentials(credentials)
        state = self._make_internal_state(challenge, user_verification)
        if descriptors is None:
            logger.debug("Starting new authentication without credentials")
        else:
            logger.debug(
                "Starting new authentication, for credentials: "
                + ", ".join(d.id.hex() for d in descriptors)
            )

        return (
            CredentialRequestOptions(
                public_key=PublicKeyCredentialRequestOptions(
                    challenge=challenge,
                    timeout=self.timeout,
                    rp_id=self.rp.id,
                    allow_credentials=descriptors,
                    user_verification=user_verification,
                    extensions=extensions,
                )
            ),
            state,
        )

    def authenticate_complete(
        self,
        state,
        credentials: Sequence[AttestedCredentialData],
        response: AuthenticationResponse | Mapping[str, Any],
    ) -> AttestedCredentialData:
        """Verify the correctness of the assertion data received from
        the client.

        :param state: The state data returned by the corresponding
            `register_begin`.
        :param credentials: The list of previously registered credentials.
        :param credential_id: The credential id from the client response.
        :param client_data: The client data.
        :param auth_data: The authenticator data.
        :param signature: The signature provided by the client."""

        authentication = AuthenticationResponse.from_dict(response)
        credential_id = authentication.raw_id
        client_data = authentication.response.client_data
        auth_data = authentication.response.authenticator_data
        signature = authentication.response.signature

        if client_data.type != CollectedClientData.TYPE.GET:
            raise ValueError("Incorrect type in CollectedClientData.")
        if not self._verify(client_data.origin):
            raise ValueError("Invalid origin in CollectedClientData.")
        if websafe_decode(state["challenge"]) != client_data.challenge:
            raise ValueError("Wrong challenge in response.")
        if not constant_time.bytes_eq(self.rp.id_hash or b"", auth_data.rp_id_hash):
            raise ValueError("Wrong RP ID hash in response.")
        if not auth_data.is_user_present():
            raise ValueError("User Present flag not set.")

        if (
            state["user_verification"] == UserVerificationRequirement.REQUIRED
            and not auth_data.is_user_verified()
        ):
            raise ValueError(
                "User verification required, but user verified flag not set."
            )

        for cred in credentials:
            if cred.credential_id == credential_id:
                try:
                    cred.public_key.verify(auth_data + client_data.hash, signature)
                except _InvalidSignature:
                    raise ValueError("Invalid signature.")
                logger.info(f"Credential authenticated: {credential_id.hex()}")
                return cred
        raise ValueError("Unknown credential ID.")

    @staticmethod
    def _make_internal_state(
        challenge: bytes, user_verification: UserVerificationRequirement | None
    ):
        return {
            "challenge": websafe_encode(challenge),
            "user_verification": user_verification,
        }
```

## File: fido2/utils.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Various utility functions.

This module contains various functions used throughout the rest of the project.
"""

from __future__ import annotations

import struct
from abc import abstractmethod
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import Field, fields
from io import BytesIO
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Hashable,
    Mapping,
    Sequence,
    TypeVar,
    get_type_hints,
    overload,
)

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        # Fallback for Python 3.10 and earlier
        Self = TypeVar("Self", bound="_DataClassMapping")

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

__all__ = [
    "websafe_encode",
    "websafe_decode",
    "sha256",
    "hmac_sha256",
    "bytes2int",
    "int2bytes",
]


LOG_LEVEL_TRAFFIC = 5


def sha256(data: bytes) -> bytes:
    """Produces a SHA256 hash of the input.

    :param data: The input data to hash.
    :return: The resulting hash.
    """
    h = hashes.Hash(hashes.SHA256(), default_backend())
    h.update(data)
    return h.finalize()


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    """Performs an HMAC-SHA256 operation on the given data, using the given key.

    :param key: The key to use.
    :param data: The input data to hash.
    :return: The resulting hash.
    """
    h = hmac.HMAC(key, hashes.SHA256(), default_backend())
    h.update(data)
    return h.finalize()


def bytes2int(value: bytes) -> int:
    """Parses an arbitrarily sized integer from a byte string.

    :param value: A byte string encoding a big endian unsigned integer.
    :return: The parsed int.
    """
    return int.from_bytes(value, "big")


def int2bytes(value: int, minlen: int = -1) -> bytes:
    """Encodes an int as a byte string.

    :param value: The integer value to encode.
    :param minlen: An optional minimum length for the resulting byte string.
    :return: The value encoded as a big endian byte string.
    """
    ba = []
    while value > 0xFF:
        ba.append(0xFF & value)
        value >>= 8
    ba.append(value)
    ba.extend([0] * (minlen - len(ba)))
    return bytes(reversed(ba))


def websafe_decode(data: str | bytes) -> bytes:
    """Decodes a websafe-base64 encoded string.
    See: "Base 64 Encoding with URL and Filename Safe Alphabet" from Section 5
    in RFC4648 without padding.

    :param data: The input to decode.
    :return: The decoded bytes.
    """
    if isinstance(data, str):
        data_b = data.encode("ascii")
    else:
        data_b = bytes(data)

    data_b += b"=" * (-len(data_b) % 4)
    return urlsafe_b64decode(data_b)


def websafe_encode(data: bytes) -> str:
    """Encodes a byte string into websafe-base64 encoding.

    :param data: The input to encode.
    :return: The encoded string.
    """
    return urlsafe_b64encode(data).replace(b"=", b"").decode("ascii")


class ByteBuffer(BytesIO):
    """BytesIO-like object with the ability to unpack values."""

    def unpack(self, fmt: str):
        """Reads and unpacks a value from the buffer.

        :param fmt: A struct format string yielding a single value.
        :return: The unpacked value.
        """
        s = struct.Struct(fmt)
        return s.unpack(self.read(s.size))[0]

    def read(self, size: int | None = -1) -> bytes:
        """Like BytesIO.read(), but checks the number of bytes read and raises an error
        if fewer bytes were read than expected.
        """
        data = super().read(size)
        if size is not None and size > 0 and len(data) != size:
            raise ValueError(
                "Not enough data to read (need: %d, had: %d)." % (size, len(data))
            )
        return data


_T = TypeVar("_T", bound=Hashable)


class _DataClassMapping(Mapping[_T, Any]):
    """A data class with members also accessible as a Mapping."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]

    def __post_init__(self):
        hints = get_type_hints(type(self))
        self._field_keys: dict[_T, Field[Any]]
        object.__setattr__(self, "_field_keys", {})

        for f in fields(self):
            self._field_keys[self._get_field_key(f)] = f
            value = getattr(self, f.name)
            if value is not None:
                try:
                    value = self._parse_value(hints[f.name], value)
                    object.__setattr__(self, f.name, value)
                except (TypeError, KeyError, ValueError):
                    raise ValueError(
                        f"Error parsing field {f.name} for {self.__class__.__name__}"
                    )

    @classmethod
    @abstractmethod
    def _get_field_key(cls, field: Field) -> _T:
        raise NotImplementedError()

    def __iter__(self):
        return (
            k for k, f in self._field_keys.items() if getattr(self, f.name) is not None
        )

    def __len__(self):
        return len(list(iter(self)))

    def __getitem__(self, key):
        f = self._field_keys[key]
        value = getattr(self, f.name)
        if value is None:
            raise KeyError(key)
        serialize = f.metadata.get("serialize")
        if serialize:
            return serialize(value)
        if isinstance(value, Mapping) and not isinstance(value, dict):
            return dict(value)
        if isinstance(value, Sequence) and all(isinstance(v, Mapping) for v in value):
            return [v if isinstance(v, dict) else dict(v) for v in value]
        return value

    @classmethod
    def _parse_value(cls, t, value):
        if (t | None) == t:  # Optional, get the type
            t = t.__args__[0]

        # Check if type is already correct
        try:
            if t is Any or isinstance(value, t):
                return value
        except TypeError:
            pass

        # Handle list of values
        if issubclass(getattr(t, "__origin__", object), Sequence):
            t = getattr(t, "__args__")[0]
            return [cls._parse_value(t, v) for v in value]

        # Handle Mappings
        elif issubclass(getattr(t, "__origin__", object), Mapping) and isinstance(
            value, Mapping
        ):
            t_k, t_v = getattr(t, "__args__")
            return {
                cls._parse_value(t_k, k): cls._parse_value(t_v, v)
                for k, v in value.items()
            }

        # Check if type has from_dict
        from_dict = getattr(t, "from_dict", None)
        if from_dict:
            return from_dict(value)

        # Convert to enum values, other wrappers
        wrap = getattr(t, "__call__", None)
        if wrap:
            return wrap(value)

        raise ValueError(f"Unparseable value of type {type(value)} for {t}")

    @overload
    @classmethod
    def from_dict(cls: type[Self], data: None) -> None: ...

    @overload
    @classmethod
    def from_dict(cls: type[Self], data: Self | Mapping[_T, Any]) -> Self: ...

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        if not isinstance(data, Mapping):
            raise TypeError(
                f"{cls.__name__}.from_dict called with non-Mapping data of type"
                f"{type(data)}"
            )
        return cls._parse_from_dict(data)

    @classmethod
    def _parse_from_dict(cls: type[Self], data: Mapping[_T, Any]) -> Self:
        kwargs = {}
        hints = get_type_hints(cls)
        for f in fields(cls):
            key = cls._get_field_key(f)
            value = data.get(key)
            if value is None:
                continue
            deserialize = f.metadata.get("deserialize")
            if deserialize:
                value = deserialize(value)
            else:
                t = hints[f.name]
                value = cls._parse_value(t, value)

            kwargs[f.name] = value
        return cls(**kwargs)


class _JsonDataObject(_DataClassMapping[str]):
    """A data class with members also accessible as a JSON-serializable Mapping."""

    @classmethod
    def _get_field_key(cls, field: Field) -> str:
        name = field.metadata.get("name")
        if name:
            return name
        parts = field.name.split("_")
        return parts[0] + "".join(p.title() for p in parts[1:])

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, bytes):
            return websafe_encode(value)
        return value

    @classmethod
    def _parse_value(cls, t, value):
        if (t | None) == t:  # Optional, get the type
            t2 = t.__args__[0]
        else:
            t2 = t
        # bytes are encoded as websafe_b64 strings
        if isinstance(t2, type) and issubclass(t2, bytes) and isinstance(value, str):
            return websafe_decode(value)

        return super()._parse_value(t, value)
```

## File: fido2/webauthn.py
```python
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import json
import struct
from dataclasses import dataclass, field
from enum import Enum, EnumMeta, IntFlag, unique
from typing import Any, Mapping, Sequence, cast

from . import cbor
from .cose import ES256, CoseKey
from .utils import (
    ByteBuffer,
    _JsonDataObject,
    sha256,
    websafe_decode,
    websafe_encode,
)

"""
Data classes based on the W3C WebAuthn specification (https://www.w3.org/TR/webauthn/).

See the specification for a description and details on their usage.

Most of these classes can be serialized to JSON-compatible dictionaries by passing them
to dict(), and then deserialized by calling DataClass.from_dict(data). For example:

    user = PublicKeyCredentialUserEntity(id=b"1234", name="Alice")
    data = dict(user)
    # data is now a JSON-compatible dictionary, json.dumps(data) will work
    user2 = PublicKeyCredentialUserEntity.from_dict(data)
    assert user == user2
"""

# Binary types


class Aaguid(bytes):
    def __init__(self, data: bytes):
        if len(self) != 16:
            raise ValueError("AAGUID must be 16 bytes")

    def __bool__(self):
        return self != Aaguid.NONE

    def __str__(self):
        h = self.hex()
        return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"

    def __repr__(self):
        return f"AAGUID({str(self)})"

    @classmethod
    def parse(cls, value: str) -> Aaguid:
        return cls.fromhex(value.replace("-", ""))

    NONE: Aaguid


# Special instance of AAGUID used when there is no AAGUID
Aaguid.NONE = Aaguid(b"\0" * 16)


@dataclass(init=False, frozen=True)
class AttestedCredentialData(bytes):
    aaguid: Aaguid
    credential_id: bytes
    public_key: CoseKey

    def __init__(self, _: bytes):
        super().__init__()

        parsed = AttestedCredentialData._parse(self)
        object.__setattr__(self, "aaguid", parsed[0])
        object.__setattr__(self, "credential_id", parsed[1])
        object.__setattr__(self, "public_key", parsed[2])
        if parsed[3]:
            raise ValueError("Wrong length")

    def __str__(self):  # Override default implementation from bytes.
        return repr(self)

    @staticmethod
    def _parse(data: bytes) -> tuple[bytes, bytes, CoseKey, bytes]:
        """Parse the components of an AttestedCredentialData from a binary
        string, and return them.

        :param data: A binary string containing an attested credential data.
        :return: AAGUID, credential ID, public key, and remaining data.
        """
        reader = ByteBuffer(data)
        aaguid = Aaguid(reader.read(16))
        cred_id = reader.read(reader.unpack(">H"))
        pub_key, rest = cbor.decode_from(reader.read())
        return aaguid, cred_id, CoseKey.parse(pub_key), rest

    @classmethod
    def create(
        cls, aaguid: bytes, credential_id: bytes, public_key: CoseKey
    ) -> AttestedCredentialData:
        """Create an AttestedCredentialData by providing its components.

        :param aaguid: The AAGUID of the authenticator.
        :param credential_id: The binary ID of the credential.
        :param public_key: A COSE formatted public key.
        :return: The attested credential data.
        """
        return cls(
            aaguid
            + struct.pack(">H", len(credential_id))
            + credential_id
            + cbor.encode(public_key)
        )

    @classmethod
    def unpack_from(cls, data: bytes) -> tuple[AttestedCredentialData, bytes]:
        """Unpack an AttestedCredentialData from a byte string, returning it and
        any remaining data.

        :param data: A binary string containing an attested credential data.
        :return: The parsed AttestedCredentialData, and any remaining data from
            the input.
        """
        aaguid, cred_id, pub_key, rest = cls._parse(data)
        return cls.create(aaguid, cred_id, pub_key), rest

    @classmethod
    def from_ctap1(cls, key_handle: bytes, public_key: bytes) -> AttestedCredentialData:
        """Create an AttestatedCredentialData from a CTAP1 RegistrationData instance.

        :param key_handle: The CTAP1 credential key_handle.
        :type key_handle: bytes
        :param public_key: The CTAP1 65 byte public key.
        :type public_key: bytes
        :return: The credential data, using an all-zero AAGUID.
        :rtype: AttestedCredentialData
        """
        return cls.create(Aaguid.NONE, key_handle, ES256.from_ctap1(public_key))


@dataclass(init=False, frozen=True)
class AuthenticatorData(bytes):
    """Binary encoding of the authenticator data.

    :param _: The binary representation of the authenticator data.
    :ivar rp_id_hash: SHA256 hash of the RP ID.
    :ivar flags: The flags of the authenticator data, see
        AuthenticatorData.FLAG.
    :ivar counter: The signature counter of the authenticator.
    :ivar credential_data: Attested credential data, if available.
    :ivar extensions: Authenticator extensions, if available.
    """

    class FLAG(IntFlag):
        """Authenticator data flags

        See https://www.w3.org/TR/webauthn/#sec-authenticator-data for details
        """

        # Names used in WebAuthn
        UP = 0x01
        UV = 0x04
        BE = 0x08
        BS = 0x10
        AT = 0x40
        ED = 0x80

        # Aliases (for historical purposes)
        USER_PRESENT = 0x01
        USER_VERIFIED = 0x04
        BACKUP_ELIGIBILITY = 0x08
        BACKUP_STATE = 0x10
        ATTESTED = 0x40
        EXTENSION_DATA = 0x80

    rp_id_hash: bytes
    flags: AuthenticatorData.FLAG
    counter: int
    credential_data: AttestedCredentialData | None
    extensions: Mapping | None

    def __init__(self, _: bytes):
        super().__init__()

        reader = ByteBuffer(self)
        object.__setattr__(self, "rp_id_hash", reader.read(32))
        object.__setattr__(self, "flags", reader.unpack("B"))
        object.__setattr__(self, "counter", reader.unpack(">I"))
        rest = reader.read()

        if self.flags & AuthenticatorData.FLAG.AT:
            credential_data, rest = AttestedCredentialData.unpack_from(rest)
        else:
            credential_data = None
        object.__setattr__(self, "credential_data", credential_data)

        if self.flags & AuthenticatorData.FLAG.ED:
            extensions, rest = cbor.decode_from(rest)
        else:
            extensions = None
        object.__setattr__(self, "extensions", extensions)

        if rest:
            raise ValueError("Wrong length")

    def __str__(self):  # Override default implementation from bytes.
        return repr(self)

    @classmethod
    def create(
        cls,
        rp_id_hash: bytes,
        flags: AuthenticatorData.FLAG,
        counter: int,
        credential_data: bytes = b"",
        extensions: Mapping | None = None,
    ):
        """Create an AuthenticatorData instance.

        :param rp_id_hash: SHA256 hash of the RP ID.
        :param flags: Flags of the AuthenticatorData.
        :param counter: Signature counter of the authenticator data.
        :param credential_data: Authenticated credential data (only if attested
            credential data flag is set).
        :param extensions: Authenticator extensions (only if ED flag is set).
        :return: The authenticator data.
        """
        return cls(
            rp_id_hash
            + struct.pack(">BI", flags, counter)
            + credential_data
            + (cbor.encode(extensions) if extensions is not None else b"")
        )

    def is_user_present(self) -> bool:
        """Return true if the User Present flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.UP)

    def is_user_verified(self) -> bool:
        """Return true if the User Verified flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.UV)

    def is_backup_eligible(self) -> bool:
        """Return true if the Backup Eligibility flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.BE)

    def is_backed_up(self) -> bool:
        """Return true if the Backup State flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.BS)

    def is_attested(self) -> bool:
        """Return true if the Attested credential data flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.AT)

    def has_extension_data(self) -> bool:
        """Return true if the Extenstion data flag is set."""
        return bool(self.flags & AuthenticatorData.FLAG.ED)


@dataclass(init=False, frozen=True)
class AttestationObject(bytes):  # , Mapping[str, Any]):
    """Binary CBOR encoded attestation object.

    :param _: The binary representation of the attestation object.
    :ivar fmt: The type of attestation used.
    :ivar auth_data: The attested authenticator data.
    :ivar att_statement: The attestation statement.
    """

    fmt: str
    auth_data: AuthenticatorData
    att_stmt: Mapping[str, Any]

    def __init__(self, _: bytes):
        super().__init__()

        data = cast(Mapping[str, Any], cbor.decode(bytes(self)))
        object.__setattr__(self, "fmt", data["fmt"])
        object.__setattr__(self, "auth_data", AuthenticatorData(data["authData"]))
        object.__setattr__(self, "att_stmt", data["attStmt"])

    def __str__(self):  # Override default implementation from bytes.
        return repr(self)

    @classmethod
    def create(
        cls, fmt: str, auth_data: AuthenticatorData, att_stmt: Mapping[str, Any]
    ) -> AttestationObject:
        return cls(
            cbor.encode({"fmt": fmt, "authData": auth_data, "attStmt": att_stmt})
        )

    @classmethod
    def from_ctap1(cls, app_param: bytes, registration) -> AttestationObject:
        """Create an AttestationObject from a CTAP1 RegistrationData instance.

        :param app_param: SHA256 hash of the RP ID used for the CTAP1 request.
        :type app_param: bytes
        :param registration: The CTAP1 registration data.
        :type registration: RegistrationData
        :return: The attestation object, using the "fido-u2f" format.
        :rtype: AttestationObject
        """
        return cls.create(
            "fido-u2f",
            AuthenticatorData.create(
                app_param,
                AuthenticatorData.FLAG.AT | AuthenticatorData.FLAG.UP,
                0,
                AttestedCredentialData.from_ctap1(
                    registration.key_handle, registration.public_key
                ),
            ),
            {"x5c": [registration.certificate], "sig": registration.signature},
        )


@dataclass(init=False, frozen=True)
class CollectedClientData(bytes):
    @unique
    class TYPE(str, Enum):
        CREATE = "webauthn.create"
        GET = "webauthn.get"

    _data: Mapping[str, Any]
    type: str
    challenge: bytes
    origin: str
    cross_origin: bool = False

    def __init__(self, _: bytes):
        super().__init__()

        object.__setattr__(self, "_data", json.loads(self.decode()))
        object.__setattr__(self, "type", self._data["type"])
        object.__setattr__(self, "challenge", websafe_decode(self._data["challenge"]))
        object.__setattr__(self, "origin", self._data["origin"])
        object.__setattr__(self, "cross_origin", self._data.get("crossOrigin", False))

    @classmethod
    def create(
        cls,
        type: str,
        challenge: bytes | str,
        origin: str,
        cross_origin: bool = False,
        **kwargs,
    ) -> CollectedClientData:
        if isinstance(challenge, bytes):
            encoded_challenge = websafe_encode(challenge)
        else:
            encoded_challenge = challenge
        return cls(
            json.dumps(
                {
                    "type": type,
                    "challenge": encoded_challenge,
                    "origin": origin,
                    "crossOrigin": cross_origin,
                    **kwargs,
                },
                separators=(",", ":"),
            ).encode()
        )

    def __str__(self):  # Override default implementation from bytes.
        return repr(self)

    @property
    def b64(self) -> str:
        return websafe_encode(self)

    @property
    def hash(self) -> bytes:
        return sha256(self)


class _StringEnumMeta(EnumMeta):
    def _get_value(cls, value):
        return None

    def __call__(cls, value, *args, **kwargs):  # type: ignore
        try:
            return super().__call__(value, *args, **kwargs)
        except ValueError:
            return cls._get_value(value)


class _StringEnum(str, Enum, metaclass=_StringEnumMeta):
    """Enum of strings for WebAuthn types.

    Unrecognized values are treated as missing.
    """


@unique
class AttestationConveyancePreference(_StringEnum):
    NONE = "none"
    INDIRECT = "indirect"
    DIRECT = "direct"
    ENTERPRISE = "enterprise"


@unique
class UserVerificationRequirement(_StringEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    DISCOURAGED = "discouraged"


@unique
class ResidentKeyRequirement(_StringEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    DISCOURAGED = "discouraged"


@unique
class AuthenticatorAttachment(_StringEnum):
    PLATFORM = "platform"
    CROSS_PLATFORM = "cross-platform"


@unique
class AuthenticatorTransport(_StringEnum):
    USB = "usb"
    NFC = "nfc"
    BLE = "ble"
    HYBRID = "hybrid"
    INTERNAL = "internal"


@unique
class PublicKeyCredentialType(_StringEnum):
    PUBLIC_KEY = "public-key"


@unique
class PublicKeyCredentialHint(_StringEnum):
    SECURITY_KEY = "security-key"
    CLIENT_DEVICE = "client-device"
    HYBRID = "hybrid"


def _as_cbor(data: _JsonDataObject) -> Mapping[str, Any]:
    return {k: super(_JsonDataObject, data).__getitem__(k) for k in data}


@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialRpEntity(_JsonDataObject):
    name: str
    id: str | None = None

    @property
    def id_hash(self) -> bytes | None:
        """Return SHA256 hash of the identifier."""
        return sha256(self.id.encode("utf8")) if self.id else None


# Note that name and display_name are required in the WebAuthn spec, but CTAP2
# allows them to be omitted, so we make them optional here.
@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialUserEntity(_JsonDataObject):
    name: str | None = None
    id: bytes
    display_name: str | None = None


@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialParameters(_JsonDataObject):
    type: PublicKeyCredentialType
    alg: int


@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialDescriptor(_JsonDataObject):
    type: PublicKeyCredentialType
    id: bytes
    transports: Sequence[AuthenticatorTransport] | None = None


@dataclass(eq=False, frozen=True, kw_only=True)
class AuthenticatorSelectionCriteria(_JsonDataObject):
    authenticator_attachment: AuthenticatorAttachment | None = None
    resident_key: ResidentKeyRequirement | None = None
    user_verification: UserVerificationRequirement | None = None
    require_resident_key: bool | None = False

    def __post_init__(self):
        super().__post_init__()

        if self.resident_key is None:
            object.__setattr__(
                self,
                "resident_key",
                (
                    ResidentKeyRequirement.REQUIRED
                    if self.require_resident_key
                    else ResidentKeyRequirement.DISCOURAGED
                ),
            )
        object.__setattr__(
            self,
            "require_resident_key",
            self.resident_key == ResidentKeyRequirement.REQUIRED,
        )


@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialCreationOptions(_JsonDataObject):
    rp: PublicKeyCredentialRpEntity
    user: PublicKeyCredentialUserEntity
    challenge: bytes
    pub_key_cred_params: Sequence[PublicKeyCredentialParameters]
    timeout: int | None = None
    exclude_credentials: Sequence[PublicKeyCredentialDescriptor] | None = None
    authenticator_selection: AuthenticatorSelectionCriteria | None = None
    hints: Sequence[PublicKeyCredentialHint] | None = None
    attestation: AttestationConveyancePreference | None = None
    attestation_formats: Sequence[str] | None = None
    extensions: Mapping[str, Any] | None = None


@dataclass(eq=False, frozen=True, kw_only=True)
class PublicKeyCredentialRequestOptions(_JsonDataObject):
    challenge: bytes
    timeout: int | None = None
    rp_id: str | None = None
    allow_credentials: Sequence[PublicKeyCredentialDescriptor] | None = None
    user_verification: UserVerificationRequirement | None = None
    hints: Sequence[PublicKeyCredentialHint] | None = None
    extensions: Mapping[str, Any] | None = None


@dataclass(eq=False, frozen=True, kw_only=True)
class AuthenticatorAttestationResponse(_JsonDataObject):
    client_data: CollectedClientData = field(metadata=dict(name="clientDataJSON"))
    attestation_object: AttestationObject


@dataclass(eq=False, frozen=True, kw_only=True)
class AuthenticatorAssertionResponse(_JsonDataObject):
    client_data: CollectedClientData = field(metadata=dict(name="clientDataJSON"))
    authenticator_data: AuthenticatorData
    signature: bytes
    user_handle: bytes | None = None


class AuthenticationExtensionsClientOutputs(Mapping[str, Any]):
    """Holds extension output from a call to MakeCredential or GetAssertion.

    When accessed as a dict, all bytes values will be serialized to base64url encoding,
    capable of being serialized to JSON.

    When accessed using attributes, richer types will instead be returned.
    """

    def __init__(self, outputs: Mapping[str, Any] = {}):
        self._members = {k: v for k, v in outputs.items() if v is not None}

    def __iter__(self):
        return iter(self._members)

    def __len__(self):
        return len(self._members)

    def __getitem__(self, key):
        value = self._members[key]
        if isinstance(value, bytes):
            return websafe_encode(value)
        elif isinstance(value, Mapping) and not isinstance(value, dict):
            return dict(value)
        return value

    def __getattr__(self, key):
        parts = key.split("_")
        name = parts[0] + "".join(p.title() for p in parts[1:])
        return self._members.get(name)

    def __repr__(self):
        return repr(dict(self))


@dataclass(eq=False, frozen=True, kw_only=True)
class RegistrationResponse(_JsonDataObject):
    """
    Represents the RegistrationResponse structure from the WebAuthn specification,
    with fields modeled after the JSON serialization.

    Serializing this object to JSON can be done by using json.dumps(dict(response)).

    See: https://www.w3.org/TR/webauthn-3/#dictdef-registrationresponsejson
    """

    id: str = field(init=False)
    raw_id: bytes
    response: AuthenticatorAttestationResponse
    authenticator_attachment: AuthenticatorAttachment | None = None
    client_extension_results: AuthenticationExtensionsClientOutputs = field(
        default_factory=AuthenticationExtensionsClientOutputs
    )
    type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY

    def __post_init__(self):
        object.__setattr__(self, "id", websafe_encode(self.raw_id))
        super().__post_init__()

    @classmethod
    def _parse_value(cls, t, value):
        if t == Mapping[str, Any] | None:
            # Don't convert extension_results
            return value
        return super()._parse_value(t, value)

    @classmethod
    def _parse_from_dict(cls, data):
        if "id" in data:
            data = dict(data)
            credential_id = data.pop("id")
            if credential_id != data["rawId"]:
                raise ValueError("id does not match rawId")

        return super()._parse_from_dict(data)


@dataclass(eq=False, frozen=True, kw_only=True)
class AuthenticationResponse(_JsonDataObject):
    """
    Represents the AuthenticationResponse structure from the WebAuthn specification,
    with fields modeled after the JSON serialization.

    Serializing this object to JSON can be done by using json.dumps(dict(response)).

    See: https://www.w3.org/TR/webauthn-3/#dictdef-authenticationresponsejson
    """

    id: str = field(init=False)
    raw_id: bytes
    response: AuthenticatorAssertionResponse
    authenticator_attachment: AuthenticatorAttachment | None = None
    client_extension_results: AuthenticationExtensionsClientOutputs = field(
        default_factory=AuthenticationExtensionsClientOutputs
    )
    type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY

    def __post_init__(self):
        object.__setattr__(self, "id", websafe_encode(self.raw_id))
        super().__post_init__()

    @classmethod
    def _parse_value(cls, t, value):
        if t == Mapping[str, Any] | None:
            # Don't convert extension_results
            return value
        return super()._parse_value(t, value)

    @classmethod
    def _parse_from_dict(cls, data):
        if "id" in data:
            data = dict(data)
            credential_id = data.pop("id")
            if credential_id != data["rawId"]:
                raise ValueError("id does not match rawId")
        return super()._parse_from_dict(data)


@dataclass(eq=False, frozen=True, kw_only=True)
class CredentialCreationOptions(_JsonDataObject):
    public_key: PublicKeyCredentialCreationOptions


@dataclass(eq=False, frozen=True, kw_only=True)
class CredentialRequestOptions(_JsonDataObject):
    public_key: PublicKeyCredentialRequestOptions
```

## File: tests/device/__init__.py
```python
from fido2.client import UserInteraction

TEST_PIN = "a1b2c3d4"


class Printer:
    def __init__(self, capmanager):
        self.capmanager = capmanager

    def print(self, *messages):
        with self.capmanager.global_and_fixture_disabled():
            print("")
            for m in messages:
                print(m)

    def touch(self):
        self.print("👉 Touch the Authenticator")

    def insert(self, nfc=False):
        self.print(
            "♻️  "
            + (
                "Place the Authenticator on the NFC reader"
                if nfc
                else "Connect the Authenticator"
            )
        )

    def remove(self, nfc=False):
        self.print(
            "🚫 "
            + (
                "Remove the Authenticator from the NFC reader"
                if nfc
                else "Disconnect the Authenticator"
            )
        )


# Handle user interaction
class CliInteraction(UserInteraction):
    def __init__(self, printer, pin=TEST_PIN):
        self.printer = printer
        self.pin = pin

    def prompt_up(self):
        self.printer.touch()

    def request_pin(self, permissions, rd_id):
        return self.pin

    def request_uv(self, permissions, rd_id):
        self.printer.print("User Verification required.")
        return True
```

## File: tests/device/conftest.py
```python
import logging
from dataclasses import replace
from threading import Event, Thread

import pytest

from fido2.client import ClientError, DefaultClientDataCollector, Fido2Client
from fido2.cose import CoseKey
from fido2.ctap2 import Ctap2
from fido2.ctap2.credman import CredentialManagement
from fido2.ctap2.pin import ClientPin, PinProtocolV1, PinProtocolV2
from fido2.hid import (
    CAPABILITY,
    CtapHidDevice,
    list_descriptors,
    open_connection,
    open_device,
)

from . import TEST_PIN, CliInteraction, Printer

logger = logging.getLogger(__name__)


class DeviceManager:
    def __init__(self, printer, reader_name, ccid):
        self.printer = printer

        self.printer.print(
            "⚠️  Tests will now run against a connected FIDO authenticator. ⚠️ ",
            "",
            "You may be prompted to interact with the authenticator throughout these "
            "tests.",
            "",
            "          ☠️  WARNING! THESE TESTS ARE DESTRUCTIVE! ☠️ ",
            "ANY CREDENTIALS ON THIS AUTHENTICATOR WILL BE PERMANENTLY DELETED!",
        )

        self._transport = "usb"
        if reader_name:
            try:
                from fido2.pcsc import _list_readers
            except ImportError:
                pytest.exit("pyscard not installed, install package with 'pcsc' extra")

            readers = [
                r for r in _list_readers() if reader_name.lower() in r.name.lower()
            ]
            if len(readers) == 1:
                self._reader = readers[0]
                self._dev = self._connect_pcsc(self._reader, not ccid)
                if not ccid:
                    self._transport = "nfc"
            else:
                pytest.exit(f"No/Multiple NFC readers found matching '{reader_name}'")
        else:
            self._reader = None
            self._dev = self._select()

        if self.has_ctap2():
            info = Ctap2(self.device).info
            if info.transports_for_reset:
                self._can_reset = self._transport in info.transports_for_reset
            else:
                self._can_reset = True
            if info.options.get("clientPin") or info.options.get("uv"):
                self.printer.print(
                    "As a precaution, these tests will not run on an authenticator "
                    "which is configured with any form of UV. Factory reset the "
                    "authenticator prior to running tests against it."
                )
                pytest.exit("Authenticator must be in a newly-reset state!")

            if not self._can_reset:
                self.printer.print(
                    "⚠️  FACTORY RESET NOT ENABLED FOR THIS TRANSPORT! ⚠️ ",
                    "Some tests will be skipped, and the authenticator will be left "
                    "in a state where it will need to be factory reset through another"
                    "transport to be used.",
                )

        self.setup()

    def _select(self):
        event = Event()
        selected = []

        def select(descriptor):
            dev = CtapHidDevice(descriptor, open_connection(descriptor))
            # This client is only used for selection
            client = Fido2Client(
                dev,
                client_data_collector=DefaultClientDataCollector("https://example.com"),
            )
            try:
                while not event.is_set():
                    try:
                        client.selection(event)
                        selected.append(dev)
                        event.set()
                        break
                    except ClientError as e:
                        if e.code != ClientError.ERR.TIMEOUT:
                            raise
            except Exception:
                logger.debug(
                    f"Authenticator selection failed for {descriptor.path}",
                    exc_info=True,
                )

        self.printer.touch()

        descriptors: set[str | bytes] = set()
        threads: list[Thread] = []
        try:
            while not event.wait(0.1):
                if event.is_set():
                    break
                removed = set(descriptors)
                for d in list_descriptors():
                    if d.path not in descriptors:
                        descriptors.add(d.path)
                        t = Thread(target=select, args=(d,))
                        threads.append(t)
                        t.start()
                    else:
                        removed.remove(d.path)
                descriptors -= removed
        finally:
            event.set()

        for t in threads:
            # wait for child threads to finish
            t.join()

        if selected:
            logger.debug("Authenticator selected")
            return selected[0]
        else:
            pytest.exit("No Authenticator selected")

    def _connect_pcsc(self, reader, reconnect=True):
        from fido2.pcsc import CtapPcscDevice
        from smartcard.Exceptions import NoCardException, CardConnectionException
        from smartcard.ExclusiveConnectCardConnection import (
            ExclusiveConnectCardConnection,
        )

        logger.debug(f"(Re-)connect over NFC using reader: {reader.name}")
        event = Event()

        def _connect():
            connection = ExclusiveConnectCardConnection(reader.createConnection())
            return CtapPcscDevice(connection, reader.name)

        if not reconnect:
            return _connect()

        self.printer.remove(nfc=True)
        removed = False
        while not event.wait(0.5):
            try:
                dev = _connect()
                if removed:
                    dev.close()
                    event.wait(1.0)  # Wait for the device to settle
                    return _connect()
                dev.close()
            except CardConnectionException:
                pass  # Expected, ignore
            except (NoCardException, KeyError):
                if not removed:
                    self.printer.insert(nfc=True)
                    removed = True

        raise Exception("Failed to (re-)connect to Authenticator")

    @property
    def device(self):
        return self._dev

    def has_ctap2(self):
        return self.device.capabilities & CAPABILITY.CBOR

    @property
    def ctap2(self):
        if self.has_ctap2():
            return Ctap2(self.device)
        pytest.skip("Authenticator does not support CTAP 2")

    @property
    def info(self):
        return self.ctap2.get_info()

    @property
    def on_keepalive(self):
        prompted = [0]

        def on_keepalive(status):
            if status != prompted[0]:
                prompted[0] = status
                if status == 2:
                    self.printer.touch()

        return on_keepalive

    @property
    def client(self):
        return Fido2Client(
            self.device,
            client_data_collector=DefaultClientDataCollector("https://example.com"),
            user_interaction=CliInteraction(self.printer),
        )

    def _reconnect_usb(self):
        event = Event()
        dev_path = self._dev.descriptor.path
        info = Ctap2(self._dev).info
        logger.debug(f"Reconnect over USB: {dev_path}")

        self.printer.remove()
        ds = {d.path for d in list_descriptors()}
        while dev_path in ds:
            event.wait(0.5)
            ds = {d.path for d in list_descriptors()}
        self.printer.insert()
        ds2 = ds
        while True:
            event.wait(0.5)
            ds2 = {d.path for d in list_descriptors()}
            added = ds2 - ds
            if len(added) == 1:
                device = open_device(added.pop())
                info2 = Ctap2(device).info
                assert replace(info, enc_identifier=None) == replace(
                    info2, enc_identifier=None
                )
                return device
            elif len(added) > 1:
                raise ValueError("Multiple Authenticators inserted")

    def _reconnect_ccid(self):
        name = self._reader.name
        info = Ctap2(self._dev).info

        logger.debug(f"Reconnect over CCID: {name}")
        from fido2.pcsc import _list_readers

        self.printer.remove()
        event = Event()
        removed = False
        while not event.wait(0.5):
            readers = [r for r in _list_readers() if name == r.name]
            if removed and len(readers) == 1:
                self._reader = readers[0]
                dev = self._connect_pcsc(self._reader, False)
                info2 = Ctap2(dev).info
                assert replace(info, enc_identifier=None) == replace(
                    info2, enc_identifier=None
                )

                return dev
            elif not removed and len(readers) == 0:
                self.printer.insert()
                removed = True

    def reconnect(self):
        if self._transport == "nfc":
            self._dev.close()
            self._dev.connect()
        elif self._reader:
            self._dev = self._reconnect_ccid()
        else:
            self._dev = self._reconnect_usb()
        return self._dev

    def _factory_reset(self, setup=False):
        if not self._can_reset:
            self.printer.print(
                "☠️  FACTORY RESET CALLED! ☠️ ",
                "",
                "This test should have been marked as requiring reset!",
            )
            pytest.exit("FACTORY RESET CALLED")

        self.printer.print("⚠️  PERFORMING FACTORY RESET! ⚠️ ")

        self.reconnect()

        if self.info.long_touch_for_reset:
            prompted = [0]

            def on_keepalive_reset(status):
                if status != prompted[0]:
                    prompted[0] = status
                    if status == 2:
                        self.printer.print(
                            "👉👉👉 Press the Authenticator button for 10 seconds..."
                        )
                    elif status == 1:
                        self.printer.print("✅ You can now release the button!")

        else:
            on_keepalive_reset = self.on_keepalive

        self.ctap2.reset(on_keepalive=on_keepalive_reset)

        if setup:
            self.setup()

    def setup(self):
        if self.has_ctap2() and ClientPin.is_supported(self.info):
            ClientPin(self.ctap2).set_pin(TEST_PIN)


@pytest.fixture(scope="session")
def printer(request):
    capmanager = request.config.pluginmanager.getplugin("capturemanager")
    return Printer(capmanager)


@pytest.fixture(scope="session", autouse=True)
def dev_manager(pytestconfig, printer):
    if pytestconfig.getoption("no_device"):
        pytest.skip("Skip device tests")

    reader = pytestconfig.getoption("reader")
    ccid = pytestconfig.getoption("ccid")
    manager = DeviceManager(printer, reader, ccid)

    yield manager

    # after the test, reset the device, if possible
    if manager._can_reset:
        manager._factory_reset()


@pytest.fixture(scope="session")
def factory_reset(dev_manager):
    if dev_manager._can_reset:
        return dev_manager._factory_reset
    pytest.skip("Requires factory reset")


@pytest.fixture
def device(dev_manager):
    return dev_manager.device


@pytest.fixture
def ctap2(dev_manager):
    return dev_manager.ctap2


@pytest.fixture
def on_keepalive(dev_manager):
    return dev_manager.on_keepalive


@pytest.fixture
def client(dev_manager):
    return dev_manager.client


@pytest.fixture
def info(ctap2):
    return ctap2.get_info()


@pytest.fixture(params=[CoseKey.for_alg(alg) for alg in CoseKey.supported_algorithms()])
def algorithm(request, info):
    alg_cls = request.param
    alg = {"alg": alg_cls.ALGORITHM, "type": "public-key"}
    if alg not in info.algorithms:
        pytest.skip(f"Algorithm {alg_cls.__name__} not supported")
    return alg


@pytest.fixture(params=[PinProtocolV1, PinProtocolV2])
def pin_protocol(request, info):
    proto = request.param
    if proto.VERSION not in info.pin_uv_protocols:
        pytest.skip(f"PIN/UV protocol {proto.VERSION} not supported")

    all_protocols = ClientPin.PROTOCOLS
    # Ensure we always negotiate only the selected protocol
    ClientPin.PROTOCOLS = [proto]
    yield proto()

    ClientPin.PROTOCOLS = all_protocols


@pytest.fixture
def clear_creds(dev_manager):
    # Clears any discoverable credentials after a test
    yield None
    clientpin = ClientPin(dev_manager.ctap2)
    token = clientpin.get_pin_token(TEST_PIN, ClientPin.PERMISSION.CREDENTIAL_MGMT)
    credman = CredentialManagement(dev_manager.ctap2, clientpin.protocol, token)
    for rp in credman.enumerate_rps():
        for cred in credman.enumerate_creds(rp[4]):
            credman.delete_cred(cred[7])
    assert len(credman.enumerate_rps()) == 0
```

## File: tests/device/test_bioenroll.py
```python
import pytest

from fido2.client import ClientError, DefaultClientDataCollector, Fido2Client
from fido2.ctap import CtapError
from fido2.ctap2.bio import BioEnrollment, CaptureError, FPBioEnrollment
from fido2.ctap2.pin import ClientPin
from fido2.server import Fido2Server

from . import TEST_PIN, CliInteraction


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if not BioEnrollment.is_supported(dev_manager.info):
        pytest.skip("BioEnrollment not supported by authenticator")
    if dev_manager.info.options["uv"]:
        pytest.skip("UV already configured")


def get_bio(ctap2, pin_protocol=None, permissions=ClientPin.PERMISSION.BIO_ENROLL):
    if pin_protocol:
        token = ClientPin(ctap2, pin_protocol).get_pin_token(TEST_PIN, permissions)
    else:
        token = None
    return FPBioEnrollment(ctap2, pin_protocol, token)


def test_get_sensor_info(ctap2):
    bio = get_bio(ctap2)
    info = bio.get_fingerprint_sensor_info()
    assert info.get(2) in (1, None)
    assert info.get(3, 1) > 0
    assert info.get(8, 1) > 0


def test_enroll_use_delete(device, ctap2, pin_protocol, printer):
    bio = get_bio(ctap2, pin_protocol)
    assert len(bio.enumerate_enrollments()) == 0

    context = bio.enroll()
    template_id = None
    while template_id is None:
        printer.print("Press your fingerprint against the sensor now...")
        try:
            template_id = context.capture()
            printer.print(f"{context.remaining} more scans needed.")
        except CaptureError as e:
            printer.print(e)

    enrollments = bio.enumerate_enrollments()
    assert len(enrollments) == 1
    assert enrollments[template_id] in ("", None)

    # Test name/rename
    info = bio.get_fingerprint_sensor_info()
    fname = "Test 1"
    bio.set_name(template_id, fname)

    enrollments = bio.enumerate_enrollments()
    assert len(enrollments) == 1
    assert enrollments[template_id] == fname

    fname = "Test".ljust(info.get(8, 0), "!")
    bio.set_name(template_id, fname)
    enrollments = bio.enumerate_enrollments()
    assert len(enrollments) == 1
    assert enrollments[template_id] == fname

    # Create a credential using fingerprint
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}
    create_options, state = server.register_begin(user, user_verification="required")

    client = Fido2Client(
        device,
        client_data_collector=DefaultClientDataCollector("https://example.com"),
        user_interaction=CliInteraction(printer, "WrongPin"),
    )

    # Allow multiple attempts
    for _ in range(3):
        try:
            result = client.make_credential(create_options.public_key)
            break
        except ClientError as e:
            if e.cause.code == CtapError.ERR.UV_INVALID:
                continue
            raise

    server.register_complete(state, result)

    # Delete fingerprint
    bio = get_bio(ctap2, pin_protocol)
    bio.remove_enrollment(template_id)
    assert len(bio.enumerate_enrollments()) == 0
```

## File: tests/device/test_client.py
```python
import os

import pytest

from fido2.client import ClientError
from fido2.ctap2.credman import CredentialManagement
from fido2.ctap2.pin import ClientPin
from fido2.server import Fido2Server, to_descriptor

from . import TEST_PIN

rp = {"id": "example.com", "name": "Example RP"}
user = {"id": b"user_id", "name": "A. User"}
server = Fido2Server(rp)


@pytest.fixture(scope="module")
def excluded_match(dev_manager):
    if dev_manager.has_ctap2():
        return "CREDENTIAL_EXCLUDED"
    return "DEVICE_INELIGIBLE"


@pytest.fixture(scope="module")
def credential(dev_manager):
    create_options, state = server.register_begin(user)
    result = dev_manager.client.make_credential(create_options.public_key)
    auth_data = server.register_complete(state, result)
    return auth_data.credential_data


@pytest.fixture(scope="module")
def discoverable_credential(request, dev_manager):
    if not dev_manager.has_ctap2():
        pytest.skip("Authenticator does not support CTAP 2")

    has_credman = CredentialManagement.is_supported(dev_manager.info)
    if not has_credman:
        # Request dynamically since we don't want to skip the test unless needed
        factory_reset = request.getfixturevalue("factory_reset")

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
    )
    result = dev_manager.client.make_credential(create_options.public_key)
    auth_data = server.register_complete(state, result)
    yield auth_data.credential_data

    # Delete credential via credman, or factory reset
    if has_credman:
        client_pin = ClientPin(dev_manager.ctap2)
        token = client_pin.get_pin_token(TEST_PIN, ClientPin.PERMISSION.CREDENTIAL_MGMT)
        credman = CredentialManagement(dev_manager.ctap2, client_pin.protocol, token)
        cred_id = {"id": auth_data.credential_data.credential_id, "type": "public-key"}
        credman.delete_cred(cred_id)
    else:
        factory_reset(setup=True)


def test_exclude_credentials_single(credential, client, excluded_match):
    create_options, state = server.register_begin(user, [credential])
    with pytest.raises(ClientError, match=excluded_match):
        client.make_credential(create_options.public_key)


def test_exclude_credentials_multiple(credential, client, excluded_match):
    exclude = [{"id": os.urandom(32), "type": "public-key"} for _ in range(5)]
    exclude.insert(3, to_descriptor(credential))
    create_options, state = server.register_begin(user, exclude)
    with pytest.raises(ClientError, match=excluded_match):
        client.make_credential(create_options.public_key)


def test_exclude_credentials_max(info, client):
    max_len = info.max_cred_id_length
    n_creds = (info.max_creds_in_list or 1) + 2
    exclude = [
        {"id": os.urandom(max_len), "type": "public-key"} for _ in range(n_creds)
    ]
    create_options, state = server.register_begin(user, exclude)
    client.make_credential(create_options.public_key)


def test_exclude_credentials_others(client):
    exclude = [{"id": os.urandom(32), "type": "public-key"} for _ in range(5)]
    create_options, state = server.register_begin(user, exclude)
    client.make_credential(create_options.public_key)


def test_allow_credentials_empty(discoverable_credential, client):
    request_options, state = server.authenticate_begin()
    result = client.get_assertion(request_options.public_key).get_response(0)
    server.authenticate_complete(state, [discoverable_credential], result)


def test_allow_credentials_single(credential, client):
    credentials = [credential]
    request_options, state = server.authenticate_begin(credentials)
    result = client.get_assertion(request_options.public_key).get_response(0)
    server.authenticate_complete(state, credentials, result)


def test_allow_credentials_multiple(credential, client):
    credentials = [credential]
    allow = [{"id": os.urandom(32), "type": "public-key"} for _ in range(5)]
    allow.insert(3, to_descriptor(credential))
    request_options, state = server.authenticate_begin(allow)
    result = client.get_assertion(request_options.public_key).get_response(0)
    server.authenticate_complete(state, credentials, result)


def test_allow_credentials_ineligible(client):
    allow = [{"id": os.urandom(32), "type": "public-key"} for _ in range(5)]
    request_options, state = server.authenticate_begin(allow)
    with pytest.raises(ClientError, match="DEVICE_INELIGIBLE"):
        client.get_assertion(request_options.public_key)
```

## File: tests/device/test_clientpin.py
```python
import pytest

from fido2.ctap import CtapError
from fido2.ctap2.pin import ClientPin

from . import TEST_PIN


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if not ClientPin.is_supported(dev_manager.info):
        pytest.skip("ClientPin not supported by authenticator")


@pytest.fixture
def client_pin(ctap2, pin_protocol):
    return ClientPin(ctap2, pin_protocol)


def test_pin_validation(dev_manager, client_pin):
    assert dev_manager.ctap2.get_info().options["clientPin"] is True
    assert client_pin.get_pin_retries()[0] == 8

    # Wrong PIN decreases the retries remaining
    for retries in range(7, 4, -1):
        # Third attempt uses AUTH_BLOCKED
        with pytest.raises(CtapError, match="PIN_(INVALID|AUTH_BLOCKED)"):
            client_pin.get_pin_token("123456")
        assert client_pin.get_pin_retries()[0] == retries

    # Now soft-locked, does not decrement or unlock with any PIN
    for pin in (TEST_PIN, "123456"):
        with pytest.raises(CtapError, match="PIN_AUTH_BLOCKED"):
            client_pin.get_pin_token(pin)
    assert client_pin.get_pin_retries()[0] == retries

    dev_manager.reconnect()
    client_pin = ClientPin(dev_manager.ctap2, client_pin.protocol)

    # Wrong PIN decreases the retries remaining again
    with pytest.raises(CtapError, match="PIN_INVALID"):
        client_pin.get_pin_token("123456")
    assert client_pin.get_pin_retries()[0] == retries - 1

    # Unlocks with correct PIN
    token = client_pin.get_pin_token(TEST_PIN)
    assert client_pin.get_pin_retries()[0] == 8
    assert token


def test_change_pin(client_pin):
    client_pin.get_pin_token(TEST_PIN)

    new_pin = TEST_PIN[::-1]

    client_pin.change_pin(TEST_PIN, new_pin)
    with pytest.raises(CtapError, match="PIN_INVALID"):
        client_pin.get_pin_token(TEST_PIN)

    client_pin.get_pin_token(new_pin)

    client_pin.change_pin(new_pin, TEST_PIN)
    client_pin.get_pin_token(TEST_PIN)


def test_set_and_reset(dev_manager, client_pin, factory_reset):
    assert dev_manager.ctap2.get_info().options["clientPin"] is True
    assert client_pin.get_pin_retries()[0] == 8

    factory_reset()
    client_pin = ClientPin(dev_manager.ctap2, client_pin.protocol)
    # Factory reset clears the PIN
    assert dev_manager.ctap2.get_info().options["clientPin"] is False
    with pytest.raises(CtapError, match="PIN_NOT_SET"):
        client_pin.get_pin_retries()

    # Setup includes setting the default PIN. More correct would be to just set
    # the PIN ourselves here and test that, but then we need another factory reset
    dev_manager.setup()
    assert dev_manager.ctap2.get_info().options["clientPin"] is True
    assert client_pin.get_pin_retries()[0] == 8
```

## File: tests/device/test_config.py
```python
import pytest

from fido2.client import ClientError, DefaultClientDataCollector, Fido2Client
from fido2.ctap import CtapError
from fido2.ctap2.config import Config
from fido2.ctap2.pin import ClientPin
from fido2.server import Fido2Server

from . import TEST_PIN, CliInteraction


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if not Config.is_supported(dev_manager.info):
        pytest.skip("Config not supported by authenticator")


@pytest.fixture
def client_pin(ctap2, pin_protocol):
    return ClientPin(ctap2, pin_protocol)


def get_config(
    ctap2,
    pin_protocol,
    pin=TEST_PIN,
    permissions=ClientPin.PERMISSION.AUTHENTICATOR_CFG,
):
    token = ClientPin(ctap2, pin_protocol).get_pin_token(pin, permissions)
    return Config(ctap2, pin_protocol, token)


def test_always_uv(ctap2, pin_protocol, device, printer):
    always_uv = ctap2.info.options.get("alwaysUv")
    if always_uv is None:
        pytest.skip("AlwaysUv not supported")

    if ctap2.info.options.get("uv"):
        pytest.skip("UV already configured")

    # Toggle on, if off
    if not always_uv:
        config = get_config(ctap2, pin_protocol)
        config.toggle_always_uv()

    assert ctap2.get_info().options["alwaysUv"] is True

    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(user, user_verification="discouraged")

    # Create a credential
    client = Fido2Client(
        device,
        client_data_collector=DefaultClientDataCollector("https://example.com"),
        user_interaction=CliInteraction(printer, "WrongPin"),
    )

    # Should require PIN due to alwaysUV and fail
    with pytest.raises(ClientError, match="PIN_INVALID"):
        client.make_credential(create_options.public_key)

    # Toggle back off, if toggled on
    if not always_uv:
        config = get_config(ctap2, pin_protocol)
        config.toggle_always_uv()
        assert ctap2.get_info().options["alwaysUv"] is False

        # Now create the credential without requiring auth
        client.make_credential(create_options.public_key)


def test_force_pin_change(ctap2, pin_protocol, client_pin):
    assert ctap2.get_info().force_pin_change is False
    client_pin.get_pin_token(TEST_PIN)

    config = get_config(ctap2, pin_protocol)
    config.set_min_pin_length(force_change_pin=True)
    assert ctap2.get_info().force_pin_change is True

    with pytest.raises(CtapError, match="PIN_INVALID"):
        client_pin.get_pin_token(TEST_PIN)

    pin = TEST_PIN[::-1]
    client_pin.change_pin(TEST_PIN, pin)
    client_pin.change_pin(pin, TEST_PIN)
    client_pin.get_pin_token(TEST_PIN)


def test_min_pin_length(
    dev_manager, ctap2, pin_protocol, client_pin, printer, factory_reset
):
    config = get_config(ctap2, pin_protocol)

    orig_len = ctap2.info.min_pin_length

    config.set_min_pin_length(min_pin_length=orig_len + 2)

    pin = TEST_PIN * 4

    # Too short
    with pytest.raises(CtapError, match="PIN_POLICY_VIOLATION"):
        client_pin.change_pin(TEST_PIN, pin[:orig_len])

    # Just long enough
    client_pin.change_pin(TEST_PIN, pin[: orig_len + 2])

    # Even longer
    client_pin.change_pin(pin[: orig_len + 2], pin[: orig_len + 4])

    config = get_config(ctap2, pin_protocol, pin=pin[: orig_len + 4])

    # Cannot shorten min pin length
    with pytest.raises(CtapError, match="PIN_POLICY_VIOLATION"):
        config.set_min_pin_length(min_pin_length=orig_len)

    config.set_min_pin_length(min_pin_length=orig_len + 6)

    # Current PIN is too short
    assert ctap2.get_info().force_pin_change is True

    client_pin.change_pin(pin[: orig_len + 4], pin[: orig_len + 6])
    assert ctap2.get_info().force_pin_change is False

    # Test minPinLength extension
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(user, user_verification="discouraged")

    if "setMinPINLength" in ctap2.info.options:
        config = get_config(ctap2, pin_protocol, pin=pin[: orig_len + 6])
        config.set_min_pin_length(rp_ids=[rp["id"]])
        client = Fido2Client(
            dev_manager.device,
            client_data_collector=DefaultClientDataCollector("https://example.com"),
            user_interaction=CliInteraction(printer, pin[: orig_len + 6]),
        )

        result = client.make_credential(
            {
                **create_options["publicKey"],
                "extensions": {"minPinLength": True},
            }
        )
        auth_data = server.register_complete(state, result)
        assert auth_data.extensions["minPinLength"] == orig_len + 6

    # Restore original config
    factory_reset(setup=True)
    assert dev_manager.info.min_pin_length == orig_len


@pytest.fixture(scope="module")
def enable_ep(dev_manager, factory_reset):
    if "ep" not in dev_manager.info.options:
        pytest.skip("Enterprise Attestation not supported")

    assert dev_manager.info.options["ep"] is False

    # Enable EP
    pin_protocol = ClientPin(dev_manager.ctap2).protocol
    config = get_config(dev_manager.ctap2, pin_protocol)
    config.enable_enterprise_attestation()
    assert dev_manager.info.options["ep"] is True

    yield None

    # Restore original config
    factory_reset(setup=True)
    assert dev_manager.info.options["ep"] is False


@pytest.fixture(scope="module")
def att_cert(dev_manager):
    rp = {"id": "example.com", "name": "Example RP"}
    user = {"id": b"user_id", "name": "A. User"}

    server = Fido2Server(rp, attestation="direct")
    create_options, state = server.register_begin(user)
    result = dev_manager.client.make_credential(create_options.public_key)
    return result.response.attestation_object.att_stmt["x5c"][0]


def test_ep_platform(client, enable_ep, att_cert):
    rp = {"id": "example.com", "name": "Example RP"}
    user = {"id": b"user_id", "name": "A. User"}

    server = Fido2Server(rp, attestation="enterprise")
    create_options, state = server.register_begin(user)

    client._enterprise_rpid_list = [rp["id"]]
    result = client.make_credential(create_options.public_key)
    cert = result.response.attestation_object.att_stmt["x5c"][0]

    assert att_cert != cert


def test_ep_vendor(pytestconfig, device, printer, enable_ep, att_cert):
    ep_rp_id = pytestconfig.getoption("ep_rp_id")
    if not ep_rp_id:
        pytest.skip("No RP ID provided with --ep-rp-id")

    rp = {"id": ep_rp_id, "name": "Example RP"}
    user = {"id": b"user_id", "name": "A. User"}

    server = Fido2Server(rp, attestation="enterprise")
    create_options, state = server.register_begin(user)

    client = Fido2Client(
        device,
        client_data_collector=DefaultClientDataCollector(f"https://{ep_rp_id}"),
        user_interaction=CliInteraction(printer),
    )

    result = client.make_credential(create_options.public_key)
    cert = result.response.attestation_object.att_stmt["x5c"][0]

    assert att_cert != cert
```

## File: tests/device/test_credblob.py
```python
import os

import pytest

from fido2.server import Fido2Server


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if "credBlob" not in dev_manager.info.extensions:
        pytest.skip("CredBlob not supported by authenticator")


def test_read_write(client, ctap2, clear_creds):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
        user_verification="required",
    )

    # Create a credential
    blob = os.urandom(32)
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"credBlob": blob},
        }
    )
    auth_data = server.register_complete(state, result)
    credentials = [auth_data.credential_data]

    assert auth_data.extensions["credBlob"] is True

    request_options, state = server.authenticate_begin(
        credentials, user_verification="required"
    )

    selection = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {"getCredBlob": True},
        }
    )
    result = selection.get_response(0)

    assert result.response.authenticator_data.extensions.get("credBlob") == blob
```

## File: tests/device/test_credentials.py
```python
from fido2.server import Fido2Server


def test_make_assert(client, pin_protocol, algorithm):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(user)

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "pubKeyCredParams": [algorithm],
        }
    )

    auth_data = server.register_complete(state, result)
    cred = auth_data.credential_data
    assert cred.public_key[3] == algorithm["alg"]
    credentials = [cred]

    # Get assertion
    request_options, state = server.authenticate_begin(credentials)

    # Authenticate the credential
    result = client.get_assertion(request_options.public_key).get_response(0)
    cred_data = server.authenticate_complete(state, credentials, result)
    assert cred_data == cred
```

## File: tests/device/test_credman.py
```python
import pytest

from fido2.ctap import CtapError
from fido2.ctap2.credman import CredentialManagement
from fido2.ctap2.pin import ClientPin
from fido2.server import Fido2Server

from . import TEST_PIN


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if not CredentialManagement.is_supported(dev_manager.info):
        pytest.skip("CredentialManagement not supported by authenticator")


def get_credman(ctap2, pin_protocol, permissions=ClientPin.PERMISSION.CREDENTIAL_MGMT):
    token = ClientPin(ctap2, pin_protocol).get_pin_token(TEST_PIN, permissions)
    return CredentialManagement(ctap2, pin_protocol, token)


def test_list_and_delete(client, ctap2, pin_protocol, algorithm):
    # Ensure no credentials exist initially
    credman = get_credman(ctap2, pin_protocol)
    metadata = credman.get_metadata()
    assert metadata[CredentialManagement.RESULT.EXISTING_CRED_COUNT] == 0
    remaining = metadata[CredentialManagement.RESULT.MAX_REMAINING_COUNT]
    assert remaining > 0

    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
    )

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "pubKeyCredParams": [algorithm],
            "extensions": {"credProps": True},
        }
    )

    # Need new PIN token as old one is expired by make_credential
    credman = get_credman(ctap2, pin_protocol)

    metadata = credman.get_metadata()
    assert metadata[CredentialManagement.RESULT.EXISTING_CRED_COUNT] == 1
    assert metadata[CredentialManagement.RESULT.MAX_REMAINING_COUNT] < remaining

    # Complete registration
    auth_data = server.register_complete(state, result)
    cred = auth_data.credential_data
    assert cred.public_key[3] == algorithm["alg"]

    rps = credman.enumerate_rps()
    assert len(rps) == 1

    # Not all keys are required in response, but those that are should match
    for k, v in rps[0][3].items():
        assert rp[k] == v

    rp_id_hash = rps[0][4]
    creds = credman.enumerate_creds(rp_id_hash)
    assert len(creds) == 1
    assert creds[0][6] == user
    assert creds[0][7]["id"] == cred.credential_id
    assert creds[0][8] == cred.public_key

    credman.delete_cred(creds[0][7])
    metadata = credman.get_metadata()
    assert metadata[CredentialManagement.RESULT.EXISTING_CRED_COUNT] == 0
    assert metadata[CredentialManagement.RESULT.MAX_REMAINING_COUNT] == remaining


def test_update(client, ctap2, pin_protocol):
    if not CredentialManagement.is_update_supported(ctap2.info):
        pytest.skip("ClientPin update not supported")

    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User", "displayName": "Display Name"}

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
    )

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"credProps": True},
        }
    )
    auth_data = server.register_complete(state, result)
    cred_id = {"id": auth_data.credential_data.credential_id, "type": "public-key"}

    credman = get_credman(ctap2, pin_protocol)
    rps = credman.enumerate_rps()
    rp_id_hash = rps[0][4]

    # Check user data
    creds = credman.enumerate_creds(rp_id_hash)
    assert len(creds) == 1

    # Authenticators may or may not store name/displayName
    stores_name = "name" in creds[0][6]
    stores_display_name = "displayName" in creds[0][6]

    if not stores_name:
        del user["name"]
    if not stores_display_name:
        del user["displayName"]

    assert creds[0][6] == user

    # Update user data
    user2 = {"id": b"user_id"}
    if stores_name:
        user2["name"] = "A. User 2"
    if stores_display_name:
        user2["displayName"] = "Display Name 2"

    credman.update_user_info(cred_id, user2)

    creds = credman.enumerate_creds(rp_id_hash)
    assert len(creds) == 1
    assert creds[0][6] == user2
    assert creds[0][7] == cred_id

    # Test deleting fields
    user3 = {"id": b"user_id"}
    credman.update_user_info(cred_id, user3)
    creds = credman.enumerate_creds(rp_id_hash)
    assert len(creds) == 1
    assert creds[0][6] == user3
    assert creds[0][7] == cred_id

    # Clean up
    credman.delete_cred(cred_id)


def test_missing_permissions(ctap2, pin_protocol):
    if not ClientPin.is_token_supported(ctap2.info):
        pytest.skip("Permissions not supported")

    credman = get_credman(ctap2, pin_protocol, ClientPin.PERMISSION(0))

    with pytest.raises(CtapError, match="PIN_AUTH_INVALID"):
        credman.get_metadata()


def test_read_only_management(dev_manager, pin_protocol):
    if not CredentialManagement.is_readonly_supported(dev_manager.info):
        pytest.skip("Persistent PUAT not supported")

    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
    )

    # Create a credential
    result = dev_manager.client.make_credential(create_options["publicKey"])
    auth_data = server.register_complete(state, result)
    cred_id = {"id": auth_data.credential_data.credential_id, "type": "public-key"}
    rp_id_hash = server.rp.id_hash

    token = ClientPin(dev_manager.ctap2, pin_protocol).get_pin_token(
        TEST_PIN, ClientPin.PERMISSION.PERSISTENT_CREDENTIAL_MGMT
    )

    # Get enc_identifier before reconnect
    ident = dev_manager.ctap2.get_info().get_identifier(token)

    # Test token before and after reconnect
    for reconnect in (False, True):
        if reconnect:
            dev_manager.reconnect()

        # Use persistent token
        credman = CredentialManagement(dev_manager.ctap2, pin_protocol, token)

        # Test metadata
        assert credman.get_metadata()[1] == 1

        # Test enumerate RPs and creds
        rps = credman.enumerate_rps()
        assert len(rps) == 1
        creds = credman.enumerate_creds(rp_id_hash)
        assert len(creds) == 1

        # Ensure update isn't allowed
        user2 = {"id": b"user_id", "name": "A. User 2"}
        with pytest.raises(CtapError, match="PIN_AUTH_INVALID"):
            credman.update_user_info(cred_id, user2)

        # Ensure delete isn't allowed
        with pytest.raises(CtapError, match="PIN_AUTH_INVALID"):
            credman.delete_cred(cred_id)

    # Compare enc_identifier after reconnect
    assert dev_manager.ctap2.get_info().get_identifier(token) == ident

    # Use new (non-persistent) PIN token
    credman = get_credman(dev_manager.ctap2, pin_protocol)
    credman.delete_cred(cred_id)
```

## File: tests/device/test_hid.py
```python
def test_ping(device):
    msg1 = b"hello world!"
    msg2 = b"            "
    msg3 = b""
    assert device.ping(msg1) == msg1
    assert device.ping(msg2) == msg2
    assert device.ping(msg3) == msg3
```

## File: tests/device/test_info.py
```python
from fido2.webauthn import Aaguid


def assert_list_of(typ, value):
    assert isinstance(value, list)
    for v in value:
        assert isinstance(v, typ)


def assert_dict_of(k_type, v_type, value):
    assert isinstance(value, dict)
    for k, v in value.items():
        assert isinstance(k, k_type)
        assert isinstance(v, v_type)


def assert_unique(value):
    assert len(set(value)) == len(value)


def test_get_info_fields(ctap2):
    info = ctap2.get_info()

    assert_list_of(str, info.versions)
    assert len(info.versions) > 0

    assert_list_of(str, info.extensions)
    assert isinstance(info.aaguid, Aaguid)
    assert_dict_of(str, bool | None, info.options)
    assert isinstance(info.max_msg_size, int)
    assert_list_of(int, info.pin_uv_protocols)
    assert_unique(info.pin_uv_protocols)
    assert isinstance(info.max_creds_in_list, int)
    assert isinstance(info.max_cred_id_length, int)
    assert_list_of(str, info.transports)
    assert_unique(info.transports)

    assert_list_of(dict, info.algorithms)
    assert isinstance(info.max_large_blob, int)
    assert isinstance(info.force_pin_change, bool)
    assert isinstance(info.min_pin_length, int)
    assert info.min_pin_length >= 4
    assert isinstance(info.firmware_version, int)
    assert isinstance(info.max_cred_blob_length, int)
    assert isinstance(info.max_rpids_for_min_pin, int)
    assert isinstance(info.preferred_platform_uv_attempts, int)
    assert isinstance(info.uv_modality, int)
    assert_dict_of(str, int, info.certifications)

    assert isinstance(info.remaining_disc_creds, int | None)
    assert_list_of(int, info.vendor_prototype_config_commands)
    assert_list_of(str, info.attestation_formats)
    assert_unique(info.attestation_formats)
    assert len(info.attestation_formats) > 0

    assert isinstance(info.uv_count_since_pin, int | None)
    assert isinstance(info.long_touch_for_reset, bool)


def test_enc_identifier_changes(ctap2):
    if ctap2.info.enc_identifier:
        assert ctap2.get_info().enc_identifier != ctap2.get_info().enc_identifier
```

## File: tests/device/test_largeblobs.py
```python
import os
import struct

import pytest

from fido2 import cbor
from fido2.ctap import CtapError
from fido2.ctap2.blob import LargeBlobs
from fido2.ctap2.pin import ClientPin
from fido2.server import Fido2Server
from fido2.utils import sha256, websafe_decode, websafe_encode

from . import TEST_PIN


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if not LargeBlobs.is_supported(dev_manager.info):
        pytest.skip("LargeBlobs not supported by authenticator")


def get_lb(ctap2, pin_protocol, permissions=ClientPin.PERMISSION.LARGE_BLOB_WRITE):
    token = ClientPin(ctap2, pin_protocol).get_pin_token(TEST_PIN, permissions)
    return LargeBlobs(ctap2, pin_protocol, token)


def test_read_write(ctap2, pin_protocol):
    lb = get_lb(ctap2, pin_protocol)
    assert len(lb.read_blob_array()) == 0

    key1 = os.urandom(32)
    data1 = b"test data"
    key2 = os.urandom(32)
    data2 = b"some other data"

    assert lb.get_blob(key1) is None
    lb.put_blob(key1, data1)
    assert lb.get_blob(key1) == data1
    assert len(lb.read_blob_array()) == 1

    lb.put_blob(key2, data2)
    assert lb.get_blob(key1) == data1
    assert lb.get_blob(key2) == data2
    assert len(lb.read_blob_array()) == 2

    lb.delete_blob(key1)
    assert lb.get_blob(key1) is None
    assert lb.get_blob(key2) == data2
    assert len(lb.read_blob_array()) == 1

    lb.delete_blob(key2)
    assert lb.get_blob(key2) is None
    assert len(lb.read_blob_array()) == 0


def test_invalid_checksum(ctap2, pin_protocol):
    lb = get_lb(ctap2, pin_protocol)

    data = cbor.encode([])
    # Set the checksum to an invalid value to ensure the authenticator checks it
    data += sha256(data)[:15] + b"\xff"
    offset = 0
    size = len(data)

    msg = b"\xff" * 32 + b"\x0c\x00" + struct.pack("<I", offset) + sha256(data)
    pin_uv_protocol = pin_protocol.VERSION
    pin_uv_param = pin_protocol.authenticate(lb.pin_uv.token, msg)

    with pytest.raises(CtapError, match="INTEGRITY_FAILURE"):
        ctap2.large_blobs(
            0,
            set=data,
            length=size,
            pin_uv_protocol=pin_uv_protocol,
            pin_uv_param=pin_uv_param,
        )


def test_size_bounds(ctap2, pin_protocol):
    lb = get_lb(ctap2, pin_protocol)
    assert len(lb.read_blob_array()) == 0

    # The max storage is the CBOR-encoded array, minus a 16 byte checksum
    max_size = ctap2.info.max_large_blob - 16

    # Create data which when cbor-encoded is exactly max_size bytes
    array = [{1: os.urandom(max_size - 8)}]
    array.extend([0] * (max_size - len(cbor.encode(array))))

    lb.write_blob_array(array)

    # Ensure writing larger data fails:
    array.append(1)
    with pytest.raises(CtapError, match="LARGE_BLOB_STORAGE_FULL"):
        lb.write_blob_array(array)

    # Clear the data
    lb.write_blob_array([])


def test_missing_permissions(ctap2, pin_protocol):
    key = os.urandom(32)
    data = b"test data"

    # Try write without PIN token
    lb = LargeBlobs(ctap2, pin_protocol)
    blobs = lb.read_blob_array()
    assert len(blobs) == 0

    with pytest.raises(CtapError, match="PUAT_REQUIRED"):
        lb.put_blob(key, data)

    # Try with wrong permissions
    lb = get_lb(ctap2, pin_protocol, ClientPin.PERMISSION.CREDENTIAL_MGMT)
    with pytest.raises(CtapError, match="PIN_AUTH_INVALID"):
        lb.put_blob(key, data)


def test_large_blob_key(client, ctap2, pin_protocol, clear_creds):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
        user_verification="required",
    )

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"largeBlob": {"support": "required"}},
        }
    )
    auth_data = server.register_complete(state, result)
    credentials = [auth_data.credential_data]

    assert result.client_extension_results.large_blob.supported is True
    assert result.client_extension_results["largeBlob"]["supported"] is True

    request_options, state = server.authenticate_begin(
        credentials, user_verification="required"
    )

    data = b"test data"

    selection = client.get_assertion(
        {
            **request_options["publicKey"],
            # Write a large blob
            "extensions": {"largeBlob": {"write": websafe_encode(data)}},
        }
    )
    result = selection.get_response(0)

    assert result.client_extension_results.large_blob.written is True
    assert result.client_extension_results["largeBlob"]["written"] is True

    # Authenticate the credential
    selection = client.get_assertion(
        {
            **request_options["publicKey"],
            # Read back the blob
            "extensions": {"largeBlob": {"read": True}},
        }
    )
    result = selection.get_response(0)

    assert result.client_extension_results.large_blob.blob == data
    assert websafe_decode(result.client_extension_results["largeBlob"]["blob"]) == data

    # Clear the data
    lb = get_lb(ctap2, pin_protocol)
    lb.write_blob_array([])
    assert len(lb.read_blob_array()) == 0
```

## File: tests/device/test_payment.py
```python
import pytest

from fido2.client import Fido2Client
from fido2.ctap2.extensions import (
    PaymentCredentialInstrument,
    PaymentCurrencyAmount,
    ThirdPartyPaymentExtension,
)
from fido2.payment import (
    CollectedClientAdditionalPaymentData,
    PaymentClientDataCollector,
)
from fido2.server import Fido2Server

from . import TEST_PIN, CliInteraction


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if "thirdPartyPayment" not in dev_manager.info.extensions:
        pytest.skip("thirdPartyPayment not supported by authenticator")


def test_payment_extension(device, printer):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}

    # Prepare parameters for makeCredential
    create_options, state = server.register_begin(
        user,
        resident_key_requirement="required",
        user_verification="required",
        authenticator_attachment="cross-platform",
    )

    client = Fido2Client(
        device,
        client_data_collector=PaymentClientDataCollector("https://example.com"),
        user_interaction=CliInteraction(printer, TEST_PIN),
        extensions=[ThirdPartyPaymentExtension()],
    )

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"payment": {"isPayment": True}},
        }
    )

    # Complete registration
    auth_data = server.register_complete(state, result)
    credentials = [auth_data.credential_data]

    print("Payment credential created!")

    # Prepare parameters for getAssertion
    request_options, state = server.authenticate_begin(
        credentials, user_verification="required"
    )

    # Prepare payment options
    payment = CollectedClientAdditionalPaymentData(
        rp_id="example.com",
        top_origin="https://top.example.com",
        payee_name="Mr. Payee",
        payee_origin="https://payee.example.com",
        total=PaymentCurrencyAmount(
            currency="USD",
            value="1.00",
        ),
        instrument=PaymentCredentialInstrument(
            display_name="My Payment",
            icon="https://example.com/icon.png",
        ),
    )

    # Authenticate the credential
    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {
                "payment": dict(payment, isPayment=True),
            },
        }
    )

    # Only one cred in allowCredentials, only one response.
    result = result.get_response(0)

    # Verify that the key includes the payment extension
    assert result.response.authenticator_data.extensions["thirdPartyPayment"] is True

    # Verify that the client has added the payment data
    assert result.response.client_data.type == "payment.get"
    assert result.response.client_data.payment == payment
```

## File: tests/device/test_prf.py
```python
import os

import pytest

from fido2.client import DefaultClientDataCollector, Fido2Client
from fido2.ctap2.extensions import HmacSecretExtension
from fido2.server import Fido2Server
from fido2.utils import websafe_encode

from . import TEST_PIN, CliInteraction


@pytest.fixture(autouse=True, scope="module")
def preconditions(dev_manager):
    if "hmac-secret" not in dev_manager.info.extensions:
        pytest.skip("hmac-secret not supported by authenticator")


def test_prf(client, pin_protocol):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}
    uv = "required"

    create_options, state = server.register_begin(user, user_verification=uv)

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"prf": {}},
        }
    )
    assert result.client_extension_results.prf.enabled is True
    assert result.client_extension_results["prf"]["enabled"] is True

    auth_data = server.register_complete(state, result)
    credentials = [auth_data.credential_data]

    # Complete registration
    auth_data = server.register_complete(state, result)
    credential = auth_data.credential_data

    # Generate a salt for PRF:
    salt = websafe_encode(os.urandom(32))

    # Prepare parameters for getAssertion
    credentials = [credential]
    request_options, state = server.authenticate_begin(
        credentials, user_verification=uv
    )

    # Authenticate the credential
    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {"prf": {"eval": {"first": salt}}},
        }
    )

    # Only one cred in allowCredentials, only one response.
    response = result.get_response(0)

    output1 = response.client_extension_results.prf.results.first
    assert response.client_extension_results["prf"]["results"][
        "first"
    ] == websafe_encode(output1)

    # Authenticate again, using two salts to generate two secrets.

    # This time we will use evalByCredential, which can be used if there are multiple
    # credentials which use different salts. Here it is not needed, but provided for
    # completeness of the example.

    # Generate a second salt for PRF:
    salt2 = websafe_encode(os.urandom(32))
    # The first salt is reused, which should result in the same secret.

    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {
                "prf": {
                    "evalByCredential": {
                        websafe_encode(credential.credential_id): {
                            "first": salt,
                            "second": salt2,
                        }
                    }
                }
            },
        }
    )

    response = result.get_response(0)

    output = response.client_extension_results.prf.results
    assert output.first == output1
    assert output.second != output1
    assert response.client_extension_results["prf"]["results"][
        "second"
    ] == websafe_encode(output.second)


def test_hmac_secret(device, pin_protocol, printer):
    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}
    uv = "required"

    create_options, state = server.register_begin(user, user_verification=uv)

    client = Fido2Client(
        device,
        client_data_collector=DefaultClientDataCollector("https://example.com"),
        user_interaction=CliInteraction(printer, TEST_PIN),
        extensions=[HmacSecretExtension(allow_hmac_secret=True)],
    )

    # Create a credential
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"hmacCreateSecret": True},
        }
    )
    assert result.client_extension_results.hmac_create_secret is True
    assert result.client_extension_results["hmacCreateSecret"] is True

    # Complete registration
    auth_data = server.register_complete(state, result)
    credentials = [auth_data.credential_data]

    # Generate a salt for HmacSecret:
    salt = os.urandom(32)

    # Prepare parameters for getAssertion
    request_options, state = server.authenticate_begin(
        credentials, user_verification=uv
    )

    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {"hmacGetSecret": {"salt1": salt}},
        }
    )
    result = result.get_response(0)

    output1 = result.client_extension_results.hmac_get_secret.output1
    assert result.client_extension_results["hmacGetSecret"][
        "output1"
    ] == websafe_encode(output1)

    salt2 = os.urandom(32)

    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {"hmacGetSecret": {"salt1": salt, "salt2": salt2}},
        }
    )
    result = result.get_response(0)

    output = result.client_extension_results.hmac_get_secret
    assert output.output1 == output1
    assert output.output2 != output1


def test_prf_mc(client, pin_protocol, info):
    if "hmac-secret-mc" not in info.extensions:
        pytest.skip("hmac-secret-mc not supported by authenticator")

    rp = {"id": "example.com", "name": "Example RP"}
    server = Fido2Server(rp)
    user = {"id": b"user_id", "name": "A. User"}
    uv = "required"

    create_options, state = server.register_begin(user, user_verification=uv)

    # Generate salts for PRF:
    salt1 = websafe_encode(os.urandom(32))
    salt2 = websafe_encode(os.urandom(32))

    # Create a credential, with salts
    result = client.make_credential(
        {
            **create_options["publicKey"],
            "extensions": {"prf": {"eval": {"first": salt1, "second": salt2}}},
        }
    )
    auth_data = server.register_complete(state, result)
    credential = auth_data.credential_data

    assert result.client_extension_results.prf.enabled is True
    assert result.client_extension_results["prf"]["enabled"] is True

    output = result.client_extension_results.prf.results
    assert output.first
    assert output.second

    # Prepare parameters for getAssertion
    credentials = [credential]
    request_options, state = server.authenticate_begin(
        credentials, user_verification=uv
    )

    # Authenticate the credential
    result = client.get_assertion(
        {
            **request_options["publicKey"],
            "extensions": {
                "prf": {
                    "evalByCredential": {
                        websafe_encode(credential.credential_id): {
                            "first": salt1,
                            "second": salt2,
                        }
                    }
                }
            },
        }
    )

    response = result.get_response(0)
    assert output == response.client_extension_results.prf.results
```

## File: tests/conftest.py
```python
def pytest_addoption(parser):
    parser.addoption("--reader", action="store")
    parser.addoption("--no-device", action="store_true")
    parser.addoption("--ep-rp-id", action="store")
    parser.addoption("--ccid", action="store_true")
```

## File: tests/test_attestation.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

from cryptography.exceptions import UnsupportedAlgorithm, _Reasons

from fido2.attestation import (
    AndroidSafetynetAttestation,
    AppleAttestation,
    Attestation,
    AttestationType,
    FidoU2FAttestation,
    InvalidData,
    InvalidSignature,
    NoneAttestation,
    PackedAttestation,
    TpmAttestation,
    UnsupportedAttestation,
    UnsupportedType,
    verify_x509_chain,
)
from fido2.webauthn import AuthenticatorData

# GS Root R2 (https://pki.goog/)
_GSR2_DER = bytes.fromhex(
    "308203ba308202a2a003020102020b0400000000010f8626e60d300d06092a864886f70d0101050500304c3120301e060355040b1317476c6f62616c5369676e20526f6f74204341202d20523231133011060355040a130a476c6f62616c5369676e311330110603550403130a476c6f62616c5369676e301e170d3036313231353038303030305a170d3231313231353038303030305a304c3120301e060355040b1317476c6f62616c5369676e20526f6f74204341202d20523231133011060355040a130a476c6f62616c5369676e311330110603550403130a476c6f62616c5369676e30820122300d06092a864886f70d01010105000382010f003082010a0282010100a6cf240ebe2e6f28994542c4ab3e21549b0bd37f8470fa12b3cbbf875fc67f86d3b2305cd6fdadf17bdce5f86096099210f5d053defb7b7e7388ac52887b4aa6ca49a65ea8a78c5a11bc7a82ebbe8ce9b3ac962507974a992a072fb41e77bf8a0fb5027c1b96b8c5b93a2cbcd612b9eb597de2d006865f5e496ab5395e8834ecbc780c0898846ca8cd4bb4a07d0c794df0b82dcb21cad56c5b7de1a02984a1f9d39449cb24629120bcdd0bd5d9ccf9ea270a2b7391c69d1bacc8cbe8e0a0f42f908b4dfbb0361bf6197a85e06df26113885c9fe0930a51978a5aceafabd5f7aa09aa60bddcd95fdf72a960135e0001c94afa3fa4ea070321028e82ca03c29b8f0203010001a3819c308199300e0603551d0f0101ff040403020106300f0603551d130101ff040530030101ff301d0603551d0e041604149be20757671c1ec06a06de59b49a2ddfdc19862e30360603551d1f042f302d302ba029a0278625687474703a2f2f63726c2e676c6f62616c7369676e2e6e65742f726f6f742d72322e63726c301f0603551d230418301680149be20757671c1ec06a06de59b49a2ddfdc19862e300d06092a864886f70d01010505000382010100998153871c68978691ece04ab8440bab81ac274fd6c1b81c4378b30c9afcea2c3c6e611b4d4b29f59f051d26c1b8e983006245b6a90893b9a9334b189ac2f887884edbdd71341ac154da463fe0d32aab6d5422f53a62cd206fba2989d7dd91eed35ca23ea15b41f5dfe564432de9d539abd2a2dfb78bd0c080191c45c02d8ce8f82da4745649c505b54f15de6e44783987a87ebbf3791891bbf46f9dc1f08c358c5d01fbc36db9ef446d7946317e0afea982c1ffefab6e20c450c95f9d4d9b178c0ce501c9a0416a7353faa550b46e250ffb4c18f4fd52d98e69b1e8110fde88d8fb1d49f7aade95cf2078c26012db25408c6afc7e4238406412f79e81e1932e"  # noqa E501
)


class TestAttestationObject(unittest.TestCase):
    def test_unsupported_attestation(self):
        attestation = Attestation.for_type("__unsupported__")()
        self.assertIsInstance(attestation, UnsupportedAttestation)
        with self.assertRaises(UnsupportedType) as ctx:
            attestation.verify({}, 0, b"")
        self.assertEqual(ctx.exception.fmt, "__unsupported__")

    def test_none_attestation(self):
        attestation = Attestation.for_type("none")()
        self.assertIsInstance(attestation, NoneAttestation)

        auth_data = AuthenticatorData(
            bytes.fromhex(
                "0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12410000002BF8A011F38C0A4D15800617111F9EDC7D0040A17370D9C1759005700C8DE77E7DFD3A0A5300E0A26E5213AA40D6DF10EE4028B58B5F34167035D840BEBAE0C5CE8FD05AD9BD33E3BE7D1C558D81AB4803570BA5010203262001215820A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1225820FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"  # noqa E501
            )
        )
        res = attestation.verify({}, auth_data, b"deadbeef" * 8)
        self.assertEqual(res.attestation_type, AttestationType.NONE)
        self.assertEqual(res.trust_path, [])

        with self.assertRaises(InvalidData):
            attestation.verify({"not": "empty"}, auth_data, b"deadbeef" * 8)

    def test_none_windows_hello_attestation(self):
        attestation = Attestation.for_type("none")()
        self.assertIsInstance(attestation, NoneAttestation)

        auth_data = AuthenticatorData(
            bytes.fromhex(
                "54ce651ed715b4aaa755eecebd4ea0950815b334bd07d109893e963018cddbd945000000006028b017b1d44c02b4b3afcdafc96bb200201decfcd6d6a05c2826d52348afdc70a9800df007845047b1a23706aa6e2f315ca401030339010020590100af59f4ad4f71da800bb91045b267e240e06317f7b2b1d76f78e239a433811faeca58a1869fb00225eb2727f81b6b20cbc18c0ad8d38fa450e8df11b4ad3bc3ee5d13c77ed172fa3af0195ec6ac0c4bac8c950115dfce6d38737cbafefbe117d8401cd56c638043a0d585131bc48a153b17a8dcb96671e15a90ba1b4ff810b138b77ac0a050b039b87b6089dd8dfa45611b992109d554aad3e6b72ac82d801496e4d2d230aa466090bbbf4f5632fe4b588e4f571462378fa6f514a536a5945b223c8d98f730b7cf85de86b98c217090f9e9ebf9643cf3feceeacb837d7a18542e03271cd8c70cf81186cdb63e4cbf4efc0cbbd3c93231b06f19580d0a980264d12143010001"  # noqa
            )
        )  # noqa
        res = attestation.verify({}, auth_data, b"deadbeef" * 8)
        self.assertEqual(res.attestation_type, AttestationType.NONE)
        self.assertEqual(res.trust_path, [])

        with self.assertRaises(InvalidData):
            attestation.verify({"not": "empty"}, auth_data, b"deadbeef" * 8)

    def test_tpm_windows_hello_attestation(self):
        attestation = Attestation.for_type("tpm")()
        self.assertIsInstance(attestation, TpmAttestation)
        statement = {
            "alg": -65535,
            "sig": bytes.fromhex(
                """80e564d8cbb236577de68d2e68ecae200a8eaf6992889b5
fdc24624a4cb69caaab18df965058fbac39df9714b9c80b9a12d715cfc4dd15ed3a6e191a6d26e
7206fd402b0733c2c8b91f62ad44e4d41c940e2e914253b1d1a1c8889b1cdaf668b5449245dc33
1fab12e0b0dcdfc530cbe1f370e1f2b06c163fbd6177925a1a8998edd2e726989246a1980fa34e
6d65d3ca284944cb10254d85db0d8948294fb8174a41206c6b5e36406bae447343f8c9f97420e3
9f361815dfb268b33ccde5f29e4348a70f95abc30754c839fa7126e5bd882377d6abe3c0c95ba5
c21190a5e4fff5380b2c23cc1655e593244019e172ba8284618471d95b92c231c1ffe98ff23
""".replace("\n", "")
            ),
            "x5c": [
                bytes.fromhex(
                    """308204b23082039aa0030201020210789e1a3657344c52bad2
2ed1ceb1bfaf300d06092a864886f70d01010b05003041313f303d060355040313364e43552d4e
54432d4b455949442d394642423739414130463532363237384245443135303932394137313731
45393641333542454637301e170d3139303430313038353934305a170d32393034303130383539
34305a300030820122300d06092a864886f70d01010105000382010f003082010a0282010100a6
60d1fe41564c26f943c70ff89fbd9ed6d957191d5ecaf727393d73cfff85e3ccfb9830027fe84b
171cc4b0b13811df4d9deff2bce4d8a8f9797169f7b8fc25016d9ba687c003083693716180c8f1
eccaa4410a9a7fe07b198ad7ba94ecf744e9bef0273a5e0723a4ac197994ca1ac0e5f595433970
0cf14ead419ae7cde8c3e81389771d5fa3d339f8d0856e918fd3746fa9a944d3c1f1c6a4e0ce3f
99b5ac5ba05166b3b8695405ae7d3777f9cc8e3ab8570f2191ba4f2cfc4c544337596f48d3d5f5
f9ae80575bf9eb81d5c477e99c58854645d587dd0ccdea2b0e3d482e69b326b289e65741e6b214
3fc2bca35ca7dd60e554affdcb85000762ff09b0410203010001a38201e5308201e1300e060355
1d0f0101ff040403020780300c0603551d130101ff04023000306d0603551d200101ff04633061
305f06092b060104018237151f3052305006082b0601050507020230441e420054004300500041
002000200054007200750073007400650064002000200050006c006100740066006f0072006d00
200020004900640065006e007400690074007930100603551d250409300706056781050803304a
0603551d110101ff0440303ea43c303a3138300e060567810502030c0569643a31333010060567
810502020c074e5043543678783014060567810502010c0b69643a3445353434333030301f0603
551d23041830168014c799ef2371327cb2e9e03838d0a9009fe9ed29e7301d0603551d0e041604
1429fb5f05c6187d8463b8b250b8f0ff128fd3a0713081b306082b060105050701010481a63081
a33081a006082b0601050507300286819368747470733a2f2f617a637370726f646e637561696b
7075626c6973682e626c6f622e636f72652e77696e646f77732e6e65742f6e63752d6e74632d6b
657969642d39666262373961613066353236323738626564313530393239613731373165393661
3335626566372f66383530353438392d303235612d343235322d383239302d3934646532633633
643039362e636572300d06092a864886f70d01010b0500038201010084bc4b9ac3ab6c2438bdec
dd3d99e6179bfc465995481d856683602bdcf0c26327b8ab77f7b695c8c6aab5f283b079c29369
29727b839e5bf08c687a33fc59bf281ebf28e9d04e78fd626573028014028badca038e68361017
a4501b18d56a6a73e35f00e043d8febb7a4c719c837bc5cb801efe23570d6c8b40699ba411fe66
f6fe5558f7d1c56a7646ba483cd601690a9323caba9257ae561781b13c658083ad1281047d94d4
c1ab9759d90a16fbe167cec388e7b67027a20dbc1b88986dbb636107ef91ffec22c413ac5fbfec
3de9ee4aa1c6e4c173e43246193890c8b024587fcc8028eb379f515de3c678b11dfb81aef3547c
3c6e790577d52f775f9148""".replace("\n", "")
                ),
                bytes.fromhex(
                    """308205e8308203d0a003020102021333000000a5304bb34bf0
bee43e0000000000a5300d06092a864886f70d01010b050030818c310b30090603550406130255
53311330110603550408130a57617368696e67746f6e3110300e060355040713075265646d6f6e
64311e301c060355040a13154d6963726f736f667420436f72706f726174696f6e313630340603
550403132d4d6963726f736f66742054504d20526f6f7420436572746966696361746520417574
686f726974792032303134301e170d3136303831383230323032305a170d323931323331323032
3032305a3041313f303d060355040313364e43552d4e54432d4b455949442d3946424237394141
304635323632373842454431353039323941373137314539364133354245463730820122300d06
092a864886f70d01010105000382010f003082010a0282010100e0b963203494ff3b8b93855f4d
0086aabf9f5038fe2a2c04311609074565097dd16de61ae1e6086f5d16997dc7ee5342bf9988f6
bb73ca614f3f5d8ea084fd047112892ae22db792e2efbe24bcb07fd01af124666db7ad53677e45
6a95e972a659c04fe3569e882afbf019c3c5890c52d2e81d175f97234fbe341406cbf834cafa76
184c077c9bd058fbe14b4032039142128fe985ee6041819eee86a62a43491d11af9d78f08e722a
28c0e9b522fed12f172dddfd032a634a6eba2fc90c332997d3ba5f297230cd7d666b6925c0e6ea
79b2459f68fc283cd7a09e09973a610fb88eb63bb1cc29e0dc5e033ace6b966c78038c1adc049e
f5360ae28696825ed10203010001a382018b30820187300b0603551d0f040403020186301b0603
551d250414301206092b06010401823715240605678105080330160603551d20040f300d300b06
092b060104018237151f30120603551d130101ff040830060101ff020100301d0603551d0e0416
0414c799ef2371327cb2e9e03838d0a9009fe9ed29e7301f0603551d230418301680147a8c0ace
2f486217e294d1ae55c152ec7174a45630700603551d1f046930673065a063a061865f68747470
3a2f2f7777772e6d6963726f736f66742e636f6d2f706b696f70732f63726c2f4d6963726f736f
667425323054504d253230526f6f742532304365727469666963617465253230417574686f7269
7479253230323031342e63726c307d06082b060105050701010471306f306d06082b0601050507
30028661687474703a2f2f7777772e6d6963726f736f66742e636f6d2f706b696f70732f636572
74732f4d6963726f736f667425323054504d253230526f6f742532304365727469666963617465
253230417574686f72697479253230323031342e637274300d06092a864886f70d01010b050003
820201003e91d074e6d6b9719bf13ffd7cd16b733938c092edaa580136ac7d8bb5295242e432f6
7c3ca5b1c8968b994665e99796a39d579a85cbe6eab02dfce1d08a4ce802b41bf6b00a01533c7c
f3b96c7d0b9c0f3a5d2e04350037aea5140a5cc781ca73f370998110bd1031cfa427760920574a
5d7709a1765921d61cb36d91d2ce9d3301f0798ae4b23592b080e70bb535cdf57403f96fe6f0ff
4c0f0363f785a918a1fd3debfaaaebe6b08724a216b491e95e6e300e3d43e4e156fe3c036afba1
7ad2b442f904568af1cc3fd9ad1888cbbd9ec98d42e55af5b26fa8790b6b7da677a585fff6ae90
18e492742d4e9c5ca1a06990a3abff76c6bc4b1e22d8c226d09a96fdcc12801345b647e15850d1
0d0cdb609160b1a7a7c2c6f0eb3dbc2fcd42b765fd22a5672b26009b9a83b44388b62cb89e9169
a455ff5be5ce8f7bde0420b5d7d24ec254affdc2e7e946c961ec159b6dfc703e3934f9445b0072
8e137e11a7c66f76709ca2177b39159fc08593aaa83724b159abb93e535aef53d7d6066a317f92
d42d17888534fee9daf844260de901c3b18b49ccb2a5f81f0f4639f2e2cfa1ce1d7c791cef6f48
5d10df989aac02b1e9afd1094603f5307133f5f59ce105a5910700f98fea5a5fcf8f5cf4c797bd
79d440cc4f9161f5cc61e0e8f06592050cd1f0f0fd066bd1d6335710fdf8159b75281ee1082bff
1da2fc0b631bd346ac""".replace("\n", "")
                ),
            ],
            "certInfo": bytes.fromhex(
                """ff54434780170022000b68cec627cc6411099a1f80
9fde4379f649aa170c7072d1adf230de439efc80810014f7c8b0cdeb31328648130a19733d6fff
16e76e1300000003ef605603446ed8c56aa7608d01a6ea5651ee67a8a20022000bdf681917e185
29c61e1b85a1e7952f3201eb59c609ed5d8e217e5de76b228bbd0022000b0a10d216b0c3ab82bf
dc1f0a016ab9493384c7aee1937ee8800f76b30c9b71a7""".replace("\n", "")
            ),
            "pubArea": bytes.fromhex(
                """0001000b0006047200209dffcbf36c383ae699fb986
8dc6dcb89d7153884be2803922c124158bfad22ae001000100800000000000100c706586c7f46c
dffede0ee0c5ebc8b7a08b36555c8091669e9ef2cb4fd858134a01e9522d3ef924069aeeec2271
823fe9879b5079eb3123be2eb39a7e954f8b83b5ebefefda25aed01bd19eab6db1962a3713985b
7a2dd1aa7770b5c1567fb0d18521e14abebbccc16832ef10bb05dcc818bbb70c91c224475928ad
a6f6181ed64f1cfb40db5e01687454cfacafa8318bdc6a677550baa6e24f8af864fa5324e9d930
a97cdeb1995b476f21a017b33ab7fe4139f2524c784fcb04cf5241c89f0c145eb23da914ad1722
d47a843692a0b2a567d94dd808c13678a51c5a0583dc042dcbba1b9ceff12b159d0539248b0994
ee18128ed50dd7a855e54d2459db005""".replace("\n", "")
            ),
        }
        auth_data = AuthenticatorData(
            bytes.fromhex(
                "54ce651ed715b4aaa755eecebd4ea0950815b334bd07d109893e963018cddbd9450000000008987058cadc4b81b6e130de50dcbe9600206053b7b599d16fb3fb11ea17a344850ebd0d18183a5b7ca6dfbd20c63cdb462aa401030339010020590100c706586c7f46cdffede0ee0c5ebc8b7a08b36555c8091669e9ef2cb4fd858134a01e9522d3ef924069aeeec2271823fe9879b5079eb3123be2eb39a7e954f8b83b5ebefefda25aed01bd19eab6db1962a3713985b7a2dd1aa7770b5c1567fb0d18521e14abebbccc16832ef10bb05dcc818bbb70c91c224475928ada6f6181ed64f1cfb40db5e01687454cfacafa8318bdc6a677550baa6e24f8af864fa5324e9d930a97cdeb1995b476f21a017b33ab7fe4139f2524c784fcb04cf5241c89f0c145eb23da914ad1722d47a843692a0b2a567d94dd808c13678a51c5a0583dc042dcbba1b9ceff12b159d0539248b0994ee18128ed50dd7a855e54d2459db0052143010001"  # noqa
            )
        )
        client_param = bytes.fromhex(
            "057a0ecbe7e3e99e8926941614f6af078c802b110be89eb221d69be2e17a1ba4"
        )

        try:
            res = attestation.verify(statement, auth_data, client_param)
        except UnsupportedAlgorithm as e:
            if e._reason == _Reasons.UNSUPPORTED_HASH:
                self.skipTest(
                    "SHA1 signature verification not supported on this machine"
                )
            else:
                raise e

        self.assertEqual(res.attestation_type, AttestationType.ATT_CA)
        verify_x509_chain(res.trust_path)

    def test_fido_u2f_attestation(self):
        attestation = Attestation.for_type("fido-u2f")()
        self.assertIsInstance(attestation, FidoU2FAttestation)

        statement = {
            "sig": bytes.fromhex(
                "30450220324779C68F3380288A1197B6095F7A6EB9B1B1C127F66AE12A99FE8532EC23B9022100E39516AC4D61EE64044D50B415A6A4D4D84BA6D895CB5AB7A1AA7D081DE341FA"  # noqa E501
            ),
            "x5c": [
                bytes.fromhex(
                    "3082024A30820132A0030201020204046C8822300D06092A864886F70D01010B0500302E312C302A0603550403132359756269636F2055324620526F6F742043412053657269616C203435373230303633313020170D3134303830313030303030305A180F32303530303930343030303030305A302C312A302806035504030C2159756269636F205532462045452053657269616C203234393138323332343737303059301306072A8648CE3D020106082A8648CE3D030107034200043CCAB92CCB97287EE8E639437E21FCD6B6F165B2D5A3F3DB131D31C16B742BB476D8D1E99080EB546C9BBDF556E6210FD42785899E78CC589EBE310F6CDB9FF4A33B3039302206092B0601040182C40A020415312E332E362E312E342E312E34313438322E312E323013060B2B0601040182E51C020101040403020430300D06092A864886F70D01010B050003820101009F9B052248BC4CF42CC5991FCAABAC9B651BBE5BDCDC8EF0AD2C1C1FFB36D18715D42E78B249224F92C7E6E7A05C49F0E7E4C881BF2E94F45E4A21833D7456851D0F6C145A29540C874F3092C934B43D222B8962C0F410CEF1DB75892AF116B44A96F5D35ADEA3822FC7146F6004385BCB69B65C99E7EB6919786703C0D8CD41E8F75CCA44AA8AB725AD8E799FF3A8696A6F1B2656E631B1E40183C08FDA53FA4A8F85A05693944AE179A1339D002D15CABD810090EC722EF5DEF9965A371D415D624B68A2707CAD97BCDD1785AF97E258F33DF56A031AA0356D8E8D5EBCADC74E071636C6B110ACE5CC9B90DFEACAE640FF1BB0F1FE5DB4EFF7A95F060733F5"  # noqa E501
                )
            ],
        }
        auth_data = AuthenticatorData(
            bytes.fromhex(
                "1194228DA8FDBDEEFD261BD7B6595CFD70A50D70C6407BCF013DE96D4EFB17DE41000000000000000000000000000000000000000000403EBD89BF77EC509755EE9C2635EFAAAC7B2B9C5CEF1736C3717DA48534C8C6B654D7FF945F50B5CC4E78055BDD396B64F78DA2C5F96200CCD415CD08FE420038A5010203262001215820E87625896EE4E46DC032766E8087962F36DF9DFE8B567F3763015B1990A60E1422582027DE612D66418BDA1950581EBC5C8C1DAD710CB14C22F8C97045F4612FB20C91"  # noqa E501
            )
        )
        client_param = bytes.fromhex(
            "687134968222EC17202E42505F8ED2B16AE22F16BB05B88C25DB9E602645F141"
        )

        res = attestation.verify(statement, auth_data, client_param)
        self.assertEqual(res.attestation_type, AttestationType.BASIC)
        self.assertEqual(len(res.trust_path), 1)

        statement["sig"] = b"a" * len(statement["sig"])
        with self.assertRaises(InvalidSignature):
            attestation.verify(statement, auth_data, client_param)

    def test_packed_attestation(self):
        attestation = Attestation.for_type("packed")()
        self.assertIsInstance(attestation, PackedAttestation)

        statement = {
            "alg": -7,
            "sig": bytes.fromhex(
                "304502200D15DAF337D727AB4719B4027114A2AC43CD565D394CED62C3D9D1D90825F0B3022100989615E7394C87F4AD91F8FDAE86F7A3326DF332B3633DB088AAC76BFFB9A46B"  # noqa E501
            ),
            "x5c": [
                bytes.fromhex(
                    "308202B73082019FA00302010202041D31330D300D06092A864886F70D01010B0500302A3128302606035504030C1F59756269636F2050726576696577204649444F204174746573746174696F6E301E170D3138303332383036333932345A170D3139303332383036333932345A306E310B300906035504061302534531123010060355040A0C0959756269636F20414231223020060355040B0C1941757468656E74696361746F72204174746573746174696F6E3127302506035504030C1E59756269636F205532462045452053657269616C203438393736333539373059301306072A8648CE3D020106082A8648CE3D030107034200047D71E8367CAFD0EA6CF0D61E4C6A416BA5BB6D8FAD52DB2389AD07969F0F463BFDDDDDC29D39D3199163EE49575A3336C04B3309D607F6160C81E023373E0197A36C306A302206092B0601040182C40A020415312E332E362E312E342E312E34313438322E312E323013060B2B0601040182E51C0201010404030204303021060B2B0601040182E51C01010404120410F8A011F38C0A4D15800617111F9EDC7D300C0603551D130101FF04023000300D06092A864886F70D01010B050003820101009B904CEADBE1F1985486FEAD02BAEAA77E5AB4E6E52B7E6A2666A4DC06E241578169193B63DADEC5B2B78605A128B2E03F7FE2A98EAEB4219F52220995F400CE15D630CF0598BA662D7162459F1AD1FC623067376D4E4091BE65AC1A33D8561B9996C0529EC1816D1710786384D5E8783AA1F7474CB99FE8F5A63A79FF454380361C299D67CB5CC7C79F0D8C09F8849B0500F6D625408C77CBBC26DDEE11CB581BEB7947137AD4F05AAF38BD98DA10042DDCAC277604A395A5B3EAA88A5C8BB27AB59C8127D59D6BBBA5F11506BF7B75FDA7561A0837C46F025FD54DCF1014FC8D17C859507AC57D4B1DEA99485DF0BA8F34D00103C3EEF2EF3BBFEC7A6613DE"  # noqa E501
                )
            ],
        }
        auth_data = AuthenticatorData(
            bytes.fromhex(
                "0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE124100000003F8A011F38C0A4D15800617111F9EDC7D004060A386206A3AACECBDBB22D601853D955FDC5D11ADFBD1AA6A950D966B348C7663D40173714A9F987DF6461BEADFB9CD6419FFDFE4D4CF2EEC1AA605A4F59BDAA50102032620012158200EDB27580389494D74D2373B8F8C2E8B76FA135946D4F30D0E187E120B423349225820E03400D189E85A55DE9AB0F538ED60736EB750F5F0306A80060FE1B13010560D"  # noqa E501
            )
        )
        client_param = bytes.fromhex(
            "985B6187D042FB1258892ED637CEC88617DDF5F6632351A545617AA2B75261BF"
        )

        res = attestation.verify(statement, auth_data, client_param)
        self.assertEqual(res.attestation_type, AttestationType.BASIC)
        self.assertEqual(len(res.trust_path), 1)

        statement["sig"] = b"a" * len(statement["sig"])
        with self.assertRaises(InvalidSignature):
            attestation.verify(statement, auth_data, client_param)

    def test_android_safetynet_attestation(self):
        attestation = Attestation.for_type("android-safetynet")()
        self.assertIsInstance(attestation, AndroidSafetynetAttestation)

        statement = {
            "ver": "14574037",
            "response": b"eyJhbGciOiJSUzI1NiIsIng1YyI6WyJNSUlGa2pDQ0JIcWdBd0lCQWdJUVJYcm9OMFpPZFJrQkFBQUFBQVB1bnpBTkJna3Foa2lHOXcwQkFRc0ZBREJDTVFzd0NRWURWUVFHRXdKVlV6RWVNQndHQTFVRUNoTVZSMjl2WjJ4bElGUnlkWE4wSUZObGNuWnBZMlZ6TVJNd0VRWURWUVFERXdwSFZGTWdRMEVnTVU4eE1CNFhEVEU0TVRBeE1EQTNNVGswTlZvWERURTVNVEF3T1RBM01UazBOVm93YkRFTE1Ba0dBMVVFQmhNQ1ZWTXhFekFSQmdOVkJBZ1RDa05oYkdsbWIzSnVhV0V4RmpBVUJnTlZCQWNURFUxdmRXNTBZV2x1SUZacFpYY3hFekFSQmdOVkJBb1RDa2R2YjJkc1pTQk1URU14R3pBWkJnTlZCQU1URW1GMGRHVnpkQzVoYm1SeWIybGtMbU52YlRDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTmpYa3owZUsxU0U0bSsvRzV3T28rWEdTRUNycWRuODhzQ3BSN2ZzMTRmSzBSaDNaQ1laTEZIcUJrNkFtWlZ3Mks5RkcwTzlyUlBlUURJVlJ5RTMwUXVuUzl1Z0hDNGVnOW92dk9tK1FkWjJwOTNYaHp1blFFaFVXWEN4QURJRUdKSzNTMmFBZnplOTlQTFMyOWhMY1F1WVhIRGFDN09acU5ub3NpT0dpZnM4djFqaTZIL3hobHRDWmUybEorN0d1dHpleEtweHZwRS90WlNmYlk5MDVxU2xCaDlmcGowMTVjam5RRmtVc0FVd21LVkFVdWVVejR0S2NGSzRwZXZOTGF4RUFsK09raWxNdElZRGFjRDVuZWw0eEppeXM0MTNoYWdxVzBXaGg1RlAzOWhHazlFL0J3UVRqYXpTeEdkdlgwbTZ4RlloaC8yVk15WmpUNEt6UEpFQ0F3RUFBYU9DQWxnd2dnSlVNQTRHQTFVZER3RUIvd1FFQXdJRm9EQVRCZ05WSFNVRUREQUtCZ2dyQmdFRkJRY0RBVEFNQmdOVkhSTUJBZjhFQWpBQU1CMEdBMVVkRGdRV0JCUXFCUXdHV29KQmExb1RLcXVwbzRXNnhUNmoyREFmQmdOVkhTTUVHREFXZ0JTWTBmaHVFT3ZQbSt4Z254aVFHNkRyZlFuOUt6QmtCZ2dyQmdFRkJRY0JBUVJZTUZZd0p3WUlLd1lCQlFVSE1BR0dHMmgwZEhBNkx5OXZZM053TG5CcmFTNW5iMjluTDJkMGN6RnZNVEFyQmdnckJnRUZCUWN3QW9ZZmFIUjBjRG92TDNCcmFTNW5iMjluTDJkemNqSXZSMVJUTVU4eExtTnlkREFkQmdOVkhSRUVGakFVZ2hKaGRIUmxjM1F1WVc1a2NtOXBaQzVqYjIwd0lRWURWUjBnQkJvd0dEQUlCZ1puZ1F3QkFnSXdEQVlLS3dZQkJBSFdlUUlGQXpBdkJnTlZIUjhFS0RBbU1DU2dJcUFnaGg1b2RIUndPaTh2WTNKc0xuQnJhUzVuYjI5bkwwZFVVekZQTVM1amNtd3dnZ0VFQmdvckJnRUVBZFo1QWdRQ0JJSDFCSUh5QVBBQWR3Q2t1UW1RdEJoWUZJZTdFNkxNWjNBS1BEV1lCUGtiMzdqamQ4ME95QTNjRUFBQUFXWmREM1BMQUFBRUF3QklNRVlDSVFDU1pDV2VMSnZzaVZXNkNnK2dqLzl3WVRKUnp1NEhpcWU0ZVk0Yy9teXpqZ0loQUxTYmkvVGh6Y3pxdGlqM2RrM3ZiTGNJVzNMbDJCMG83NUdRZGhNaWdiQmdBSFVBVmhRR21pL1h3dXpUOWVHOVJMSSt4MFoydWJ5WkVWekE3NVNZVmRhSjBOMEFBQUZtWFE5ejVBQUFCQU1BUmpCRUFpQmNDd0E5ajdOVEdYUDI3OHo0aHIvdUNIaUFGTHlvQ3EySzAreUxSd0pVYmdJZ2Y4Z0hqdnB3Mm1CMUVTanEyT2YzQTBBRUF3Q2tuQ2FFS0ZVeVo3Zi9RdEl3RFFZSktvWklodmNOQVFFTEJRQURnZ0VCQUk5blRmUktJV2d0bFdsM3dCTDU1RVRWNmthenNwaFcxeUFjNUR1bTZYTzQxa1p6d0o2MXdKbWRSUlQvVXNDSXkxS0V0MmMwRWpnbG5KQ0YyZWF3Y0VXbExRWTJYUEx5RmprV1FOYlNoQjFpNFcyTlJHelBodDNtMWI0OWhic3R1WE02dFg1Q3lFSG5UaDhCb200L1dsRmloemhnbjgxRGxkb2d6L0syVXdNNlM2Q0IvU0V4a2lWZnYremJKMHJqdmc5NEFsZGpVZlV3a0k5Vk5NakVQNWU4eWRCM29MbDZnbHBDZUY1ZGdmU1g0VTl4MzVvai9JSWQzVUUvZFBwYi9xZ0d2c2tmZGV6dG1VdGUvS1Ntcml3Y2dVV1dlWGZUYkkzenNpa3daYmtwbVJZS21qUG1odjRybGl6R0NHdDhQbjhwcThNMktEZi9QM2tWb3QzZTE4UT0iLCJNSUlFU2pDQ0F6S2dBd0lCQWdJTkFlTzBtcUdOaXFtQkpXbFF1REFOQmdrcWhraUc5dzBCQVFzRkFEQk1NU0F3SGdZRFZRUUxFeGRIYkc5aVlXeFRhV2R1SUZKdmIzUWdRMEVnTFNCU01qRVRNQkVHQTFVRUNoTUtSMnh2WW1Gc1UybG5iakVUTUJFR0ExVUVBeE1LUjJ4dlltRnNVMmxuYmpBZUZ3MHhOekEyTVRVd01EQXdOREphRncweU1URXlNVFV3TURBd05ESmFNRUl4Q3pBSkJnTlZCQVlUQWxWVE1SNHdIQVlEVlFRS0V4VkhiMjluYkdVZ1ZISjFjM1FnVTJWeWRtbGpaWE14RXpBUkJnTlZCQU1UQ2tkVVV5QkRRU0F4VHpFd2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURRR005RjFJdk4wNXprUU85K3ROMXBJUnZKenp5T1RIVzVEekVaaEQyZVBDbnZVQTBRazI4RmdJQ2ZLcUM5RWtzQzRUMmZXQllrL2pDZkMzUjNWWk1kUy9kTjRaS0NFUFpSckF6RHNpS1VEelJybUJCSjV3dWRnem5kSU1ZY0xlL1JHR0ZsNXlPRElLZ2pFdi9TSkgvVUwrZEVhbHROMTFCbXNLK2VRbU1GKytBY3hHTmhyNTlxTS85aWw3MUkyZE44RkdmY2Rkd3VhZWo0YlhocDBMY1FCYmp4TWNJN0pQMGFNM1Q0SStEc2F4bUtGc2JqemFUTkM5dXpwRmxnT0lnN3JSMjV4b3luVXh2OHZObWtxN3pkUEdIWGt4V1k3b0c5aitKa1J5QkFCazdYckpmb3VjQlpFcUZKSlNQazdYQTBMS1cwWTN6NW96MkQwYzF0Skt3SEFnTUJBQUdqZ2dFek1JSUJMekFPQmdOVkhROEJBZjhFQkFNQ0FZWXdIUVlEVlIwbEJCWXdGQVlJS3dZQkJRVUhBd0VHQ0NzR0FRVUZCd01DTUJJR0ExVWRFd0VCL3dRSU1BWUJBZjhDQVFBd0hRWURWUjBPQkJZRUZKalIrRzRRNjgrYjdHQ2ZHSkFib090OUNmMHJNQjhHQTFVZEl3UVlNQmFBRkp2aUIxZG5IQjdBYWdiZVdiU2FMZC9jR1lZdU1EVUdDQ3NHQVFVRkJ3RUJCQ2t3SnpBbEJnZ3JCZ0VGQlFjd0FZWVphSFIwY0RvdkwyOWpjM0F1Y0d0cExtZHZiMmN2WjNOeU1qQXlCZ05WSFI4RUt6QXBNQ2VnSmFBamhpRm9kSFJ3T2k4dlkzSnNMbkJyYVM1bmIyOW5MMmR6Y2pJdlozTnlNaTVqY213d1B3WURWUjBnQkRnd05qQTBCZ1puZ1F3QkFnSXdLakFvQmdnckJnRUZCUWNDQVJZY2FIUjBjSE02THk5d2Eya3VaMjl2Wnk5eVpYQnZjMmwwYjNKNUx6QU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUFHb0ErTm5uNzh5NnBSamQ5WGxRV05hN0hUZ2laL3IzUk5Ha21VbVlIUFFxNlNjdGk5UEVhanZ3UlQyaVdUSFFyMDJmZXNxT3FCWTJFVFV3Z1pRK2xsdG9ORnZoc085dHZCQ09JYXpwc3dXQzlhSjl4anU0dFdEUUg4TlZVNllaWi9YdGVEU0dVOVl6SnFQalk4cTNNRHhyem1xZXBCQ2Y1bzhtdy93SjRhMkc2eHpVcjZGYjZUOE1jRE8yMlBMUkw2dTNNNFR6czNBMk0xajZieWtKWWk4d1dJUmRBdktMV1p1L2F4QlZielltcW13a201ekxTRFc1bklBSmJFTENRQ1p3TUg1NnQyRHZxb2Z4czZCQmNDRklaVVNweHU2eDZ0ZDBWN1N2SkNDb3NpclNtSWF0ai85ZFNTVkRRaWJldDhxLzdVSzR2NFpVTjgwYXRuWnoxeWc9PSJdfQ.eyJub25jZSI6InpiNVE5NFVPaHFOWnRVUWEraWY0NnF1UDRwZWZQN2JnQWRpQ3hraDFZRGs9IiwidGltZXN0YW1wTXMiOjE1NDM0ODI1Njg4NTgsImFwa1BhY2thZ2VOYW1lIjoiY29tLmdvb2dsZS5hbmRyb2lkLmdtcyIsImFwa0RpZ2VzdFNoYTI1NiI6InIxYzZiTkJmQ0hjZHcvZWpKSE1NWjhoakIrU0xXa1BSM0lreTZjV1dhNE09IiwiY3RzUHJvZmlsZU1hdGNoIjp0cnVlLCJhcGtDZXJ0aWZpY2F0ZURpZ2VzdFNoYTI1NiI6WyI4UDFzVzBFUEpjc2x3N1V6UnNpWEw2NHcrTzUwRWQrUkJJQ3RheTFnMjRNPSJdLCJiYXNpY0ludGVncml0eSI6dHJ1ZX0.Lq9WpOJ_GilocvPCTbIN2K5FtppXW2fTQzCW2pvb1Bo5qOZnJ0oOYBUqMgxx-zghlluSkkIIfPTvYl2zZUQsY-SNlBx7JASqDbksMyRsdU9r1Jn8D2zEtipFgjmZUkozi7AngnHoA5d0Yp-NF6slmr_FLMpAOnLZY9lREw8Cxnmso3Ph7zYUu7O5SxaRGwj8eMKydYJYHa23h2C8acuQKgSWL2YlG9T-oKT0CJ8jOSrKnHr39eMo7PFX0464diUvXUsv_M9kRIIQqCP0LzilGMdJVUrvFU7kg8csnFP6KMDfY70RGZ5ey3eNqs_D5-pjPfC4XPsPsksmy_wf-3UOmw",  # noqa E501
        }

        auth_data = AuthenticatorData(
            bytes.fromhex(
                "720c20fde835785e0f5ebcad8ef6a7bd88804a91612a2e820e0059b8d5358797450000000000000000000000000000000000000000004101c8fd9b533d6adacf6710ebcfb39f6361c4d7e8787db47dc0a75ae0e7c862198c9c83b81ef2547bb5669314095fc846af4ecac6875f7b230cac7359c76b0c20f7a5010203262001215820a28851e2d411b5b2c289da50d41cc41be88498941fc256dab500b21c8dafe8d1225820d289dd467715be06a622771a7b21e1bbe2372f8713d20dd7888a6e7ae1845ca8"  # noqa E501
            )
        )
        client_param = bytes.fromhex(
            "8422c80f3428e4e6465f76ebc8a4a93759a0a2e1fb845ee5eea7a02027408520"
        )

        res = attestation.verify(statement, auth_data, client_param)
        self.assertEqual(res.attestation_type, AttestationType.BASIC)
        verify_x509_chain(res.trust_path + [_GSR2_DER])

    def test_apple_attestation(self):
        attestation = Attestation.for_type("apple")()
        self.assertIsInstance(attestation, AppleAttestation)

        statement = {
            "alg": -7,
            "x5c": [
                bytes.fromhex(
                    "30820242308201c9a00302010202060176af5359ff300a06082a8648ce3d0403023048311c301a06035504030c134170706c6520576562417574686e204341203131133011060355040a0c0a4170706c6520496e632e3113301106035504080c0a43616c69666f726e6961301e170d3230313232383136323732345a170d3230313233313136323732345a3081913149304706035504030c4038303966626331313065613835663233613862323435616563363136333530663337646665393632313232373336653431663862646365663334366138306439311a3018060355040b0c114141412043657274696669636174696f6e31133011060355040a0c0a4170706c6520496e632e3113301106035504080c0a43616c69666f726e69613059301306072a8648ce3d020106082a8648ce3d030107034200041f46a2f159fde354598cdd47e005f1b6e7c9f00ed2a941ec7a88d222f5bcf55d6b078bc5b0be9552d85a974921f5bb848e2bbc3aecd6f71a386d2c87d6eafd37a3553053300c0603551d130101ff04023000300e0603551d0f0101ff0404030204f0303306092a864886f76364080204263024a1220420e56fb6212b3aae885294464fb10184b7fea62c48a6d78e61194e07ae6dacc132300a06082a8648ce3d040302036700306402301de8f0f238eee4f5ae80c59290b51e8c3f79397bf198e444ba162d4fccaab8558b072cf00a7c662f9058ff2a98af61ae0230149403b9643066e73a98d3659563dc4da49bf84e82b2b5bbeaf57755646fa243f36344d44b80a5798203bca023e030c7"  # noqa E501
                ),
                bytes.fromhex(
                    "30820234308201baa003020102021056255395c7a7fb40ebe228d8260853b6300a06082a8648ce3d040303304b311f301d06035504030c164170706c6520576562417574686e20526f6f7420434131133011060355040a0c0a4170706c6520496e632e3113301106035504080c0a43616c69666f726e6961301e170d3230303331383138333830315a170d3330303331333030303030305a3048311c301a06035504030c134170706c6520576562417574686e204341203131133011060355040a0c0a4170706c6520496e632e3113301106035504080c0a43616c69666f726e69613076301006072a8648ce3d020106052b8104002203620004832e872f261491810225b9f5fcd6bb6378b5f55f3fcb045bc735993475fd549044df9bfe19211765c69a1dda050b38d45083401a434fb24d112d56c3e1cfbfcb9891fec0696081bef96cbc77c88dddaf46a5aee1dd515b5afaab93be9c0b2691a366306430120603551d130101ff040830060101ff020100301f0603551d2304183016801426d764d9c578c25a67d1a7de6b12d01b63f1c6d7301d0603551d0e04160414ebae82c4ffa1ac5b51d4cf24610500be63bd7788300e0603551d0f0101ff040403020106300a06082a8648ce3d0403030368003065023100dd8b1a3481a5fad9dbb4e7657b841e144c27b75b876a4186c2b1475750337227efe554457ef648950c632e5c483e70c102302c8a6044dc201fcfe59bc34d2930c1487851d960ed6a75f1eb4acabe38cd25b897d0c805bef0c7f78b07a571c6e80e07"  # noqa E501
                ),
            ],
        }

        auth_data = AuthenticatorData(
            bytes.fromhex(
                "c46cef82ad1b546477591d008b08759ec3e6d2ecb4f39474bfea6969925d03b7450000000000000000000000000000000000000000001473d9429f4052d84debd035eb5bb7e716e3b81863a50102032620012158201f46a2f159fde354598cdd47e005f1b6e7c9f00ed2a941ec7a88d222f5bcf55d2258206b078bc5b0be9552d85a974921f5bb848e2bbc3aecd6f71a386d2c87d6eafd37"  # noqa E501
            )
        )
        client_param = bytes.fromhex(
            "0d3ce80fabbc3adb9dd891deabb8db84603ea1fe2da8b5d4b46d6591aab342f3"
        )

        res = attestation.verify(statement, auth_data, client_param)
        self.assertEqual(res.attestation_type, AttestationType.ANON_CA)
        self.assertEqual(len(res.trust_path), 2)
        verify_x509_chain(res.trust_path)
```

## File: tests/test_cbor.py
```python
# coding=utf-8

# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

from fido2 import cbor

_TEST_VECTORS = [
    ("00", 0),
    ("01", 1),
    ("0a", 10),
    ("17", 23),
    ("1818", 24),
    ("1819", 25),
    ("1864", 100),
    ("1903e8", 1000),
    ("1a000f4240", 1000000),
    ("1b000000e8d4a51000", 1000000000000),
    ("1bffffffffffffffff", 18446744073709551615),
    # ('c249010000000000000000', 18446744073709551616),
    ("3bffffffffffffffff", -18446744073709551616),
    # ('c349010000000000000000', -18446744073709551617),
    ("20", -1),
    ("29", -10),
    ("3863", -100),
    ("3903e7", -1000),
    # ('f90000', 0.0),
    # ('f98000', -0.0),
    # ('f93c00', 1.0),
    # ('fb3ff199999999999a', 1.1),
    # ('f93e00', 1.5),
    # ('f97bff', 65504.0),
    # ('fa47c35000', 100000.0),
    # ('fa7f7fffff', 3.4028234663852886e+38),
    # ('fb7e37e43c8800759c', 1e+300),
    # ('f90001', 5.960464477539063e-08),
    # ('f90400', 6.103515625e-05),
    # ('f9c400', -4.0),
    # ('fbc010666666666666', -4.1),
    # ('f97c00', None),
    # ('f97e00', None),
    # ('f9fc00', None),
    # ('fa7f800000', None),
    # ('fa7fc00000', None),
    # ('faff800000', None),
    # ('fb7ff0000000000000', None),
    # ('fb7ff8000000000000', None),
    # ('fbfff0000000000000', None),
    ("f4", False),
    ("f5", True),
    # ('f6', None),
    # ('f7', None),
    # ('f0', None),
    # ('f818', None),
    # ('f8ff', None),
    # ('c074323031332d30332d32315432303a30343a30305a', None),
    # ('c11a514b67b0', None),
    # ('c1fb41d452d9ec200000', None),
    # ('d74401020304', None),
    # ('d818456449455446', None),
    # ('d82076687474703a2f2f7777772e6578616d706c652e636f6d', None),
    ("40", b""),
    ("4401020304", b"\1\2\3\4"),
    ("60", ""),
    ("6161", "a"),
    ("6449455446", "IETF"),
    ("62225c", '"\\'),
    ("62c3bc", "ü"),
    ("63e6b0b4", "水"),
    ("64f0908591", "𐅑"),
    ("80", []),
    ("83010203", [1, 2, 3]),
    ("8301820203820405", [1, [2, 3], [4, 5]]),
    (
        "98190102030405060708090a0b0c0d0e0f101112131415161718181819",
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ],
    ),
    ("a0", {}),
    ("a201020304", {1: 2, 3: 4}),
    ("a26161016162820203", {"a": 1, "b": [2, 3]}),
    ("826161a161626163", ["a", {"b": "c"}]),
    (
        "a56161614161626142616361436164614461656145",
        {"c": "C", "d": "D", "a": "A", "b": "B", "e": "E"},
    ),
    # ('5f42010243030405ff', None),
    # ('7f657374726561646d696e67ff', 'streaming'),
    # ('9fff', []),
    # ('9f018202039f0405ffff', [1, [2, 3], [4, 5]]),
    # ('9f01820203820405ff', [1, [2, 3], [4, 5]]),
    # ('83018202039f0405ff', [1, [2, 3], [4, 5]]),
    # ('83019f0203ff820405', [1, [2, 3], [4, 5]]),
    # ('9f0102030405060708090a0b0c0d0e0f101112131415161718181819ff', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]),  # noqa E501
    # ('bf61610161629f0203ffff', {'a': 1, 'b': [2, 3]}),
    # ('826161bf61626163ff', ['a', {'b': 'c'}]),
    # ('bf6346756ef563416d7421ff', {'Amt': -2, 'Fun': True}),
]


def cbor2hex(data):
    return cbor.encode(data).hex()


class TestCborTestVectors(unittest.TestCase):
    """
    From https://github.com/cbor/test-vectors
    Unsupported values are commented out.
    """

    def test_vectors(self):
        for data, value in _TEST_VECTORS:
            try:
                self.assertEqual(cbor.decode_from(bytes.fromhex(data)), (value, b""))
                self.assertEqual(cbor.decode(bytes.fromhex(data)), value)
                self.assertEqual(cbor2hex(value), data)
            except Exception:
                print("\nERROR in test vector, %s" % data)
                raise


class TestFidoCanonical(unittest.TestCase):
    """
    As defined in section 6 of:
    https://fidoalliance.org/specs/fido-v2.0-ps-20170927/fido-client-to-authenticator-protocol-v2.0-ps-20170927.html
    """

    def test_integers(self):
        self.assertEqual(cbor2hex(0), "00")
        self.assertEqual(cbor2hex(0), "00")
        self.assertEqual(cbor2hex(23), "17")
        self.assertEqual(cbor2hex(24), "1818")
        self.assertEqual(cbor2hex(255), "18ff")
        self.assertEqual(cbor2hex(256), "190100")
        self.assertEqual(cbor2hex(65535), "19ffff")
        self.assertEqual(cbor2hex(65536), "1a00010000")
        self.assertEqual(cbor2hex(4294967295), "1affffffff")
        self.assertEqual(cbor2hex(4294967296), "1b0000000100000000")
        self.assertEqual(cbor2hex(-1), "20")
        self.assertEqual(cbor2hex(-24), "37")
        self.assertEqual(cbor2hex(-25), "3818")

    def test_key_order(self):
        self.assertEqual(cbor2hex({"3": 0, b"2": 0, 1: 0}), "a30100413200613300")

        self.assertEqual(cbor2hex({"3": 0, b"": 0, 256: 0}), "a3190100004000613300")

        self.assertEqual(
            cbor2hex({4294967296: 0, 255: 0, 256: 0, 0: 0}),
            "a4000018ff00190100001b000000010000000000",
        )

        self.assertEqual(
            cbor2hex({b"22": 0, b"3": 0, b"111": 0}), "a3413300423232004331313100"
        )

        self.assertEqual(
            cbor2hex({b"001": 0, b"003": 0, b"002": 0}),
            "a3433030310043303032004330303300",
        )

        self.assertEqual(cbor2hex({True: 0, False: 0}), "a2f400f500")
```

## File: tests/test_client.py
```python
# coding=utf-8

# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
from unittest import mock

from fido2 import cbor
from fido2.client import ClientError, DefaultClientDataCollector, Fido2Client
from fido2.ctap import CtapError
from fido2.ctap1 import RegistrationData
from fido2.ctap2 import AttestationResponse, Info
from fido2.hid import CAPABILITY
from fido2.utils import sha256
from fido2.webauthn import (
    AttestationObject,
    CollectedClientData,
    PublicKeyCredentialCreationOptions,
)

APP_ID = "https://foo.example.com"
CLIENT_DATA_COLLECTOR = DefaultClientDataCollector(APP_ID)
REG_DATA = RegistrationData(
    bytes.fromhex(
        "0504b174bc49c7ca254b70d2e5c207cee9cf174820ebd77ea3c65508c26da51b657c1cc6b952f8621697936482da0a6d3d3826a59095daf6cd7c03e2e60385d2f6d9402a552dfdb7477ed65fd84133f86196010b2215b57da75d315b7b9e8fe2e3925a6019551bab61d16591659cbaf00b4950f7abfe6660e2e006f76868b772d70c253082013c3081e4a003020102020a47901280001155957352300a06082a8648ce3d0403023017311530130603550403130c476e756262792050696c6f74301e170d3132303831343138323933325a170d3133303831343138323933325a3031312f302d0603550403132650696c6f74476e756262792d302e342e312d34373930313238303030313135353935373335323059301306072a8648ce3d020106082a8648ce3d030107034200048d617e65c9508e64bcc5673ac82a6799da3c1446682c258c463fffdf58dfd2fa3e6c378b53d795c4a4dffb4199edd7862f23abaf0203b4b8911ba0569994e101300a06082a8648ce3d0403020347003044022060cdb6061e9c22262d1aac1d96d8c70829b2366531dda268832cb836bcd30dfa0220631b1459f09e6330055722c8d89b7f48883b9089b88d60d1d9795902b30410df304502201471899bcc3987e62e8202c9b39c33c19033f7340352dba80fcab017db9230e402210082677d673d891933ade6f617e5dbde2e247e70423fd5ad7804a6d3d3961ef871"  # noqa E501
    )
)

rp = {"id": "example.com", "name": "Example RP"}
user = {"id": b"user_id", "name": "A. User"}
challenge = b"Y2hhbGxlbmdl"
_INFO_NO_PIN = bytes.fromhex(
    "a60182665532465f5632684649444f5f325f3002826375766d6b686d61632d7365637265740350f8a011f38c0a4d15800617111f9edc7d04a462726bf5627570f564706c6174f469636c69656e7450696ef4051904b0068101"  # noqa E501
)
_MC_RESP = bytes.fromhex(
    "a301667061636b6564025900c40021f5fc0b85cd22e60623bcd7d1ca48948909249b4776eb515154e57b66ae12410000001cf8a011f38c0a4d15800617111f9edc7d0040fe3aac036d14c1e1c65518b698dd1da8f596bc33e11072813466c6bf3845691509b80fb76d59309b8d39e0a93452688f6ca3a39a76f3fc52744fb73948b15783a5010203262001215820643566c206dd00227005fa5de69320616ca268043a38f08bde2e9dc45a5cafaf225820171353b2932434703726aae579fa6542432861fe591e481ea22d63997e1a529003a363616c67266373696758483046022100cc1ef43edf07de8f208c21619c78a565ddcf4150766ad58781193be8e0a742ed022100f1ed7c7243e45b7d8e5bda6b1abf10af7391789d1ef21b70bd69fed48dba4cb163783563815901973082019330820138a003020102020900859b726cb24b4c29300a06082a8648ce3d0403023047310b300906035504061302555331143012060355040a0c0b59756269636f205465737431223020060355040b0c1941757468656e74696361746f72204174746573746174696f6e301e170d3136313230343131353530305a170d3236313230323131353530305a3047310b300906035504061302555331143012060355040a0c0b59756269636f205465737431223020060355040b0c1941757468656e74696361746f72204174746573746174696f6e3059301306072a8648ce3d020106082a8648ce3d03010703420004ad11eb0e8852e53ad5dfed86b41e6134a18ec4e1af8f221a3c7d6e636c80ea13c3d504ff2e76211bb44525b196c44cb4849979cf6f896ecd2bb860de1bf4376ba30d300b30090603551d1304023000300a06082a8648ce3d0403020349003046022100e9a39f1b03197525f7373e10ce77e78021731b94d0c03f3fda1fd22db3d030e7022100c4faec3445a820cf43129cdb00aabefd9ae2d874f9c5d343cb2f113da23723f3"  # noqa E501
)


class TestFido2Client(unittest.TestCase):
    def test_ctap1_info(self):
        dev = mock.Mock()
        dev.capabilities = 0
        client = Fido2Client(dev, CLIENT_DATA_COLLECTOR)
        self.assertEqual(client.info.versions, ["U2F_V2"])
        self.assertEqual(client.info.pin_uv_protocols, [])

    @mock.patch("fido2.client.Ctap2")
    def test_make_credential_wrong_app_id(self, PatchedCtap2):
        dev = mock.Mock()
        dev.capabilities = CAPABILITY.CBOR
        ctap2 = mock.MagicMock()
        ctap2.get_info.return_value = Info.from_dict(cbor.decode(_INFO_NO_PIN))
        PatchedCtap2.return_value = ctap2
        client = Fido2Client(dev, CLIENT_DATA_COLLECTOR)
        try:
            client.make_credential(
                PublicKeyCredentialCreationOptions(
                    rp={"id": "bar.example.com", "name": "Invalid RP"},
                    user=user,
                    challenge=challenge,
                    pub_key_cred_params=[{"type": "public-key", "alg": -7}],
                )
            )
            self.fail("make_credential did not raise error")
        except ClientError as e:
            self.assertEqual(e.code, ClientError.ERR.BAD_REQUEST)

    @mock.patch("fido2.client.Ctap2")
    def test_make_credential_existing_key(self, PatchedCtap2):
        dev = mock.Mock()
        dev.capabilities = CAPABILITY.CBOR
        ctap2 = mock.MagicMock()
        ctap2.get_info.return_value = Info.from_dict(cbor.decode(_INFO_NO_PIN))
        ctap2.info = ctap2.get_info()
        ctap2.make_credential.side_effect = CtapError(CtapError.ERR.CREDENTIAL_EXCLUDED)
        PatchedCtap2.return_value = ctap2
        client = Fido2Client(dev, CLIENT_DATA_COLLECTOR)

        try:
            client.make_credential(
                PublicKeyCredentialCreationOptions(
                    rp=rp,
                    user=user,
                    challenge=challenge,
                    pub_key_cred_params=[{"type": "public-key", "alg": -7}],
                    authenticator_selection={"userVerification": "discouraged"},
                )
            )
            self.fail("make_credential did not raise error")
        except ClientError as e:
            self.assertEqual(e.code, ClientError.ERR.DEVICE_INELIGIBLE)

        ctap2.make_credential.assert_called_once()

    @mock.patch("fido2.client.Ctap2")
    def test_make_credential_ctap2(self, PatchedCtap2):
        dev = mock.Mock()
        dev.capabilities = CAPABILITY.CBOR
        ctap2 = mock.MagicMock()
        ctap2.get_info.return_value = Info.from_dict(cbor.decode(_INFO_NO_PIN))
        ctap2.info = ctap2.get_info()
        ctap2.make_credential.return_value = AttestationResponse.from_dict(
            cbor.decode(_MC_RESP)
        )
        PatchedCtap2.return_value = ctap2
        client = Fido2Client(dev, CLIENT_DATA_COLLECTOR)

        response = client.make_credential(
            PublicKeyCredentialCreationOptions(
                rp=rp,
                user=user,
                challenge=challenge,
                pub_key_cred_params=[{"type": "public-key", "alg": -7}],
                timeout=1000,
                authenticator_selection={"userVerification": "discouraged"},
            )
        ).response

        self.assertIsInstance(response.attestation_object, AttestationObject)
        self.assertIsInstance(response.client_data, CollectedClientData)

        ctap2.make_credential.assert_called_with(
            response.client_data.hash,
            rp,
            user,
            [{"type": "public-key", "alg": -7}],
            None,
            None,
            None,
            None,
            None,
            None,
            event=mock.ANY,
            on_keepalive=mock.ANY,
        )

        self.assertEqual(response.client_data.origin, APP_ID)
        self.assertEqual(response.client_data.type, "webauthn.create")
        self.assertEqual(response.client_data.challenge, challenge)

    def test_make_credential_ctap1(self):
        dev = mock.Mock()
        dev.capabilities = 0  # No CTAP2
        client = Fido2Client(dev, CLIENT_DATA_COLLECTOR)

        ctap1_mock = mock.MagicMock()
        ctap1_mock.get_version.return_value = "U2F_V2"
        ctap1_mock.register.return_value = REG_DATA
        client._backend.ctap1 = ctap1_mock

        response = client.make_credential(
            PublicKeyCredentialCreationOptions(
                rp=rp,
                user=user,
                challenge=challenge,
                pub_key_cred_params=[{"type": "public-key", "alg": -7}],
            )
        ).response

        self.assertIsInstance(response.attestation_object, AttestationObject)
        self.assertIsInstance(response.client_data, CollectedClientData)
        client_data = response.client_data

        ctap1_mock.register.assert_called_with(
            client_data.hash, sha256(rp["id"].encode())
        )

        self.assertEqual(client_data.origin, APP_ID)
        self.assertEqual(client_data.type, "webauthn.create")
        self.assertEqual(client_data.challenge, challenge)

        self.assertEqual(response.attestation_object.fmt, "fido-u2f")
```

## File: tests/test_cose.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from __future__ import absolute_import, unicode_literals

import unittest
from binascii import a2b_hex

from fido2 import cbor, cose
from fido2.cose import ES256, ESP256, RS256, CoseKey, Ed25519, EdDSA, UnsupportedKey

_ES256_KEY = a2b_hex(
    b"A5010203262001215820A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1225820FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"  # noqa E501
)
_ESP256_KEY = _ES256_KEY[0:4] + a2b_hex("28") + _ES256_KEY[5:]
_RS256_KEY = a2b_hex(
    b"A401030339010020590100B610DCE84B65029FAE24F7BF8A1730D37BC91435642A628E691E9B030BF3F7CEC59FF91CBE82C54DE16C136FA4FA8A58939B5A950B32E03073592FEC8D8B33601C04F70E5E2D5CF7B4E805E1990EA5A86928A1B390EB9026527933ACC03E6E41DC0BE40AA5EB7B9B460743E4DD80895A758FB3F3F794E5E9B8310D3A60C28F2410D95CF6E732749A243A30475267628B456DE770BC2185BBED1D451ECB0062A3D132C0E4D842E0DDF93A444A3EE33A85C2E913156361713155F1F1DC64E8E68ED176466553BBDE669EB82810B104CB4407D32AE6316C3BD6F382EC3AE2C5FD49304986D64D92ED11C25B6C5CF1287233545A987E9A3E169F99790603DBA5C8AD2143010001"  # noqa E501
)
_EdDSA_KEY = a2b_hex(
    b"a4010103272006215820ee9b21803405d3cf45601e58b6f4c06ea93862de87d3af903c5870a5016e86f5"  # noqa E501
)
_Ed25519_KEY = _EdDSA_KEY[0:4] + a2b_hex("32") + _EdDSA_KEY[5:]


class TestCoseKey(unittest.TestCase):
    def test_ES256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_ES256_KEY))
        self.assertIsInstance(key, ES256)
        self.assertEqual(
            key,
            {
                1: 2,
                3: -7,
                -1: 1,
                -2: a2b_hex(
                    b"A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1"
                ),
                -3: a2b_hex(
                    b"FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002C"  # noqa E501
                + b"7B89F12A9088B0F5EE0EF8F6718BCCC374249C31AEEBAEB79BD0450132CD536C"
            ),
            a2b_hex(
                b"304402202B3933FE954A2D29DE691901EB732535393D4859AAA80D58B08741598109516D0220236FBE6B52326C0A6B1CFDC6BF0A35BDA92A6C2E41E40C3A1643428D820941E0"  # noqa E501
            ),
        )

    def test_ESP256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_ESP256_KEY))
        self.assertIsInstance(key, ESP256)
        self.assertEqual(
            key,
            {
                1: 2,
                3: -9,
                -1: 1,
                -2: a2b_hex(
                    b"A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1"
                ),
                -3: a2b_hex(
                    b"FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002C"  # noqa E501
                + b"7B89F12A9088B0F5EE0EF8F6718BCCC374249C31AEEBAEB79BD0450132CD536C"
            ),
            a2b_hex(
                b"304402202B3933FE954A2D29DE691901EB732535393D4859AAA80D58B08741598109516D0220236FBE6B52326C0A6B1CFDC6BF0A35BDA92A6C2E41E40C3A1643428D820941E0"  # noqa E501
            ),
        )

    def test_RS256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_RS256_KEY))
        self.assertIsInstance(key, RS256)
        self.assertEqual(
            key,
            {
                1: 3,
                3: -257,
                -1: a2b_hex(
                    b"B610DCE84B65029FAE24F7BF8A1730D37BC91435642A628E691E9B030BF3F7CEC59FF91CBE82C54DE16C136FA4FA8A58939B5A950B32E03073592FEC8D8B33601C04F70E5E2D5CF7B4E805E1990EA5A86928A1B390EB9026527933ACC03E6E41DC0BE40AA5EB7B9B460743E4DD80895A758FB3F3F794E5E9B8310D3A60C28F2410D95CF6E732749A243A30475267628B456DE770BC2185BBED1D451ECB0062A3D132C0E4D842E0DDF93A444A3EE33A85C2E913156361713155F1F1DC64E8E68ED176466553BBDE669EB82810B104CB4407D32AE6316C3BD6F382EC3AE2C5FD49304986D64D92ED11C25B6C5CF1287233545A987E9A3E169F99790603DBA5C8AD"  # noqa E501
                ),
                -2: a2b_hex(b"010001"),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002E"  # noqa E501
                + b"CC9340FD84950987BA667DBE9B2C97C7241E15E2B54869A0DD1CE2013C4064B8"
            ),
            a2b_hex(
                b"071B707D11F0E7F62861DFACA89C4E674321AD8A6E329FDD40C7D6971348FBB0514E7B2B0EFE215BAAC0365C4124A808F8180D6575B710E7C01DAE8F052D0C5A2CE82F487C656E7AD824F3D699BE389ADDDE2CBF39E87A8955E93202BAE8830AB4139A7688DFDAD849F1BB689F3852BA05BED70897553CC44704F6941FD1467AD6A46B4DAB503716D386FE7B398E78E0A5A8C4040539D2C9BFA37E4D94F96091FFD1D194DE2CA58E9124A39757F013801421E09BD261ADA31992A8B0386A80AF51A87BD0CEE8FDAB0D4651477670D4C7B245489BED30A57B83964DB79418D5A4F5F2E5ABCA274426C9F90B007A962AE15DFF7343AF9E110746E2DB9226D785C6"  # noqa E501
            ),
        )

    def test_EdDSA_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_EdDSA_KEY))
        self.assertIsInstance(key, EdDSA)
        self.assertEqual(
            key,
            {
                1: 1,
                3: -8,
                -1: 6,
                -2: a2b_hex(
                    "EE9B21803405D3CF45601E58B6F4C06EA93862DE87D3AF903C5870A5016E86F5"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"a379a6f6eeafb9a55e378c118034e2751e682fab9f2d30ab13d2125586ce1947010000000500a11a323057d1103784ddff99a354ddd42348c2f00e88d8977b916cabf92268"  # noqa E501
            ),
            a2b_hex(
                b"e8c927ef1a57c738ff4ba8d6f90e06d837a5219eee47991f96b126b0685d512520c9c2eedebe4b88ff2de2b19cb5f8686efc7c4261e9ed1cb3ac5de50869be0a"  # noqa E501
            ),
        )

    def test_Ed25519_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_Ed25519_KEY))
        self.assertIsInstance(key, Ed25519)
        self.assertEqual(
            key,
            {
                1: 1,
                3: -19,
                -1: 6,
                -2: a2b_hex(
                    "EE9B21803405D3CF45601E58B6F4C06EA93862DE87D3AF903C5870A5016E86F5"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"a379a6f6eeafb9a55e378c118034e2751e682fab9f2d30ab13d2125586ce1947010000000500a11a323057d1103784ddff99a354ddd42348c2f00e88d8977b916cabf92268"  # noqa E501
            ),
            a2b_hex(
                b"e8c927ef1a57c738ff4ba8d6f90e06d837a5219eee47991f96b126b0685d512520c9c2eedebe4b88ff2de2b19cb5f8686efc7c4261e9ed1cb3ac5de50869be0a"  # noqa E501
            ),
        )

    def test_unsupported_key(self):
        key = CoseKey.parse({1: 4711, 3: 4712, -1: b"123", -2: b"456"})
        self.assertIsInstance(key, UnsupportedKey)
        self.assertEqual(key, {1: 4711, 3: 4712, -1: b"123", -2: b"456"})

    def test_supported_algs(self):
        self.assertEqual(CoseKey.for_alg(-7), cose.ES256)
        self.assertEqual(CoseKey.for_alg(-8), cose.EdDSA)
        self.assertEqual(CoseKey.for_alg(-9), cose.ESP256)
        self.assertEqual(CoseKey.for_alg(-19), cose.Ed25519)
        self.assertEqual(CoseKey.for_alg(-35), cose.ES384)
        self.assertEqual(CoseKey.for_alg(-36), cose.ES512)
        self.assertEqual(CoseKey.for_alg(-37), cose.PS256)
        self.assertEqual(CoseKey.for_alg(-47), cose.ES256K)
        self.assertEqual(CoseKey.for_alg(-51), cose.ESP384)
        self.assertEqual(CoseKey.for_alg(-52), cose.ESP512)
        self.assertEqual(CoseKey.for_alg(-53), cose.Ed448)
        self.assertEqual(CoseKey.for_alg(-257), cose.RS256)
        self.assertEqual(CoseKey.for_alg(-65535), cose.RS1)
```

## File: tests/test_ctap1.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
from unittest import mock

from fido2.ctap1 import ApduError, Ctap1


class TestCtap1(unittest.TestCase):
    def test_send_apdu_ok(self):
        ctap = Ctap1(mock.MagicMock())
        ctap.device.call.return_value = b"response\x90\x00"

        self.assertEqual(b"response", ctap.send_apdu(1, 2, 3, 4, b"foobar"))
        ctap.device.call.assert_called_with(0x03, b"\1\2\3\4\0\0\6foobar\0\0")

    def test_send_apdu_err(self):
        ctap = Ctap1(mock.MagicMock())
        ctap.device.call.return_value = b"err\x6a\x80"

        try:
            ctap.send_apdu(1, 2, 3, 4, b"foobar")
            self.fail("send_apdu did not raise error")
        except ApduError as e:
            self.assertEqual(e.code, 0x6A80)
            self.assertEqual(e.data, b"err")
        ctap.device.call.assert_called_with(0x03, b"\1\2\3\4\0\0\6foobar\0\0")

    def test_get_version(self):
        ctap = Ctap1(mock.MagicMock())
        ctap.device.call.return_value = b"U2F_V2\x90\x00"

        self.assertEqual("U2F_V2", ctap.get_version())
        ctap.device.call.assert_called_with(0x03, b"\0\3\0\0\0\0\0\0\0")

    def test_register(self):
        ctap = Ctap1(mock.MagicMock())
        ctap.device.call.return_value = (
            bytes.fromhex(
                "0504b174bc49c7ca254b70d2e5c207cee9cf174820ebd77ea3c65508c26da51b657c1cc6b952f8621697936482da0a6d3d3826a59095daf6cd7c03e2e60385d2f6d9402a552dfdb7477ed65fd84133f86196010b2215b57da75d315b7b9e8fe2e3925a6019551bab61d16591659cbaf00b4950f7abfe6660e2e006f76868b772d70c253082013c3081e4a003020102020a47901280001155957352300a06082a8648ce3d0403023017311530130603550403130c476e756262792050696c6f74301e170d3132303831343138323933325a170d3133303831343138323933325a3031312f302d0603550403132650696c6f74476e756262792d302e342e312d34373930313238303030313135353935373335323059301306072a8648ce3d020106082a8648ce3d030107034200048d617e65c9508e64bcc5673ac82a6799da3c1446682c258c463fffdf58dfd2fa3e6c378b53d795c4a4dffb4199edd7862f23abaf0203b4b8911ba0569994e101300a06082a8648ce3d0403020347003044022060cdb6061e9c22262d1aac1d96d8c70829b2366531dda268832cb836bcd30dfa0220631b1459f09e6330055722c8d89b7f48883b9089b88d60d1d9795902b30410df304502201471899bcc3987e62e8202c9b39c33c19033f7340352dba80fcab017db9230e402210082677d673d891933ade6f617e5dbde2e247e70423fd5ad7804a6d3d3961ef871"  # noqa E501
            )
            + b"\x90\x00"
        )

        client_param = bytes.fromhex(
            "4142d21c00d94ffb9d504ada8f99b721f4b191ae4e37ca0140f696b6983cfacb"
        )
        app_param = bytes.fromhex(
            "f0e6a6a97042a4f1f1c87f5f7d44315b2d852c2df5c7991cc66241bf7072d1c4"
        )

        resp = ctap.register(client_param, app_param)
        ctap.device.call.assert_called_with(
            0x03, b"\0\1\0\0\0\0\x40" + client_param + app_param + b"\0\0"
        )
        self.assertEqual(
            resp.public_key,
            bytes.fromhex(
                "04b174bc49c7ca254b70d2e5c207cee9cf174820ebd77ea3c65508c26da51b657c1cc6b952f8621697936482da0a6d3d3826a59095daf6cd7c03e2e60385d2f6d9"  # noqa E501
            ),
        )
        self.assertEqual(
            resp.key_handle,
            bytes.fromhex(
                "2a552dfdb7477ed65fd84133f86196010b2215b57da75d315b7b9e8fe2e3925a6019551bab61d16591659cbaf00b4950f7abfe6660e2e006f76868b772d70c25"  # noqa E501
            ),
        )
        self.assertEqual(
            resp.certificate,
            bytes.fromhex(
                "3082013c3081e4a003020102020a47901280001155957352300a06082a8648ce3d0403023017311530130603550403130c476e756262792050696c6f74301e170d3132303831343138323933325a170d3133303831343138323933325a3031312f302d0603550403132650696c6f74476e756262792d302e342e312d34373930313238303030313135353935373335323059301306072a8648ce3d020106082a8648ce3d030107034200048d617e65c9508e64bcc5673ac82a6799da3c1446682c258c463fffdf58dfd2fa3e6c378b53d795c4a4dffb4199edd7862f23abaf0203b4b8911ba0569994e101300a06082a8648ce3d0403020347003044022060cdb6061e9c22262d1aac1d96d8c70829b2366531dda268832cb836bcd30dfa0220631b1459f09e6330055722c8d89b7f48883b9089b88d60d1d9795902b30410df"  # noqa E501
            ),
        )
        self.assertEqual(
            resp.signature,
            bytes.fromhex(
                "304502201471899bcc3987e62e8202c9b39c33c19033f7340352dba80fcab017db9230e402210082677d673d891933ade6f617e5dbde2e247e70423fd5ad7804a6d3d3961ef871"  # noqa E501
            ),
        )

        resp.verify(app_param, client_param)

    def test_authenticate(self):
        ctap = Ctap1(mock.MagicMock())
        ctap.device.call.return_value = (
            bytes.fromhex(
                "0100000001304402204b5f0cd17534cedd8c34ee09570ef542a353df4436030ce43d406de870b847780220267bb998fac9b7266eb60e7cb0b5eabdfd5ba9614f53c7b22272ec10047a923f"  # noqa E501
            )
            + b"\x90\x00"
        )

        client_param = bytes.fromhex(
            "ccd6ee2e47baef244d49a222db496bad0ef5b6f93aa7cc4d30c4821b3b9dbc57"
        )
        app_param = bytes.fromhex(
            "4b0be934baebb5d12d26011b69227fa5e86df94e7d94aa2949a89f2d493992ca"
        )
        key_handle = b"\3" * 64

        resp = ctap.authenticate(client_param, app_param, key_handle)
        ctap.device.call.assert_called_with(
            0x03,
            b"\0\2\3\0\0\0\x81"
            + client_param
            + app_param
            + b"\x40"
            + key_handle
            + b"\0\0",
        )

        self.assertEqual(resp.user_presence, 1)
        self.assertEqual(resp.counter, 1)
        self.assertEqual(
            resp.signature,
            bytes.fromhex(
                "304402204b5f0cd17534cedd8c34ee09570ef542a353df4436030ce43d406de870b847780220267bb998fac9b7266eb60e7cb0b5eabdfd5ba9614f53c7b22272ec10047a923f"  # noqa E501
            ),
        )

        public_key = bytes.fromhex(
            "04d368f1b665bade3c33a20f1e429c7750d5033660c019119d29aa4ba7abc04aa7c80a46bbe11ca8cb5674d74f31f8a903f6bad105fb6ab74aefef4db8b0025e1d"  # noqa E501
        )
        resp.verify(app_param, client_param, public_key)

        key_handle = b"\4" * 8
        ctap.authenticate(client_param, app_param, key_handle)
        ctap.device.call.assert_called_with(
            0x03,
            b"\0\2\3\0\0\0\x49"
            + client_param
            + app_param
            + b"\x08"
            + key_handle
            + b"\0\0",
        )

        ctap.authenticate(client_param, app_param, key_handle, True)
        ctap.device.call.assert_called_with(
            0x03,
            b"\0\2\7\0\0\0\x49"
            + client_param
            + app_param
            + b"\x08"
            + key_handle
            + b"\0\0",
        )
```

## File: tests/test_ctap2.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
from unittest import mock

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

from fido2 import cbor
from fido2.attestation import Attestation
from fido2.ctap1 import RegistrationData
from fido2.ctap2 import (
    AssertionResponse,
    AttestationResponse,
    ClientPin,
    Ctap2,
    Info,
    PinProtocolV1,
)
from fido2.webauthn import AttestationObject, AttestedCredentialData, AuthenticatorData

_AAGUID = bytes.fromhex("F8A011F38C0A4D15800617111F9EDC7D")
_INFO = bytes.fromhex(
    "a60182665532465f5632684649444f5f325f3002826375766d6b686d61632d7365637265740350f8a011f38c0a4d15800617111f9edc7d04a462726bf5627570f564706c6174f469636c69656e7450696ef4051904b0068101"  # noqa E501
)
_INFO_EXTRA_KEY = bytes.fromhex(
    "A70182665532465F5632684649444F5F325F3002826375766D6B686D61632D7365637265740350F8A011F38C0A4D15800617111F9EDC7D04A462726BF5627570F564706C6174F469636C69656E7450696EF4051904B006810118631904D2"  # noqa E501
)


class TestInfo(unittest.TestCase):
    def test_parse_bytes(self):
        info = Info.from_dict(cbor.decode(_INFO))

        self.assertEqual(info.versions, ["U2F_V2", "FIDO_2_0"])
        self.assertEqual(info.extensions, ["uvm", "hmac-secret"])
        self.assertEqual(info.aaguid, _AAGUID)
        self.assertEqual(
            info.options, {"rk": True, "up": True, "plat": False, "clientPin": False}
        )
        self.assertEqual(info.max_msg_size, 1200)
        self.assertEqual(info.pin_uv_protocols, [1])
        assert info[0x01] == ["U2F_V2", "FIDO_2_0"]
        assert info[0x02] == ["uvm", "hmac-secret"]
        assert info[0x03] == _AAGUID
        assert info[0x04] == {
            "clientPin": False,
            "plat": False,
            "rk": True,
            "up": True,
        }
        assert info[0x05] == 1200
        assert info[0x06] == [1]

    def test_info_with_extra_field(self):
        info = Info.from_dict(cbor.decode(_INFO_EXTRA_KEY))
        self.assertEqual(info.versions, ["U2F_V2", "FIDO_2_0"])


_ATT_CRED_DATA = bytes.fromhex(
    "f8a011f38c0a4d15800617111f9edc7d0040fe3aac036d14c1e1c65518b698dd1da8f596bc33e11072813466c6bf3845691509b80fb76d59309b8d39e0a93452688f6ca3a39a76f3fc52744fb73948b15783a5010203262001215820643566c206dd00227005fa5de69320616ca268043a38f08bde2e9dc45a5cafaf225820171353b2932434703726aae579fa6542432861fe591e481ea22d63997e1a5290"  # noqa E501
)
_CRED_ID = bytes.fromhex(
    "fe3aac036d14c1e1c65518b698dd1da8f596bc33e11072813466c6bf3845691509b80fb76d59309b8d39e0a93452688f6ca3a39a76f3fc52744fb73948b15783"  # noqa E501
)
_PUB_KEY = {
    1: 2,
    3: -7,
    -1: 1,
    -2: bytes.fromhex(
        "643566c206dd00227005fa5de69320616ca268043a38f08bde2e9dc45a5cafaf"
    ),
    -3: bytes.fromhex(
        "171353b2932434703726aae579fa6542432861fe591e481ea22d63997e1a5290"
    ),
}


class TestAttestedCredentialData(unittest.TestCase):
    def test_parse_bytes(self):
        data = AttestedCredentialData(_ATT_CRED_DATA)
        self.assertEqual(data.aaguid, _AAGUID)
        self.assertEqual(data.credential_id, _CRED_ID)
        self.assertEqual(data.public_key, _PUB_KEY)

    def test_create_from_args(self):
        data = AttestedCredentialData.create(_AAGUID, _CRED_ID, _PUB_KEY)
        self.assertEqual(_ATT_CRED_DATA, data)


_AUTH_DATA_MC = bytes.fromhex(
    "0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12410000001CF8A011F38C0A4D15800617111F9EDC7D0040FE3AAC036D14C1E1C65518B698DD1DA8F596BC33E11072813466C6BF3845691509B80FB76D59309B8D39E0A93452688F6CA3A39A76F3FC52744FB73948B15783A5010203262001215820643566C206DD00227005FA5DE69320616CA268043A38F08BDE2E9DC45A5CAFAF225820171353B2932434703726AAE579FA6542432861FE591E481EA22D63997E1A5290"  # noqa E501
)
_AUTH_DATA_GA = bytes.fromhex(
    "0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000001D"
)
_RP_ID_HASH = bytes.fromhex(
    "0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12"
)


class TestAuthenticatorData(unittest.TestCase):
    def test_parse_bytes_make_credential(self):
        data = AuthenticatorData(_AUTH_DATA_MC)
        self.assertEqual(data.rp_id_hash, _RP_ID_HASH)
        self.assertEqual(data.flags, 0x41)
        self.assertEqual(data.counter, 28)
        self.assertEqual(data.credential_data, _ATT_CRED_DATA)
        self.assertIsNone(data.extensions)

    def test_parse_bytes_get_assertion(self):
        data = AuthenticatorData(_AUTH_DATA_GA)
        self.assertEqual(data.rp_id_hash, _RP_ID_HASH)
        self.assertEqual(data.flags, 0x01)
        self.assertEqual(data.counter, 29)
        self.assertIsNone(data.credential_data)
        self.assertIsNone(data.extensions)


_MC_RESP = bytes.fromhex(
    "a301667061636b65640258c40021f5fc0b85cd22e60623bcd7d1ca48948909249b4776eb515154e57b66ae12410000001cf8a011f38c0a4d15800617111f9edc7d0040fe3aac036d14c1e1c65518b698dd1da8f596bc33e11072813466c6bf3845691509b80fb76d59309b8d39e0a93452688f6ca3a39a76f3fc52744fb73948b15783a5010203262001215820643566c206dd00227005fa5de69320616ca268043a38f08bde2e9dc45a5cafaf225820171353b2932434703726aae579fa6542432861fe591e481ea22d63997e1a529003a363616c67266373696758483046022100cc1ef43edf07de8f208c21619c78a565ddcf4150766ad58781193be8e0a742ed022100f1ed7c7243e45b7d8e5bda6b1abf10af7391789d1ef21b70bd69fed48dba4cb163783563815901973082019330820138a003020102020900859b726cb24b4c29300a06082a8648ce3d0403023047310b300906035504061302555331143012060355040a0c0b59756269636f205465737431223020060355040b0c1941757468656e74696361746f72204174746573746174696f6e301e170d3136313230343131353530305a170d3236313230323131353530305a3047310b300906035504061302555331143012060355040a0c0b59756269636f205465737431223020060355040b0c1941757468656e74696361746f72204174746573746174696f6e3059301306072a8648ce3d020106082a8648ce3d03010703420004ad11eb0e8852e53ad5dfed86b41e6134a18ec4e1af8f221a3c7d6e636c80ea13c3d504ff2e76211bb44525b196c44cb4849979cf6f896ecd2bb860de1bf4376ba30d300b30090603551d1304023000300a06082a8648ce3d0403020349003046022100e9a39f1b03197525f7373e10ce77e78021731b94d0c03f3fda1fd22db3d030e7022100c4faec3445a820cf43129cdb00aabefd9ae2d874f9c5d343cb2f113da23723f3"  # noqa E501
)
_GA_RESP = bytes.fromhex(
    "a301a26269645840fe3aac036d14c1e1c65518b698dd1da8f596bc33e11072813466c6bf3845691509b80fb76d59309b8d39e0a93452688f6ca3a39a76f3fc52744fb73948b1578364747970656a7075626c69632d6b65790258250021f5fc0b85cd22e60623bcd7d1ca48948909249b4776eb515154e57b66ae12010000001d035846304402206765cbf6e871d3af7f01ae96f06b13c90f26f54b905c5166a2c791274fc2397102200b143893586cc799fba4da83b119eaea1bd80ac3ce88fcedb3efbd596a1f4f63"  # noqa E501
)
_CRED_ID = bytes.fromhex(
    "FE3AAC036D14C1E1C65518B698DD1DA8F596BC33E11072813466C6BF3845691509B80FB76D59309B8D39E0A93452688F6CA3A39A76F3FC52744FB73948B15783"  # noqa E501
)
_CRED = {"type": "public-key", "id": _CRED_ID}
_SIGNATURE = bytes.fromhex(
    "304402206765CBF6E871D3AF7F01AE96F06B13C90F26F54B905C5166A2C791274FC2397102200B143893586CC799FBA4DA83B119EAEA1BD80AC3CE88FCEDB3EFBD596A1F4F63"  # noqa E501
)


class TestAttestationObject(unittest.TestCase):
    def test_fido_u2f_attestation(self):
        att = AttestationObject.from_ctap1(
            bytes.fromhex(
                "1194228DA8FDBDEEFD261BD7B6595CFD70A50D70C6407BCF013DE96D4EFB17DE"
            ),
            RegistrationData(
                bytes.fromhex(
                    "0504E87625896EE4E46DC032766E8087962F36DF9DFE8B567F3763015B1990A60E1427DE612D66418BDA1950581EBC5C8C1DAD710CB14C22F8C97045F4612FB20C91403EBD89BF77EC509755EE9C2635EFAAAC7B2B9C5CEF1736C3717DA48534C8C6B654D7FF945F50B5CC4E78055BDD396B64F78DA2C5F96200CCD415CD08FE4200383082024A30820132A0030201020204046C8822300D06092A864886F70D01010B0500302E312C302A0603550403132359756269636F2055324620526F6F742043412053657269616C203435373230303633313020170D3134303830313030303030305A180F32303530303930343030303030305A302C312A302806035504030C2159756269636F205532462045452053657269616C203234393138323332343737303059301306072A8648CE3D020106082A8648CE3D030107034200043CCAB92CCB97287EE8E639437E21FCD6B6F165B2D5A3F3DB131D31C16B742BB476D8D1E99080EB546C9BBDF556E6210FD42785899E78CC589EBE310F6CDB9FF4A33B3039302206092B0601040182C40A020415312E332E362E312E342E312E34313438322E312E323013060B2B0601040182E51C020101040403020430300D06092A864886F70D01010B050003820101009F9B052248BC4CF42CC5991FCAABAC9B651BBE5BDCDC8EF0AD2C1C1FFB36D18715D42E78B249224F92C7E6E7A05C49F0E7E4C881BF2E94F45E4A21833D7456851D0F6C145A29540C874F3092C934B43D222B8962C0F410CEF1DB75892AF116B44A96F5D35ADEA3822FC7146F6004385BCB69B65C99E7EB6919786703C0D8CD41E8F75CCA44AA8AB725AD8E799FF3A8696A6F1B2656E631B1E40183C08FDA53FA4A8F85A05693944AE179A1339D002D15CABD810090EC722EF5DEF9965A371D415D624B68A2707CAD97BCDD1785AF97E258F33DF56A031AA0356D8E8D5EBCADC74E071636C6B110ACE5CC9B90DFEACAE640FF1BB0F1FE5DB4EFF7A95F060733F530450220324779C68F3380288A1197B6095F7A6EB9B1B1C127F66AE12A99FE8532EC23B9022100E39516AC4D61EE64044D50B415A6A4D4D84BA6D895CB5AB7A1AA7D081DE341FA"  # noqa E501
                )
            ),
        )
        Attestation.for_type(att.fmt)().verify(
            att.att_stmt,
            att.auth_data,
            bytes.fromhex(
                "687134968222EC17202E42505F8ED2B16AE22F16BB05B88C25DB9E602645F141"
            ),
        )

    def test_packed_attestation(self):
        att = AttestationResponse.from_dict(
            cbor.decode(
                bytes.fromhex(
                    "a301667061636b65640258c40021f5fc0b85cd22e60623bcd7d1ca48948909249b4776eb515154e57b66ae124100000003f8a011f38c0a4d15800617111f9edc7d004060a386206a3aacecbdbb22d601853d955fdc5d11adfbd1aa6a950d966b348c7663d40173714a9f987df6461beadfb9cd6419ffdfe4d4cf2eec1aa605a4f59bdaa50102032620012158200edb27580389494d74d2373b8f8c2e8b76fa135946d4f30d0e187e120b423349225820e03400d189e85a55de9ab0f538ed60736eb750f5f0306a80060fe1b13010560d03a363616c6726637369675847304502200d15daf337d727ab4719b4027114a2ac43cd565d394ced62c3d9d1d90825f0b3022100989615e7394c87f4ad91f8fdae86f7a3326df332b3633db088aac76bffb9a46b63783563815902bb308202b73082019fa00302010202041d31330d300d06092a864886f70d01010b0500302a3128302606035504030c1f59756269636f2050726576696577204649444f204174746573746174696f6e301e170d3138303332383036333932345a170d3139303332383036333932345a306e310b300906035504061302534531123010060355040a0c0959756269636f20414231223020060355040b0c1941757468656e74696361746f72204174746573746174696f6e3127302506035504030c1e59756269636f205532462045452053657269616c203438393736333539373059301306072a8648ce3d020106082a8648ce3d030107034200047d71e8367cafd0ea6cf0d61e4c6a416ba5bb6d8fad52db2389ad07969f0f463bfdddddc29d39d3199163ee49575a3336c04b3309d607f6160c81e023373e0197a36c306a302206092b0601040182c40a020415312e332e362e312e342e312e34313438322e312e323013060b2b0601040182e51c0201010404030204303021060b2b0601040182e51c01010404120410f8a011f38c0a4d15800617111f9edc7d300c0603551d130101ff04023000300d06092a864886f70d01010b050003820101009b904ceadbe1f1985486fead02baeaa77e5ab4e6e52b7e6a2666a4dc06e241578169193b63dadec5b2b78605a128b2e03f7fe2a98eaeb4219f52220995f400ce15d630cf0598ba662d7162459f1ad1fc623067376d4e4091be65ac1a33d8561b9996c0529ec1816d1710786384d5e8783aa1f7474cb99fe8f5a63a79ff454380361c299d67cb5cc7c79f0d8c09f8849b0500f6d625408c77cbbc26ddee11cb581beb7947137ad4f05aaf38bd98da10042ddcac277604a395a5b3eaa88a5c8bb27ab59c8127d59d6bbba5f11506bf7b75fda7561a0837c46f025fd54dcf1014fc8d17c859507ac57d4b1dea99485df0ba8f34d00103c3eef2ef3bbfec7a6613de"  # noqa E501
                )
            )
        )
        Attestation.for_type(att.fmt)().verify(
            att.att_stmt,
            att.auth_data,
            bytes.fromhex(
                "985B6187D042FB1258892ED637CEC88617DDF5F6632351A545617AA2B75261BF"
            ),
        )


class TestCtap2(unittest.TestCase):
    def mock_ctap(self):
        device = mock.MagicMock()
        device.call.return_value = b"\0" + _INFO
        return Ctap2(device)

    def test_send_cbor_ok(self):
        ctap = self.mock_ctap()
        ctap.device.call.return_value = b"\0" + cbor.encode({1: b"response"})

        self.assertEqual({1: b"response"}, ctap.send_cbor(2, b"foobar"))
        ctap.device.call.assert_called_with(
            0x10, b"\2" + cbor.encode(b"foobar"), mock.ANY, None
        )

    def test_get_info(self):
        ctap = self.mock_ctap()

        info = ctap.get_info()
        ctap.device.call.assert_called_with(0x10, b"\4", mock.ANY, None)
        self.assertIsInstance(info, Info)

    def test_make_credential(self):
        ctap = self.mock_ctap()
        ctap.device.call.return_value = b"\0" + _MC_RESP

        resp = ctap.make_credential(1, 2, 3, 4)
        ctap.device.call.assert_called_with(
            0x10, b"\1" + cbor.encode({1: 1, 2: 2, 3: 3, 4: 4}), mock.ANY, None
        )

        self.assertIsInstance(resp, AttestationResponse)
        self.assertEqual(resp, AttestationResponse.from_dict(cbor.decode(_MC_RESP)))
        self.assertEqual(resp.fmt, "packed")
        self.assertEqual(resp.auth_data, _AUTH_DATA_MC)
        self.assertSetEqual(set(resp.att_stmt.keys()), {"alg", "sig", "x5c"})

    def test_get_assertion(self):
        ctap = self.mock_ctap()
        ctap.device.call.return_value = b"\0" + _GA_RESP

        resp = ctap.get_assertion(1, 2)
        ctap.device.call.assert_called_with(
            0x10, b"\2" + cbor.encode({1: 1, 2: 2}), mock.ANY, None
        )

        self.assertIsInstance(resp, AssertionResponse)
        self.assertEqual(resp, AssertionResponse.from_dict(cbor.decode(_GA_RESP)))
        self.assertEqual(resp.credential, _CRED)
        self.assertEqual(resp.auth_data, _AUTH_DATA_GA)
        self.assertEqual(resp.signature, _SIGNATURE)
        self.assertIsNone(resp.user)
        self.assertIsNone(resp.number_of_credentials)


EC_PRIV = 0x7452E599FEE739D8A653F6A507343D12D382249108A651402520B72F24FE7684
EC_PUB_X = bytes.fromhex(
    "44D78D7989B97E62EA993496C9EF6E8FD58B8B00715F9A89153DDD9C4657E47F"
)
EC_PUB_Y = bytes.fromhex(
    "EC802EE7D22BD4E100F12E48537EB4E7E96ED3A47A0A3BD5F5EEAB65001664F9"
)
DEV_PUB_X = bytes.fromhex(
    "0501D5BC78DA9252560A26CB08FCC60CBE0B6D3B8E1D1FCEE514FAC0AF675168"
)
DEV_PUB_Y = bytes.fromhex(
    "D551B3ED46F665731F95B4532939C25D91DB7EB844BD96D4ABD4083785F8DF47"
)
SHARED = bytes.fromhex(
    "c42a039d548100dfba521e487debcbbb8b66bb7496f8b1862a7a395ed83e1a1c"
)
TOKEN_ENC = bytes.fromhex("7A9F98E31B77BE90F9C64D12E9635040")
TOKEN = bytes.fromhex("aff12c6dcfbf9df52f7a09211e8865cd")
PIN_HASH_ENC = bytes.fromhex("afe8327ce416da8ee3d057589c2ce1a9")


class TestClientPin(unittest.TestCase):
    @mock.patch("cryptography.hazmat.primitives.asymmetric.ec.generate_private_key")
    def test_establish_shared_secret(self, patched_generate):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        patched_generate.return_value = ec.derive_private_key(
            EC_PRIV, ec.SECP256R1(), default_backend()
        )

        ctap.client_pin.return_value = {
            1: {1: 2, 3: -25, -1: 1, -2: DEV_PUB_X, -3: DEV_PUB_Y}
        }

        key_agreement, shared = prot._get_shared_secret()

        self.assertEqual(shared, SHARED)
        self.assertEqual(key_agreement[-2], EC_PUB_X)
        self.assertEqual(key_agreement[-3], EC_PUB_Y)

    def test_get_pin_token(self):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        prot._get_shared_secret = mock.Mock(return_value=({}, SHARED))
        prot.ctap.client_pin.return_value = {2: TOKEN_ENC}

        self.assertEqual(prot.get_pin_token("1234"), TOKEN)
        prot.ctap.client_pin.assert_called_once()
        self.assertEqual(
            prot.ctap.client_pin.call_args[1]["pin_hash_enc"], PIN_HASH_ENC
        )

    def test_set_pin(self):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        prot._get_shared_secret = mock.Mock(return_value=({}, SHARED))

        prot.set_pin("1234")
        prot.ctap.client_pin.assert_called_with(
            1,
            3,
            key_agreement={},
            new_pin_enc=bytes.fromhex(
                "0222fc42c6dd76a274a7057858b9b29d98e8a722ec2dc6668476168c5320473cec9907b4cd76ce7943c96ba5683943211d84471e64d9c51e54763488cd66526a"  # noqa E501
            ),
            pin_uv_param=bytes.fromhex("7b40c084ccc5794194189ab57836475f"),
        )

    def test_change_pin(self):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        prot._get_shared_secret = mock.Mock(return_value=({}, SHARED))

        prot.change_pin("1234", "4321")
        prot.ctap.client_pin.assert_called_with(
            1,
            4,
            key_agreement={},
            new_pin_enc=bytes.fromhex(
                "4280e14aac4fcbf02dd079985f0c0ffc9ea7d5f9c173fd1a4c843826f7590cb3c2d080c6923e2fe6d7a52c31ea1309d3fcca3dedae8a2ef14b6330cafc79339e"  # noqa E501
            ),
            pin_uv_param=bytes.fromhex("fb97e92f3724d7c85e001d7f93e6490a"),
            pin_hash_enc=bytes.fromhex("afe8327ce416da8ee3d057589c2ce1a9"),
        )

    def test_short_pin(self):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        with self.assertRaises(ValueError):
            prot.set_pin("123")

    def test_long_pin(self):
        ctap = mock.MagicMock()
        ctap.info.options = {"clientPin": True}
        prot = ClientPin(ctap, PinProtocolV1())

        with self.assertRaises(ValueError):
            prot.set_pin("1" * 256)
```

## File: tests/test_hid.py
```python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from fido2.hid.base import parse_report_descriptor
import pytest


def test_parse_report_descriptor_1():
    max_in_size, max_out_size = parse_report_descriptor(
        bytes.fromhex(
            "06d0f10901a1010920150026ff007508954081020921150026ff00750895409102c0"
        )
    )

    assert max_in_size == 64
    assert max_out_size == 64


def test_parse_report_descriptor_2():
    with pytest.raises(ValueError):
        parse_report_descriptor(
            bytes.fromhex(
                "05010902a1010901a10005091901290515002501950575018102950175038101"
                "05010930093109381581257f750895038106c0c0"
            )
        )
```

## File: tests/test_mds3.py
```python
from base64 import b64decode

from fido2.mds3 import MdsAttestationVerifier, parse_blob

# Example data from:
# https://fidoalliance.org/specs/mds/fido-metadata-service-v3.0-ps-20210518.html#examples
EXAMPLE_CA = b64decode(
    """
MIIGGTCCBAGgAwIBAgIUdT9qLX0sVMRe8l0sLmHd3mZovQ0wDQYJKoZIhvcNAQEL
BQAwgZsxHzAdBgNVBAMMFkVYQU1QTEUgTURTMyBURVNUIFJPT1QxIjAgBgkqhkiG
9w0BCQEWE2V4YW1wbGVAZXhhbXBsZS5jb20xFDASBgNVBAoMC0V4YW1wbGUgT1JH
MRAwDgYDVQQLDAdFeGFtcGxlMQswCQYDVQQGEwJVUzELMAkGA1UECAwCTVkxEjAQ
BgNVBAcMCVdha2VmaWVsZDAeFw0yMTA0MTkxMTM1MDdaFw00ODA5MDQxMTM1MDda
MIGbMR8wHQYDVQQDDBZFWEFNUExFIE1EUzMgVEVTVCBST09UMSIwIAYJKoZIhvcN
AQkBFhNleGFtcGxlQGV4YW1wbGUuY29tMRQwEgYDVQQKDAtFeGFtcGxlIE9SRzEQ
MA4GA1UECwwHRXhhbXBsZTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1ZMRIwEAYD
VQQHDAlXYWtlZmllbGQwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDD
jF5wyEWuhwDHsZosGdGFTCcI677rW881vV+UfW38J+K2ioFFNeGVsxbcebK6AVOi
CDPFj0974IpeD9SFOhwAHoDu/LCfXdQWp8ZgQ91ULYWoW8o7NNSp01nbN9zmaO6/
xKNCa0bzjmXoGqglqnP1AtRcWYvXOSKZy1rcPeDv4Dhcpdp6W72fBw0eWIqOhsrI
tuY2/N8ItBPiG03EX72nACq4nZJ/nAIcUbER8STSFPPzvE97TvShsi1FD8aO6l1W
kR/QkreAGjMI++GbB2Qc1nN9Y/VEDbMDhQtxXQRdpFwubTjejkN9hKOtF3B71Yrw
Irng3V9RoPMFdapWMzSlI+WWHog0oTj1PqwJDDg7+z1I6vSDeVWAMKr9mq1w1OGN
zgBopIjd9lRWkRtt2kQSPX9XxqS4E1gDDr8MKbpM3JuubQtNCg9D7Ljvbz6vwvUr
bPHH+oREvucsp0PZ5PpizloepGIcLFxDQqCulGY2n7Ahl0JOFXJqOFCaK3TWHwBv
ZsaY5DgBuUvdUrwtgZNg2eg2omWXEepiVFQn3Fvj43Wh2npPMgIe5P0rwncXvROx
aczd4rtajKS1ucoB9b9iKqM2+M1y/FDIgVf1fWEHwK7YdzxMlgOeLdeV/kqRU5PE
UlLU9a2EwdOErrPbPKZmIfbs/L4B3k4zejMDH3Y+ZwIDAQABo1MwUTAdBgNVHQ4E
FgQU8sWwq1TrurK7xMTwO1dKfeJBbCMwHwYDVR0jBBgwFoAU8sWwq1TrurK7xMTw
O1dKfeJBbCMwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAgEAFw6M
1PiIfCPIBQ5EBUPNmRvRFuDpolOmDofnf/+mv63LqwQZAdo/W8tzZ9kOFhq24SiL
w0H7fsdG/jeREXiIZMNoW/rA6Uac8sU+FYF7Q+qp6CQLlSQbDcpVMifTQjcBk2xh
+aLK9SrrXBqnTAhwS+offGtAW8DpoLuH4tAcQmIjlgMlN65jnELCuqNR/wpA+zch
8LZW8saQ2cwRCwdr8mAzZoLbsDSVCHxQF3/kQjPT7Nao1q2iWcY3OYcRmKrieHDP
67yeLUbVmetfZis2d6ZlkqHLB4ZW1xX4otsEFkuTJA3HWDRsNyhTwx1YoCLsYut5
Zp0myqPNBq28w6qGMyyoJN0Z4RzMEO3R6i/MQNfhK55/8O2HciM6xb5t/aBSuHPK
lBDrFWhpRnKYkaNtlUo35qV5IbKGKau3SdZdSRciaXUd/p81YmoF01UlhhMz/Rqr
1k2gyA0a9tF8+awCeanYt5izl8YO0FlrOU1SQ5UQw4szqqZqbrf4e8fRuU2TXNx4
zk+ImE7WRB44f6mSD746ZCBRogZ/SA5jUBu+OPe4/sEtERWRcQD+fXgce9ZEN0+p
eyJIKAsl5Rm2Bmgyg5IoyWwSG5W+WekGyEokpslou2Yc6EjUj5ndZWz5EiHAiQ74
hNfDoCZIxVVLU3Qbp8a0S1bmsoT2JOsspIbtZUg=
"""
)

# NOTE: Signature changed to be properly ASN.1 formatted!
EXAMPLE_BLOB = """
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsIng1YyI6WyJNSUlDWlRDQ0FndWdBd0lCQWdJQkFUQUtC
Z2dxaGtqT1BRUURBakNCb3pFbk1DVUdBMVVFQXd3ZVJWaEJUVkJNUlNCTlJGTXpJRlJGVTFRZ1NVNVVS
VkpOUlVSSlFWUkZNU0l3SUFZSktvWklodmNOQVFrQkZoTmxlR0Z0Y0d4bFFHVjRZVzF3YkdVdVkyOXRN
UlF3RWdZRFZRUUtEQXRGZUdGdGNHeGxJRTlTUnpFUU1BNEdBMVVFQ3d3SFJYaGhiWEJzWlRFTE1Ba0dB
MVVFQmhNQ1ZWTXhDekFKQmdOVkJBZ01BazFaTVJJd0VBWURWUVFIREFsWFlXdGxabWxsYkdRd0hoY05N
akV3TkRFNU1URXpOVEEzV2hjTk16RXdOREUzTVRFek5UQTNXakNCcFRFcE1DY0dBMVVFQXd3Z1JWaEJU
VkJNUlNCTlJGTXpJRk5KUjA1SlRrY2dRMFZTVkVsR1NVTkJWRVV4SWpBZ0Jna3Foa2lHOXcwQkNRRVdF
MlY0WVcxd2JHVkFaWGhoYlhCc1pTNWpiMjB4RkRBU0JnTlZCQW9NQzBWNFlXMXdiR1VnVDFKSE1SQXdE
Z1lEVlFRTERBZEZlR0Z0Y0d4bE1Rc3dDUVlEVlFRR0V3SlZVekVMTUFrR0ExVUVDQXdDVFZreEVqQVFC
Z05WQkFjTUNWZGhhMlZtYVdWc1pEQlpNQk1HQnlxR1NNNDlBZ0VHQ0NxR1NNNDlBd0VIQTBJQUJOUUpz
NndUcWl4YytTK1ZEQWFqRmxQTmF0MTBLRVdKRTVqY1dPdm02cXBPOVNEQUFNWnZiNEhIcnZzK1A1WVJw
SHJTbFVQZHZLK3VFUWJkV2czMVA5dWpMREFxTUFrR0ExVWRFd1FDTUFBd0hRWURWUjBPQkJZRUZMcXNh
cGNYVjRab1ZIQW5ScFBad1FlN1l5MjBNQW9HQ0NxR1NNNDlCQU1DQTBnQU1FVUNJUUM2N3phOEVJdXlS
aUtnTkRYSVAxczFhTHIzanpIOVdWWGZIeDRiSit6Q3NnSWdHL3RWQnV0T0pVVSt2dm9ISW8vb3RBVUFj
SDViTkhQM3VJemlEUytQVFVjPSIsIk1JSUVIekNDQWdlZ0F3SUJBZ0lCQWpBTkJna3Foa2lHOXcwQkFR
c0ZBRENCbXpFZk1CMEdBMVVFQXd3V1JWaEJUVkJNUlNCTlJGTXpJRlJGVTFRZ1VrOVBWREVpTUNBR0NT
cUdTSWIzRFFFSkFSWVRaWGhoYlhCc1pVQmxlR0Z0Y0d4bExtTnZiVEVVTUJJR0ExVUVDZ3dMUlhoaGJY
QnNaU0JQVWtjeEVEQU9CZ05WQkFzTUIwVjRZVzF3YkdVeEN6QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZR
UUlEQUpOV1RFU01CQUdBMVVFQnd3SlYyRnJaV1pwWld4a01CNFhEVEl4TURReE9URXhNelV3TjFvWERU
UTRNRGt3TkRFeE16VXdOMW93Z2FNeEp6QWxCZ05WQkFNTUhrVllRVTFRVEVVZ1RVUlRNeUJVUlZOVUlF
bE9WRVZTVFVWRVNVRlVSVEVpTUNBR0NTcUdTSWIzRFFFSkFSWVRaWGhoYlhCc1pVQmxlR0Z0Y0d4bExt
TnZiVEVVTUJJR0ExVUVDZ3dMUlhoaGJYQnNaU0JQVWtjeEVEQU9CZ05WQkFzTUIwVjRZVzF3YkdVeEN6
QUpCZ05WQkFZVEFsVlRNUXN3Q1FZRFZRUUlEQUpOV1RFU01CQUdBMVVFQnd3SlYyRnJaV1pwWld4a01G
a3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRU5HdW1CYlluRlFuVGpQMVJTZmM3MGhzaGdi
aUkxWnRwd1E1bjZ4UkxBL1dxMFBTQ2ZMbDVxUStyN2RsY0sxZDNyM3ZMYSt2bTZHNnZLSEdDUEVlVXpx
TXZNQzB3REFZRFZSMFRCQVV3QXdFQi96QWRCZ05WSFE0RUZnUVVOazZGNFJKbkdHVkZlKzAvY2Jad2Zy
WmQ3WlV3RFFZSktvWklodmNOQVFFTEJRQURnZ0lCQUNucDFmbTBGS2xXbVV0VHBsTHVZZzdtcHM0eFAv
Q091OGRuYjM4dTFuTURWdU9UNCtDWmFpTTlBR3ozMTNHRDIyaGpMR3JtUHVZbjg2d0dPS0kzSE9yRXBz
R2RNbWZ5N3RUbUtYL2VNL2VTM0ZFRFhabkU4MlBuNW9GSXlCVC9mOHNHdVh5T3NGWnFXQnZWZEJJSURs
ZENwRDRteE1RWlpPWnRUcmx2M1d2QlFNQy9kc2ljT3hlM1FLWHZXSGk2UWIvUmh1YWlwM3JQbXdNZis0
SnBuSk8rSk1QcUFhVTFjQUg4SFZzZnJMQU1vS3MxNDhqMitjdmJwYVdtc1Q1cklvSC9lelZyUGFHL01P
aUlncTc5dy9lZnV2U2k1QVg4SitrRG9MU0VmM2Q1d09na0pZQXFVcWNSeFhURUV0S0l6RE02aHphQlFG
aUFXdlRuOUlsVldnbnRRYW1TWHZIK3R4YVRGOWlFbEh4VWY1SU5ZRlZjaUNwenRTcnlkZUh2L09DTlJm
Ny9MVnJpY01TbG84UmgrTzN5UDlWKzJ1TmYzWDhzUUpOdHVmclFOYXFxMTh3aVhsaVRMdWZTbjAyL2cr
bWtoSVVpTktmVE9KcHZDaktlQ25DRmN4UVUyL1hUM0toM0c4Z0RKd3NPNkVWUmpNVUp0NEFZS3plL2hF
VUN3RjU1SUYybTNqSElvQ3U4alZmajI0Q2VFWDVkbmZ2U3IrU1Z2TjVRQjB1WjA1TTRybXlaWHlxQm0w
ekszZlIraUUwL1pwSW51d0xDN1grVzgyelhsbk1rcGxJM1ErSnhkN2pmUTE1U1lORTJLNnJ2UklUMDF3
MFA5WnF5REY3a25HS3BSbHA3T3F4ZDM3YkQvVlViV3BRN2dJQWZzSk5INUtCTG93SEpGRmpXIl19.eyJ
sZWdhbEhlYWRlciI6IlJldHJpZXZhbCBhbmQgdXNlIG9mIHRoaXMgQkxPQiBpbmRpY2F0ZXMgYWNjZXB
0YW5jZSBvZiB0aGUgYXBwcm9wcmlhdGUgYWdyZWVtZW50IGxvY2F0ZWQgYXQgaHR0cHM6Ly9maWRvYWx
saWFuY2Uub3JnL21ldGFkYXRhL21ldGFkYXRhLWxlZ2FsLXRlcm1zLyIsIm5vIjoxNSwibmV4dFVwZGF
0ZSI6IjIwMjAtMDMtMzAiLCJlbnRyaWVzIjpbeyJhYWlkIjoiMTIzNCM1Njc4IiwibWV0YWRhdGFTdGF
0ZW1lbnQiOnsibGVnYWxIZWFkZXIiOiJodHRwczovL2ZpZG9hbGxpYW5jZS5vcmcvbWV0YWRhdGEvbWV
0YWRhdGEtc3RhdGVtZW50LWxlZ2FsLWhlYWRlci8iLCJkZXNjcmlwdGlvbiI6IkZJRE8gQWxsaWFuY2U
gU2FtcGxlIFVBRiBBdXRoZW50aWNhdG9yIiwiYWFpZCI6IjEyMzQjNTY3OCIsImFsdGVybmF0aXZlRGV
zY3JpcHRpb25zIjp7InJ1LVJVIjoi0J_RgNC40LzQtdGAIFVBRiDQsNGD0YLQtdC90YLQuNGE0LjQutC
w0YLQvtGA0LAg0L7RgiBGSURPIEFsbGlhbmNlIiwiZnItRlIiOiJFeGVtcGxlIFVBRiBhdXRoZW50aWN
hdG9yIGRlIEZJRE8gQWxsaWFuY2UifSwiYXV0aGVudGljYXRvclZlcnNpb24iOjIsInByb3RvY29sRmF
taWx5IjoidWFmIiwic2NoZW1hIjozLCJ1cHYiOlt7Im1ham9yIjoxLCJtaW5vciI6MH0seyJtYWpvciI
6MSwibWlub3IiOjF9XSwiYXV0aGVudGljYXRpb25BbGdvcml0aG1zIjpbInNlY3AyNTZyMV9lY2RzYV9
zaGEyNTZfcmF3Il0sInB1YmxpY0tleUFsZ0FuZEVuY29kaW5ncyI6WyJlY2NfeDk2Ml9yYXciXSwiYXR
0ZXN0YXRpb25UeXBlcyI6WyJiYXNpY19mdWxsIl0sInVzZXJWZXJpZmljYXRpb25EZXRhaWxzIjpbW3s
idXNlclZlcmlmaWNhdGlvbk1ldGhvZCI6ImZpbmdlcnByaW50X2ludGVybmFsIiwiYmFEZXNjIjp7InN
lbGZBdHRlc3RlZEZBUiI6MC4wMDAwMiwibWF4UmV0cmllcyI6NSwiYmxvY2tTbG93ZG93biI6MzAsIm1
heFRlbXBsYXRlcyI6NX19XV0sImtleVByb3RlY3Rpb24iOlsiaGFyZHdhcmUiLCJ0ZWUiXSwiaXNLZXl
SZXN0cmljdGVkIjp0cnVlLCJtYXRjaGVyUHJvdGVjdGlvbiI6WyJ0ZWUiXSwiY3J5cHRvU3RyZW5ndGg
iOjEyOCwiYXR0YWNobWVudEhpbnQiOlsiaW50ZXJuYWwiXSwidGNEaXNwbGF5IjpbImFueSIsInRlZSJ
dLCJ0Y0Rpc3BsYXlDb250ZW50VHlwZSI6ImltYWdlL3BuZyIsInRjRGlzcGxheVBOR0NoYXJhY3Rlcml
zdGljcyI6W3sid2lkdGgiOjMyMCwiaGVpZ2h0Ijo0ODAsImJpdERlcHRoIjoxNiwiY29sb3JUeXBlIjo
yLCJjb21wcmVzc2lvbiI6MCwiZmlsdGVyIjowLCJpbnRlcmxhY2UiOjB9XSwiYXR0ZXN0YXRpb25Sb29
0Q2VydGlmaWNhdGVzIjpbIk1JSUNQVENDQWVPZ0F3SUJBZ0lKQU91ZXh2VTNPeTJ3TUFvR0NDcUdTTTQ
5QkFNQ01Ic3hJREFlQmdOVkJBTU1GMU5oYlhCc1pTQkJkSFJsYzNSaGRHbHZiaUJTYjI5ME1SWXdGQVl
EVlFRS0RBMUdTVVJQSUVGc2JHbGhibU5sTVJFd0R3WURWUVFMREFoVlFVWWdWRmRITERFU01CQUdBMVV
FQnd3SlVHRnNieUJCYkhSdk1Rc3dDUVlEVlFRSURBSkRRVEVMTUFrR0ExVUVCaE1DVlZNd0hoY05NVFF
3TmpFNE1UTXpNek15V2hjTk5ERXhNVEF6TVRNek16TXlXakI3TVNBd0hnWURWUVFEREJkVFlXMXdiR1V
nUVhSMFpYTjBZWFJwYjI0Z1VtOXZkREVXTUJRR0ExVUVDZ3dOUmtsRVR5QkJiR3hwWVc1alpURVJNQTh
HQTFVRUN3d0lWVUZHSUZSWFJ5d3hFakFRQmdOVkJBY01DVkJoYkc4Z1FXeDBiekVMTUFrR0ExVUVDQXd
DUTBFeEN6QUpCZ05WQkFZVEFsVlRNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVIOGh
2MkQwSFhhNTkvQm1wUTdSWmVoTC9GTUd6RmQxUUJnOXZBVXBPWjNham51UTk0UFI3YU16SDMzblVTQnI
4ZkhZRHJxT0JiNThweEdxSEpSeVgvNk5RTUU0d0hRWURWUjBPQkJZRUZQb0hBM0NMaHhGYkMwSXQ3ekU
0dzhoazVFSi9NQjhHQTFVZEl3UVlNQmFBRlBvSEEzQ0xoeEZiQzBJdDd6RTR3OGhrNUVKL01Bd0dBMVV
kRXdRRk1BTUJBZjh3Q2dZSUtvWkl6ajBFQXdJRFNBQXdSUUloQUowNlFTWHQ5aWhJYkVLWUtJanNQa3J
pVmRMSWd0ZnNiRFN1N0VySmZ6cjRBaUJxb1lDWmYwK3pJNTVhUWVBSGpJekE5WG02M3JydUF4Qlo5cHM
5ejJYTmxRPT0iXSwiaWNvbiI6ImRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1V
oRVVnQUFBRThBQUFBdkNBWUFBQUNpd0pmY0FBQUFBWE5TUjBJQXJzNGM2UUFBQUFSblFVMUJBQUN4and
2OFlRVUFBQUFKY0VoWmN3QUFEc01BQUE3REFjZHZxR1FBQUFhaFNVUkJWR2hEN1pyNWJ4UmxHTWY5S3p
UQjhBTS9ZRWhFMlc3cFFaY1dLS0JjbFNwSEFUbEVMQVJFN2tORUNDQTNGa1dLMENLS1NDRklzS0JjZ1Z
DRFdHTkVTZEFZaWR3Z2dnSkJpUmlNaEZjLzR3eTg4ODR6dTlOZGxuR1RmWkpQMm4zbk8rKzg4OTMzZnZ
lQkJ4K1BxQ3pKa1RVdkJiTG1wVURXdkJUSW1wY0NTWnZYTENkWDlSMDVTazE5YmI1YXRmNTk5ZkcrL2V
yQTU0MXE0N2FQMUxMVmE5U0l5Vk5VaThJaThkNWtHVHNpMzBORnY3YWk5bjdRWlBNd2JkeXMyZXJVMlh
NcVVkeTgrWmNhTm1HaW1FOHlYTjNSVWQzYTE4bkYwZlVsb3ZaKzBDVHpXcGQyVmorZU9tMWJFeXk2RHg
0aTVwVU1HV3ZlbzUwNnEyMjdkdHVXQkl1ZmZyNm9XcFYwRlBOTGhvdzE3NTFObTIxTHZQSDNyVnRXamZ
6NjZMZnFsOHRYN0ZSbDlZRlNYc21Tc2ViOWNlT0diWWs3TU5VY0dQZzhac2JNZTlyZlFVYWFWL0pNWDl
zcWR6RENTdnAwa1pIbVRaZzl4N2JMSGNNblRoYjE2ZUorbVZmUXE4eWFVWlFORzY0aVhaKzAva3E2dU9
aRk8wUXRhdGRXS2ZYblJROTlCajkxUjVPSUZuazU0ak4wbWtVaXFsTzNYRFcrTWwrOThtS0I2dFc3cld
wWmNQYyswemc0dExyWWxVYzg2RTZlR0RqSU11YlZwY3VzZWFyZmdJWUdSazZicmhaVnIvSmNIem9vTDc
1NTBqZWRMRXhvcFdjQXBpMlpVcWh1N0pMdnJWc1FVODF6a3pPUGVlbU1SWXZWdVFzWDdQYmlEUVk1SnZ
ab25mdEsrMVZZOEg5dXR4NTMwaDBvYitqbVJZcWo2b3VhWXZFZW5XL1dsWWpwOGN3Yk1tNjgydFB3cVc
xUjR0ai8yU0gxM0lSSllsNG1vWnZYcGlTcURyN2RYdFFIeGEvUEszLytCV3NLMWRUZ0h1NlY4dFFKM2J
3Rmt3cEZyVU9RNTBzMXIzbGV2bTh6WmNxMTcrQkJhdzdLOGxFSzVxemtZZWFyazlBOHA3UDNHekRLK25
kM0RRb3crNlVDOFNWTjgyaXV2MzhpbTdOdGFYdFYxQ1ZxNlJndzRwa3NtYmRpM2J1MkRlN1lmYUJCeGN
xZnZxUHJVakZRTlRRMjJsZmRVVlZUNjhyVEpLRjVEblNtVWpnZHFnNG1TUzlwbXNmREpSM0c2VG9IMGl
XOWFWN0xXTEhZWEtsbFREdDBMVEF0a1lJYWFtcDFRalZ2Kyt1eUdVeFZkSjBETlZYU20rYjFxUnhwbDg
0ZGRmWDFMcDFPL2Q2OXRzb2QwdnM1aEdyZTl4dThvK2ZwTFIxY0doTlRENlo1N0M5S01XWGVmSmRPWjk
0YmI5b3FkMVJPblM3cUlUVHpIaW1NcWl2Yk8zZzBEZFZ5azNXUUJoQnp0SzM1WUtOZE9uYzhPM2FjUzZ
mRFpGZ0thWExzRUpwNXJkcmxpQnFwODljSmNzL203VHZzMHJrakdmTjRiMGtQb1puM1VKdUlPcm5aMjJ
5UDFmbXZVeCtPNWdTcWViVjFtK3pTdVlOVmhxN1RXYkRpTFZ2bGpwbExsb3A2Q0xYUCsycXR2R0xJTC8
xdmltSVNkTUJnelNvRlp5dTZUcWQranp4Z3NQYVY5QkNxZWUvTmpZazZ2NmxLOWN3aVVjL1NUdGYxSER
wTTNiNTkyeTdoM1RoeDVveks2OUhMcFlXdUF3YXFTNWN2MjZxN2NlYjhlZlZZYVJlUDNpRlU4emoxa25
Td1pYSE1tbkNqWTBPZ2FsbzdVUWZTQ00zcVFRcjJIL1hGUDdzc1h4NDVZbDkxQnllQ2VwNG1vWm9IKzF
mRzN4RDR0VDd4OGt3eWo4bndiOWV2MjZWMEI2ZCs3SDR6S3Z1ZEFINTM3RmpxeXpPSGRKbkhFdXptWHE
vV2p4T2J2Tk1idjduaHl3c1gyYVZzV3RDOCs0OGFMZWFwRTdwNXdLWmkwQTJBUVJWNW52UjRFK3VKYyt
iNjFrQXBxSW54QmdtZC80VjVRUC9tdDE4SERDN3NSSGZ0bWV1NWxtaFYwcm4vQUxYMjMyYnFkNEJGbkR
4N1ZpMWNXUzJ1ZmYwSWJCNDdxZXh4bVVqOVF1dFlqdXBkM3RZRDZhYldCQk1yaCthcE5iT0tyTkYxK3V
nQ2E0cmlYR2Z3TVBQdFZpYXZoVTNZTU9BQW51VWIvUjA3TDB5T1NlT2FkRTg4QXBzWEZHZmYzMHluaGx
KZ001MUNVNnZOOUV6Z25wdkhCRlV5aVZyYWVQaXdKNTNERjVaVFpub21FTmc4NWtOVWQyb0ppMldwcjR
PbW1rZk40eDR6SGZpVkZjOER2OE56dWhOcU9pZGlsR3ZBNkRHdWVad083OEFBUW42Y2lFazYrcnc1VmN
2anZxTkRZUE9vSVV3YUtTaHJ4QXVYTGxrSDRhWXVHZk1ZRGMxMFdGNVRhMzFoUEpPZmNVaHJVL0psSU5
pNmM2ZWxSWWRCcG82KytZZmp4NjFsR05mUm00TUQ1ckoxajNGb0dIbmpEU0JOYXJZVWdNTHlNc3pLcGI
3dFhwb0hmUHM4aDNXcDFMek5mTms1NFh4QzF3REdVbVl6WFllZmg2ei9jS3RWbTRFQnhhOVZRR0R6WXI
zTHJVTVJqSEVLa2s3emFGS1lRQTJoR1FVMXorODVORldwWERya3ozdngxMEdxeFE2QnplTmJvQms1bjh
rNG5lYlJoK2sxaFdmeFRGMEQxRXlXVXM1bnYrZGdRcUtheHp1Q2RFMGlzSGwwMk5ROGFoMG1YcjEyTGE
zbTBmOXdpazkrd0xOVE1ZLzg2TVBvOHlpMzFPZnhtVDZQV29xRzkrRFp1a1luYTU2bVNadDVXV1N5NXF
WQTFyd1V5SnFYQWxuemtpYWkvZ0hTRDdSa1R5aWhvZ0FBQUFCSlJVNUVya0pnZ2c9PSJ9LCJzdGF0dXN
SZXBvcnRzIjpbeyJzdGF0dXMiOiJGSURPX0NFUlRJRklFRCIsImVmZmVjdGl2ZURhdGUiOiIyMDE0LTA
xLTA0In1dLCJ0aW1lT2ZMYXN0U3RhdHVzQ2hhbmdlIjoiMjAxNC0wMS0wNCJ9LHsiYWFndWlkIjoiMDE
zMmQxMTAtYmY0ZS00MjA4LWE0MDMtYWI0ZjVmMTJlZmU1IiwibWV0YWRhdGFTdGF0ZW1lbnQiOnsibGV
nYWxIZWFkZXIiOiJodHRwczovL2ZpZG9hbGxpYW5jZS5vcmcvbWV0YWRhdGEvbWV0YWRhdGEtc3RhdGV
tZW50LWxlZ2FsLWhlYWRlci8iLCJkZXNjcmlwdGlvbiI6IkZJRE8gQWxsaWFuY2UgU2FtcGxlIEZJRE8
yIEF1dGhlbnRpY2F0b3IiLCJhYWd1aWQiOiIwMTMyZDExMC1iZjRlLTQyMDgtYTQwMy1hYjRmNWYxMmV
mZTUiLCJhbHRlcm5hdGl2ZURlc2NyaXB0aW9ucyI6eyJydS1SVSI6ItCf0YDQuNC80LXRgCBGSURPMiD
QsNGD0YLQtdC90YLQuNGE0LjQutCw0YLQvtGA0LAg0L7RgiBGSURPIEFsbGlhbmNlIiwiZnItRlIiOiJ
FeGVtcGxlIEZJRE8yIGF1dGhlbnRpY2F0b3IgZGUgRklETyBBbGxpYW5jZSIsInpoLUNOIjoi5L6G6Ie
qRklETyBBbGxpYW5jZeeahOekuuS-i0ZJRE8y6Lqr5Lu96amX6K2J5ZmoIn0sInByb3RvY29sRmFtaWx
5IjoiZmlkbzIiLCJzY2hlbWEiOjMsImF1dGhlbnRpY2F0b3JWZXJzaW9uIjo1LCJ1cHYiOlt7Im1ham9
yIjoxLCJtaW5vciI6MH1dLCJhdXRoZW50aWNhdGlvbkFsZ29yaXRobXMiOlsic2VjcDI1NnIxX2VjZHN
hX3NoYTI1Nl9yYXciLCJyc2Fzc2FfcGtjc3YxNV9zaGEyNTZfcmF3Il0sInB1YmxpY0tleUFsZ0FuZEV
uY29kaW5ncyI6WyJjb3NlIl0sImF0dGVzdGF0aW9uVHlwZXMiOlsiYmFzaWNfZnVsbCJdLCJ1c2VyVmV
yaWZpY2F0aW9uRGV0YWlscyI6W1t7InVzZXJWZXJpZmljYXRpb25NZXRob2QiOiJub25lIn1dLFt7InV
zZXJWZXJpZmljYXRpb25NZXRob2QiOiJwcmVzZW5jZV9pbnRlcm5hbCJ9XSxbeyJ1c2VyVmVyaWZpY2F
0aW9uTWV0aG9kIjoicGFzc2NvZGVfZXh0ZXJuYWwiLCJjYURlc2MiOnsiYmFzZSI6MTAsIm1pbkxlbmd
0aCI6NH19XSxbeyJ1c2VyVmVyaWZpY2F0aW9uTWV0aG9kIjoicGFzc2NvZGVfZXh0ZXJuYWwiLCJjYUR
lc2MiOnsiYmFzZSI6MTAsIm1pbkxlbmd0aCI6NH19LHsidXNlclZlcmlmaWNhdGlvbk1ldGhvZCI6InB
yZXNlbmNlX2ludGVybmFsIn1dXSwia2V5UHJvdGVjdGlvbiI6WyJoYXJkd2FyZSIsInNlY3VyZV9lbGV
tZW50Il0sIm1hdGNoZXJQcm90ZWN0aW9uIjpbIm9uX2NoaXAiXSwiY3J5cHRvU3RyZW5ndGgiOjEyOCw
iYXR0YWNobWVudEhpbnQiOlsiZXh0ZXJuYWwiLCJ3aXJlZCIsIndpcmVsZXNzIiwibmZjIl0sInRjRGl
zcGxheSI6W10sImF0dGVzdGF0aW9uUm9vdENlcnRpZmljYXRlcyI6WyJNSUlDUFRDQ0FlT2dBd0lCQWd
JSkFPdWV4dlUzT3kyd01Bb0dDQ3FHU000OUJBTUNNSHN4SURBZUJnTlZCQU1NRjFOaGJYQnNaU0JCZEh
SbGMzUmhkR2x2YmlCU2IyOTBNUll3RkFZRFZRUUtEQTFHU1VSUElFRnNiR2xoYm1ObE1SRXdEd1lEVlF
RTERBaFZRVVlnVkZkSExERVNNQkFHQTFVRUJ3d0pVR0ZzYnlCQmJIUnZNUXN3Q1FZRFZRUUlEQUpEUVR
FTE1Ba0dBMVVFQmhNQ1ZWTXdIaGNOTVRRd05qRTRNVE16TXpNeVdoY05OREV4TVRBek1UTXpNek15V2p
CN01TQXdIZ1lEVlFRRERCZFRZVzF3YkdVZ1FYUjBaWE4wWVhScGIyNGdVbTl2ZERFV01CUUdBMVVFQ2d
3TlJrbEVUeUJCYkd4cFlXNWpaVEVSTUE4R0ExVUVDd3dJVlVGR0lGUlhSeXd4RWpBUUJnTlZCQWNNQ1Z
CaGJHOGdRV3gwYnpFTE1Ba0dBMVVFQ0F3Q1EwRXhDekFKQmdOVkJBWVRBbFZUTUZrd0V3WUhLb1pJemo
wQ0FRWUlLb1pJemowREFRY0RRZ0FFSDhodjJEMEhYYTU5L0JtcFE3UlplaEwvRk1HekZkMVFCZzl2QVV
wT1ozYWpudVE5NFBSN2FNekgzM25VU0JyOGZIWURycU9CYjU4cHhHcUhKUnlYLzZOUU1FNHdIUVlEVlI
wT0JCWUVGUG9IQTNDTGh4RmJDMEl0N3pFNHc4aGs1RUovTUI4R0ExVWRJd1FZTUJhQUZQb0hBM0NMaHh
GYkMwSXQ3ekU0dzhoazVFSi9NQXdHQTFVZEV3UUZNQU1CQWY4d0NnWUlLb1pJemowRUF3SURTQUF3UlF
JaEFKMDZRU1h0OWloSWJFS1lLSWpzUGtyaVZkTElndGZzYkRTdTdFckpmenI0QWlCcW9ZQ1pmMCt6STU
1YVFlQUhqSXpBOVhtNjNycnVBeEJaOXBzOXoyWE5sUT09Il0sImljb24iOiJkYXRhOmltYWdlL3BuZzt
iYXNlNjQsaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUU4QUFBQXZDQVlBQUFDaXdKZmNBQUFBQVhOU1I
wSUFyczRjNlFBQUFBUm5RVTFCQUFDeGp3djhZUVVBQUFBSmNFaFpjd0FBRHNNQUFBN0RBY2R2cUdRQUF
BYWhTVVJCVkdoRDdacjVieFJsR01mOUt6VEI4QU0vWUVoRTJXN3BRWmNXS0tCY2xTcEhBVGxFTEFSRTd
rTkVDQ0EzRmtXSzBDS0tTQ0ZJc0tCY2dWQ0RXR05FU2RBWWlkd2dnZ0pCaVJpTWhGYy80d3k4ODg0enU
5TmRsbkdUZlpKUDJuM25PKys4ODkzM2Z2ZUJCeCtQcUN6SmtUVXZCYkxtcFVEV3ZCVEltcGNDU1p2WEx
DZFg5UjA1U2sxOWJiNWF0ZjU5OWZHKy9lckE1NDFxNDdhUDFMTFZhOVNJeVZOVWk4SWk4ZDVrR1RzaTM
wTkZ2N2FpOW43UVpQTXdiZHlzMmVyVTJYTXFVZHk4K1pjYU5tR2ltRTh5WE4zUlVkM2ExOG5GMGZVbG9
2WiswQ1R6V3BkMlZqK2VPbTFiRXl5NkR4NGk1cFVNR1d2ZW81MDZxMjI3ZHR1V0JJdWZmcjZvV3BWMEZ
QTkxob3cxNzUxTm0yMUx2UEgzclZ0V2pmejY2TGZxbDh0WDdGUmw5WUZTWHNtU3NlYjljZU9HYllrN01
OVWNHUGc4WnNiTWU5cmZRVWFhVi9KTVg5c3FkekRDU3ZwMGtaSG1UWmc5eDdiTEhjTW5UaGIxNmVKK21
WZlFxOHlhVVpRTkc2NGlYWiswL2txNnVPWkZPMFF0YXRkV0tmWG5SUTk5Qmo5MVI1T0lGbms1NGpOMG1
rVWlxbE8zWERXK01sKzk4bUtCNnRXN3JXcFpjUGMrMHpnNHRMcllsVWM4NkU2ZUdEaklNdWJWcGN1c2V
hcmZnSVlHUms2YnJoWlZyL0pjSHpvb0w3NTUwamVkTEV4b3BXY0FwaTJaVXFodTdKTHZyVnNRVTgxemt
6T1BlZW1NUll2VnVRc1g3UGJpRFFZNUp2Wm9uZnRLKzFWWThIOXV0eDUzMGgwb2Iram1SWXFqNm91YVl
2RWVuVy9XbFlqcDhjd2JNbTY4MnRQd3FXMVI0dGovMlNIMTNJUkpZbDRtb1p2WHBpU3FEcjdkWHRRSHh
hL1BLMy8rQldzSzFkVGdIdTZWOHRRSjNid0Zrd3BGclVPUTUwczFyM2xldm04elpjcTE3K0JCYXc3Szh
sRUs1cXprWWVhcms5QThwN1AzR3pESytuZDNEUW93KzZVQzhTVk44Mml1djM4aW03TnRhWHRWMUNWcTZ
SZ3c0cGtzbWJkaTNidTJEZTdZZmFCQnhjcWZ2cVByVWpGUU5UUTIybGZkVVZWVDY4clRKS0Y1RG5TbVV
qZ2RxZzRtU1M5cG1zZkRKUjNHNlRvSDBpVzlhVjdMV0xIWVhLbGxURHQwTFRBdGtZSWFhbXAxUWpWdis
rdXlHVXhWZEowRE5WWFNtK2IxcVJ4cGw4NGRkZlgxTHAxTy9kNjl0c29kMHZzNWhHcmU5eHU4bytmcEx
SMWNHaE5URDZaNTdDOUtNV1hlZkpkT1o5NGJiOW9xZDFST25TN3FJVFR6SGltTXFpdmJPM2cwRGRWeWs
zV1FCaEJ6dEszNVlLTmRPbmM4TzNhY1M2ZkRaRmdLYVhMc0VKcDVyZHJsaUJxcDg5Y0pjcy9tN1R2czB
ya2pHZk40YjBrUG9abjNVSnVJT3JuWjIyeVAxZm12VXgrTzVnU3FlYlYxbSt6U3VZTlZocTdUV2JEaUx
WdmxqcGxMbG9wNkNMWFArMnF0dkdMSUwvMXZpbUlTZE1CZ3pTb0ZaeXU2VHFkK2p6eGdzUGFWOUJDcWV
lL05qWWs2djZsSzljd2lVYy9TVHRmMUhEcE0zYjU5Mnk3aDNUaHg1b3pLNjlITHBZV3VBd2FxUzVjdjI
2cTdjZWI4ZWZWWWFSZVAzaUZVOHpqMWtuU3daWEhNbW5DalkwT2dhbG83VVFmU0NNM3FRUXIySC9YRlA
3c3NYeDQ1WWw5MUJ5ZUNlcDRtb1pvSCsxZkczeEQ0dFQ3eDhrd3lqOG53YjlldjI2VjBCNmQrN0g0ekt
2dWRBSDUzN0ZqcXl6T0hkSm5IRXV6bVhxL1dqeE9idk5NYnY3bmh5d3NYMmFWc1d0QzgrNDhhTGVhcEU
3cDV3S1ppMEEyQVFSVjVudlI0RSt1SmMrYjYxa0FwcUlueEJnbWQvNFY1UVAvbXQxOEhEQzdzUkhmdG1
ldTVsbWhWMHJuL0FMWDIzMmJxZDRCRm5EeDdWaTFjV1MydWZmMEliQjQ3cWV4eG1VajlRdXRZanVwZDN
0WUQ2YWJXQkJNcmgrYXBOYk9Lck5GMSt1Z0NhNHJpWEdmd01QUHRWaWF2aFUzWU1PQUFudVViL1IwN0w
weU9TZU9hZEU4OEFwc1hGR2ZmMzB5bmhsSmdNNTFDVTZ2TjlFemducHZIQkZVeWlWcmFlUGl3SjUzREY
1WlRabm9tRU5nODVrTlVkMm9KaTJXcHI0T21ta2ZONHg0ekhmaVZGYzhEdjhOenVoTnFPaWRpbEd2QTZ
ER3VlWndPNzhBQVFuNmNpRWs2K3J3NVZjdmp2cU5EWVBPb0lVd2FLU2hyeEF1WExsa0g0YVl1R2ZNWUR
jMTBXRjVUYTMxaFBKT2ZjVWhyVS9KbElOaTZjNmVsUllkQnBvNisrWWZqeDYxbEdOZlJtNE1ENXJKMWo
zRm9HSG5qRFNCTmFyWVVnTUx5TXN6S3BiN3RYcG9IZlBzOGgzV3AxTHpOZk5rNTRYeEMxd0RHVW1Zelh
ZZWZoNnovY0t0Vm00RUJ4YTlWUUdEellyM0xyVU1SakhFS2trN3phRktZUUEyaEdRVTF6Kzg1TkZXcFh
Ecmt6M3Z4MTBHcXhRNkJ6ZU5ib0JrNW44azRuZWJSaCtrMWhXZnhURjBEMUV5V1VzNW52K2RnUXFLYXh
6dUNkRTBpc0hsMDJOUThhaDBtWHIxMkxhM20wZjl3aWs5K3dMTlRNWS84Nk1Qbzh5aTMxT2Z4bVQ2UFd
vcUc5K0RadWtZbmE1Nm1TWnQ1V1dTeTVxVkExcndVeUpxWEFsbnpraWFpL2dIU0Q3UmtUeWlob2dBQUF
BQkpSVTVFcmtKZ2dnPT0iLCJzdXBwb3J0ZWRFeHRlbnNpb25zIjpbeyJpZCI6ImhtYWMtc2VjcmV0Iiw
iZmFpbF9pZl91bmtub3duIjpmYWxzZX0seyJpZCI6ImNyZWRQcm90ZWN0IiwiZmFpbF9pZl91bmtub3d
uIjpmYWxzZX1dLCJhdXRoZW50aWNhdG9yR2V0SW5mbyI6eyJ2ZXJzaW9ucyI6WyJVMkZfVjIiLCJGSUR
PXzJfMCJdLCJleHRlbnNpb25zIjpbImNyZWRQcm90ZWN0IiwiaG1hYy1zZWNyZXQiXSwiYWFndWlkIjo
iMDEzMmQxMTBiZjRlNDIwOGE0MDNhYjRmNWYxMmVmZTUiLCJvcHRpb25zIjp7InBsYXQiOiJmYWxzZSI
sInJrIjoidHJ1ZSIsImNsaWVudFBpbiI6InRydWUiLCJ1cCI6InRydWUiLCJ1diI6InRydWUiLCJ1dlR
va2VuIjoiZmFsc2UiLCJjb25maWciOiJmYWxzZSJ9LCJtYXhNc2dTaXplIjoxMjAwLCJwaW5VdkF1dGh
Qcm90b2NvbHMiOlsxXSwibWF4Q3JlZGVudGlhbENvdW50SW5MaXN0IjoxNiwibWF4Q3JlZGVudGlhbEl
kTGVuZ3RoIjoxMjgsInRyYW5zcG9ydHMiOlsidXNiIiwibmZjIl0sImFsZ29yaXRobXMiOlt7InR5cGU
iOiJwdWJsaWMta2V5IiwiYWxnIjotN30seyJ0eXBlIjoicHVibGljLWtleSIsImFsZyI6LTI1N31dLCJ
tYXhBdXRoZW50aWNhdG9yQ29uZmlnTGVuZ3RoIjoxMDI0LCJkZWZhdWx0Q3JlZFByb3RlY3QiOjIsImZ
pcm13YXJlVmVyc2lvbiI6NX19LCJzdGF0dXNSZXBvcnRzIjpbeyJzdGF0dXMiOiJGSURPX0NFUlRJRkl
FRCIsImVmZmVjdGl2ZURhdGUiOiIyMDE5LTAxLTA0In0seyJzdGF0dXMiOiJGSURPX0NFUlRJRklFRF9
MMSIsImVmZmVjdGl2ZURhdGUiOiIyMDIwLTExLTE5IiwiY2VydGlmaWNhdGlvbkRlc2NyaXB0b3IiOiJ
GSURPIEFsbGlhbmNlIFNhbXBsZSBGSURPMiBBdXRoZW50aWNhdG9yIiwiY2VydGlmaWNhdGVOdW1iZXI
iOiJGSURPMjEwMDAyMDE1MTIyMTAwMSIsImNlcnRpZmljYXRpb25Qb2xpY3lWZXJzaW9uIjoiMS4wLjE
iLCJjZXJ0aWZpY2F0aW9uUmVxdWlyZW1lbnRzVmVyc2lvbiI6IjEuMC4xIn1dLCJ0aW1lT2ZMYXN0U3R
hdHVzQ2hhbmdlIjoiMjAxOS0wMS0wNCJ9XX0.MEYCIQD6RzXCuiskDXpvEtdfN4OQUQ4KxsoDLZYMTOg
Jj4B6PwIhAM3RtYg4CaGkcbFJrcJeCbAXCAC7LbfQSr8EdM79GyGw
""".replace("\n", "").encode()


AAGUID = bytes.fromhex("0132d110bf4e4208a403ab4f5f12efe5")


def test_parse_blob():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    assert data.no == 15
    assert len(data.entries) == 2


def test_find_by_aaguid():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    mds = MdsAttestationVerifier(data)
    entry = mds.find_entry_by_aaguid(AAGUID)
    assert (
        entry.metadata_statement.description
        == "FIDO Alliance Sample FIDO2 Authenticator"
    )


def test_find_by_aaguid_miss():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    mds = MdsAttestationVerifier(data)
    entry = mds.find_entry_by_aaguid(bytes.fromhex("0102030405060708090a0b0c0d0e0f"))
    assert entry is None


def test_find_by_chain_miss():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    mds = MdsAttestationVerifier(data)
    entry = mds.find_entry_by_chain([EXAMPLE_CA])
    assert entry is None


def test_filter_entries():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    mds = MdsAttestationVerifier(data, entry_filter=lambda e: e.aaguid != AAGUID)
    entry = mds.find_entry_by_aaguid(AAGUID)
    assert entry is None

    mds = MdsAttestationVerifier(data, entry_filter=lambda e: e.aaguid == AAGUID)
    assert mds.find_entry_by_aaguid(AAGUID)


def test_lookup_filter_does_not_affect_find_entry_by_aaguid():
    data = parse_blob(EXAMPLE_BLOB, EXAMPLE_CA)
    mds = MdsAttestationVerifier(
        data, attestation_filter=lambda e, _: e.aaguid != AAGUID
    )
    assert mds.find_entry_by_aaguid(AAGUID)
```

## File: tests/test_pcsc.py
```python
# Copyright (c) 2019 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from unittest import mock

import pytest

from fido2.hid import CTAPHID


@pytest.fixture(autouse=True, scope="module")
def preconditions():
    global CtapPcscDevice
    try:
        from fido2.pcsc import CtapPcscDevice
    except ImportError:
        pytest.skip("pyscard is not installed")


def test_pcsc_call_cbor():
    connection = mock.Mock()
    connection.transmit.side_effect = [(b"U2F_V2", 0x90, 0x00), (b"", 0x90, 0x00)]

    CtapPcscDevice(connection, "Mock")

    connection.transmit.assert_called_with(
        [0x80, 0x10, 0x80, 0x00, 0x01, 0x04, 0x00], None
    )


def test_pcsc_call_u2f():
    connection = mock.Mock()
    connection.transmit.side_effect = [
        (b"U2F_V2", 0x90, 0x00),
        (b"", 0x90, 0x00),
        (b"u2f_resp", 0x90, 0x00),
    ]

    dev = CtapPcscDevice(connection, "Mock")
    res = dev.call(CTAPHID.MSG, b"\x00\x01\x00\x00\x05" + b"\x01" * 5 + b"\x00")

    connection.transmit.assert_called_with(
        [0x00, 0x01, 0x00, 0x00, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00], None
    )
    assert res == b"u2f_resp\x90\x00"


def test_pcsc_call_version_2():
    connection = mock.Mock()
    connection.transmit.side_effect = [(b"U2F_V2", 0x90, 0x00), (b"", 0x90, 0x00)]

    dev = CtapPcscDevice(connection, "Mock")

    assert dev.version == 2


def test_pcsc_call_version_1():
    connection = mock.Mock()
    connection.transmit.side_effect = [(b"U2F_V2", 0x90, 0x00), (b"", 0x63, 0x85)]

    dev = CtapPcscDevice(connection, "Mock")

    assert dev.version == 1
```

## File: tests/test_rpid.py
```python
# coding=utf-8

# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

from fido2.rpid import verify_rp_id


class TestRpId(unittest.TestCase):
    def test_valid_ids(self):
        self.assertTrue(verify_rp_id("example.com", "https://register.example.com"))
        self.assertTrue(verify_rp_id("example.com", "https://fido.example.com"))
        self.assertTrue(verify_rp_id("example.com", "https://www.example.com:444"))

    def test_invalid_ids(self):
        self.assertFalse(verify_rp_id("example.com", "http://example.com"))
        self.assertFalse(verify_rp_id("example.com", "http://www.example.com"))
        self.assertFalse(verify_rp_id("example.com", "https://example-test.com"))

        self.assertFalse(
            verify_rp_id("companyA.hosting.example.com", "https://register.example.com")
        )
        self.assertFalse(
            verify_rp_id(
                "companyA.hosting.example.com", "https://companyB.hosting.example.com"
            )
        )

    def test_suffix_list(self):
        self.assertFalse(verify_rp_id("co.uk", "https://foobar.co.uk"))
        self.assertTrue(verify_rp_id("foobar.co.uk", "https://site.foobar.co.uk"))
        self.assertFalse(verify_rp_id("appspot.com", "https://example.appspot.com"))
        self.assertTrue(
            verify_rp_id("example.appspot.com", "https://example.appspot.com")
        )

    def test_localhost_http_secure_context(self):
        # Localhost and subdomains are secure contexts in most browsers
        self.assertTrue(verify_rp_id("localhost", "http://localhost"))
        self.assertTrue(verify_rp_id("localhost", "http://example.localhost"))
        self.assertTrue(verify_rp_id("example.localhost", "http://example.localhost"))
        self.assertTrue(verify_rp_id("localhost", "http://localhost:8000"))
        self.assertFalse(verify_rp_id("localhost", "http://"))
```

## File: tests/test_server.py
```python
import unittest

from fido2.server import Fido2Server
from fido2.utils import websafe_encode
from fido2.webauthn import (
    AttestedCredentialData,
    AuthenticationResponse,
    AuthenticatorAssertionResponse,
    AuthenticatorData,
    CollectedClientData,
    PublicKeyCredentialRpEntity,
    UserVerificationRequirement,
)

from .test_ctap2 import _ATT_CRED_DATA, _CRED_ID


class TestPublicKeyCredentialRpEntity(unittest.TestCase):
    def test_id_hash(self):
        rp = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        rp_id_hash = (
            b"\xa3y\xa6\xf6\xee\xaf\xb9\xa5^7\x8c\x11\x804\xe2u\x1eh/"
            b"\xab\x9f-0\xab\x13\xd2\x12U\x86\xce\x19G"
        )
        self.assertEqual(rp.id_hash, rp_id_hash)


USER = {"id": b"user_id", "name": "A. User"}


class TestFido2Server(unittest.TestCase):
    def test_register_begin_rp(self):
        rp = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        server = Fido2Server(rp)

        request, state = server.register_begin(USER)

        self.assertEqual(
            request["publicKey"]["rp"], {"id": "example.com", "name": "Example"}
        )

    def test_register_begin_custom_challenge(self):
        rp = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        server = Fido2Server(rp)

        challenge = b"1234567890123456"
        request, state = server.register_begin(USER, challenge=challenge)

        self.assertEqual(request["publicKey"]["challenge"], websafe_encode(challenge))

    def test_register_begin_custom_challenge_too_short(self):
        rp = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        server = Fido2Server(rp)

        challenge = b"123456789012345"
        with self.assertRaises(ValueError):
            request, state = server.register_begin(USER, challenge=challenge)

    def test_authenticate_complete_invalid_signature(self):
        rp = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        server = Fido2Server(rp)

        state = {
            "challenge": "GAZPACHO!",
            "user_verification": UserVerificationRequirement.PREFERRED,
        }
        client_data = CollectedClientData.create(
            CollectedClientData.TYPE.GET,
            "GAZPACHO!",
            "https://example.com",
        )
        _AUTH_DATA = bytes.fromhex(
            "A379A6F6EEAFB9A55E378C118034E2751E682FAB9F2D30AB13D2125586CE1947010000001D"
        )
        response = AuthenticationResponse(
            raw_id=_CRED_ID,
            response=AuthenticatorAssertionResponse(
                client_data=client_data,
                authenticator_data=AuthenticatorData(_AUTH_DATA),
                signature=b"INVALID",
            ),
        )

        with self.assertRaisesRegex(ValueError, "Invalid signature."):
            server.authenticate_complete(
                state,
                [AttestedCredentialData(_ATT_CRED_DATA)],
                response,
            )
```

## File: tests/test_tpm.py
```python
# Copyright (c) 2019 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

from fido2.attestation.tpm import TpmAttestationFormat, TpmPublicFormat


class TestTpmObject(unittest.TestCase):
    def test_parse_tpm(self):
        data = bytes.fromhex(
            "ff54434780170022000b68cec627cc6411099a1f809fde4379f649aa170c7072d1adf230de439efc80810014f7c8b0cdeb31328648130a19733d6fff16e76e1300000003ef605603446ed8c56aa7608d01a6ea5651ee67a8a20022000bdf681917e18529c61e1b85a1e7952f3201eb59c609ed5d8e217e5de76b228bbd0022000b0a10d216b0c3ab82bfdc1f0a016ab9493384c7aee1937ee8800f76b30c9b71a7"  # noqa
        )

        tpm = TpmAttestationFormat.parse(data)
        self.assertEqual(
            tpm.data, bytes.fromhex("f7c8b0cdeb31328648130a19733d6fff16e76e13")
        )

    def test_parse_too_short_of_a_tpm(self):
        with self.assertRaises(ValueError):
            TpmAttestationFormat.parse(bytes.fromhex("ff5443"))
        with self.assertRaises(ValueError) as e:
            data = bytes.fromhex(
                "ff54434780170022000b68cec627cc6411099a1f809fde4379f649aa170c7072d1adf230de439efc80810014f7c8b0cdeb31328648"  # noqa
            )
            TpmAttestationFormat.parse(data)
        self.assertEqual(
            e.exception.args[0], "Not enough data to read (need: 20, had: 9)."
        )

    def test_parse_public_ecc(self):
        data = bytes.fromhex(
            "0023000b00060472000000100010000300100020b9174cd199f77552afcffe6b1f069c032ffdc4f56068dec4e189e7967b3bf6b0002037bf8aa7d93fddb9507319141c6fa31c8e48a1c6da013603a9f6e3913d157c66"  # noqa
        )
        TpmPublicFormat.parse(data)
```

## File: tests/test_utils.py
```python
# coding=utf-8

# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import unittest

from fido2.utils import hmac_sha256, sha256, websafe_decode, websafe_encode


class TestSha256(unittest.TestCase):
    def test_sha256_vectors(self):
        self.assertEqual(
            sha256(b"abc"),
            bytes.fromhex(
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
            ),
        )
        self.assertEqual(
            sha256(b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"),
            bytes.fromhex(
                "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
            ),
        )


class TestHmacSha256(unittest.TestCase):
    def test_hmac_sha256_vectors(self):
        self.assertEqual(
            hmac_sha256(b"\x0b" * 20, b"Hi There"),
            bytes.fromhex(
                "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"
            ),
        )

        self.assertEqual(
            hmac_sha256(b"Jefe", b"what do ya want for nothing?"),
            bytes.fromhex(
                "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"
            ),
        )


class TestWebSafe(unittest.TestCase):
    # Base64 vectors adapted from https://tools.ietf.org/html/rfc4648#section-10

    def test_websafe_decode(self):
        self.assertEqual(websafe_decode(b""), b"")
        self.assertEqual(websafe_decode(b"Zg"), b"f")
        self.assertEqual(websafe_decode(b"Zm8"), b"fo")
        self.assertEqual(websafe_decode(b"Zm9v"), b"foo")
        self.assertEqual(websafe_decode(b"Zm9vYg"), b"foob")
        self.assertEqual(websafe_decode(b"Zm9vYmE"), b"fooba")
        self.assertEqual(websafe_decode(b"Zm9vYmFy"), b"foobar")

    def test_websafe_decode_unicode(self):
        self.assertEqual(websafe_decode(""), b"")
        self.assertEqual(websafe_decode("Zm9vYmFy"), b"foobar")

    def test_websafe_encode(self):
        self.assertEqual(websafe_encode(b""), "")
        self.assertEqual(websafe_encode(b"f"), "Zg")
        self.assertEqual(websafe_encode(b"fo"), "Zm8")
        self.assertEqual(websafe_encode(b"foo"), "Zm9v")
        self.assertEqual(websafe_encode(b"foob"), "Zm9vYg")
        self.assertEqual(websafe_encode(b"fooba"), "Zm9vYmE")
        self.assertEqual(websafe_encode(b"foobar"), "Zm9vYmFy")
```

## File: tests/test_webauthn.py
```python
# Copyright (c) 2019 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import json
import unittest

from fido2.utils import websafe_encode
from fido2.webauthn import (
    Aaguid,
    AuthenticatorSelectionCriteria,
    CollectedClientData,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    ResidentKeyRequirement,
)


class TestAaguid(unittest.TestCase):
    def test_aaguid(self):
        bs = b"\1" * 16
        a = Aaguid(bs)
        assert a
        assert a == bs
        assert bs == a

    def test_aaguid_none(self):
        a = Aaguid(b"\0" * 16)
        assert not a
        assert a == Aaguid.NONE
        assert Aaguid.NONE == a

    def test_aaguid_wrong_length(self):
        with self.assertRaises(ValueError):
            Aaguid(b"1234")

        with self.assertRaises(ValueError):
            Aaguid.fromhex("11" * 15)

        with self.assertRaises(ValueError):
            Aaguid(b"\2" * 17)

    def test_aaguid_parse(self):
        a = Aaguid.parse("00000000-0000-0000-0000-000000000000")
        assert a == Aaguid.NONE

        b = Aaguid.parse("01020304-0102-0304-0506-010203040506")
        assert b == Aaguid.fromhex("01020304010203040506010203040506")
        assert b == Aaguid(bytes.fromhex("01020304010203040506010203040506"))


class TestWebAuthnDataTypes(unittest.TestCase):
    def test_collected_client_data(self):
        o = CollectedClientData(
            b'{"type":"webauthn.create","challenge":"cdySOP-1JI4J_BpOeO9ut25rlZJueF16aO6auTTYAis","origin":"https://demo.yubico.com","crossOrigin":false}'  # noqa
        )

        assert o.type == "webauthn.create"
        assert o.origin == "https://demo.yubico.com"
        assert o.challenge == bytes.fromhex(
            "71dc9238ffb5248e09fc1a4e78ef6eb76e6b95926e785d7a68ee9ab934d8022b"
        )
        assert o.cross_origin is False

        assert (
            o.b64
            == "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiY2R5U09QLTFKSTRKX0JwT2VPOXV0MjVybFpKdWVGMTZhTzZhdVRUWUFpcyIsIm9yaWdpbiI6Imh0dHBzOi8vZGVtby55dWJpY28uY29tIiwiY3Jvc3NPcmlnaW4iOmZhbHNlfQ"  # noqa
        )
        assert o.hash == bytes.fromhex(
            "8b20a0b904b4747aacae71d55bf60b4eb2583f7e639f55f40baac23c2600c178"
        )

        assert o == CollectedClientData.create(
            "webauthn.create",
            "cdySOP-1JI4J_BpOeO9ut25rlZJueF16aO6auTTYAis",
            "https://demo.yubico.com",
        )

        o = CollectedClientData.create(
            "webauthn.create",
            "cdySOP-1JI4J_BpOeO9ut25rlZJueF16aO6auTTYAis",
            "https://demo.yubico.com",
            True,
        )
        assert o.cross_origin is True

    def test_authenticator_selection_criteria(self):
        o = AuthenticatorSelectionCriteria(
            authenticator_attachment="platform",
            require_resident_key=True,
            user_verification="required",
        )
        self.assertEqual(
            dict(o),
            {
                "authenticatorAttachment": "platform",
                "requireResidentKey": True,
                "residentKey": "required",
                "userVerification": "required",
            },
        )
        self.assertEqual(o.authenticator_attachment, "platform")
        self.assertEqual(o.require_resident_key, True)
        self.assertEqual(o.user_verification, "required")

        self.assertIsNone(
            AuthenticatorSelectionCriteria(
                authenticator_attachment="invalid"
            ).authenticator_attachment
        )

        self.assertIsNone(
            AuthenticatorSelectionCriteria(
                user_verification="invalid"
            ).user_verification
        )

        self.assertEqual(
            AuthenticatorSelectionCriteria(resident_key="invalid").resident_key,
            "discouraged",
        )

        o = AuthenticatorSelectionCriteria()
        self.assertEqual(o.resident_key, "discouraged")
        self.assertEqual(o.require_resident_key, False)
        self.assertIsNone(o.authenticator_attachment)
        self.assertIsNone(o.user_verification)

        o = AuthenticatorSelectionCriteria(require_resident_key=True)
        self.assertEqual(o.resident_key, ResidentKeyRequirement.REQUIRED)
        self.assertEqual(o.require_resident_key, True)

        o = AuthenticatorSelectionCriteria(resident_key=False)
        self.assertEqual(o.require_resident_key, False)

        o = AuthenticatorSelectionCriteria(resident_key="required")
        self.assertEqual(o.resident_key, ResidentKeyRequirement.REQUIRED)
        self.assertEqual(o.require_resident_key, True)

        o = AuthenticatorSelectionCriteria(resident_key="preferred")
        self.assertEqual(o.resident_key, ResidentKeyRequirement.PREFERRED)
        self.assertEqual(o.require_resident_key, False)

        o = AuthenticatorSelectionCriteria(resident_key="discouraged")
        self.assertEqual(o.resident_key, ResidentKeyRequirement.DISCOURAGED)
        self.assertEqual(o.require_resident_key, False)

    def test_rp_entity(self):
        o = PublicKeyCredentialRpEntity(name="Example", id="example.com")
        self.assertEqual(o, {"id": "example.com", "name": "Example"})
        self.assertEqual(o.id, "example.com")
        self.assertEqual(o.name, "Example")

        with self.assertRaises(TypeError):
            PublicKeyCredentialRpEntity(id="example.com")

        with self.assertRaises(TypeError):
            PublicKeyCredentialRpEntity()

    def test_user_entity(self):
        o = PublicKeyCredentialUserEntity(
            name="Example", id=b"user", display_name="Display"
        )
        self.assertEqual(
            o,
            {
                "id": websafe_encode(b"user"),
                "name": "Example",
                "displayName": "Display",
            },
        )
        self.assertEqual(o.id, b"user")
        self.assertEqual(o.name, "Example")
        self.assertEqual(o.display_name, "Display")

        with self.assertRaises(TypeError):
            PublicKeyCredentialUserEntity(name=b"user")

        with self.assertRaises(TypeError):
            PublicKeyCredentialUserEntity()

    def test_parameters(self):
        o = PublicKeyCredentialParameters(type="public-key", alg=-7)
        self.assertEqual(o, {"type": "public-key", "alg": -7})
        self.assertEqual(o.type, "public-key")
        self.assertEqual(o.alg, -7)

        p = PublicKeyCredentialParameters(type="invalid-type", alg=-7)
        assert p.type is None

        with self.assertRaises(TypeError):
            PublicKeyCredentialParameters("public-key")

        with self.assertRaises(TypeError):
            PublicKeyCredentialParameters()

    def test_descriptor(self):
        o = PublicKeyCredentialDescriptor(type="public-key", id=b"credential_id")
        self.assertEqual(
            o, {"type": "public-key", "id": websafe_encode(b"credential_id")}
        )
        self.assertEqual(o.type, "public-key")
        self.assertEqual(o.id, b"credential_id")
        self.assertIsNone(o.transports)

        o = PublicKeyCredentialDescriptor(
            type="public-key", id=b"credential_id", transports=["usb", "nfc"]
        )
        self.assertEqual(
            o,
            {
                "type": "public-key",
                "id": websafe_encode(b"credential_id"),
                "transports": ["usb", "nfc"],
            },
        )
        self.assertEqual(o.transports, ["usb", "nfc"])

        PublicKeyCredentialDescriptor(
            type="public-key", id=b"credential_id", transports=["valid_value"]
        )

        d = PublicKeyCredentialDescriptor(type="wrong-type", id=b"credential_id")
        assert d.type is None

        with self.assertRaises(TypeError):
            PublicKeyCredentialDescriptor(type="public-key")

        with self.assertRaises(TypeError):
            PublicKeyCredentialDescriptor()

    def test_creation_options(self):
        o = PublicKeyCredentialCreationOptions(
            rp=PublicKeyCredentialRpEntity(id="example.com", name="Example"),
            user=PublicKeyCredentialUserEntity(id=b"user_id", name="A. User"),
            challenge=b"request_challenge",
            pub_key_cred_params=[{"type": "public-key", "alg": -7}],
            timeout=10000,
            exclude_credentials=[{"type": "public-key", "id": b"credential_id"}],
            authenticator_selection={
                "authenticatorAttachment": "platform",
                "residentKey": "required",
                "userVerification": "required",
            },
            attestation="direct",
        )
        self.assertEqual(o.rp, {"id": "example.com", "name": "Example"})
        self.assertEqual(o.user, {"id": websafe_encode(b"user_id"), "name": "A. User"})
        self.assertIsNone(o.extensions)

        js = json.dumps(dict(o))
        o2 = PublicKeyCredentialCreationOptions.from_dict(json.loads(js))
        self.assertEqual(o, o2)

        o = PublicKeyCredentialCreationOptions.from_dict(
            {
                "rp": {"id": "example.com", "name": "Example"},
                "user": {"id": websafe_encode(b"user_id"), "name": "A. User"},
                "challenge": websafe_encode(b"request_challenge"),
                "pubKeyCredParams": [{"type": "public-key", "alg": -7}],
            }
        )
        self.assertEqual(o.user.id, b"user_id")
        self.assertEqual(o.challenge, b"request_challenge")
        self.assertIsNone(o.timeout)
        self.assertIsNone(o.authenticator_selection)
        self.assertIsNone(o.attestation)

        self.assertIsNone(
            PublicKeyCredentialCreationOptions(
                rp={"id": "example.com", "name": "Example"},
                user={"id": b"user_id", "name": "A. User"},
                challenge=b"request_challenge",
                pub_key_cred_params=[{"type": "public-key", "alg": -7}],
                attestation="invalid",
            ).attestation
        )

        js = json.dumps(dict(o))
        o2 = PublicKeyCredentialCreationOptions.from_dict(json.loads(js))

        self.assertEqual(o, o2)

    def test_request_options(self):
        o = PublicKeyCredentialRequestOptions(
            challenge=b"request_challenge",
            timeout=10000,
            rp_id="example.com",
            allow_credentials=[
                PublicKeyCredentialDescriptor(type="public-key", id=b"credential_id")
            ],
            user_verification="discouraged",
        )
        self.assertEqual(o.challenge, b"request_challenge")
        self.assertEqual(o.rp_id, "example.com")
        self.assertEqual(o.timeout, 10000)
        self.assertIsNone(o.extensions)

        js = json.dumps(dict(o))
        o2 = PublicKeyCredentialRequestOptions.from_dict(json.loads(js))
        self.assertEqual(o, o2)

        o = PublicKeyCredentialRequestOptions(challenge=b"request_challenge")
        self.assertIsNone(o.timeout)
        self.assertIsNone(o.rp_id)
        self.assertIsNone(o.allow_credentials)
        self.assertIsNone(o.user_verification)

        self.assertIsNone(
            PublicKeyCredentialRequestOptions(
                challenge=b"request_challenge", user_verification="invalid"
            ).user_verification
        )
```

