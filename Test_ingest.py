from app.rag.ingest import chunk_text


def test_chunk_text_basic():
    text = "word " * 500  # long text
    chunks = chunk_text(text, source="unit-test", chunk_size=100, overlap=20)
    assert len(chunks) > 1
    for c in chunks:
        assert c.metadata["source"] == "unit-test"
        assert len(c.text) <= 100


def test_chunk_text_empty():
    assert chunk_text("", source="empty") == []


def test_chunk_text_short():
    chunks = chunk_text("hello world", source="short", chunk_size=1000, overlap=100)
    assert len(chunks) == 1
    assert chunks[0].text == "hello world"
