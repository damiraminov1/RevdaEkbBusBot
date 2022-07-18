echo Здравствуйте! Давайте приступим к настройке бота.
echo Введите Telegram token:
read telegram_token
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install docker-compose -y
sudo TELEGRAM_BOT_TOKEN="$telegram_token" docker-compose up -d --build