from keycloak import KeycloakOpenID

class DDKeyCloak:
    def __init__(self,
                 server_url: str = "https://keycloak.ddns.net",
                 client_id: str = "admin-cli",
                 realm_name: str = "master",
                 username: str=None,
                 password: str=None,
                 client_secret_key:str=None,
                 verify: bool=False):
        self.username = username
        self.password = password
        self.realm_name = realm_name
        self.client_id = client_id
        self.url = server_url

        try:
            self.keycloak_openid =  KeycloakOpenID(
                server_url=self.url,
                client_id=self.client_id,
                realm_name=self.realm_name,
                client_secret_key=client_secret_key,
                verify=verify  # Avoid this in production
            )
        except Exception as e:
            print(f"cannot connect to keycloack due to {e}")
            raise e

    def get_user_token(self, username=None, password=None) -> str:
        """
        Get user token by username and password
        :param username:str
        :param password:str
        :return token:str
        """
        try:
            token = self.keycloak_openid.token(grant_type="password",
                                   username=self.username if username is None else username,
                                   password=self.password if password is None else password)
        except Exception as e:
            print(f"cannot get token due to {e}")
            raise e

        return token["access_token"]

    def get_client_token(self) -> str:
        """
        Get client token by client_id and client_secret_key
        :return toekn:str
        """
        try:
            token = self.keycloak_openid.token(grant_type="client_credentials")
        except Exception as e:
            print(f"cannot get token due to {e}")
            raise e

        return token["access_token"]

if __name__ == "__main__":
    keycloak_client = DDKeyCloak(server_url="https://keycloak.dd.wwest.local",
    client_id="testers",
    realm_name="dd-realm",
    client_secret_key="ELSV2QYEFbYbl2yAVq56MDNJnfnmN6tD",
    verify=False)

    token = keycloak_client.get_client_token()

    print(token)

    keycloak_client = DDKeyCloak(server_url="https://keycloak.dd.wwest.local",
                                 client_id="testing_ddfe",
                                 realm_name="dd-realm",
                                 verify=False)

    token = keycloak_client.get_user_token(username="ddadmin", password="Ad3110$$Ad3110$$")

    print(token)
