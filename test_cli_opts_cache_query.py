
import sys

from envycontrol import CACHE_FILE_PATH, main


def test_cache_query_shows_cache_file(capsys) -> None:
    sys.argv = [sys.argv[0], '--cache-query']
    main()

    captured = capsys.readouterr()
    actual = captured.out.strip()

    expected = ''
    with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
        expected = f.read()

    assert expected == actual
