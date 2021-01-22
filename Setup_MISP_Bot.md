# Get token

```bash
curl -XPOST -d '{"type":"m.login.password", "user":"admin_user", "password":"password"}' "https://matrix.server.lu/_matrix/client/r0/login"
```

Response:

```json
{
    "access_token": "TOKEN",
    "device_id": "XYKJZXOXXI",
    "home_server": "matrix.server.lu",
    "user_id": "@admin_user:matrix.server.lu",
    "well_known": {
        "m.homeserver": {
            "base_url": "https://matrix.server.lu/"
        },
        "m.identity_server": {
            "base_url": "https://matrix.server.lu"
        }
    }
}
```

# Get user info

```bash
curl --header "Authorization: Bearer TOKEN" https://matrix.server.lu/_synapse/admin/v2/users/@admin_user:matrix.server.lu
```

Response

```json
{
    "admin": 1,
    "appservice_id": null,
    "avatar_url": null,
    "consent_server_notice_sent": null,
    "consent_version": null,
    "creation_ts": 1611320309,
    "deactivated": 0,
    "displayname": "admin_user",
    "is_guest": 0,
    "name": "@admin_user:matrix.server.lu",
    "password_hash": "<HASH>",
    "threepids": [],
    "user_type": null
}
```

# Create account


PUT that thing:
```json
{
    "password": "<PASSWORD>",
    "displayname": "MISP Bot",
    "threepids": [
        {
            "medium": "email",
            "address": "info@circl.lu"
        }
    ],
    "admin": false,
    "deactivated": false
}
```

```bash
curl --header "Authorization: Bearer TOKEN" \
  https://matrix.server.lu/_synapse/admin/v2/users/@mispbot:matrix.server.lu \
  -X PUT
  --data @json_blob
```

```json
{
    "admin": 0,
    "appservice_id": null,
    "avatar_url": null,
    "consent_server_notice_sent": null,
    "consent_version": null,
    "creation_ts": 1611323179,
    "deactivated": 0,
    "displayname": "MISP Bot",
    "is_guest": 0,
    "name": "@mispbot:matrix.server.lu",
    "password_hash": "<HASH>",
    "threepids": [
        {
            "added_at": 1611323179554,
            "address": "info@circl.lu",
            "medium": "email",
            "validated_at": 1611323179554
        }
    ],
    "user_type": null
}
```

# Config

copy and configure config.yaml

# Dependencies

needs buster-backports => https://wiki.debian.org/Backports#Using_the_command_line

```bash
apt -t buster-backports install libolm3 libolm-dev
apt install tmux virtualenv python3-dev libfuzzy-dev
```

# Install and run

```bash
source env/bin/activate
pip install -e .
matrix-misp-bot config.yaml
```
