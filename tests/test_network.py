import pytest
import uuid
import royalherald as h


async def echo_request_handler(message):
    return message


def test_package_serialization():
    pkg = h.Package({"ciao": "ciao"},
                    source=str(uuid.uuid4()),
                    destination=str(uuid.uuid4()),
                    source_conv_id=str(uuid.uuid4()),
                    destination_conv_id=str(uuid.uuid4()))
    assert pkg == h.Package.from_dict(pkg.to_dict())
    assert pkg == h.Package.from_json_string(pkg.to_json_string())
    assert pkg == h.Package.from_json_bytes(pkg.to_json_bytes())


def test_request_creation():
    request = h.Request("pytest", {"testing": "is fun", "bugs": "are less fun"})
    assert request == h.Request.from_dict(request.to_dict())
