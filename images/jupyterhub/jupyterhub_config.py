# Configuration file for JupyterHub
import os
import shutil

def format_volume_name(label_template, spawner):
    path = label_template.format(username=spawner.escaped_name)

    # creates user notebooks dir
    if not os.path.isdir(path):
        os.makedirs(path)
        shutil.chown(path, user='jovyan', group='users')
        os.chmod(path, 0o755)

    return path

c = get_config()


# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {
  'jupyterhub-user-{username}': notebook_dir,
  'jh_shared': '/home/jovyan/shared',
  'sftp_radboud_home': {'bind': '/home/jovyan/shared/radboud', 'mode': 'ro'},
}
c.DockerSpawner.format_volume_name = format_volume_name
###test same thing for conda and julia
#notebook_dir_conda = os.environ.get('DOCKER_CONDA_DIR') or '/opt/conda'
#c.DockerSpawner.notebook_dir = notebook_dir_conda
#c.DockerSpawner.volumes = { 'jupyterhub-conda-{username}': notebook_dir_conda }
#notebook_dir_julia = os.environ.get('DOCKER_JULIA_DIR') or '/opt/julia'
#c.DockerSpawner.notebook_dir = notebook_dir_julia
#c.DockerSpawner.volumes = { 'jupyterhub-julia-{username}': notebook_dir_julia }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# Authenticate users with Keycloak
### https://github.com/jupyterhub/oauthenticator/issues/107#issuecomment-332572483 - from a discussion of an issue
#c.JupyterHub.authenticator_class = 'oauthenticator.generic.GenericOAuthenticator'
#c.OAuthenticator.client_id # oauth2 client id for your app
#c.OAuthenticator.client_secret # oauth2 client secret for your app
#c.GenericOAuthenticator.token_url # oauth2 provider's token url
#c.GenericOAuthenticator.userdata_url # oauth2 provider's endpoint with user data
#c.GenericOAuthenticator.userdata_method # method used to request user data endpoint
#c.GenericOAuthenticator.userdata_params # params to send for userdata endpoint
#c.GenericOAuthenticator.username_key # username key from json returned from user data endpoint
### https://github.com/jupyterhub/oauthenticator/pull/183#issuecomment-384071251 - from a discussion to an PR
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.login_service = 'keycloak'

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://{user}:{password}@{host}:5432/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
)
