import pytest
import j2f5


class Test_j2_environment_params:
    @staticmethod
    def test_dict():
        """j2_environment_params must return dict"""
        assert isinstance(j2f5.j2_environment_params(), dict)

    @staticmethod
    def test_custom_delimeters():
        """custom delimeters in the _TEMPLATING_NAMESPACE must update j2 environment params"""
        # our custom delimter test set
        delimeter_test_set = {
            "block_start_string": "<start>",
            "block_end_string": "<end>",
            "variable_start_string": "<var=>",
            "variable_end_string": "<=var>",
            "comment_start_string": "<#>",
            "comment_end_string": "</#>",
        }
        # mocked ctx, place delimeter_test_set in _TEMPLATING_NAMESPACE
        ctx_mock = {j2f5._TEMPLATING_NAMESPACE: delimeter_test_set}

        # update context
        j2f5.alter_context(ctx_mock)

        # generate j2 environment parameters dict
        j2_environment_params = j2f5.j2_environment_params()

        # iterate delimeter test set and check that the values match
        for (delimeter, value) in delimeter_test_set.items():
            assert j2_environment_params.get(delimeter) == value
