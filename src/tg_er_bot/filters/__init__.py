from .role import AdminFilter


def setup(dp):  # TODO
    # dp.filters_factory.bind(BlockFilter, event_handlers=[dp.message_handlers])
    # dp.filters_factory.bind(CreatorFilter)
    dp.filters_factory.bind(AdminFilter)
