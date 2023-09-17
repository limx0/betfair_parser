import bz2
import tarfile
import typing

import msgspec

from betfair_parser.spec.streaming import stream_decode


def iter_tar_file(tar_file: str, file_path: str):
    tf = tarfile.open(tar_file)
    assert file_path in tf.getnames(), f"Can't find `{file_path}` in {tf.getnames()[:5]}... "
    f = tf.extractfile(file_path)
    assert f is not None
    if file_path.endswith("bz2"):
        f = bz2.open(f)
    yield from iter_stream(f)  # type: ignore


def iter_stream(file_like: typing.BinaryIO):
    for line in file_like:
        try:
            data = stream_decode(line)
        except (msgspec.DecodeError, msgspec.ValidationError) as e:
            print(f"{type(e).__name__}: {e}\n{msgspec.json.decode(line)}")
            raise e
        yield data
