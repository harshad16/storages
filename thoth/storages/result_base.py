"""Adapter for storing analysis results onto a persistence remote store."""

import typing

from .base import StorageBase
from .ceph import CephStore
from .result_schema import RESULT_SCHEMA
from .exceptions import SchemaError


class ResultStorageBase(StorageBase):
    """Adapter base for storing results."""

    RESULT_TYPE = None

    def __init__(self, *, host: str=None, key_id: str=None, secret_key: str=None, bucket: str=None, region: str=None):
        assert self.RESULT_TYPE is not None, "Make sure you define RESULT_TYPE in derived classes " \
                                             "to distinguish between adapter type instances."
        self.ceph = CephStore(
            self.RESULT_TYPE,
            host=host,
            key_id=key_id,
            secret_key=secret_key,
            bucket=bucket,
            region=region
        )

    @classmethod
    def get_document_id(cls, document: dict) -> str:
        """Get document id under which the given document should be stored."""
        # We use hostname that matches pod id generated by OpenShift so document id
        # matches returned pod id on user API endpoint.
        return document['metadata']['hostname']

    def is_connected(self) -> bool:
        """Check if the given database adapter is in connected state."""
        return self.ceph.is_connected()

    def connect(self) -> None:
        """Connect the given storage adapter."""
        self.ceph.connect()

    def get_document_listing(self) -> typing.Generator[str, None, None]:
        """Get listing of documents available in Ceph as a generator."""
        yield from self.ceph.get_document_listing()

    def store_document(self, document: dict) -> str:
        """Store the given document in Ceph."""
        try:
            RESULT_SCHEMA(document)
        except Exception as exc:
            raise SchemaError("Failed to validate document schema") from exc

        document_id = self.get_document_id(document)
        self.ceph.store_document(document, document_id)
        return document_id

    def retrieve_document(self, document_id: str) -> dict:
        """Retrieve a document from Ceph by its id."""
        return self.ceph.retrieve_document(document_id)

    def iterate_results(self) -> typing.Generator[tuple, None, None]:
        """Iterate over results available in the Ceph."""
        return self.ceph.iterate_results()
