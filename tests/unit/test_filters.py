import pytest
from unittest import mock
import j2f5

try:
    from ansible.plugins.filter import core as ansible_core_filters
except ImportError:
    pass


@pytest.fixture(scope="function")
def fixture_unload_ansible_module():
    """unloads ansible module"""
    import sys

    with mock.patch.dict(sys.modules, {"ansible.plugins.filter": None}):
        yield


def ansible_not_available():
    """ansible is not available"""
    try:
        ansible_core_filters
    except NameError:
        return True
    return False


class Test_ansible_filters:
    @staticmethod
    def test_dict():
        """must return dict"""
        assert isinstance(j2f5.ansible_filters(), dict)

    @staticmethod
    @pytest.mark.skipif(ansible_not_available(), reason="ansible not available")
    def test_load():
        """test ansible filters (when ansible available)"""
        # call ansible_filters() and save to dict
        j2f5_ansible_filters = j2f5.ansible_filters()

        # when ansible filters available, check each filter
        if ansible_core_filters:
            for filter in ansible_core_filters.FilterModule().filters():
                assert filter in j2f5_ansible_filters

    @pytest.mark.usefixtures("fixture_unload_ansible_module")
    def test_ansible_unavailable(self):
        """test behavior loading ansible filters when ansible is unavailable"""
        # call ansible_filters() and save to dict
        j2f5_ansible_filters = j2f5.ansible_filters()

        # ansible_filters must be empty
        assert not j2f5_ansible_filters


class Test_extra_filters:
    @staticmethod
    def test_dict():
        """extra_filters must return dict"""
        assert isinstance(j2f5.extra_filters(), dict)

    @staticmethod
    @pytest.mark.skipif(ansible_not_available(), reason="ansible not available")
    def test_contain_ansible_filters():
        """test that extra filters contain ansible filters"""

        # call ansible_filters() and save to dict
        j2f5_ansible_filters = j2f5.ansible_filters()

        # call extra_filters() and save to dict
        j2f5_extra_filters = j2f5.extra_filters()

        for filter in j2f5_ansible_filters:
            assert filter in j2f5_extra_filters
