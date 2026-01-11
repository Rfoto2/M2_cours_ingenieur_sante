## Pour mettre à jour les packages dans votre environnement virtuel par rapport au pyproject.toml et au uv.lock

```bash
uv sync
```

## Pour lancer la fonction main du fichier process_data.py

```bash
uv run process_data
```

(Le pyproject.toml contient :

```bash
[project.scripts]
process_data = "clinical_cool_etud.process_data:main"
```
ce qui signifie : si je lance la commande process_data, alors je lance la fonction main du module process_data du package clinical_cool_etud)
