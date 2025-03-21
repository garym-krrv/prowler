from unittest import mock
from uuid import uuid4

from tests.providers.azure.azure_fixtures import DOMAIN, set_mocked_azure_provider


class Test_entra_non_privileged_user_has_mfa:
    def test_entra_no_tenants(self):
        entra_client = mock.MagicMock

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )

            entra_client.users = {}

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 0

    def test_entra_tenant_no_users(self):
        entra_client = mock.MagicMock

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )

            entra_client.users = {DOMAIN: {}}

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 0

    def test_entra_user_no_privileged_no_mfa(self):
        entra_client = mock.MagicMock
        user_id = str(uuid4())

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )
            from prowler.providers.azure.services.entra.entra_service import (
                AuthMethod,
                DirectoryRole,
                User,
            )

            user = User(
                id=user_id,
                name="foo",
                authentication_methods=[AuthMethod(id=str(uuid4()), type="foo")],
            )

            entra_client.users = {DOMAIN: {f"foo@{DOMAIN}": user}}
            entra_client.directory_roles = {
                DOMAIN: {
                    "Global Administrator": DirectoryRole(id=str(uuid4()), members=[])
                }
            }

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "Non-privileged user foo does not have MFA."
            )
            assert result[0].resource_name == "foo"
            assert result[0].resource_id == user_id
            assert result[0].subscription == f"Tenant: {DOMAIN}"

    def test_entra_user_no_privileged_mfa(self):
        entra_client = mock.MagicMock
        user_id = str(uuid4())

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )
            from prowler.providers.azure.services.entra.entra_service import (
                AuthMethod,
                DirectoryRole,
                User,
            )

            user = User(
                id=user_id,
                name="foo",
                authentication_methods=[
                    AuthMethod(id=str(uuid4()), type="foo"),
                    AuthMethod(id=str(uuid4()), type="bar"),
                ],
            )

            entra_client.users = {DOMAIN: {f"foo@{DOMAIN}": user}}
            entra_client.directory_roles = {
                DOMAIN: {
                    "Global Administrator": DirectoryRole(id=str(uuid4()), members=[])
                }
            }

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert result[0].status_extended == "Non-privileged user foo has MFA."
            assert result[0].resource_name == "foo"
            assert result[0].resource_id == user_id
            assert result[0].subscription == f"Tenant: {DOMAIN}"

    def test_entra_user_privileged_no_mfa(self):
        entra_client = mock.MagicMock
        user_id = str(uuid4())

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )
            from prowler.providers.azure.services.entra.entra_service import (
                AuthMethod,
                DirectoryRole,
                User,
            )

            user = User(
                id=user_id,
                name="foo",
                authentication_methods=[AuthMethod(id=str(uuid4()), type="foo")],
            )

            entra_client.users = {DOMAIN: {f"foo@{DOMAIN}": user}}
            entra_client.directory_roles = {
                DOMAIN: {
                    "Global Administrator": DirectoryRole(
                        id=str(uuid4()), members=[user]
                    )
                }
            }

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 0

    def test_entra_user_privileged_mfa(self):
        entra_client = mock.MagicMock
        user_id = str(uuid4())

        with (
            mock.patch(
                "prowler.providers.common.provider.Provider.get_global_provider",
                return_value=set_mocked_azure_provider(),
            ),
            mock.patch(
                "prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa.entra_client",
                new=entra_client,
            ),
        ):
            from prowler.providers.azure.services.entra.entra_non_privileged_user_has_mfa.entra_non_privileged_user_has_mfa import (
                entra_non_privileged_user_has_mfa,
            )
            from prowler.providers.azure.services.entra.entra_service import (
                AuthMethod,
                DirectoryRole,
                User,
            )

            user = User(
                id=user_id,
                name="foo",
                authentication_methods=[
                    AuthMethod(id=str(uuid4()), type="foo"),
                    AuthMethod(id=str(uuid4()), type="bar"),
                ],
            )

            entra_client.users = {DOMAIN: {f"foo@{DOMAIN}": user}}
            entra_client.directory_roles = {
                DOMAIN: {
                    "Global Administrator": DirectoryRole(
                        id=str(uuid4()), members=[user]
                    )
                }
            }

            check = entra_non_privileged_user_has_mfa()
            result = check.execute()
            assert len(result) == 0
