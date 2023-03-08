import os
from typing import Dict, Any

from lldb import SBDebugger, SBCommandReturnObject

from pydevd_support import configure_pydevd

configure_pydevd()

def test_breakpoint(
    debugger: SBDebugger,
    command: str,
    result: SBCommandReturnObject,
    dict: Dict[str, Any]
):
    print('Hello\n')
    print('World!\n')


# i.e. "test" for this file
module = os.path.splitext(os.path.basename(__file__))[0]


def __lldb_init_module(debugger: SBDebugger, dict):
    for function in [
        test_breakpoint,
    ]:
        print(f'\nRegistering {module}.{function.__name__}. Call "{function.__name__}" from lldb to run the script')
        debugger.HandleCommand(f'command script add -f {module}.{function.__name__} {function.__name__}')
    print(f'\nAttach to lldb at: {os.getpid()}\n')
