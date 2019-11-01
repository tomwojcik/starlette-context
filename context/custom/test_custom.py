from unittest.mock import patch

from fastapi import FastAPI
from starlette.testclient import TestClient

from context.custom import PreserveCustomContextMiddleware, get_context


class CustomContext(PreserveCustomContextMiddleware):
    def set_context(self, request) -> dict:
        return {"cid": self.get_correlation_id(request)}


cid_value = "test_cid"

app = FastAPI(title="PreserveIdentifiersExample")
app.add_middleware(CustomContext)


@app.get("/")
async def main():
    return {"cid": get_context()["cid"]}


client = TestClient(app)


def test_get_context():
    response = client.get("/", headers={CustomContext.cid: cid_value})
    assert response.status_code == 200
    assert response.json() == {"cid": cid_value}


@patch(
    "context.custom.middleware.PreserveCustomContextMiddleware.get_uuid",
    return_value=cid_value,
)
def test_generate_uuid_for_missing(_):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"cid": cid_value}
