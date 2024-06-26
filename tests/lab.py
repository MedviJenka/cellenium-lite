from typing import Optional
from dataclasses import dataclass


value_dictionary = {
    "access_all_calls": "tenant/calls/access",
    "user_own_group_call_access": "tenant/calls/access",
    "play_media_related_calls": "tenant/calls/plbk",
    "download_media_related_calls": "tenant/calls/dwnld",
    "email_media_related_calls": "tenant/calls/email",
    "tag_calls": "tenant/calltag/r,tenant/calltag/rw",
    "add_notes": "tenant/note/r,tenant/note/rw",
    "delete_notes": "tenant/note/del",
    "delete_calls": "tenant/calls/del",
    "create_modify_recording_profiles": "tenant/recrdprfl/r,tenant/recrdprfl/rw",
    "create_modify_security_profiles": "tenant/accessprfl/r,tenant/accessprfl/rw",
    "create_modify_tags": "tenant/tags/r,tenant/ta/rw",
    "configure_system": "tenant/system/r,tenant/system/rw",
    "audit_access_export": "tenant/audit/r",
}

# shirels function
data_token = "tenant/admins/r:* tenant/admins/rw:* tenant/calls/access:* tenant/calls/plbk:* tenant/calls/dwnld:* tenant/calls/email:* tenant/calltag/r:* tenant/calltag/rw:* tenant/note/r:* tenant/note/rw:* tenant/note/del:* tenant/calls/del:* tenant/recrdprfl/r:* tenant/recrdprfl/rw:* tenant/accessprfl/r:* tenant/accessprfl/rw:* tenant/tags/r:* tenant/tags/rw:* tenant/system/r:* tenant/system/rw:* tenant/audit/r:* tenant/users/r:* tenant/activitylog/r:*"

# efrat function
local_dd = {
    "play_media_related_calls": "TRUE",
    "download_media_related_calls": "",
    "email_media_related_calls": "",
    "tag_calls": "",
    "add_notes": "",
    "delete_notes": "",
    "delete_calls": "TRUE",
    "create_modify_recording_profiles": "",
    "create_modify_security_profiles": "",
    "create_modify_tags": "TRUE",
    "configure_system": "",
    "audit_access_export": "",
}


@dataclass
class AccessTokenValidator:
    """
    :TODO:

        1. The function receives a token and a scope ............................................................. DONE
        2. It processes the token and splits it into a list at each comma ........................................ DONE
        3. It then processes the new list and splits each value into two parts, before the colon and after ....... DONE
        4. Now it starts iterating through the ATTR from the third position ...................................... DONE
        5. It checks each value in ATTR to see if it is TRUE ..................................................... DONE
        6. If yes, it checks what the VALUE of that KEY is in the DICTIONARY ..................................... DONE
        7. It takes the found VALUE and checks if it is present in the TOKEN ..................................... DONE
        8. If found, it checks if the position [1] is identical to the SCOPE that the function received .......... DONE
        9. If yes, it performs a POP - removing this value from the list.
           If not, it raises an EXCEPTION that the SCOPE is different from the permissions that were given,
           and of course, it mentions what was expected and what is actually there.
           If there is more than one VALUE, it repeats this until all VALUES are exhausted.
           Once it finishes iterating through all the ATTR, it exits the loop.
           Now it checks if any value remains in the list.
           If yes, it raises an EXCEPTION that there are more roles in the token than there should be and the test fails.

    """
    data_token: str

    @property
    def get_token_values(self) -> list:

        # takes all data right to column

        _list = []
        tokens = self.data_token.split()

        for token in tokens:
            clean_token = token.split(':')[1]
            _list.append(clean_token)

        return _list

    def get_token_keys(self, disregard: Optional[bool] = True) -> list:

        # takes all data left to column

        _list = []
        tokens = self.data_token.split()

        # always disregards these five permanent values
        disregard_list = [
            'tenant/calls/access',
            'tenant/calls/plbk',
            'tenant/calls/dwnld',
            'tenant/calls/email',
            'tenant/note/del',
            'tenant/calls/del'
        ]

        for token in tokens:
            clean_token = token.split(':')[0]
            _list.append(clean_token)

        if disregard:
            for each in disregard_list:
                _list.remove(each)

        return _list

    @staticmethod
    def get_all_keys_with_true_value_from_dict(dd_dict: dict) -> list:
        # return all keys with TRUE
        _list = []
        for key, value in dd_dict.items():
            if value == 'TRUE':
                _list.append(key)
        return _list

    def validate_token_displays_r_or_rw(self) -> None:

        outcome_list = []
        exception_list = []

        for token in self.get_token_keys(disregard=True):
            if token.endswith('/r') or token.endswith('/rw'):
                outcome_list.append(token)
            else:
                exception_list.append(token)

        if exception_list:
            raise AssertionError(f' r and rw not found in {exception_list}')

    def validate_token_data_displays_asterisks_my_group(self, expected: str) -> None:

        # expected will validate: *, my, or group

        outcome_list = []
        exception_list = []

        for token in self.get_token_values:
            outcome = token.split(':')
            if expected not in outcome:
                outcome_list.append(f'{expected} not found in token: {outcome}')
                print(f'{expected} not found in {token}')
                exception_list.append(token)

        if outcome_list:
            raise AssertionError(f'{expected} not found in {self.data_token}')

    @property
    def compare_data_driven_to_value_dictionary(self) -> list:
        _list = []
        _list_2 = []
        for key, value in value_dictionary.items():
            for each in self.get_all_keys_with_true_value_from_dict(dd_dict=local_dd):
                if key == each:
                    if ',' in value:
                        _list.extend(value.split(','))
                    else:
                        _list.append(value)
        return _list

    # @property
    # def compare_data_driven_to_value_dictionary(self) -> list:
    #     _list = []
    #     for key, value in value_dictionary.items():
    #         for each in self.get_all_keys_with_true_value_from_dict(dd_dict=local_dd):
    #             if key == each:
    #                 _list.append(value)
    #     return _list

    def validate_values_in_data_token(self) -> None:

        all_values = self.compare_data_driven_to_value_dictionary
        all_keys = self.get_token_keys(disregard=False)

        for value in all_values:
            if value in all_keys:
                all_keys.remove(value)
                print(f'{value}: PASSED')
            else:
                raise AssertionError(f"Scope mismatch: Expected {self.data_token}, found different permissions. {all_keys}")


if __name__ == '__main__':
    access = AccessTokenValidator(data_token=data_token)
    access.validate_values_in_data_token()
