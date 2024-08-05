import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime
${imports if imports else ""}

"""
${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

# Revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


# -- Notes For Developers --
# When making an alembic revision file, think carefully about the database structure,
# and ask yourself the following questions:
# 1. Should I allow null values?
#    EG: `client_users` login via email, so `email` column must not be null.
#
# 3. Should I set a default value?
#    EG: `payment_type` in sites must be `standard_payment` by default, indicating bank transfer.
#
# 4. Should I enforce a value (or combination of values) to be unique?
#    EG: Our accounting software doesn't allow multiple invoices with the same invoice number. Therefore
#    `invoice_num` must be unique in the invoice table
#
# 5. Am I using foreign keys to directly relate relevant tables?
#    EG: All prices have a retailer. To ensure data-consistency, we use a `retailer_id` to reference
#    the retailers table.
#
# 6. Are there any constraints I can add to prevent the data model breaking?
#    EG: We must not record bill usage twice for a site. Therefore, we have a
#    unique constraint on the combination of `site_id`, `invoice_num`, and `start_date`.
#
# 7. Do I need to migrate existing data while updating my schema?
#    EG: We used to store`invoicing_contact` email in the sites table. When we deprecated this,
#    we used the alembic revision file migrated the existing data into the new contacts table.
#
# Before opening a pull-request, ensure you have answered each of these questions.
# If necessary, ask for a clone of the production database and test your hypothesis.


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
