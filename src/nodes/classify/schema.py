from typing import Literal

from pydantic import BaseModel, Field


class ClassificationResult(BaseModel):
    category: Literal["billing", "technical", "account", "account"] = Field(
        description="Główna kategoria zgłoszenia")

    priority: Literal["low", "medium", "high"] = Field(
        description="Priorytet zgłoszenia"
    )
    reasoning: str = Field(description="Krótkie uzasadnienie decyzji")
