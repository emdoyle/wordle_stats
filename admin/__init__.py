# responsibilities
# - manage bot servers (and data)
#   - docker_py
#     - spin_up == create volume, build server image, run server container with volume, secrets, crontab config mounted
#     - tear_down == stop and remove container, remove volumes
#     - upgrade == (look into docker service) stop container, rebuild image (try to frontload), start container
#       - also may need to use an entrypoint file to run migrations before server starts
