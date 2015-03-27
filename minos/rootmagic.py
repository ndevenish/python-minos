# Based on rootpy's magic.py copyright 2012

from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

from rootpy.logger.magic import _keep_alive, get_dll

import contextlib
import ctypes
import ROOT

def get_seterrcb():
    ErrMsgCallback_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

    dll = get_dll("libCint")
    SetErrorCallback = None
    GetErrorCallback = None
    try:
        if dll:
            SetErrorCallback = dll.G__set_errmsgcallback
            GetErrorCallback = dll.G__get_errmsgcallback
    except AttributeError:
        pass

    if not SetErrorCallback:
        logger.warning("Could not find SetErrorCallback function in dll")
        return lambda x: None

    SetErrorCallback.argtypes = ErrMsgCallback_t,
    GetErrorCallback.restype = ErrMsgCallback_t

    def _SetErrorMessageCallback(fn):
        # Force evaluation of a class inside ROOT, to force loading of TPyApplication
        assert ROOT.gApplication
        handler = ErrMsgCallback_t(fn)
        _keep_alive.append(handler)
        retval = None
        if GetErrorCallback is not None:
            retval = GetErrorCallback()
            retval.argtypes = ctypes.c_char_p,
        SetErrorCallback(handler)
        # Clean up if we now no-longer need this method
        if retval in _keep_alive:
            _keep_alive.remove(retval)
        return retval

    return _SetErrorMessageCallback


set_error_callback = get_seterrcb()

@contextlib.contextmanager
def suppress():
    def _discard(msg):
        pass
    old = set_error_callback(_discard)
    yield
    set_error_callback(old)