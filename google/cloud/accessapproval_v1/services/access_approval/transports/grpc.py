# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.accessapproval_v1.types import accessapproval
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import AccessApprovalTransport


class AccessApprovalGrpcTransport(AccessApprovalTransport):
    """gRPC backend transport for AccessApproval.

    This API allows a customer to manage accesses to cloud resources by
    Google personnel. It defines the following resource model:

    -  The API has a collection of
       [ApprovalRequest][google.cloud.accessapproval.v1.ApprovalRequest]
       resources, named ``approvalRequests/{approval_request_id}``
    -  The API has top-level settings per Project/Folder/Organization,
       named ``accessApprovalSettings``

    The service also periodically emails a list of recipients, defined
    at the Project/Folder/Organization level in the
    accessApprovalSettings, when there is a pending ApprovalRequest for
    them to act on. The ApprovalRequests can also optionally be
    published to a Cloud Pub/Sub topic owned by the customer (for Beta,
    the Pub/Sub setup is managed manually).

    ApprovalRequests can be approved or dismissed. Google personel can
    only access the indicated resource or resources if the request is
    approved (subject to some exclusions:
    https://cloud.google.com/access-approval/docs/overview#exclusions).

    Note: Using Access Approval functionality will mean that Google may
    not be able to meet the SLAs for your chosen products, as any
    support response times may be dramatically increased. As such the
    SLAs do not apply to any service disruption to the extent impacted
    by Customer's use of Access Approval. Do not enable Access Approval
    for projects where you may require high service availability and
    rapid response by Google Cloud Support.

    After a request is approved or dismissed, no further action may be
    taken on it. Requests with the requested_expiration in the past or
    with no activity for 14 days are considered dismissed. When an
    approval expires, the request is considered dismissed.

    If a request is not approved or dismissed, we call it pending.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "accessapproval.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "accessapproval.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_approval_requests(
        self,
    ) -> Callable[
        [accessapproval.ListApprovalRequestsMessage],
        accessapproval.ListApprovalRequestsResponse,
    ]:
        r"""Return a callable for the list approval requests method over gRPC.

        Lists approval requests associated with a project,
        folder, or organization. Approval requests can be
        filtered by state (pending, active, dismissed). The
        order is reverse chronological.

        Returns:
            Callable[[~.ListApprovalRequestsMessage],
                    ~.ListApprovalRequestsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_approval_requests" not in self._stubs:
            self._stubs["list_approval_requests"] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/ListApprovalRequests",
                request_serializer=accessapproval.ListApprovalRequestsMessage.serialize,
                response_deserializer=accessapproval.ListApprovalRequestsResponse.deserialize,
            )
        return self._stubs["list_approval_requests"]

    @property
    def get_approval_request(
        self,
    ) -> Callable[
        [accessapproval.GetApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        r"""Return a callable for the get approval request method over gRPC.

        Gets an approval request. Returns NOT_FOUND if the request does
        not exist.

        Returns:
            Callable[[~.GetApprovalRequestMessage],
                    ~.ApprovalRequest]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_approval_request" not in self._stubs:
            self._stubs["get_approval_request"] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/GetApprovalRequest",
                request_serializer=accessapproval.GetApprovalRequestMessage.serialize,
                response_deserializer=accessapproval.ApprovalRequest.deserialize,
            )
        return self._stubs["get_approval_request"]

    @property
    def approve_approval_request(
        self,
    ) -> Callable[
        [accessapproval.ApproveApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        r"""Return a callable for the approve approval request method over gRPC.

        Approves a request and returns the updated ApprovalRequest.

        Returns NOT_FOUND if the request does not exist. Returns
        FAILED_PRECONDITION if the request exists but is not in a
        pending state.

        Returns:
            Callable[[~.ApproveApprovalRequestMessage],
                    ~.ApprovalRequest]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "approve_approval_request" not in self._stubs:
            self._stubs["approve_approval_request"] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/ApproveApprovalRequest",
                request_serializer=accessapproval.ApproveApprovalRequestMessage.serialize,
                response_deserializer=accessapproval.ApprovalRequest.deserialize,
            )
        return self._stubs["approve_approval_request"]

    @property
    def dismiss_approval_request(
        self,
    ) -> Callable[
        [accessapproval.DismissApprovalRequestMessage], accessapproval.ApprovalRequest
    ]:
        r"""Return a callable for the dismiss approval request method over gRPC.

        Dismisses a request. Returns the updated ApprovalRequest.

        NOTE: This does not deny access to the resource if another
        request has been made and approved. It is equivalent in effect
        to ignoring the request altogether.

        Returns NOT_FOUND if the request does not exist.

        Returns FAILED_PRECONDITION if the request exists but is not in
        a pending state.

        Returns:
            Callable[[~.DismissApprovalRequestMessage],
                    ~.ApprovalRequest]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "dismiss_approval_request" not in self._stubs:
            self._stubs["dismiss_approval_request"] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/DismissApprovalRequest",
                request_serializer=accessapproval.DismissApprovalRequestMessage.serialize,
                response_deserializer=accessapproval.ApprovalRequest.deserialize,
            )
        return self._stubs["dismiss_approval_request"]

    @property
    def get_access_approval_settings(
        self,
    ) -> Callable[
        [accessapproval.GetAccessApprovalSettingsMessage],
        accessapproval.AccessApprovalSettings,
    ]:
        r"""Return a callable for the get access approval settings method over gRPC.

        Gets the settings associated with a project, folder,
        or organization.

        Returns:
            Callable[[~.GetAccessApprovalSettingsMessage],
                    ~.AccessApprovalSettings]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_access_approval_settings" not in self._stubs:
            self._stubs["get_access_approval_settings"] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/GetAccessApprovalSettings",
                request_serializer=accessapproval.GetAccessApprovalSettingsMessage.serialize,
                response_deserializer=accessapproval.AccessApprovalSettings.deserialize,
            )
        return self._stubs["get_access_approval_settings"]

    @property
    def update_access_approval_settings(
        self,
    ) -> Callable[
        [accessapproval.UpdateAccessApprovalSettingsMessage],
        accessapproval.AccessApprovalSettings,
    ]:
        r"""Return a callable for the update access approval
        settings method over gRPC.

        Updates the settings associated with a project, folder, or
        organization. Settings to update are determined by the value of
        field_mask.

        Returns:
            Callable[[~.UpdateAccessApprovalSettingsMessage],
                    ~.AccessApprovalSettings]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_access_approval_settings" not in self._stubs:
            self._stubs[
                "update_access_approval_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/UpdateAccessApprovalSettings",
                request_serializer=accessapproval.UpdateAccessApprovalSettingsMessage.serialize,
                response_deserializer=accessapproval.AccessApprovalSettings.deserialize,
            )
        return self._stubs["update_access_approval_settings"]

    @property
    def delete_access_approval_settings(
        self,
    ) -> Callable[[accessapproval.DeleteAccessApprovalSettingsMessage], empty.Empty]:
        r"""Return a callable for the delete access approval
        settings method over gRPC.

        Deletes the settings associated with a project,
        folder, or organization. This will have the effect of
        disabling Access Approval for the project, folder, or
        organization, but only if all ancestors also have Access
        Approval disabled. If Access Approval is enabled at a
        higher level of the hierarchy, then Access Approval will
        still be enabled at this level as the settings are
        inherited.

        Returns:
            Callable[[~.DeleteAccessApprovalSettingsMessage],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_access_approval_settings" not in self._stubs:
            self._stubs[
                "delete_access_approval_settings"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.accessapproval.v1.AccessApproval/DeleteAccessApprovalSettings",
                request_serializer=accessapproval.DeleteAccessApprovalSettingsMessage.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_access_approval_settings"]


__all__ = ("AccessApprovalGrpcTransport",)
