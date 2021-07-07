# ohdsi-docker

Atlas and WebAPI setup, with Synthea dataset loaded. All data will be managed in the configured `ohdsi` PostgreSQL database.

## Dependencies

The OHDSI vocabularies are not included in this repository, because this is a large download and they are updated regularly. The installer expects a zipped version of the vocabularies in `data/vocabulary/vocab.zip`. You can obtain these from [OHDSI Athena](https://athena.ohdsi.org).

Docker and docker-compose installed, with version at least 18.06.

## Configuration

Start by copying `env.template` to `.env`. Configuration can be customized in `.env`. It has the following variables:
- `HOSTNAME`: the hostname where the data will be hosted. This must be a resolvable DNS name. Also, `console.<HOSTNAME>` must be a resolvable DNS name to the same server.
- `BASE_URL`: the public base URL where the API will be hosted. This must be a resolvable DNS name.
- `POSTGRESQL_PASSWORD`: password to the PostgreSQL database for the `postgres` user. This is only used inside the docker-compose stack, outside and host access is disabled.
- `WEBAPI_IMAGE`: the image that will be used to host WebAPI.
- `ATLAS_IMAGE`: the image that will be used to host Atlas.
- `JUPYTERHUB_POSTGRESQL_PASSWORD`: Jupyterhub Postgres password (only used inside the stack)
- `KEYCLOAK_ADMIN_PASSWORD`: Keycloak password of the admin user
- `KEYCLOAK_POSTGRESQL_PASSWORD`: Keycloak Postgres password (only used inside the stack)
- `WEBAPI_CLIENT_SECRET`: secret of the webapi OAuth client in keycloak. Can only be retrieved after the client is registered.
- `JUPYTER_CLIENT_SECRET`: secret of the jupyterhub OAuth client in keycloak. Can only be retrieved after the client is registered.
- `COMPOSE_PROJECT_NAME`: internal docker project name. Does not need to change.

Ensure that the host has an entry in `/etc/hosts` with your DNS hostname:

```
<IP address>   <full-hostname>  <first-part-hostname> console.<full-hostname>
```

## Usage

To run the stack, run

```shell
bin/start
```

This will start the stack and load the vocabularies stored in `data/vocabulary/vocab.zip`. Loading the vocabularies takes a long time and so this step will only be performed once. Running the `start` command again will not load the vocabularies, unless the `vocab.concept` table is removed.

Once the stack is started, the following URL's are available:
`https://<HOSTNAME>/atlas/` contains the Atlas installation
`https://<HOSTNAME>/auth/` contains the Keycloak installation
`https://console.<HOSTNAME>/` contains the JupyterHub installation.

### Keycloak

To fully configure WebAPI and Jupyterhub, navigate to `https://<HOSTNAME>/auth/`. Start the admin console and login with the admin user, `KEYCLOAK_ADMIN_PASSWORD` password. At the top-left of the screen, select _Master_ and press _Add realm_. Import the realm set in `data/keycloak-realm-export.json`.

#### Client setup

After Keycloak is running, the services need to be configured to use it. These services are called Clients in Keycloak.

Navigate to _Clients_, _jupyterhub_. Set the Redirect URL value to `https://console.<HOSTNAME>/hub/oauth_callback`. Then navigate to the _Credentials_ tab and press the _Regenerate Secret_ button there. Copy the value of _Secret_ to `JUPYTER_CLIENT_SECRET`.

Next, do the same for the _webapi_ client: change the Redirect URL to `https://<HOSTNAME>/WebAPI/*`, regenerate the secret and copy it to `WEBAPI_CLIENT_SECRET`.

Once the clients are configured, please reload the jupyterhub and webapi services:

```shell
docker-compose up -d webapi jupyterhub
```

#### User management

Any users that should get access can be created in the _Users_ tab. If they should be able to create new users themselves, select the user, _Role Mappings_, _Client Roles_ set to _realm-management_, select _realm-admin_ and press _Add selected_.

### SFTP

A [Docker SFTP server](https://github.com/atmoz/sftp) is exposed on port 2222 for external parties to add their data. To add a new user, edit `etc/sftp/users.conf` as stated in the linked server. For example, to create a `radboud` user, add a row
```
radboud::1001:101:data
```
to give user `radboud` user ID `1001`, group ID `101`, storing data in the `/home/radboud/data` folder. Add pubilc SSH keys of the user that should log in to `etc/sftp/keys/radboud` and mount that as a volume to `/home/radboud/.ssh/keys`. Finally, mount the data directory for use in Jupyterhub by creating a new volume in the docker-compose stack and mounting that as `sftp_radboud_data:/home/radboud/data`. The same volume should then be mounted in the Jupyter notebook image by modifying `images/jupyterhub/jupyterhub_config.py`. The variable `c.DockerSpawner.volumes` should get a new entry with
```python
  'sftp_radboud_home': {'bind': '/home/jovyan/shared/radboud', 'mode': 'ro'},
```
Now the data uploaded by Radboud is be shown in Jupyter notebooks under the directory `shared/radboud`.

Rebuild the sftp and Jupyterhub stack as follows:
```
sudo docker-compose stop sftp
sudo docker-compose rm -vf sftp
sudo docker-compose up -d --build sftp jupyterhub
```

### Scripts

To load a Synthea dataset, run `bin/load-synthea <dataset_name> <dataset_schema> [<synthea parameters>]`. For example:

```shell
bin/load-synthea "Synthea1K" "synthea1k" -p 1000
```

This will create a Synthea dataset of 1000 people and load it into the `cdm_synthea1k` schema using name `Synthea1K`. Afterwards, it is analysed with Achilles. The original generated Synthea dataset is available in schema `synthea1k`. For more command-line parameters to Synthea, please see [Synthea command-line instructions](https://github.com/synthetichealth/synthea/wiki/Basic-Setup-and-Running). To regenerate the dataset, run `bin/generate-synthea` with synthea runtime parameters.

Other helper scritps in the `bin/` directory have the following purpose:
- `generate-results <CDM name> <raw schema name>` lets you generate the results table and schema of a given source.
- `run-script` lets you run one of the scripts in the `docker-compose.scripts.yml` file. Examples: `bin/run-script synthea` generates a Synthea dataset, `bin/run-script achilles r /scripts/myscript.R` runs your own script in `src/r/myscript.R`.
- `run-sql <file>` lets you run the commands in a given SQL file. It does environment variable substitution, substituting the value of the `MY_ENV` variable into any `${MY_ENV}` references in the given SQL.
- `run-sql-cmd <CMD>` lets you run a single SQL command.
- `webapi-reload-sources` reloads the sources defined in WebAPI by reading creating source entries from each CSV record in `data/sources.csv`. Records have the following columns: unique numeric source ID, name, CDM schema, results schema.

To stop the stack, run

```
docker-compose down
```

and to remove all existing data as well, run

```
docker-compose down -v
```

### Other operations

To completely reload the vocabulary, run
```
bin/run-sql-cmd "DROP SCHEMA vocab CASCADE"
bin/run-sql-cmd "CREATE SCHEMA vocab"
bin/start
```
