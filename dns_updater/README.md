# mgs-dns-updater
### Mgs-dns-updater
Mgs-dns-updater docker container

### Primary task
Сyclically updating DNS records in Cloudflare.

### How to use this image
1. Сontainer uses environment variables to send put and get requests. You need to enter variable values ​​in `docker-compose.yml`
2. Build and run the container using the command ```docker compose up -d --build```

### ENVIRONMENT VARIABLES
Can be written at the level of dockerfile and docker-compose. The preferred and more flexible option is docker-compose

- `CF_API_TOKEN` - API token Cloudflare, you can find out [here](https://dash.cloudflare.com/profile/api-tokens)
- `CF_ZONE_ID`- Zone id - Cloudflare (look at Overview tab of your domain on Cloudflare)
- `CF_DNS_NAME` - enter the DNS name for which we will monitor and update
- `CF_TTL` - TTL value specifies the interval in seconds, after which changes made to a DNS record will take effect.

### Features of work
- Logs are stored in a separate folder, by default it is mounted in the parent OS
- To reduce the container size, a [python-slim](https://hub.docker.com/_/python/) image was used. In this case, dependencies must be specified explicitly. They are listed in the requirements.txt file.
- The program is in infinite loop, the delay between iterations is equal to `CF_TTL` of the DNS record