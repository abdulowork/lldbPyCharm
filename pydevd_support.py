import os
from pathlib import Path
import _ctypes
import platform

__pydevd_arm_library_path = os.environ.get('PYDEVD_ARM_LIBRARY_PATH') or '/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/pydevd_attach_to_process/linux_and_mac/attach_arm64.dylib'
__pydevd_configured = False


def configure_pydevd():
    global __pydevd_configured
    if __pydevd_configured:
        return

    try:
        processor = platform.processor()
        if processor != 'arm':
            print(f'lldb is running in {processor} arch, skipping arm fix')
            return

        if not Path(__pydevd_arm_library_path).exists():
            print(f"Couldn't find arm64 library for pydevd at: {__pydevd_arm_library_path}, skipping arm fix")
            return

        library_handle = _ctypes.dlopen(
            __pydevd_arm_library_path,
            os.RTLD_NOW
        )
        if library_handle == 0:
            print("Library didn't load")
            return
        print(f"Library handle is {hex(library_handle)}")

        function = 'DoAttach'
        do_attach_address = _ctypes.dlsym(library_handle, function)
        if do_attach_address == 0:
            print(f"Couldn't find {function} in library at {library_handle}")
            return
        print(f"{function} loaded at {hex(do_attach_address)}")
    except Exception as e:
        print(f"Something went wrong while loading pydevd library: {e}")
    finally:
        __pydevd_configured = True
