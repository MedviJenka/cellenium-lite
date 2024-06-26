from core.engine.ai_engine import Bini


bini = Bini()


def test_user_is_displayed() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png",
        prompt='Is Efrat Lang displayed on the right side of the screen? at the end type Passed if yes')
    assert 'Passed' in response


def test_meeting_insights() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_5.png",
        prompt='validate the dates are displayed are from 4/4/24 to 14/5/24, parse the date type as day/month/year')
    assert 'Passed' in response


def test_user_is_not_displayed() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png",
        prompt='Is Evgeny Petrusenko displayed on the right of the screen?')
    assert 'Fail' in response


def test_outgoing_calls_under_external_p2p() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_3.png",
        prompt='how many Outgoing" has the call type "External p2p')
    assert '3' or 'Three' in response


def test_count_rows() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_1.png",
        prompt='count all the rows that starts with blue play button on the left, expected result is 10')
    assert 'Passed' in response


def test_no_rows() -> None:
    response = bini.image(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_2.png",
                          prompt='are there any rows?, expected is: No Rows')
    assert 'Passed' in response
