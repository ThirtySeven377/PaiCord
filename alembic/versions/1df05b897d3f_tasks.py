"""tasks

Revision ID: 1df05b897d3f
Revises: a1c10da5704b
Create Date: 2023-07-23 14:44:59.592519

"""
import logging

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import NoSuchTableError

# revision identifiers, used by Alembic.
revision = "1df05b897d3f"
down_revision = "a1c10da5704b"
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    task_table = op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("chat_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "SIGN",
                "RESIN",
                "REALM",
                "EXPEDITION",
                "TRANSFORMER",
                "CARD",
                name="tasktypeenum",
            ),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "STATUS_SUCCESS",
                "INVALID_COOKIES",
                "ALREADY_CLAIMED",
                "NEED_CHALLENGE",
                "GENSHIN_EXCEPTION",
                "TIMEOUT_ERROR",
                "BAD_REQUEST",
                "FORBIDDEN",
                name="taskstatusenum",
            ),
            nullable=True,
        ),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_general_ci",
    )
    op.create_index("task_1", "task", ["user_id"], unique=False)
    try:
        statement = "SELECT * FROM sign;"
        old_sign_table_data = connection.execute(text(statement))
    except NoSuchTableError:
        logger.warning("Table 'sign' doesn't exist")
        return  # should not happen
    if old_sign_table_data is not None:
        for row in old_sign_table_data:
            try:
                user_id = row["user_id"]
                chat_id = row["chat_id"]
                time_created = row["time_created"]
                time_updated = row["time_updated"]
                status = row["status"]
                task_type = "SIGN"
                insert = task_table.insert().values(
                    user_id=int(user_id),
                    chat_id=int(chat_id),
                    time_created=time_created,
                    time_updated=time_updated,
                    type=task_type,
                    status=status,
                )
                with op.get_context().autocommit_block():
                    connection.execute(insert)
            except Exception as exc:  # pylint: disable=W0703
                logger.error("Process sign->task Exception", exc_info=exc)  # pylint: disable=W0703
    op.drop_table("sign")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sign",
        sa.Column("id", mysql.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("user_id", mysql.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("chat_id", mysql.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("time_created", mysql.DATETIME(), nullable=True),
        sa.Column("time_updated", mysql.DATETIME(), nullable=True),
        sa.Column(
            "status",
            mysql.ENUM(
                "STATUS_SUCCESS",
                "INVALID_COOKIES",
                "ALREADY_CLAIMED",
                "GENSHIN_EXCEPTION",
                "TIMEOUT_ERROR",
                "BAD_REQUEST",
                "FORBIDDEN",
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", "user_id"),
        mysql_collate="utf8mb4_general_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.drop_index("task_1", table_name="task")
    op.drop_table("task")
    # ### end Alembic commands ###
