import fsspec
import msgspec

from betfair_parser.spec.streaming import STREAM_DECODER, STREAM_MESSAGE


def parse(line: bytes) -> STREAM_MESSAGE:
    return STREAM_DECODER.decode(line)


def read_file(fsspec_url: str):
    with fsspec.open(fsspec_url, compression="infer") as f:
        for line in f:
            try:
                data = parse(line)
            except (msgspec.DecodeError, msgspec.ValidationError) as e:
                print("ERR", e)
                print(msgspec.json.decode(line))
                raise e
            yield data
