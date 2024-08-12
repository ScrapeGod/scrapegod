# ScrapeGod (MVP developement phase)
ScrapeGod.com is a powerful web scraping service designed to extract publicly available data from the internet for customers. Our platform provides reliable, efficient, and customizable scraping solutions to meet your data needs.

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
- https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow#:~:text=Gitflow%20is%20a%20legacy%20Git,software%20development%20and%20DevOps%20practices

## Run Unit Test

The unit test makes use of pytest.

Tests **must** be run inside the docker containers. You can either run the unit test on the whole **Flask App**, **or** you can run tests on entire **directories**, **or** you can run pytest on a **module**, **or** you can run unit tests on single classes/methods.

1. Running Unit Test Inside the docker container (`-rA` is an additional option to show all available information, inc. logs)\
   `docker-compose run scrapegod pytest  -rA`

2. Command to run unit test on specific directory(/file). \
   `docker-compose run scrapegod pytest scrapegod/tests/accounting(/test_accountant.py)`

3. Specific Class(/method) \
   `docker-compose run scrapegod pytest scrapegod/tests/accounting/test_accountant.py::TestSitePayBillAccountant(::test_credit_has_occur)`

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
3. Modify the file with the instructions. Example (this was used to create `elec_distributors` table):

```
def upgrade():
    op.create_table(
        "elec_distributors",
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('distributor_id', sa.Integer, nullable=False),
        sa.Column('company_name', sa.String(90), nullable=False),
        sa.Column('display', sa.String(90), nullable=False),
        sa.Column('name', sa.String(90), nullable=False),
        sa.Column('api_origin', sa.String(90), nullable=False),
    )

def downgrade():
    op.drop_table("elec_distributors")
```

4. Run `docker-compose exec scrapegod alembic upgrade head` to add the new table.

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

### Inline code refers to each table

- Threadlet keeps every `site` and `gas_site` on the lowest `price/gas_price` for our client.
- This is based on their annual `usage` or `gas_usage`.
- We receive a bill every month for each `site` that is stored in the `usage` and `price` table.
- We create an `invoice` for each bill from these rows.
- Every `invoice` is related to a `site`.
- Multiple `sites` are related to a single business entity, labelled `users`.
- Our `clients` can have multiple `users` for their different businesses.
- percent saved is what determines whether one price is better than another `price` or `offer`
- percent saved is calculated in `rate_reviews`.
- percent_saved is saved as half of the actual savings as we take a 50% cut of the savings we find.

## Switching sites to the best rates

- We scrape or manually add new `elec_offers` or `gas_offers` to be compared with their current price.
- We do this by creating a `elec_rate_review/gas_rate_review` to calculate the percent_saved of each offer compared to the latest price.
- This should be calculated based on the **estimated annual usage** for each site.
- If the percent_saved is better than the last_best_price percent_saved we change the rate_review stage to "To Switch"
- Once the admin team makes the switch this will be updated to "Switch Pending" unless the offer is "Invalid"
- Only one rate_review should be labelled as "To Switch" for a given site at any time
- If there is an offer that has less savings than the lates price, we label as "No Savings Found"
- If there is an offer that has less savings than another offer but more savings than the latest price, we label as "Not Best Offer"

## Quote Flow

- Upload invoice to endpoint /admin/quote-upload
- The bill gets processed in the class QuoteFlowManager
- If Bill is OG and NMI/MIRN is unique, then Site, Price and Usage is created in the database for the bill
- The Site is added as a row on /admin/rate-reviews. Note that instead of creating an empty rate-review, we display it statically on the rate-reviews page
- To get displayed on the rate-reviews, site.converted == False.
- When the offer is created for the site by clicking the "Add offer" button, site status is changed to "Ready To Send". This means you can now create a quote.
- Select the newly created RateReview and click on "Create Quote" btn on /admin/rate-reviews.
- Fill First Name, Last Name, Trading Name of the client.
- On submitting, email template is generated with the PDs link persoanlized for the client.

# Review Round Overview

The Review Round is a recurring cycle designed to identify the best electricity and gas offers. This process involves several related tables to manage and track various aspects of the review and decision-making process.

## Related Tables

**1. review_round:**

- Corresponds to each site.
- Contains price snapshots such as the best offer, best_rate_review, and last_active_price.
- Includes start date and end date information.

**2. rate_review_round_association:**

- Records the review_round_id and rate_review_id for each unexpired, available rate_review (offers).

**3. task:**

- Responsible for notifying administrators of their tasks.
- Tasks include confirming the eligibility of offers, confirming the switch process, etc.
- Includes details such as description, priority, assignee, assigned to, status (open, pending, complete), and type.

**4. task_review_rounds:**

- Connects task_id and review_round_id.
- Each row corresponds to a review_round task.
- Automatically created when a new review round is initiated or when any rate-review in a review-round is marked as 'to_switch,' requiring a review_round task.

**5. task_review:**

- Created when any rate review is marked as 'Admin to Switch.'
- Holds the rate_review_id and task_id for those switch-required tasks.

## Review Round Cycle

**1. Review Round starts with this check:**

- System checks for price changes.
- Triggers a new review round if the site does not have an active review round.
- Celery task triggers a new review round if over 30 days have passed since the last one.

**2. Admin Tasks:**

- Review Round task is created when a new review round is initiated or when any rate-review is marked as TO SWITCH.
- Switch required task is created when any rate review in the review round is marked as ADMIN TO SWITCH.
- On admin action, these tasks get completed.

**3. Process Ends:**

- Whenever any rate review stage is marked as SWITCH CONFIRMED, then the review round ends. The cycle continues.

## Key Methods

**Class: ReviewRound**

- **create_next_round**: If a new review round is required (considering the above conditions) for a site, then this function is called.
- **create_admin_task_for_review_round**: Creates review round tasks.
- **create_admin_task_for_switch_required**: Responsible for handling switch-required tasks.
- **store_price_snapshot**: Finds out the last_active_price, benchmark_price, benchmark_usage, best_rate_review, best_offer in the review round.
- **end_round**: When any rate review in the review round is marked as switch confirmed, this function is called.

**Class: ReviewRoundAssociation**

- **create_or_update_review_round_association**: Takes in review_round_id and rate_review_id and populates the review_round_association table.
- **bulk_create_or_update_review_round_association**: Takes in a list of rate reviews in a review round and bulk populates the same table.

**Class: Task**

- **create_task**: Creates different types of tasks for notifying admin.

## Key Celery Tasks

- **daily_rate_review_new_offers**: It does daily checks for new offers and concurrently rate reviews new offers. As new offers are rate reviewed, it populates them in the rate_review_round_association table.

- **review_round_scheduler**: It checks daily if a new review round is required for a site.

# Glossary

- Bill : Bill is a report of utility for electricity/gas. it issued by retailer to a particular site. Depending on the number of supply days, it may be issued once or twice a month.

- Invoice : Invoice is a utility report for electricity and gas. Unlike a bill, this one is issued by threadlet to the customer for a specific site or multiple sites for a specific period of time. We should have calculated a few things before issuing the invoice, such as the percent saved, revenue, merchant fee, credit, and so on.

- Usage : A measured of electricity or gas consumption.

- Price : Electricity or gas tariff per unit of usage.

- Percent Saved : The percent saved is the proportion of money saved after customer using our service. this compare to a benchmark.

- Benchmark : The benchmark is a reference where price is compared to calculate the percent saved. The benchmark can be an original price or the previous highest price.

- OG (Original) Price/Usage : it's the tariff/consumption of electricity or gas before customer uses our service.

- Bill Combine : It's a schema of invoicing. where two small bills are merged into a single invoice. The bills are from a single site, and small bill is identified by the number of supply days and subtotal.

- Site Combine : It's a schema of invoicing. where two or more bill from multiple sites are merged into a single invoice. the bills are from a single user.

- Offer : ....

- Rate Review : ....

# Roadmap

## Automated rate reviews for unbundled sites

- We need to be able to create dynamic percent saved values based on the contract terms.
- The savings multiplier for unbundled sites is: 1 year = 15%, 2 year = 7.5%, 3 year = 5%, 4 year = 3.5%
- percent saved can be calculated between bundled and bundled if the site ramps up or ramps down usage (as unbundled threshold is 100MWh / year).

## Running the offer scraper (displayed in /rate-reviews)

- Sites having a month since a rate review will be displayed on the /rate-reviews page as "Awaiting Result". No rate review/offer will have been made yet.
- The scraper will run a celery task every month for each site.
- If it succeeds and offer is better, rate_review stage == "To Switch". If offer is worse than last_best_price, Stage == "No Savings Found.
- If it fails the "Scrape & save" button will be listed as Scrape failed. Clicking the button will display the traceback. Stage == "Awaiting result"
- Clicking new offer will add the offer manually and create a new rate review when the form is submitted.

## Automated quotes

- Emails with quotes will be forwarded to support@threadlet.com.au
- Our API "watches" incoming emails and sends the attachments to `/quote-upload`.
- Each different business name on the bills are added to the users table as different business entities.
- Once bills are parsed as the original bills "OG" for a client, we run a celery task to scrape offers and add to the `/rate-reviews` list.
- Once new offers have been found and rate reviews calculated, we select each site's checkbox and "Create Quote" to send to the client.
- When Create Quote is created for each site, if no client is found, a modal appears to add the client's first name, last name and the Trading name of the client.
- we create a new client that relates to each user corresponding to those sites when we create a quote.
- The client-quote template is tempalated with a PDS link that contains the client_id to update to converted when the client is saved.
- When the quote is sent, the stage is updated to "Result Sent"
- When the client signs the pds, they add the missing business names and ABNs for each entity.
- The client is updated to converted==True and the stages in rate_review are updated to "To Switch".
- If the Stage was "No Savings Found" but the client is converted we need to send an email to their current retailer.
- We create an email (or add to Close CRM) the email with the LOA attached to update the company of the new comms email.
- We also create the same email for their current retailers to update the comms to accounts@threadlet.com.au.

## Client Comms

- When `offer.offer_type == price_change` we need to draft a **price change email** to send to the client.
- It must contain the expected monthly dollar increase/decrease based on their past 12 month usage.
- When `rate_review.percent_saved` > last_best_price.percent_saved we draft a **found more savings email**.

## Integrate client login

- Every pds is created with client details and email so clients are associated with sites and user_email is created
- email is sent to clients to create a password (during onboarding)
- If client attempts to sign in with an email with no password, an email is sent to create password

## Onboarding: (\* = not created yet)

1. receive link to share their bills via xero \*
2. email, name and role in the company is saved \* (either from xero login or create quote form)
3. new offers are found/added for each site
4. savings estimate is sent with details added
5. Start saving page is clicked (with condition that agree to electronically sign pds) - message that all switches are made automatically
6. redirected to a create password page (and email for create password link after delay if client doesnt add after clicking switch)\*
7. if email is the same as the email in step 2) that client_user is saved as one, if not, create a new client_user \*
8. if 2 emails don't match, send the other person in the company a link to create their password and access the dashboard \*

## Find tariff codes from distrubutor pricing schedules based on bills
