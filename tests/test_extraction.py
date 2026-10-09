from clausewise.services.extraction import extract_document_bytes


def test_extracts_txt_lines_with_references() -> None:
    segments = extract_document_bytes('sample.txt', b'First line\n\nSecond line\n')
    assert len(segments) == 2
    assert segments[0].reference == 'Line 1'
    assert segments[1].reference == 'Line 3'
    assert segments[1].text == 'Second line'

