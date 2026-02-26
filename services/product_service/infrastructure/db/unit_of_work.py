"""Unit of Work pour le service Product."""

from typing import Self
from sqlalchemy.orm import Session, sessionmaker


class UnitOfWork:
    """Gestionnaire de transactions base de donnees."""

    def __init__(self, session_factory: sessionmaker) -> None:
        """Initialise l'UoW avec une factory de sessions."""
        self.session_factory = session_factory

    def __enter__(self) -> Self:
        """Ouvre une nouvelle session."""
        self.session: Session = self.session_factory()
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: object) -> None:
        """Ferme la session, rollback en cas d'erreur."""
        if exc_type:
            self.session.rollback()
        self.session.close()

    def commit(self) -> None:
        """Valide la transaction en cours."""
        self.session.commit()
