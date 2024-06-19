from src.models.track import Track


def test_track():
    test_track = Track(name='test_name', album='test_album', artists=['test_artist'])

    assert len(test_track.artists) == 1
