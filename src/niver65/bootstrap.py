import inspect
from src.adbs.config import setup

# TODO: Verificar necessidade desse arquivo
# setup()
# from src.adbs.service_layer import handlers, messagebus, unit_of_work
#
#
# def bootstrap(
#         start_orm: bool = True,
#         uow: unit_of_work.AbstractUnitOfWork = unit_of_work.KafkaUnitOfWork()
# ) -> messagebus.MessageBus:
#     dependencies = {'uow': uow}
#
#     injected_command_handlers = {
#         command_type: inject_dependencies(handler, dependencies)
#         for command_type, handler in handlers.COMMAND_HANDLERS.items()
#     }
#
#     return messagebus.MessageBus(
#         uow=uow,
#         command_handlers=injected_command_handlers,
#     )
#
#
# def inject_dependencies(handler, dependencies):
#     params = inspect.signature(handler).parameters
#     deps = {
#         name: dependency
#         for name, dependency in dependencies.items()
#         if name in params
#     }
#     return lambda message: handler(message, **deps)
# #