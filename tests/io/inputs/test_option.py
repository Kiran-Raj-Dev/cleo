from __future__ import annotations

import pytest

from cleo.exceptions import LogicException
from cleo.exceptions import ValueException
from cleo.io.inputs.option import Option


def test_create():
    opt = Option("option")

    assert opt.name == "option"
    assert opt.shortcut is None
    assert opt.is_flag()
    assert not opt.accepts_value()
    assert not opt.requires_value()
    assert not opt.is_list()
    assert not opt.default


def test_dashed_name():
    opt = Option("--option")

    assert opt.name == "option"


def test_fail_if_name_is_empty():
    with pytest.raises(ValueException):
        Option("")


def test_fail_if_default_value_provided_for_flag():
    with pytest.raises(LogicException):
        Option("option", flag=True, default="default")


def test_fail_if_wrong_default_value_for_list_option():
    with pytest.raises(LogicException):
        Option("option", flag=False, is_list=True, default="default")


def test_shortcut():
    opt = Option("option", "o")

    assert opt.shortcut == "o"


def test_dashed_shortcut():
    opt = Option("option", "-o")

    assert opt.shortcut == "o"


def test_multiple_shortcuts():
    opt = Option("option", "-o|oo|-ooo")

    assert opt.shortcut == "o|oo|ooo"


def test_fail_if_shortcut_is_empty():
    with pytest.raises(ValueException):
        Option("option", "")


def test_optional_value():
    opt = Option("option", flag=False, requires_value=False)

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert not opt.requires_value()
    assert not opt.is_list()
    assert opt.default is None


def test_optional_value_with_default():
    opt = Option("option", flag=False, requires_value=False, default="Default")

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert not opt.requires_value()
    assert not opt.is_list()
    assert opt.default == "Default"


def test_required_value():
    opt = Option("option", flag=False, requires_value=True)

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert opt.requires_value()
    assert not opt.is_list()
    assert opt.default is None


def test_required_value_with_default():
    opt = Option("option", flag=False, requires_value=True, default="Default")

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert opt.requires_value()
    assert not opt.is_list()
    assert opt.default == "Default"


def test_list():
    opt = Option("option", flag=False, is_list=True)

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert opt.requires_value()
    assert opt.is_list()
    assert [] == opt.default


def test_multi_valued_with_default():
    opt = Option("option", flag=False, is_list=True, default=["foo", "bar"])

    assert not opt.is_flag()
    assert opt.accepts_value()
    assert opt.requires_value()
    assert opt.is_list()
    assert ["foo", "bar"] == opt.default
