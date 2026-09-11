# Peter

### Git Workflow
* **Commits:** Conventional Commits
* **Branching:** GitHub Flow

## Configuration

### Discord Bot

- Change `<Your-Discord-Bot-Token>` in `.env` with your discord bot token.
- Change fields containing `~` in `./discord-bot/config.yaml` with valid values.
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