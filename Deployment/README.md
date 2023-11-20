# GetAround Project

Pour démarrer le projet en dev, il faut téléchargé l'extension `devcontainer` de VS Code.

Une fois installé, il faut `Rebuild and Reopen in container` le container une première fois via les commandes de l'extension. Ensuite il suffira de le `reopen`.

## Dashboarding
Une fois le container construit, pour démarrer le server streamlit, il faut executer les commandes :

``` shell
cd dashboard/
```
puis 
``` shell
streamlit run --server.port 80 ./home.py
```

le dashboard sera disponible au port défini dans le fichier .devcontainer/devcontainer.json