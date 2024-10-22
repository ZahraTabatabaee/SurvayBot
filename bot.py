from time import time
from balethon import Client
from balethon.conditions import regex, private
from balethon.objects import Message, User, CallbackQuery, InlineKeyboard
from balethon.states import StateMachine
import sqlite3

# Configurations for the bot
import config


bot = Client(config.TOKEN)

# To manage user states
User.state_machine = StateMachine("user_states.db")

# Database class to handle SQLite operations
class Database:
    def __init__(self, db_file="poll_responses.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        """Create a table for poll responses if it doesn't exist"""
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS poll_responses (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    poll_code TEXT,
                                    question_number INTEGER,
                                    selected_option INTEGER
                                 )''')

    def save_poll(self, poll):
        # This function is for saving the poll itself, not required for user responses
        pass

    def load_poll(self, poll_code):
        # Since this is a mock, we handle polls in-memory
        return Database.polls.get(poll_code)

    def save_user_response(self, user_id, poll_code, question_number, selected_option):
        """Save the user's response to the database"""
        with self.conn:
            self.conn.execute('''INSERT INTO poll_responses (user_id, poll_code, question_number, selected_option)
                                 VALUES (?, ?, ?, ?)''', (user_id, poll_code, question_number, selected_option))
        print(f"User {user_id}'s response saved: poll {poll_code}, question {question_number}, option {selected_option}")

    def has_user_voted(self, user_id, poll_code):
        """Check if the user has already voted in the poll"""
        with self.conn:
            result = self.conn.execute('''SELECT COUNT(*) FROM poll_responses
                                          WHERE user_id = ? AND poll_code = ?''', 
                                          (user_id, poll_code)).fetchone()
        return result[0] > 0


# Mock Database (replace with actual database functionality)
Database.polls = {}  # Mock poll storage

# Poll Class Definition
class Poll:
    def __init__(self, code, creator, question_1, options_1, question_2, options_2, question_3, options_3, question_4, options_4):
        self.code = code
        self.creator = creator
        self.questions = [
            (question_1, options_1),
            (question_2, options_2),
            (question_3, options_3),
            (question_4, options_4)
        ]
        self.is_anonymous = True
        self.is_closed = False

    def to_inline_keyboard(self, question_number):
        """Generate the inline keyboard based on the question number"""
        if 1 <= question_number <= len(self.questions):
            options = self.questions[question_number - 1][1]
        else:
            return None

        # Create inline keyboard layout
        buttons = []
        for i, option in enumerate(options):
            buttons.append([(option, f"option.{self.code}.{question_number}.{i}")])
        
        return buttons

    def get_question(self, question_number):
        """Get the question text based on the question number"""
        if 1 <= question_number <= len(self.questions):
            return self.questions[question_number - 1][0]
        return None

async def ask_question(poll, question_number, message):
    """Helper function to ask a question or finish the poll"""
    if question_number <= len(poll.questions):
        # Display the question with options
        question_text = poll.get_question(question_number)
        options = poll.to_inline_keyboard(question_number)
        await message.edit_text(question_text, InlineKeyboard(*options))
    else:
        # Poll finished
        await message.edit_text("از شرکت شما در نظرسنجی سپاسگزاریم!")

# Command to start interaction with the bot and show polls
@bot.on_message(private)
async def start(message: Message):
    if message.content == '/start' or message.content == '/list':
        await message.reply(
            "سلام!\nلطفاً نظرسنجی‌ مورد نظرت رو انتخاب کن:",
            InlineKeyboard(
                [("نظرسنجی 1", "poll.1")],
            )
        )

# Handle callback for showing selected poll
@bot.on_callback_query(regex("^poll"))
async def show_poll(callback_query: CallbackQuery):
    _, poll_code = callback_query.data.split(".")
    
    # Assign the fake poll based on the selected poll code
    polls = {"1": poll1}
    selected_poll = polls.get(poll_code)

    user_id = callback_query.author.id

    # Check if the user has already voted in this poll
    if db.has_user_voted(user_id, poll_code):
        await callback_query.message.reply("شما قبلاً در این نظرسنجی شرکت کرده‌اید!")
        return

    if selected_poll:
        # Start the survey with question 1
        opt = selected_poll.to_inline_keyboard(1)
        await callback_query.message.reply(f"{selected_poll.get_question(1)}",  
                                        InlineKeyboard(*opt))


# Callback query handler for voting/answering
@bot.on_callback_query(regex("^option"))
async def handle_vote(callback_query: CallbackQuery):
    _, poll_code, question_number, option_index = callback_query.data.split(".")
    question_number = int(question_number)
    option_index = int(option_index)

    user_id = callback_query.author.id

    # Fetch the correct poll from our mock database
    polls = {
        "1": db.load_poll("1"),
    }
    poll = polls.get(poll_code)
    
    if not poll:
        return

    # Save user response in the database
    db.save_user_response(user_id, poll_code, question_number, option_index)

    # Ask the next question or finish the poll
    if question_number == len(poll.questions):
        await ask_question(poll, question_number + 1, callback_query.message)
    else:
        await ask_question(poll, question_number + 1, callback_query.message)


# Entry point for the bot
if __name__ == "__main__":
    # Creating fake polls (this should be from the database in a real case)
    poll1 = Poll(
        code="1",
        creator=1,
        question_1="به این مورد نمره بده \nارائه خلاقانه",
        options_1=["خیلی خوب", "خوب", "متوسط", "بد" , "خیلی بد"],
        question_2="به این مورد نمره بده \nارائه مشارکتی (اینگیج کردن شنونده‌ها)",
        options_2=["خیلی خوب", "خوب", "متوسط", "بد" , "خیلی بد"],
        question_3="به این مورد نمره بده \nارائه دقیق (دیتامحور بودن و زمانبندی مناسب)",
        options_3=["خیلی خوب", "خوب", "متوسط", "بد" , "خیلی بد"],
        question_4="به این مورد نمره بده \nارائه آموزنده (درس آموخته‌ها به خوبی گفته شدن)",
        options_4=["خیلی خوب", "خوب", "متوسط", "بد" , "خیلی بد"],
    )

    # Creating fake polls in the mock database
    db = Database()  # Initialize the database
    Database.polls["1"] = poll1  # Save poll in mock storage
    
    bot.run()
