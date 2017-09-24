from cffi import FFI

ffibuilder = FFI()

with open("../lib/clips.c") as source_file:
    CLIPS_SOURCE = source_file.read()

with open("../lib/clips.cffi") as header_file:
    CLIPS_HEADER = header_file.read()

ffibuilder.set_source("_clips",
                      CLIPS_SOURCE,
                      libraries=["clips"],
                      include_dirs=["../../clips/core"])
ffibuilder.cdef(CLIPS_HEADER)


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
