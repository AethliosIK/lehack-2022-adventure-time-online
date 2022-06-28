### Adventure Time Online - LeHack 2022

Here is the code of one of the two challenges I provided for the Wargame (Public CTF) of the 2022 edition of the Hack which took place from June 24th to 25th.
You are now able to inspect the code and replay the challenge locally if you wish.

- Description : A friend of yours wants to launch the new Rottentomatoes, targeting the Adventure Time community first. Help him review the security of his website's beginnings.
- Category : Web
- Difficulty: Easy / Medium

### Start Guide :

```bash
cd lehack-2022-adventure-time-online
docker-compose up -d
# Go to http://localhost:5000
```

### .env:

```bash
MYSQL_ROOT_PASSWORD=<Your Value>
MYSQL_USER=<Your Value>
MYSQL_PASSWORD=<Your Value>
SECRET_KEY_FLASK=<Your Value>
PASSWORD_SALT_FLASK=<Your Value>
REDIS_URI=<Your Value>
```
