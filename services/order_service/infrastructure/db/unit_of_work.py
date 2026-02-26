from sqlalchemy.orm import Session, sessionmaker


class UnitOfWork:
    """Context manager for managing database transactions.

    Implements the Unit of Work pattern to handle session creation,
    commits, and rollbacks within a context manager.
    """
    def __init__(self, session_factory: sessionmaker):
        """Initialize UnitOfWork with a session factory.

        Parameters:
            session_factory (sessionmaker): SQLAlchemy session factory.

        Returns:
            None
        """
        self.session_factory = session_factory

    def __enter__(self):
        """Enter the context manager and create a session.

        Returns:
            UnitOfWork: The context manager instance.
        """
        self.session: Session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager and handle session cleanup.

        Rolls back the transaction if an exception occurred,
        otherwise the session remains open for the user to commit.
        Closes the session in all cases.

        Parameters:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.

        Returns:
            None
        """
        if exc_type:
            self.session.rollback()
        self.session.close()

    def commit(self):
        """Commit the current transaction.

        Returns:
            None
        """
        self.session.commit()
