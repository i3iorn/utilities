from src.utilities.query_builder.base import BuilderBase


class TriggerBuilder(BuilderBase):
    def create_trigger(self, name: str, event: str, table: str, action: str) -> str:
        return f"CREATE TRIGGER {name} {event} ON {table} FOR EACH ROW {action}"
