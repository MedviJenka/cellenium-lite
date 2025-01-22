from bini.engine.utils import BiniUtils


bini = BiniUtils()
IMAGE = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\bini\test\img_1.png'
SAMPLE_IMAGE = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\bini\test\img.png'


def test_user_is_displayed() -> None:
    response = bini.run(
        image_path=IMAGE,
        prompt='Is Joni Sherman displayed on the right side of the screen '
               'and how many rows with blue icon with play button are displayed? '
               '** return an integer as an answer **')
    assert 'Passed' in response
    assert '1' or 'once' in response


def test_find_icon_sample() -> None:
    response = bini.run(image_path=IMAGE,
                        sample_image=SAMPLE_IMAGE,
                        prompt='how many times the icon sample is displayed in provided image?')
    assert '10' in response
    assert 'Passed' in response


def test_bini_code() -> None:
    bini.get_browser_recorder_list()
    # bini.bini_code()
