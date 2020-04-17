
# slackcop
Bot to keep your channels in Slack organized.

## Running

    python3 -m pip install -r requirements.txt
    export SLACK_USER_TOKEN='xoxb-XXXXXXXXXXXX-xxxxxxxxxxxx-XXXXXXXXXXXXXXXXXXXXXXXX'
    export SLACK_BOT_TOKEN='xoxb-XXXXXXXXXXXX-xxxxxxxxxxxx-XXXXXXXXXXXXXXXXXXXXXXXX'
    export SLACK_SIGNING_SECRET='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

### Listar canais que devem ser arquivados
    pyhton3 channels-list.py > channels.csv

### Arquivar canais
    python3 bot-channels-archive.py 
ou

	python3 bot-channels-archive.py channel_id1 channel_id2 channel_id3

### Notificar canais com nome fora do padrão
    python3 bot-channels-name.py
