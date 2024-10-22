# Poll Bot

This repository contains a simple poll bot built for the Bale Messenger platform using the Balethon library. The bot allows users to participate in polls and record their responses, ensuring that each user can only respond once per poll.

## Features

- Start polls with the `/start` command.
- Users can choose from multiple polls.
- Each poll consists of multiple questions with options for responses.
- User responses are saved in a SQLite database.
- Each user can only participate in a poll once.
- The bot provides feedback on user participation.

## Technologies Used

- **Python**: The main programming language used for the bot.
- **Balethon**: A Python library for building bots for the Bale Messenger.
- **SQLite**: A lightweight database for storing user responses.

## Setup

### Prerequisites

- Python 3.x
- An account on Bale Messenger
- Your bot token from the Bale Messenger Bot API

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/poll-bot.git
   cd poll-bot
   ```

2. Change `config.py` file in the root directory and add your bot token:
   ```python
   TOKEN = "YOUR_BOT_TOKEN"
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot by sending `/start` in a private chat.
2. Choose a poll to participate in.
3. Answer the questions presented in the poll.
4. Your responses will be recorded, and you will receive a thank-you message after completing the poll.

## Database

User responses are stored in a SQLite database named `poll_responses.db`. This database contains a table for tracking user responses to polls.

## Contribution

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

