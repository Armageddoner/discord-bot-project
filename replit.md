# Discord Quote Bot

## Overview

This is a Discord bot application designed to store and manage quotes from Discord server members. The bot uses Discord's slash command system to allow users to add, retrieve, and manage quotes on a per-guild (server) basis. Quotes are persisted to a local JSON file, with each guild maintaining its own separate collection of quotes.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Technology**: Discord.py library with slash commands (app_commands)
- **Rationale**: Uses Discord's modern slash command interface rather than traditional prefix commands for better user experience and discoverability
- **Bot Structure**: Custom `QuoteBot` class extending `discord.Client` with integrated `CommandTree` for slash command management

### Authentication & Authorization
- **Token Management**: Environment-based authentication using dotenv
- **Security**: Discord bot token stored in `.env` file and loaded via environment variables
- **Permissions**: Bot uses Discord Intents for message_content, members, and messages access

### Data Storage
- **Solution**: Local JSON file-based storage (`quotes.json`)
- **Structure**: Nested dictionary with guild IDs as keys, each containing an array of quote objects
- **Quote Schema**: 
  - `id`: Sequential integer identifier
  - `user_id`: Discord user ID (snowflake)
  - `user_name`: Discord username string
  - `quote`: The actual quote text
- **Rationale**: Simple, file-based storage is appropriate for this scale. No complex queries or relationships require a database
- **Alternatives Considered**: Could migrate to SQLite or PostgreSQL for better concurrent access and querying capabilities if the bot scales

### Multi-Tenancy
- **Approach**: Guild-based quote isolation - each Discord server maintains its own independent quote collection
- **Implementation**: Guild IDs (stored as strings) serve as top-level keys in the JSON structure
- **Benefits**: Prevents quote collision between different servers, allows the bot to operate in multiple guilds simultaneously

### Logging
- **Implementation**: File-based logging to `discord.log` with UTF-8 encoding
- **Purpose**: Debug and monitor bot activity and errors

### Design Patterns
- **Lazy Loading**: Quotes are loaded once at bot initialization and kept in memory
- **Write-Through Cache**: In-memory quotes dictionary is immediately synced to disk on updates
- **Encapsulation**: Quote management logic (load, save, get_guild_quotes) is encapsulated within the QuoteBot class

## External Dependencies

### Discord API
- **Library**: discord.py
- **Purpose**: Primary interface for Discord bot functionality, event handling, and slash commands
- **Integration Points**: 
  - Gateway connection for receiving events
  - Slash command registration and handling via CommandTree
  - User and guild data access

### Environment Configuration
- **Library**: python-dotenv
- **Purpose**: Manage sensitive credentials and configuration
- **Variables**: `DISCORD_TOKEN` for bot authentication

### Standard Libraries
- **json**: Quote data serialization and persistence
- **os**: File system operations and environment variable access
- **logging**: Application logging and debugging

### Discord Developer Portal
- **Purpose**: Bot application registration and OAuth2 configuration
- **Required Setup**: Bot token generation, intent configuration, OAuth2 URL generation for server invites