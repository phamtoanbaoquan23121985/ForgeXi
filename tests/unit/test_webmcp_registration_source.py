from pathlib import Path


def test_browser_registration_uses_current_document_model_context_contract():
    source = Path("apps/dashboard/public/forgexi-webmcp.js").read_text()
    assert "document.modelContext.registerTool" in source
    assert "navigator.modelContext" not in source
    assert "provideContext" not in source
    assert "clearContext" not in source
    assert "Authorization" not in source
    assert "NEBIUS_API_KEY" not in source
