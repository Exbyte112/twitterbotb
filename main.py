import os
import time
import random
import json
from typing import NoReturn, Dict, List
import pymongo
from twikit import Client, Tweet, TwitterException

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
mongoClient = pymongo.MongoClient(MONGO_URI)
mongoDB = mongoClient["KronosTwikit"]
main_acct = mongoDB["KronosTwikit"]
secondary_accts = mongoDB["KronosTwikitSecondary"]
secondary_acct_replies = mongoDB["KronosTwikitSecondaryReplies"]
bot_power_state = mongoDB["KronosTwikitPowerState"]

def get_power_state() -> str:
    power_state = bot_power_state.find()[0]
    return power_state["power_state"]

def get_secondary_accounts() -> Dict[str, Dict[str, str]]:
    formatted_details = {}
    secondary_accts_details = secondary_accts.find()
    for secondary_acct in secondary_accts_details:
        formatted_details[str(secondary_acct["_id"])] = {
            "email": secondary_acct["email"],
            "password": secondary_acct["password"],
            "username": secondary_acct["username"],
        }
    return formatted_details

def clean_up_old_tweet_files(directory: str, max_age_hours: int) -> None:
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            if (current_time - os.path.getmtime(file_path)) > max_age_seconds:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

def watch_main_account(
    client: Client, main_acct_username: str, main_acct_id: str
) -> NoReturn:
    usr = client.get_user_by_screen_name(main_acct_username)
    old_reply = usr.get_tweets(tweet_type="Replies")[0]
    first_run = True

    while True:
        print(f"\n\nChecking {main_acct_username}'s account\n\n")
        new_tweet = usr.get_tweets(tweet_type="Replies")[0]

        if new_tweet.replies is None:
            print(f"Skipping tweet: {new_tweet.text}\nNo replies found")
            time.sleep(random.randint(10, 20))
            continue

        new_reply = next(
            (reply for reply in new_tweet.replies if reply.user.id == main_acct_id),
            None,
        )

        if new_reply and new_reply.id != old_reply.id:
            print(f"New reply found: {new_reply.text}")

            if not first_run:
                handle_new_reply(client, new_reply)

            old_reply = new_reply
            first_run = False
        else:
            print("No new replies found")

        sleep_time = random.randint(15, 40) 
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

def random_reply() -> str:
    replies = secondary_acct_replies.find()
    replies_list = []
    for reply in replies:
        replies_list.append(reply["replies"])
    
    replies_list = replies_list[0]
    return random.choice(replies_list)

def handle_new_reply(client: Client, new_reply: Tweet) -> None:
    secondary_accounts = get_secondary_accounts()

    for bot_data in secondary_accounts.values():
        try:
            client.logout()
        except Exception as e:
            print(f"Error logging out: {str(e)}")

        try:
            client.login(
                auth_info_1=bot_data["email"],
                password=bot_data["password"],
            )
            print(f"Logged in as {bot_data['username']}")

            try:
                new_reply.favorite()
                print("Favorited the tweet")
            except Exception as e:
                print(f"Error favoriting the tweet: {str(e)}")

            try:
                selected_reply = random_reply()
                print(f"Selected reply: {selected_reply}")
                new_reply.reply(selected_reply)
                print("Replied to the tweet")
            except Exception as e:
                print(f"Error replying to the tweet: {str(e)}")

            time.sleep(random.randint(60, 120))  # Sleep between 1-2 minutes between actions

        except Exception as e:
            print(f"Error with bot {bot_data['username']}: {str(e)}")

def main():
    main_acct_details = main_acct.find_one({"_id": 0})

    client = Client("en-US")
    client.login(
        auth_info_1=main_acct_details["main_bot_username"],
        auth_info_2=main_acct_details["main_bot_email"],
        password=main_acct_details["main_bot_password"],
    )

    main_acct_username = main_acct_details["main_bot_username"]
    main_acct_id = client.get_user_by_screen_name(main_acct_username).id

    try:
        watch_main_account(client, main_acct_username, main_acct_id)
    except TwitterException as e:
        print(f"Twitter Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    while True:
        try:
            state = get_power_state()
            if state == "on":
                main()
            else:
                print("Bot is currently turned off")
                time.sleep(60)
        except Exception as e:
            print(f"Main loop exception: {str(e)}")
        time.sleep(60) 