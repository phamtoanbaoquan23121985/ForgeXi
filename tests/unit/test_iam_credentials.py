from services.runtime.iam_credentials import IAMCredentialProvider


class Clock:
    now = 1000.0
    def __call__(self):
        return self.now


def test_iam_provider_uses_reported_expiry_and_refreshes():
    clock = Clock()
    issued = []
    def exchange():
        issued.append(1)
        return {"accessToken": f"token-{len(issued)}", "expiresIn": "120"}

    provider = IAMCredentialProvider(exchange, refresh_skew_seconds=10, clock=clock)
    first = provider.get()
    assert first.value == "token-1"
    assert first.expires_at == 1120.0
    clock.now = 1111.0
    assert provider.get().value == "token-2"


def test_iam_provider_repr_does_not_expose_access_token():
    provider = IAMCredentialProvider(lambda: {"accessToken":"private","expiresIn":"120"})
    provider.get()
    assert "private" not in repr(provider)
