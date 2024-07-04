CREATE VIEW view_ids AS
    SELECT users.username, users.id, telegram.telegram_id, discord.discord_id, steam.steam_id
    FROM users
    JOIN telegram ON users.id = telegram.user_id
    JOIN discord ON users.id = discord.user_id
    JOIN steam ON users.id = steam.user_id;
