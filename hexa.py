from datetime import datetime, timedelta, timezone
import logging
import time
import feedparser
import json
import requests


def format_for_telegram(entry):
    """Formats an RSS feed entry for publishing to Telegram"""
    tags = ' '.join('\#' + tag.get('term') for tag in entry.tags)
    return f'''{tags}
[{entry.title}]({entry.link})'''


def publish_to_telegram(entry, channel_id, telegram_bot_token):
    """Publishes an RSS feed entry to a Telegram channel"""
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "chat_id": channel_id,
        "text": format_for_telegram(entry),
        "disable_web_page_preview": False,
        "parse_mode": "MarkdownV2"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
    except Exception as e: logging.error(f'Error sending message to Telegram channel {channel_id}: {e}')

def analyze_rss():
    """Analyzes the RSS feed and publishes new entries to the designated Telegram channels"""
    global last_sync
    rss_feed_url = config['rss_feed_url']
    telegram_channels = config['telegram_channels']
    telegram_bot_token = config['telegram_bot_token']
    feed = feedparser.parse(rss_feed_url)
    for entry in feed.entries:
        published_time = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S.%fZ")
        logging.info(f'last post: {published_time}, last sync: {last_sync}')
        if published_time > last_sync:
            for _, channel in telegram_channels.items() :
                if "rss_feed_url" in channel:
                    rss_feed_url = channel["rss_feed_url"]
                publish_to_telegram(entry, channel['id'], telegram_bot_token)
                last_sync = now
        else: break

if __name__ == '__main__':
    logging.basicConfig(filename='file_logger.txt', level=logging.ERROR)
    with open('config.json', 'r') as f:
        config = json.load(f) 
    while True:
        now = datetime.now(timezone(timedelta(hours=config['timedelta']))).replace(tzinfo=None)
        last_sync = config.get('last_sync') and datetime.fromisoformat(config.get('last_sync')) or now
        analyze_rss()
        config['last_sync'] = last_sync.isoformat()
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        time.sleep(config["sync_interval"])