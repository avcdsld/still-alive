# Still Alive

e-Paper display for Raspberry Pi Pico (800x480, 3-color)

## Setup

```bash
pip3 install Pillow mpremote
```

## Contract Deploy

```bash
# install octez-client (macOS)
curl -q "https://packages.nomadic-labs.com/homebrew/Formula/octez.rb" -O
brew tap-new octez/local
mv octez.rb $(brew --repository)/Library/Taps/octez/homebrew-local/Formula/
brew install octez/local/octez

# testnet (shadownet)
octez-client --endpoint https://rpc.shadownet.teztnets.com config update
octez-client gen keys local_account
octez-client show address local_account
# get tez from https://faucet.shadownet.teztnets.com/
octez-client originate contract still_alive \
  transferring 0 from local_account \
  running <(tr '\n' ' ' < contract/still_alive.tz) \
  --init 'Pair 0 ""' \
  --burn-cap 0.5
octez-client transfer 0 from local_account to still_alive \
  --arg '"still alive"' \
  --burn-cap 0.1

# mainnet
octez-client --endpoint https://mainnet.api.tez.ie config update
octez-client import secret key mainnet_account unencrypted:edsk...
octez-client originate contract still_alive \
  transferring 0 from my_wallet \
  running <(tr '\n' ' ' < contract/still_alive.tz) \
  --init 'Pair 0 ""' \
  --burn-cap 0.5
octez-client transfer 0 from mainnet_account to still_alive \
  --arg '"still alive"' \
  --burn-cap 0.1
```

## Image Generation

```bash
cd image
python3 generate.py
python3 convert_bmp.py
```

## e-Paper Deploy

```bash
cd image
python3 -m mpremote cp epaper7in5b.py :epaper7in5b.py
python3 -m mpremote cp framebuf2.py :framebuf2.py
python3 -m mpremote cp main.py :main.py
python3 -m mpremote cp image_black.bin :image_black.bin
python3 -m mpremote cp image_red.bin :image_red.bin
python3 -m mpremote reset
```
