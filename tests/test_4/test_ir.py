from core.modules.decorators import negative
from bini.infrastructure.ai_utils import IRBiniUtils


bini = IRBiniUtils(use_agents=False)  # use agents can be more accurate but more expensive and a slower runtime


def test_user_is_displayed() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png",
        prompt='Is Efrat Lang displayed on the right side of the screen? at the end type Passed if yes')
    assert 'Passed' in response


def test_meeting_insights() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_5.png",
        prompt='validate the dates are displayed are from 4/4/24 to 13/5/24, parse the date type as day/month/year')
    assert 'Passed' in response


@negative
def test_meeting_insights_negative() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_5.png",
        prompt='validate the dates are displayed are from 4/4/24 to 14/5/24, parse the date type as day/month/year')
    assert 'Failed' in response


def test_user_is_not_displayed() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png",
        prompt='Is Evgeny Petrusenko displayed on the right of the screen?')
    assert 'Fail' or 'No' in response


def test_outgoing_calls_under_external_p2p() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_3.png",
        prompt='how many Outgoing" has the call type "External p2p')
    assert '3' or 'Three' in response


@negative
def test_outgoing_calls_under_external_p2p() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_3.png",
        prompt='how many Outgoing" has the call type "External p2p, return answer in integer')
    assert '0' in response


def test_count_rows() -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_1.png",
        prompt='count all the rows that starts with blue play button on the left, expected result is 10, return hole answer with integer at the end')
    assert '10' in response


def test_no_rows() -> None:
    response = bini.run(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_2.png",
                        prompt='are there any rows?, expected is: No Rows')
    assert 'Passed' in response


def call_duration_in_specific_row(duration: str, row: int) -> None:
    response = bini.run(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_3.png",
        prompt=f'list all rows with circle icons, under call duration header locate the {duration} and row number: {row}, return me the full time answer')
    assert duration in response


def test_call_duration_in_specific_row_3() -> None:
    call_duration_in_specific_row(duration='00:02:26', row=3)


def test_call_duration_in_specific_row_4() -> None:
    call_duration_in_specific_row(duration='00:01:54', row=4)


def test_call_duration_in_specific_row_5() -> None:
    call_duration_in_specific_row(duration='00:01:54', row=5)


def test_complex_metadata_validations() -> None:
    image = r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_11.png'
    bini.validate_call_metadata_for_each_row(image=image,
                                             row=1,
                                             start_time='11:52:10',
                                             direction=None,
                                             release_cause='Normal',
                                             call_expiration='Jun 25, 2025',
                                             recording_type='Audio')


@negative
def test_complex_metadata_validations_1() -> None:
    image = r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_11.png'
    bini.validate_call_metadata_for_each_row(image=image,
                                             row=1,
                                             start_time='11:52:00',
                                             direction=None,
                                             release_cause='Normal',
                                             call_expiration='Jun 25, 2024',
                                             recording_type='Audio')


@negative
def test_complex_metadata_validations_2() -> None:
    image = r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_11.png'
    bini.validate_call_metadata_for_each_row(image=image,
                                             row=1,
                                             start_time='11:70:00',
                                             direction=None,
                                             release_cause='Normal',
                                             call_expiration='Nov 25, 2023',
                                             recording_type='Audio')


@negative
def test_user_name_displayed_in_recording_row_1() -> None:
    bini.validate_call_metadata_for_each_row(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_1.png',
                                             row=1,
                                             recording_type='Audio',
                                             user_name='st_user2')


def test_user_name_displayed_in_recording_row_2() -> None:
    bini.validate_call_metadata_for_each_row(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_1.png',
                                             row=1,
                                             recording_type='Audio',
                                             user_name='st_user1')


@negative
def test_user_name_displayed_in_recording_row_3() -> None:
    bini.validate_call_metadata_for_each_row(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_1.png',
                                             row=1,
                                             recording_type='Audio',
                                             user_name='teams_test_user')


def test_duration_displayed_in_recording_row() -> None:
    bini.validate_call_metadata_for_each_row(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img_1.png',
                                             row=1,
                                             duration='00:04:44')
