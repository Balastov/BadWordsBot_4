#!/bin/bash

# Скрипт для подготовки ВМ на Cloud.ru Evolution к автодеплою
# Запустить как root: bash setup_vm.sh

set -e

echo "=========================================="
echo "🚀 Подготовка ВМ Cloud.ru для автодеплоя"
echo "=========================================="

# 1. Проверяем, что скрипт запущен с правами root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Этот скрипт должен быть запущен с правами root (sudo)"
   exit 1
fi

# 2. Устанавливаем необходимые пакеты
echo "📦 Установка зависимостей..."
apt-get update
apt-get install -y \
  git \
  python3 \
  python3-pip \
  curl \
  wget

# 3. Создаем рабочую директорию
echo "📂 Создание рабочей директории..."
DEPLOY_DIR="/root/BadWordsBot_4"
mkdir -p $DEPLOY_DIR

# 4. Клонируем репозиторий (если еще не клонирован)
echo "📥 Клонирование репозитория..."
if [ ! -d "$DEPLOY_DIR/.git" ]; then
  echo "Введите URL вашего GitHub репозитория (например: https://github.com/username/BadWordsBot):"
  read REPO_URL
  git clone $REPO_URL $DEPLOY_DIR
fi

cd $DEPLOY_DIR

# 5. Устанавливаем Python зависимости
echo "📚 Установка Python пакетов..."
pip3 install --upgrade pip

if [ -f "requirements.txt" ]; then
  echo "📦 Устанавливаем пакеты из requirements.txt..."
  pip3 install -r requirements.txt
else
  echo "⚠️ requirements.txt не найден, устанавливаем стандартные пакеты..."
  pip3 install pyTelegramBotAPI requests beautifulsoup4
fi

# 6. Копируем systemd сервис
echo "⚙️ Настройка systemd сервиса..."
SERVICE_FILE="/etc/systemd/system/BadWords_4.service"

if [ -f ".github/BadWords_4.service" ]; then
  cp .github/BadWords_4.service $SERVICE_FILE
else
  echo "⚠️ .github/BadWords_4.service не найден, создаю вручную..."
  cat > $SERVICE_FILE << 'SERVICE_EOF'
[Unit]
Description=BadWordsBot Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/BadWordsBot_4
ExecStart=/usr/bin/python3 /root/BadWordsBot_4/BadWords_4.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICE_EOF
fi

chmod 644 $SERVICE_FILE

# 7. Перезагружаем systemd конфигурацию
echo "🔄 Перезагрузка systemd конфигурации..."
systemctl daemon-reload

# 8. Включаем автозапуск
echo "✅ Включение автозапуска бота..."
systemctl enable BadWords_4.service

# 9. Стартуем сервис
echo "🚀 Запуск бота..."
systemctl restart BadWords_4.service

# 10. Проверяем статус
sleep 2
if systemctl is-active --quiet BadWords_4.service; then
  echo "✅ Бот успешно запущен!"
  echo ""
  systemctl status BadWords_4.service --no-pager
else
  echo "❌ Ошибка при запуске бота!"
  echo "📋 Логи:"
  journalctl -u BadWords_4.service -n 20 --no-pager
  exit 1
fi

# 11. Инструкция для GitHub Actions
echo ""
echo "=========================================="
echo "✅ ВМ готова к автодеплою!"
echo "=========================================="
echo ""
echo "🔐 Добавьте в GitHub Secrets следующие переменные:"
echo ""
echo "SSH_PRIVATE_KEY:"
echo "  (содержимое вашего приватного SSH ключа)"
echo ""
echo "SSH_USER: root"
echo ""
echo "SSH_HOST:"
HOSTNAME=$(hostname -I | awk '{print $1}')
echo "  $HOSTNAME (или ваш домен)"
echo ""
echo "SSH_PORT: 22"
echo ""
echo "DEPLOY_PATH: /root/BadWordsBot_4"
echo ""
echo "=========================================="
echo "📝 Полезные команды для работы:"
echo "=========================================="
echo ""
echo "Просмотр статуса бота:"
echo "  sudo systemctl status BadWords_4.service"
echo ""
echo "Просмотр логов в реальном времени:"
echo "  sudo journalctl -u BadWords_4.service -f"
echo ""
echo "Просмотр последних 50 строк логов:"
echo "  sudo journalctl -u BadWords_4.service -n 50"
echo ""
echo "Перезапуск бота:"
echo "  sudo systemctl restart BadWords_4.service"
echo ""
echo "Остановка бота:"
echo "  sudo systemctl stop BadWords_4.service"
echo ""
echo "Удаление сервиса:"
echo "  sudo systemctl disable BadWords_4.service"
echo "  sudo rm /etc/systemd/system/BadWords_4.service"
echo "  sudo systemctl daemon-reload"
echo ""
