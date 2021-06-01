from alembic import op
import sqlalchemy as sa


revision = 'c8ac14f4ea7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('youtube_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__youtube_channels')),
    sa.UniqueConstraint('url', name=op.f('uq__youtube_channels__url'))
    )


def downgrade():
    op.drop_table('youtube_channels')
