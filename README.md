# Peter

### Git Workflow
* **Commits:** Conventional Commits
* **Branching:** GitHub Flow

## Configuration

### General

- Rename `.env-example` to `.env`

### Discord Bot

- Change `<Your-Discord-Bot-Token>` in `.env` with your discord bot token.
- Change fields containing `~` in `./discord-bot/config.yaml` with valid values.
More information about them, check the config file.

### Nettskjema Parser

- Setup a Nettskjema client by following these [steps](https://www.uio.no/english/services/it/adm-services/nettskjema/help/api-clients-v3.md#:~:text=Creating%20an%20API%20client).
- Change `<Your-Nettskjema-Client-Id>` and `<Your-Nettskjema-Client-Secret>` in `.env` with
your nettskjema client id and secret repectively.
- Change fields containing `~` in `./nettskjema-parser/config.yaml` with valid values.
More information about them, check the config file.


## Steps to Run

1. Make sure Docker Desktop and Docker Compose is installed on your machine
2. Clone the repository
```
git clone https://github.com/IFI-Prog-Sys/peter.git
```
3. cd into the project directory
```
cd ./peter
```
4. Run Docker Compose
```
docker compose up
```
Or use compose watch to enable hotloading.
```
docker compose watch
```