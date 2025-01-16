# -*- coding: utf-8 -*-
# code generated by Prisma. DO NOT EDIT.
# pyright: reportUnusedImport=false
# fmt: off

# global imports for type checking
from builtins import bool as _bool
from builtins import int as _int
from builtins import float as _float
from builtins import str as _str
import sys
import decimal
import datetime
from typing import (
    TYPE_CHECKING,
    Optional,
    Iterable,
    Iterator,
    Sequence,
    Callable,
    ClassVar,
    NoReturn,
    TypeVar,
    Generic,
    Mapping,
    Tuple,
    Union,
    List,
    Dict,
    Type,
    Any,
    Set,
    overload,
    cast,
)
from typing_extensions import TypedDict, Literal


LiteralString = str
# -- template models.py.jinja --
from pydantic import BaseModel

from . import fields, actions
from ._types import FuncType
from ._builder import serialize_base64
from ._compat import PYDANTIC_V2, ConfigDict

if TYPE_CHECKING:
    from .client import Prisma


_PrismaModelT = TypeVar('_PrismaModelT', bound='_PrismaModel')


class _PrismaModel(BaseModel):
    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(
            use_enum_values=True,
            arbitrary_types_allowed=True,
            populate_by_name=True,
        )
    elif not TYPE_CHECKING:
        from ._compat import BaseConfig

        class Config(BaseConfig):
            use_enum_values: bool = True
            arbitrary_types_allowed: bool = True
            allow_population_by_field_name: bool = True
            json_encoders: Dict[Any, FuncType] = {
                fields.Base64: serialize_base64,
            }

    # TODO: ensure this is required by subclasses
    __prisma_model__: ClassVar[str]


class BaseUser(_PrismaModel):
    __prisma_model__: ClassVar[Literal['User']] = 'User'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.UserActions[_PrismaModelT]':
        from .client import get_client

        return actions.UserActions[_PrismaModelT](client or get_client(), cls)


class BaseProblem(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Problem']] = 'Problem'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.ProblemActions[_PrismaModelT]':
        from .client import get_client

        return actions.ProblemActions[_PrismaModelT](client or get_client(), cls)


class BaseProblem_code(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Problem_code']] = 'Problem_code'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.Problem_codeActions[_PrismaModelT]':
        from .client import get_client

        return actions.Problem_codeActions[_PrismaModelT](client or get_client(), cls)


class BaseSubmission(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Submission']] = 'Submission'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.SubmissionActions[_PrismaModelT]':
        from .client import get_client

        return actions.SubmissionActions[_PrismaModelT](client or get_client(), cls)


class BaseContest(_PrismaModel):
    __prisma_model__: ClassVar[Literal['Contest']] = 'Contest'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.ContestActions[_PrismaModelT]':
        from .client import get_client

        return actions.ContestActions[_PrismaModelT](client or get_client(), cls)


class BaseContestProblem(_PrismaModel):
    __prisma_model__: ClassVar[Literal['ContestProblem']] = 'ContestProblem'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.ContestProblemActions[_PrismaModelT]':
        from .client import get_client

        return actions.ContestProblemActions[_PrismaModelT](client or get_client(), cls)


class BaseContestParticipant(_PrismaModel):
    __prisma_model__: ClassVar[Literal['ContestParticipant']] = 'ContestParticipant'  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def prisma(cls: Type[_PrismaModelT], client: Optional['Prisma'] = None) -> 'actions.ContestParticipantActions[_PrismaModelT]':
        from .client import get_client

        return actions.ContestParticipantActions[_PrismaModelT](client or get_client(), cls)


