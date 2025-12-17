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
<!-- 
### Установка Docker

https://docs.docker.com/engine/install/ubuntu/

```
curl -sSL https://get.docker.com | sh

sudo sh -eux <<EOF
# Install newuidmap & newgidmap binaries
apt-get install -y uidmap
EOF

dockerd-rootless-setuptool.sh install
``` -->

### Установка подходящей версии Python

```bash
# install pyenv
# https://github.com/pyenv/pyenv
curl -fsSL https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

exec "$SHELL"
```

```bash
# install python build essentials
# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

```bash
# install python 3.9.2
pyenv install 3.9.2
pyenv global 3.9.2
```

### Установка библиотеки lgpio

```bash
# https://abyz.me.uk/lg/download.html

cd ~/Downloads
wget http://abyz.me.uk/lg/lg.zip
unzip lg.zip
cd lg
make
sudo make install
```

### Включение SPI

```bash
sudo sed -i "s/#dtparam=spi=on/dtparam=spi=on/" /boot/firmware/config.txt

sudo vi /boot/firmware/config.txt
# https://raspberrypi.stackexchange.com/a/147321
# add "dtoverlay=spi0-0cs" to the same file

sudo reboot
```

### Клонирование репозитория

#### Выпуск ключа для развертывания (Deploy key)

```bash
mkdir ~/.ssh
cd ~/.ssh
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

#### Развертывание окружения

```bash
cd ~
git clone --branch <version-name> git@github.com:SPbUnited/Remote-Robot-Controller.git rcu
cd rcu

pip install -r requirements.txt
```

### Настройка автозапуска

```bash
sudo apt install supervisor

cd ~/rcu/supervisor
sudo ln rcu.conf /etc/supervisor/conf.d/

sudo supervisorctl reread
sudo supervisorctl update
```

## Ручной запуск

### Все сразу

```bash
honcho start
```

### Только бекэнд

```bash
python3 start.py console
```

### Только фронтэнд

```bash
./chrome.sh # При первом запуске спросит пароль для new keyring. Можно оставить пустым
```
