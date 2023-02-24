import bz2
import tarfile

import fsspec
import msgspec

from betfair_parser.spec.streaming import STREAM_DECODER, STREAM_MESSAGE


def parse(line: bytes) -> STREAM_MESSAGE:
    return STREAM_DECODER.decode(line)


def iter_parse(file_like):
    for line in file_like:
        try:
            data = parse(line)
        except (msgspec.DecodeError, msgspec.ValidationError) as e:
            print("ERR", e)
            print(msgspec.json.decode(line))
            raise e
        yield data


def read_file(fsspec_url: str):
    with fsspec.open(fsspec_url, compression="infer") as f:
        yield from iter_parse(f)


def read_tar_file(tar_file: str, file_path: str):
    tf = tarfile.open(tar_file)
    assert file_path in tf.getnames(), f"Can't find `{file_path}` in {tf.getnames()[:5]}... "
    f = tf.extractfile(file_path)
    if file_path.endswith("bz2"):
        f = bz2.open(f)
    yield from iter_parse(f)
