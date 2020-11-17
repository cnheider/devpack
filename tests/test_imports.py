#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 01/08/2020
           '''

__all__ = []


def test_import():
  import devpack
  print(devpack.__version__)


def test_apppath_import():
  import apppath
  print(apppath.__version__)


def test_draugr_import():
  import draugr
  print(draugr.__version__)


def test_warg_import():
  import warg
  print(warg.__version__)
