import ctypes

from ._callbacks import _create_wrapped_callback


def _create_wrapped_attribute_callback(callback):
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(
            None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p
        )

        # We wrap in order to decode string representation.
        # There is no SWIG layer here, as the capi calls us directly
        # using a function pointer. This means that the arguments
        # are bytearrays.
        def decoder_callback(id, key, value):
            decoded_key = key.decode(encoding="utf-8")
            decoded_value = value.decode(encoding="utf-8")
            callback(id, decoded_key, decoded_value)

        return _create_wrapped_callback(decoder_callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_strid_attribute_callback(callback):
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(
            None, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
        )

        # We wrap in order to decode string representation.
        # There is no SWIG layer here, as the capi calls us directly
        # using a function pointer. This means that the arguments
        # are bytearrays.
        def decoder_callback(id, key, value):
            decoded_id = id.decode(encoding="utf-8")
            decoded_key = key.decode(encoding="utf-8")
            decoded_value = value.decode(encoding="utf-8")
            callback(decoded_id, decoded_key, decoded_value)

        return _create_wrapped_callback(decoder_callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_import_string_id_callback(callback):
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)

        # We wrap in order to decode string representation.
        # There is no SWIG layer here, as the capi calls us directly
        # using a function pointer. This means that the arguments
        # are bytearrays.
        def decoder_callback(id):
            decoded_id = id.decode(encoding="utf-8")
            return callback(decoded_id)

        return _create_wrapped_callback(decoder_callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_import_integer_id_callback(callback):
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_notify_id_callback(callback):
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(None, ctypes.c_int)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)
