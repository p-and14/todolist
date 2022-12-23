from pytest_factoryboy import register

from tests import factories

# Factories
register(factories.UserFactory)
register(factories.BoardFactory)
register(factories.CategoryFactory)
register(factories.GoalFactory)
register(factories.BoardParticipantFactory)
