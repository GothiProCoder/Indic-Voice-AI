"""Add response_audio_base64 column to conversations table.

Revision ID: 002_add_audio_base64
Revises: 001_add_auth_columns
Create Date: 2025-12-26

Stores TTS audio as compressed base64 for reliable playback from history.
Audio is gzip-compressed before base64 encoding (40-60% size reduction).
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_audio_base64'
down_revision = '001_add_auth_columns'
branch_labels = None
depends_on = None


def upgrade():
    """Add response_audio_base64 column to conversations table."""
    # Add nullable TEXT column for compressed base64 audio
    # TEXT can hold up to 1GB in PostgreSQL (our audio is ~500KB-1MB max)
    op.add_column(
        'conversations',
        sa.Column('response_audio_base64', sa.Text(), nullable=True)
    )
    
    # Add column to track if audio is compressed (for backwards compatibility)
    op.add_column(
        'conversations',
        sa.Column('audio_is_compressed', sa.Boolean(), nullable=True, server_default='true')
    )
    
    # Add column for audio duration (for UI display without decoding)
    op.add_column(
        'conversations',
        sa.Column('response_audio_duration_seconds', sa.Float(), nullable=True)
    )
    
    print("✅ Added response_audio_base64, audio_is_compressed, response_audio_duration_seconds columns")


def downgrade():
    """Remove audio columns."""
    op.drop_column('conversations', 'response_audio_duration_seconds')
    op.drop_column('conversations', 'audio_is_compressed')
    op.drop_column('conversations', 'response_audio_base64')
    
    print("✅ Removed audio columns")
