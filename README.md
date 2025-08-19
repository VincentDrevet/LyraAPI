# Before start instance

You must create a .env file at the root of this project.

The file must contain at the moment 2 parameters :
- DATABASE_URL which the URL to the database
- DEVICE_PASSWORD_SIZE which is the size of generated device password.

Example of content of .env file:
````toml
DATABASE_URL="sqlite:///Lyra.db"
DEVICE_PASSWORD_SIZE=12
````

# Launch dev instance

```sh
fastapi dev
```