# Contributor's guide

## Branches and tags

The `main` branch represents the current state of the bot.

New features are developed on `feature/*` branches for the development of specific features; these are to be squashed as a single commit onto the `main` branch.

Pushing a `v*` tag will automatically trigger the build of a new Docker image for the tagged commit.  
Please use annotated tags (`git tag -a`) if possible!

Old Royalnet versions are available for reference on the `historic/*/*` orphan branches.

## Setting up a development environment

Follow these instructions to setup a Royalnet development environment, so that you may be able to test your changes!

### Installing Rust

You'll need to have the latest stable version of the [Rust] toolchain installed.

[Rust]: https://www.rust-lang.org/

#### On Linux

1. Download `rustup` from your distribution's package manager:
   ```shell
   # On Arch Linux
   pacman -Syu rustup
   ```
2. Use `rustup` to install the latest stable toolchain:
   ```shell
   rustup default stable   
   ```

#### On Windows

1. Follow the instructions at the [Install Rust] page.
2. Use `rustup` to install the latest stable toolchain:
   ```shell
   rustup default stable   
   ```

[Install Rust]: https://www.rust-lang.org/tools/install

### Installing an IDE

Using an IDE for Rust is highly recommended!

Steffo's personal recommendation is [RustRover] by [Jetbrains] with the [Steffula Ultra] color scheme, which provides a fully visual environment for interacting with the Rust toolchain.

[RustRover]: https://www.jetbrains.com/rust/
[Jetbrains]: https://www.jetbrains.com/
[Steffula Ultra]: https://plugins.jetbrains.com/plugin/22749-steffulaultra-color-scheme

### Installing Git

To contribute changes to the project, you need to have the [Git] version control system installed.

#### On Linux

It's very likely that `git` is bundled with your Linux distribution.

In case it isn't:

1. Download it from your distribution's package manager:
   ```shell
   # On Arch Linux
   pacman -Syu git
   ```

#### On Windows

Windows doesn't bundle `git`, so you'll need to download and install it externally.

1. Download it from the [Git download page].
2. Install it by running the downloaded executable.
   - The default options provided by the installer are fine, but you might want to change the one allowing you to pick the text editor to use with `git` to match the one you're most comfortable with.

[Git download page]: https://git-scm.com/downloads

### Configuring Git

If you have never used Git before on your machine, you have to configure your identity before you're able to create new commits:

```shell
# This will be publicly visible, if you're uncomfortable with that, you may use a pseudonym.
git config --global user.name "Name Surname"
# This needs to be the same email you've used to sign up to GitHub!
git config --global user.email "example@example.org"
```

### Creating a configuration file

To configure the bot's features with parameters whose value has to remain secret, an `.env` file in the root directory of the project is used.

An example file `.example.env` is provided with the repository; copy it to `.env` to make use of it as a template:
```shell
cp .example.env .env
```

### Selecting features

To minimize compilation times and configuration work needed, Royalnet supports [conditional compilation] via [Cargo features].

The following features are currently available:
- `interface_database`
  - allows interaction with a [PostgreSQL] database
- `interface_stratz`
  - allows interaction with the [STRATZ] [GraphQL API]
- `service_telegram`
  - processes commands sent to a [Telegram] [bot]
- `service_brooch`
  - sends notifications to a [Telegram] group about recently played [Dota 2] matches via a bot
- `default`
  - includes all features

[conditional compilation]: https://doc.rust-lang.org/reference/conditional-compilation.html
[Cargo features]: https://doc.rust-lang.org/cargo/reference/features.html

#### On RustRover

If you're editing the project with RustRover, you can graphically toggle features on and off:

1. Open `Cargo.toml`.
2. Scroll to the `[features]` section
3. Tick or untick the features you want to use.
   - `default` is ignored if you use the provided run configurations.

#### Elsewhere

To toggle features on other editors, remember to pass the `--no-default-features` and `--features` option to Cargo when running commands:
```shell
cargo --no-default-features --features="interface_database,interface_stratz,service_telegram,service_brooch" run
```

### Configuring PostgreSQL

> [!Note]
> You'll need to configure PostgreSQL only if you're developing something using the `interface_database` feature.

Royalnet stores some persistent data inside a [PostgreSQL] database, so you might need one installed to test things that use it:

1. Make sure you have an instance of the DBMS available to use somewhere reachable from your machine.
2. Create an user to use with royalnet.
   - If you're on a Linux system, and you have installed PostgreSQL via your package manager, most likely you'll be able to create an usable user with:
     ```shell
     sudo --user=postgres -- createuser "$USER"
     ```
3. Create a database
   - If you're on a Linux system, and you have installed PostgreSQL via your package manager, most likely you'll be able to create an usable database with:
     ```shell
     sudo --user=postgres -- createdb --owner="$USER" royalnet
     ```
4. Use the [connection URI] documentation page to determine the string to use to access your database:
   - If you're on a Linux system, and you have installed PostgreSQL via your package manager, most likely the connection string will be:
      ```url
      postgres:///royalnet?host=/run/postgresql/
      ```
5. Set the `DATABASE_URL`, `TELEGRAM_DATABASE_URL` and `BROOCH_DATABASE_URL` variables in the `.env` file to the connection URI:
   ```dotenv
   export DATABASE_URL='postgres:///royalnet?host=/run/postgresql/'
   export TELEGRAM_DATABASE_URL='postgres:///royalnet?host=/run/postgresql/'
   export BROOCH_DATABASE_URL='postgres:///royalnet?host=/run/postgresql/'
   ```
6. Install [cargo-binstall] to allow `cargo` to download pre-compiled executables:
   ```shell
   cargo install cargo-binstall
   ```
7. Binstall [diesel_cli] to allow `cargo` to perform operations on the database:
   ```shell
   cargo binstall diesel_cli
   ```
8. Load the `.env` file into your current environment:
   ```shell
   source .env
   ```
9. Generate the database schema by running all migrations with `diesel_cli`:
   ```shell
   ~/.cargo/bin/diesel_cli migration run
   ```

[PostgreSQL]: https://www.postgresql.org/
[connection URI]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS
[cargo-binstall]: https://crates.io/crates/cargo-binstall

### Configuring the STRATZ GraphQL API

> [!Note]
> You'll need to configure the STRATZ GraphQL API only if you're developing something using the `interface_stratz` feature.

Royalnet uses the [STRATZ] [GraphQL API] to retrieve information about past [Dota 2] matches, so you might need to configure it to make some data available:

1. Log in to [STRATZ] with your [Steam] account.
2. Visit the [My Tokens] page.
3. Click the "Show Token Information" button.
4. Copy the displayed token.
5. Set the `BROOCH_STRATZ_TOKEN` variable in your `.env` to the token you've just copied:
   ```dotenv
   export BROOCH_STRATZ_TOKEN='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
   ```

[STRATZ]: https://stratz.com/
[GraphQL API]: https://api.stratz.com/graphiql/
[Dota 2]: https://store.steampowered.com/app/570/Dota_2/
[Steam]: https://steamcommunity.com/
[My Tokens]: https://stratz.com/api

### Configuring a Telegram bot

> [!Note]
> You'll need to configure a Telegram bot for commands only if you're developing something using the `service_telegram` or `service_brooch` features. 

Royalnet can be interacted with via a [Telegram] [bot], a special user account that allows for automated interactions with chat rooms, which needs to be manually created:

1. Log in to Telegram using [Telegram Desktop].
2. Search for the account with the username `@BotFather`.
3. Send the `/start` command.
4. Send the `/newbot` command.
5. Answer the questions asked by the BotFather.
6. Once the bot is created, copy the displayed token.
7. Set the `TELEGRAM_BOT_TOKEN` and `BROOCH_TELEGRAM_BOT_TOKEN` variables in your `.env` to the token you've just copied.
8. Open Telegram Desktop's "Settings" modal.
9. Navigate to the "Advanced" category.
10. Navigate to the "Experimental settings" subcategory.
11. Enable the "Show Peer IDs in Profile" option.
12. Close the modal.
13. Create a new group containing just you and the bot you've just created.
14. Open the "Manage group" menu.
15. Navigate to the "Administrators" category.
16. Click on your profile.
17. Enter anything in the "Custom title" field.
18. Click "Save" two times.
19. Close the modal.
20. Click the group's name on the top of the window.
21. Click on the group's id to copy it.
22. Set the `TELEGRAM_NOTIFICATION_CHATID` and `BROOCH_NOTIFICATION_CHAT_ID` variables in your `.env` to `-100`, followed by the ID you've just copied:
    ```dotenv
    # Assuming the copied chat id is `123456789`
    export TELEGRAM_NOTIFICATION_CHATID='-100123456789'
    export BROOCH_NOTIFICATION_CHAT_ID='-100123456789'
    ```

[Telegram Desktop]: https://desktop.telegram.org/
[bot]: https://core.telegram.org/bots
[official client]: https://telegram.org/apps

## Using the development environment

The following recipes are available to perform most frequently used actions.

### Run Royalnet

The ***Run*** run configuration or the following script runs Royalnet with all the enabled features:

```shell
source .env
cargo run
```

### Check the validity and quality of the code

The ***Clippy*** run configuration or the following script checks the whole source code for errors, warnings, anti-patterns and potential mistakes:

```shell
source .env
cargo clippy
```

### Open documentation

The ***Doc*** run configuration or the following script compiles the documentation of all available crates, then opens it in your web browser:

```shell
source .env
cargo doc --open
```
