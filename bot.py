import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# Retrieve the bot token from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Connect to the SQLite database
conn = sqlite3.connect('real_madrid.db', check_same_thread=False)
cursor = conn.cursor()
print(conn)

# Handle the /start and /hello commands with an image and buttons
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    username = message.from_user.username
    first_name = message.from_user.first_name

    # If the user has a username, use it; otherwise, use their first name
    user_identifier = f"{username}" if username else first_name

    # Welcome message
    welcome_message = (f"Welcome {user_identifier} to the ultimate Real Madrid C.F. 2024-25 experience—"
                       "Where champions are made and legends live on! \n"
                       "Choose an option below to explore:")

    # Path to the image or URL
    image_path = 'Color-Real-Madrid-Logo.jpg'  # Local image file
    
    # Inline keyboard buttons
    markup = InlineKeyboardMarkup()
    stats_button = InlineKeyboardButton("Player Stats", callback_data='player_stats')
    news_button = InlineKeyboardButton("Team Updates and Latest News", callback_data='team_news')
    match_links_button = InlineKeyboardButton("Match Links", callback_data='match_links')
    
    # Add the buttons to the markup
    markup.add(stats_button, news_button, match_links_button)

    # Sending the image along with the message and buttons
    with open(image_path, 'rb') as image_file:  # Ensure the image is present in the working directory
        bot.send_photo(message.chat.id, image_file, caption=welcome_message, reply_markup=markup)

# Callback handler for button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'player_stats':
        # Create a new inline keyboard with jersey numbers
        markup = InlineKeyboardMarkup(row_width=5)  # Adjust row_width for better layout
        # Dynamically add buttons for numbers 1 to 25
        buttons = [InlineKeyboardButton(str(i), callback_data=f'jersey_{i}') for i in range(1, 26)]
        markup.add(*buttons)

        # Send message with the buttons
        bot.send_message(call.message.chat.id, "Click the Jersey No to know the details and stats of the player", reply_markup=markup)
    
    elif call.data == 'team_news':
        bot.send_message(call.message.chat.id, "To know the team updates and latest news click the channel link below  https://t.me/+uccr6ljfLTkyYzZl!")
    
    elif call.data == 'match_links':
        bot.send_message(call.message.chat.id, "Laliga matches will be freely available at https://www.gxr.world/")

# Function to retrieve player stats from SQLite
def get_player_stats(jersey_number):
    try:
        cursor.execute('SELECT player_name, position, age, goals, assists, matches_played FROM players WHERE jersey_number = ?', (int(jersey_number),))
        player = cursor.fetchone()  # Fetch one matching record
        if player:
            print(f"Player data found for jersey number {jersey_number}: {player}")  # Debugging info
        else:
            print(f"No data found for jersey number: {jersey_number}")  # Debugging info
        return player
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")  # Error handling for database issues
        return None

# Handle jersey number selections
@bot.callback_query_handler(func=lambda call: call.data.startswith('jersey_'))
def handle_jersey(call):
    jersey_number = int(call.data.split('_')[1])  # Extract the jersey number
    print(f"Jersey number selected: {jersey_number}")  # Debugging info
    player = get_player_stats(jersey_number)  # Fetch player stats
    
    if player:
        player_name, position, age, goals, assists, matches_played = player
        # Send a formatted message with the player stats
        bot.send_message(
            call.message.chat.id, 
            f"Player Stats for Jersey No: {jersey_number}\n"
            f"Name: {player_name}\n"
            f"Position: {position}\n"
            f"Age: {age}\n"
            f"Goals: {goals}\n"
            f"Assists: {assists}\n"
            f"Matches Played: {matches_played}"
        )
    else:
        bot.send_message(call.message.chat.id, f"No player found for Jersey No: {jersey_number}")

# Handle all other text messages
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, 'To initiate or set up the bot just type /start or /hello')

# Start polling to keep the bot running
bot.infinity_polling()
