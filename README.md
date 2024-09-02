# ScrapeGod (MVP developement phase)
ScrapeGod.com is a powerful web scraping service designed to extract publicly available data from the internet for customers. Our platform provides reliable, efficient, and customizable scraping solutions to meet your data needs.
This is the backend API which will be served by NEXTjs UI frontend

## Setup

1. Download docker and docker-compose (including Docker Desktop if you are on Windows)
2. Download development .env file
3. after pulling the codebase, open the folder in your cli and run:
   `chmod +x run` (or if using Windows, right click properties and make sure files in /bin are executable by editing permissions)
   `docker compose up`
4. Once you have built the containers for the first time, you can `docker compose up` to start the containers without needing to rebuild.
5. Ensure .env is up to date with POSTGRE_xx variables.
6. seed database by running: `./run seed_db`
7. Run database migrations with: `docker compose exec scrapegod alembic upgrade head`
9. run `docker compose exec scrapegod alembic upgrade head` to update database architecture

To create new alembic migration files for updating the db: `docker compose exec scrapegod alembic revision -m '<your revision>'`

## Connecting to the Development Database

1. Install _pgAdmin_, _DBeaver_, or some other database client.
2. `docker compose up` to bring all services online, or `docker compose up postgres` to bring only the database online
3. Open a new Postgres connection, using the following connection settings:
   - Host: `localhost`
   - port: `5432`
   - user: `scrapegod`
   - password: `password`

**Note**: If you need to reset your database, then

- `docker compose up scrapegod -d`
- `./run reset_db`

## Docker-Compose Versions:

- If you are having trouble with the above, it might be due to your version of docker-compose.
- Check your version with `docker-compose --version`
- If you are using version 2 or greater, create an alias with `alias docker-compose='docker compose'`. Consider adding this to your bashrc file.

## Attaching Debugger in VS Code:

1. Run `docker-compose -f docker-compose.debug.yml up scrapegod` to compose the containers in a way that allows the debugger to be attached.
2. In the Run & Debug tool, add a remote configuration for python under 'Add Configuration' > 'Python' > 'Remote attach'.
3. **OR** add the following to your launch.json

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "0.0.0.0",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ],
            "justMyCode": true
        }
    ]
}
```

4. Start debugging!

## Setup Pre-Commit Hooks

1. Make sure you already installed pre-commit package.
2. Then using command line, run this in the repo root folder "pre-commit install"
3. After pre-commit install, check you `.pre-commit-config.yaml` file and ensure the style guide enforcement is set to github.com, not gitlab.com.\
   `# Style Guide Enforcement`\
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`repo: https://github.com/PyCQA/flake8`

## Docstring Standardization

Pre-commit hook has interrogate that will force you to add documentation to your code. because we believe that documentation is just as important as code. to improve the quality of our documentation We prefer for NumPy docstring as our format. It is already used in the majority of this project's modules.

Use "Mintlify Doc Writer" to assist you generate documentation and save your time. To use it, you must first install it in your IDE. It's available in vscode.
After installing it, navigate to the extension settings and select the NumPy docstring format.

![Alt text](Mintlify_Doc_Writer_Setting.png?raw=true "Title")

## Formatting

The black formatter is installed within the docker container. It can be run with `./run format`, which will format the entire codebase. Use of this will be enforced by GitHub Actions, so this must be done for every PR.

## Git Commit Principle

When committing code, the set of code being committed should adhere to the single concern principle. Please do not commit code that addresses multiple issues, such as fixing two bugs or adding a bunch of new features, etc. Please make commit wisely to making your code reviewer happy and not wasting their time.

so the point are :

1. Follow sinigle concern principle.
2. Dont commit code that has many changes, if possible split it in multiple commit.

The commit message standardization :

Message Format : [TYPE Task-No] Subject

#### Type

This indicates the type of the git commit. The type are following :

1. **FEAT** : Introduces a new feature
2. **FIX** : Fixes a bug found.
3. **DOC** : Commits documentation only changes.
4. **REFACTOR** : Commits a code change the way the code is written. it neither fixes a bug nor adds a feature.
5. **PERF** : Commits optimization changes, such as to improve performance and experience.
6. **TEST** : Adds tests.
7. **MERGE** : Merges Code

#### Task No.

This is the task number in JIRA. If the commited code has no tasks in the jira, skip this.

![Alt text](Jira_Task.png?raw=true "Title")

#### Subject

The subject is a brief description of the purpose of a commit

Example Commit Message :

- [FEAT TS-324] Create a daily function for bill extraction summary
- [FIX TS-234] Bill Combine being queued multiple times.
- [TEST TS-342] Unit test create invoice

## Development Database

1. Use the command `./run new_keys` to generate a new set of keys for the database access. Copy the output and give it to the database admin.
2. If you forgot to save your key, run `./run print_key`
3. After your key has been added to production, you can load the dev database.
4. `./run load_structure`
5. `./run load_fake_data`

## Data

If data is required for development:

1. 1. new_keys, and add to gitignore 2) admin adds to allowed_users, 3) load_structure, 4) load_fake_data
1. Ask the product team for development data for the database
1. Add the dummy data sql file to your working directory
1. Run ./import_database.sh

## Issues with Windows OS

- Sometimes the different End of Line Sequence causes unexpected behaviour in Windows OS docker systems compared to linux. To avoid this ensure your End Of Line Sequence is CRLF

## Issues with Mac OS

## Script to install dependencies

Step 1:

```
$ brew install gcc mupdf swig freetype postgresql openssl
```

Step 2:

```
$ brew info openssl
openssl@3: stable 3.0.1 (bottled) [keg-only]
Cryptography and SSL/TLS Toolkit
https://openssl.org/
/opt/homebrew/Cellar/openssl@3/3.0.1 (6,420 files, 27.8MB)
  Poured from bottle on 2022-02-23 at 15:43:27
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/openssl@3.rb
License: Apache-2.0
==> Dependencies
Required: ca-certificates ✔
==> Caveats
A CA file has been bootstrapped using certificates from the system
keychain. To add additional certificates, place .pem files in
  /opt/homebrew/etc/openssl@3/certs

and run
  /opt/homebrew/opt/openssl@3/bin/c_rehash

openssl@3 is keg-only, which means it was not symlinked into /opt/homebrew,
because macOS provides LibreSSL.

If you need to have openssl@3 first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/openssl@3/bin:$PATH"' >> ~/.zshrc

For compilers to find openssl@3 you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include"

For pkg-config to find openssl@3 you may need to set:
  export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@3/lib/pkgconfig"


$ export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib"
$ export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include"
```

Step 3:

```
pip install -U pip setuptools wheel
pip install -r requirements-lock.txt
```

Step 4:

Done.

- There seems to be a bug with Mac M1 computers and python 3.9:

```
  distutils.errors.CompileError: command '/usr/bin/clang' failed with exit code 1

----------------------------------------
ERROR: Failed building wheel for grpcio
```

These solutions may or may not work but will hopefully point you in the right direction if not:
https://stackoverflow.com/questions/69374842/cant-install-tensorflow-macos-on-macm1-errors-while-installing-grpcio
https://github.com/grpc/grpc/issues/24026

## Database Seeding

The following steps can be used to insert initial data into your database :

1. Copy scrapegod.sql into postgres container by executing this command. `docker cp ./scrapegod.sql scrapegod_postgres_1:/`
2. Execute SQL script inside docker container to insert data to your database.
   docker exec -t -e PGPASSWORD=password scrapegod_postgres_1 psql -h 127.0.0.1 -p 5432 -U postgres_user -d postgres_db -f /scrapegod.sql

## Git Workflow

- The main branch for production is `master` branch.
- Each new feature should reside in its own branch for backup/collaboration. This branch descends from the `master` branch as parent branch. It should be named feature/feature_name.
- When pushing updates, merge with the `develop` branch, never the `master` branch

## Run Unit Test

The unit test makes use of pytest.

Tests **must** be run inside the docker containers. You can either run the unit test on the whole **Flask App**, **or** you can run tests on entire **directories**, **or** you can run pytest on a **module**, **or** you can run unit tests on single classes/methods.

1. Running Unit Test Inside the docker container (`-rA` is an additional option to show all available information, inc. logs)\
   `docker-compose run scrapegod pytest  -rA`

2. Command to run unit test on specific directory(/file). \
   `docker-compose run scrapegod pytest scrapegod/tests/amazon(/test_amazon.py)`

3. Specific Class(/method) \
   `docker-compose run scrapegod pytest scrapegod/tests/amazon/test_amazon.py::TestSiteScrape(::test_search_result_price)`

## Running Webpack in development

- ensure the correct docker-compose.override.yaml is in your working directory
- When updating npm packages, run: docker-compose run webpack yarn install

# To-do

2. Download Aileron and Roboto Font
3. Make upload directory if not exists

Note: To prevent overwrites between windows and linux systems git ignores docker-compose and Dockerfile

# Add/Update JS Liblary

1. Edit package.json
2. run this command "docker-compose run webpack yarn install"

# Create new table

1. Define the new sqlalchemy model: class name, columns, tablename, etc.
2. Run `docker-compose exec --user "$(id -u):$(id -g)" scrapegod alembic revision -m "create tablename table"`. If you are in linux and it doesn't work, use `sudo`. This will create a file inside `db/versions/`.

3. Run `docker-compose exec scrapegod alembic upgrade head` to add the new table.

### Add column

Do the same as before, but run un step 2:
`sudo docker-compose exec --user "$(id -u):$(id -g)" scrapegod alembic revision -m "alter table tablename add column column_name type"`
And in step 3 consider this example:
`op.add_column('tablename', sa.Column('column_name', sa.Integer(), nullable=True))`

## Git Submodule

git submodule update --init
git submodule deinit --all -f

# Database Operation

## Backup DB

```bash
docker exec -t -e PGPASSWORD=password scrapegod-postgres-1 pg_dump -h 127.0.0.1 -p 5432 -U scrapegod -d scrapegod_2 --insert > scrapegod_backup_test_insert.sql
```

## Create Migrations script

```bash
docker exec scrapegod_scrapegod_1 alembic revision -m "comment"
```

## Upgrade Db

```bash
docker exec scrapegod_scrapegod_1 alembic upgrade heads
```

## downgrade db 1 step

```
docker exec scrapegod_scrapegod_1 alembic downgrade -1
```

additional info :

1. You can add "--autogenerate" after "revision" in order alembic compare your db state with SQLAlchemy models. then create the candidate command for migations.

## Upgrade Db

# Unit Test

You can run the automated test inside your container by running the following command :
"docker exec scrapegod_scrapegod_1 pytest"

or you can run the automated test locally, but you require :

1. Python Environment with the same python version and required package for scrapegod app.
2. run "pytest"

# Database Schema

