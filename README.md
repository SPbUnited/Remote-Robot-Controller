# Прошивка коробки связи команды SPbUnited

## Подготовка Raspberry Pi

### Имя пользователя и пароль

- login: `ssl`
- password: `1`

### Включение SSH

1. Открыть терминал
2. Ввести команду `sudo raspi-config`
3. Выбрать пункт `Interfacing Options`
4. Выбрать пункт `SSH`
5. Подтвердить включение SSH
6. Закрыть утилиту

Теперь можно подключиться к Raspberry Pi через SSH

### Настройка статического IP

1. Открыть терминал
2. Открыть `sudo nmtui` -> `Edit a connection` -> `Wired connection 1` -> `Edit...`
3. Изменить `IPv4 CONFIGURATION`: с `<Automatic>` на `<Manual>`
4. Открыв подробные настроки добавить необходимый IP адрес в поле `Addresses`, например: `10.0.120.220/24`
5. Указать в поле `Gateway` адрес роутера: `10.0.120.1`
5. Изменить `IPv6 CONFIGURATION`: с `<Automatic>` на `<Disabled>`
6. Сохранить изменения и выйти из утилиты
7. Выполнить `sudo systemctl restart NetworkManager`
8. (Опционально) Выполнить `sudo reboot`

### Настройка времени на малине

```bash
# https://unix.stackexchange.com/a/400176
sudo date -s "$(wget --method=HEAD -qSO- --max-redirect=0 google.com 2>&1 | sed -n 's/^ *Date: *//p')"
```

### Клонирование репозитория

#### Выпуск ключа для развертывания (Deploy key)

```bash
mkdir .ssh
cd .ssh
ssh-keygen
<Enter>x3
cat id_ed25519.pub
# Скопировать вывод команды. Он должен быть примерно таким:
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGGh9nHIX0ZH2xIPKUWfJ6XLmzL4VeettdvTZR5BKw+q ssl@raspberrypi

# НИ В КОЕМ СЛУЧАЕ НЕ КОПИРУЕМ ПРИВАТНЫЙ КЛЮЧ (файл без разширения .pub)
```

#### Привязывание ключа

Открываем настройки ключей развертывания:

https://github.com/SPbUnited/Remote-Robot-Controller/settings/keys

Нажимаем `Add deploy key`. В поле `Key` вставляем содержимое файла `id_ed25519.pub`. В поле `Title` вводим название ключа, например `Control box 220`.

Ставим галочку `Allow write access`. Нажимаем `Add key`.


#### Клонирование репозитория

```bash
cd ~
git clone --branch <version-name> git@github.com:SPbUnited/Remote-Robot-Controller.git rcu
cd rcu

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```
./start.py
```