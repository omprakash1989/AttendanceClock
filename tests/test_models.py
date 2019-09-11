"""
This module is used to write the test cases for database models.
Added couple of initial model tests.

The test cases written in this module uses fixtures therefore
this file needs to be run using py test, use below command to run this file.
py.test tests/test_models.py
"""


def test_environment_and_migration(db):
    """
    This test case test the application environment and database migration
    by internally calling fixtures named db written in conftest.py
    The intention of this test case is to call db fixture.
    """
    assert True


def test_environment_and_migration_and_session(session):
    """
    This test case test the application environment, database migration and sessions
    by internally calling fixtures named session written in conftest.py
    The intention of this test case is to call session fixture.
    """
    assert True
