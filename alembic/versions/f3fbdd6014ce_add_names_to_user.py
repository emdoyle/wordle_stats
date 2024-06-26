"""add names to user

Revision ID: f3fbdd6014ce
Revises: 4991b958931a
Create Date: 2022-01-24 14:00:06.411067

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "f3fbdd6014ce"
down_revision = "4991b958931a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("display_name", sa.String(), server_default="", nullable=False),
    )
    op.add_column(
        "user", sa.Column("real_name", sa.String(), server_default="", nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "real_name")
    op.drop_column("user", "display_name")
    # ### end Alembic commands ###
