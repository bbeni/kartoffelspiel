# Kartoffelspiel
Be a potato and eat your friends. Peg-Solitaire game in pygame. 🥔

## Quick setup
Tested with python 3.7

```bash
pip3 install pygame
python3 ./main.py
```

## Building APK for android
⚠️Buildozer for building for android is a little bit annoying with pygame⚠️ \
That's why I write down most of the versions of the dependencies that worked for me. On Ubunutu server 20.04, using python 3.7.17 installed with pyenv and pygame==2.5.2. Closely following [Buildozer 1.4.0](https://buildozer.readthedocs.io/en/1.4.0/installation.html) guide. Install dependencies:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-13-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
curl https://pyenv.run | bash && eval "$(pyenv init -)" && exec "$SHELL"
pyenv install 3.7.17 && pyenv global 3.7.17
pip3 install --user --upgrade Cython==0.29.19 virtualenv pygame==2.5.2 buildozer==1.4.0
```

Then run buildozer. Does take very long the first time (> 5 min)
```bash
python -m buildozer -v android debug
```
