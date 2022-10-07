# Copyright (c) 2016-2021, Matteo Cafasso
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sysconfig
from pathlib import Path
from cffi import FFI


ffibuilder = FFI()
CLIPS_SOURCE = """
#include <clips.h>

/* Return true if the template is implied. */
bool ImpliedDeftemplate(Deftemplate *template)
{
    return template->implied;
}

/* User Defined Functions support. */
static void python_function(Environment *env, UDFContext *udfc, UDFValue *out);

int DefinePythonFunction(Environment *environment)
{
    return AddUDF(
        environment, "python-function",
        NULL, UNBOUNDED, UNBOUNDED, NULL,
        python_function, "python_function", NULL);
}
"""


with open("lib/clips.cdef") as cdef_file:
    CLIPS_CDEF = cdef_file.read()


extra_compile_args = sysconfig.get_config_var("CFLAGS").split()
extra_compile_args.extend(["-O3", "-fno-strict-aliasing"])

ffibuilder.set_source("_clips",
                      CLIPS_SOURCE,
                      sources=[str(p) for p in Path("clips_source").glob("*.c")],
                      include_dirs=["clips_source"],
                      extra_compile_args=extra_compile_args,
                    #   libraries=["clips"],
                      )


ffibuilder.cdef(CLIPS_CDEF)


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
