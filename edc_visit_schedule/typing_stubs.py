from typing import Protocol


class VisitScheduleFieldsProtocol(Protocol):
    def visit_code(self) -> str:
        ...

    def visit_code_sequence(self) -> int:
        ...

    def visit_schedule_name(self) -> str:
        ...

    def schedule_name(self) -> str:
        ...