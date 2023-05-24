# Hexagram

Designed to be forgotten.

## [Hexa](https://t.me/felicia_pub/249)

Sync your Hexo(RSS/Atom) posts to Telegram.
- [x] tags and categories
- [ ] instant view
## Gram

Sync your Telegram posts to Hexo.
- [ ] Edit
- [ ] RSS as middleware if possible

# Deploy


1. git clone this repository, cd into it
2. `pip install -r requirement.txt`
2. `mv config.json.sample config.json`
3. Edit config.json with your telegram_bot_token, channel_id(s) and rss_feed_url(s)
4. `python hexa.py`
5. you write gram.py