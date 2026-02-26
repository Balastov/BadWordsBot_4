# 🚀 Настройка автоматического деплоя для Cloud.ru Evolution

## 📋 Ваша конфигурация

- ✅ Платформа: Cloud.ru Evolution
- ✅ Бот: `BadWords_4.py`
- ✅ Управление: systemd (`sudo systemctl restart BadWords_4.service`)
- ✅ Доступ: SSH

---

## 🛠️ ШАГ 1: Подготовка ВМ на Cloud.ru (ОДНОкратно)

### 1.1. Подключитесь к ВМ по SSH

```bash
# Windows PowerShell
ssh root@YOUR_VM_IP

# Или Linux/Mac
ssh -l root YOUR_VM_IP
```

### 1.2. Загрузите и запустите скрипт подготовки

```bash
# Клонируем репозиторий (первое клонирование)
cd /root
git clone https://github.com/YOUR_USER/BadWordsBot.git BadWordsBot_4
cd BadWordsBot_4

# Запускаем скрипт подготовки
bash .github/setup_vm.sh
```

**Что сделает скрипт:**
- ✅ Установит Python3, Git, pip
- ✅ Скачает зависимости
- ✅ Создаст systemd сервис `BadWords_4.service`
- ✅ Запустит бота автоматически при перезагрузке ВМ
- ✅ Выведет инструкции для GitHub Actions

### 1.3. Проверьте, что бот работает

```bash
sudo systemctl status BadWords_4.service

# Должно быть:
# ● BadWords_4.service - BadWordsBot Telegram Bot
#    Loaded: loaded
#    Active: active (running)
```

---

## 🔐 ШАГ 2: Генерирование SSH ключа для GitHub Actions

### 2.1. На локальной машине (Windows PowerShell)

```powershell
# Переходим в директорию проекта
cd "G:\Pet Progects Python\BadWordsBot_4\BadWordsBot_4"

# Генерируем SSH ключ (без пароля!)
ssh-keygen -t rsa -b 4096 -f github_deploy_key -N ""

# Проверяем, что ключи созданы
ls github_deploy_key*

# Должны быть два файла:
# - github_deploy_key (ПРИВАТНЫЙ - сохраняем в GitHub Secrets)
# - github_deploy_key.pub (ПУБЛИЧНЫЙ - добавляем на ВМ)
```

### 2.2. Добавляем публичный ключ на ВМ

На ВМ (SSH сессия):

```bash
# Создаем директорию .ssh если ее нет
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Вставляем содержимое github_deploy_key.pub в authorized_keys
cat >> ~/.ssh/authorized_keys << 'EOF'
[ВСТАВЬТЕ СОДЕРЖИМОЕ github_deploy_key.pub ЗДЕСЬ]
EOF

chmod 600 ~/.ssh/authorized_keys

# Проверяем права
ls -la ~/.ssh/
# Должны быть:
# drwx------ (700) ssh
# -rw------- (600) authorized_keys
```

### 2.3. Проверяем SSH доступ с локальной машины

Windows PowerShell:

```powershell
# Проверяем подключение с новым ключом
ssh -i github_deploy_key root@YOUR_VM_IP "echo 'SSH работает!'"

# Если сработало - переходим к следующему шагу
```

---

## 🔒 ШАГ 3: Добавляем Secrets в GitHub

1. Откройте ваш GitHub репозиторий
2. Перейдите: **Settings → Secrets and variables → Actions**
3. Нажмите **"New repository secret"**

Создайте 5 секретов:

### 3.1. SSH_PRIVATE_KEY

- **Name:** `SSH_PRIVATE_KEY`
- **Value:** Полное содержимое файла `github_deploy_key`

```powershell
# Windows: автоматически скопировать в буфер обмена
Get-Content github_deploy_key | Set-Clipboard

# Или открыть файл и скопировать вручную
notepad github_deploy_key
```

### 3.2. SSH_USER

- **Name:** `SSH_USER`
- **Value:** `root`

### 3.3. SSH_HOST

- **Name:** `SSH_HOST`
- **Value:** IP адрес вашей ВМ на Cloud.ru (например: `185.203.112.45`)

```bash
# Узнать IP ВМ можно с личного кабинета Cloud.ru или командой:
hostname -I | awk '{print $1}'
```

### 3.4. SSH_PORT

- **Name:** `SSH_PORT`
- **Value:** `22` (стандартный SSH порт)

### 3.5. DEPLOY_PATH

- **Name:** `DEPLOY_PATH`
- **Value:** `/root/BadWordsBot_4`

---

## ✅ ШАГ 4: Тестируем деплой

### 4.1. Внесите небольшое изменение в код

```powershell
# На локальной машине
cd "G:\Pet Progects Python\BadWordsBot_4\BadWordsBot_4"

# Отредактируйте любой файл или добавьте комментарий
# Например, в BadWords_4.py добавьте пустую строку в конце

# Сохраните файл
```

### 4.2. Создайте commit и push в main

```powershell
git add .
git commit -m "test: github actions deploy"
git push origin main
```

### 4.3. Смотрите статус деплоя на GitHub

1. Откройте ваш репозиторий на GitHub
2. Перейдите на вкладку **"Actions"**
3. Нажмите на workflow "Deploy Bot to Cloud.ru (systemd)"
4. Смотрите логи в реальном времени

---

## 📊 Проверка логов

### На GitHub Actions:
```
✅ Начало деплоя BadWordsBot
📂 Рабочая директория: /root/BadWordsBot_4
🔍 Текущий коммит: ...
📥 Обновляем код из репозитория...
✅ Новый коммит: ...
🔄 Перезагружаем сервис BadWords_4...
✅ Сервис успешно запущен!
```

### На ВМ (проверка вручную):
```bash
# Просмотр статуса бота
sudo systemctl status BadWords_4.service

# Просмотр логов в реальном времени
sudo journalctl -u BadWords_4.service -f

# Просмотр последних 50 строк
sudo journalctl -u BadWords_4.service -n 50 --no-pager
```

---

## 🐛 Troubleshooting

### ❌ "Permission denied (publickey)" при деплое

**Решение:**
```bash
# На ВМ проверьте права
ls -la ~/.ssh/

# Должно быть:
# drwx------ 2 root root 4096 ... ssh
# -rw------- 1 root root 1234 ... authorized_keys

# Если прав неправильно - исправьте:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### ❌ "Сервис не запущен" при деплое

**Решение:**
```bash
# На ВМ проверьте логи бота
sudo journalctl -u BadWords_4.service -n 50

# Проверьте синтаксис Python файла
python3 -m py_compile /root/BadWordsBot_4/BadWords_4.py

# Проверьте зависимости
pip3 list | grep -E "telebot|requests|beautifulsoup"
```

### ❌ "git: command not found" при деплое

**Решение:**
```bash
# На ВМ переустановите git
sudo apt-get update
sudo apt-get install -y git
```

### ❌ SSH ключ не работает локально

**Решение:**
```powershell
# Проверьте что ключ имеет правильные права (Windows)
Get-Item github_deploy_key | Select-Object Mode

# Попробуйте подключиться с явным указанием ключа
ssh -i github_deploy_key -v root@YOUR_VM_IP

# -v показывает детальные логи подключения
```

---

## 📝 Полезные команды

### Работа с ботом вручную

```bash
# Статус
sudo systemctl status BadWords_4.service

# Запустить
sudo systemctl start BadWords_4.service

# Остановить
sudo systemctl stop BadWords_4.service

# Перезагрузить
sudo systemctl restart BadWords_4.service

# Логи в реальном времени
sudo journalctl -u BadWords_4.service -f

# Логи за сегодня
sudo journalctl -u BadWords_4.service --since today

# Логи последние 100 строк
sudo journalctl -u BadWords_4.service -n 100
```

### Работа с кодом на ВМ

```bash
# Обновить код вручную
cd /root/BadWordsBot_4
git pull origin main

# Проверить синтаксис
python3 -m py_compile *.py

# Запустить бота вручную (без systemd)
python3 BadWords_4.py
```

---

## 🎯 Как работает деплой

```
┌─────────────────────────┐
│  Локальная машина       │
│  git push origin main   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  GitHub Webhook         │
│  Триггер: push в main   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  GitHub Actions (Ubuntu)            │
│  1. Проверка кода                   │
│  2. SSH подключение к ВМ            │
│  3. git pull origin main            │
│  4. systemctl restart               │
└────────────┬────────────────────────┘
             │
             ▼
     ┌──────────────┐
     │ Cloud.ru ВМ  │
     │              │
     │  ✅ Обновлен │
     │  ✅ Запущен  │
     └──────────────┘
```

---

## ✨ Готово!

Теперь ваш деплой полностью автоматизирован:

✅ Каждый `git push origin main` = автоматический деплой на ВМ
✅ Бот перезагружается через systemd
✅ Все ошибки видны в GitHub Actions
✅ Логи доступны через `journalctl` на ВМ

**Успех! 🚀**
