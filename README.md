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

## Pour tester le modèle et la fonction de loss

Vous pouvez vérifier que le code pour votre modèle et votre fonction de loss fonctionne en créant une instance d'environnement virtuel dans votre terminal (équivalent à créer un notebook temporaire dans le terminal):

```bash
uv run python
```

Puis ensuite entrer les lignes :

```bash
import numpy as np
import torch

from clinical_cool_etud.model import LSTM_risk_estimator
from clinical_cool_etud.NLLsurv import NLLSurvLoss

input_tensor = torch.ones(8).reshape(2,2,2)
model = LSTM_risk_estimator(2,2,1,10)
loss_fn = NLLSurvLoss()

risk_estimation = model(input_tensor)
list_times_to_event = [6,8]
list_status_event = [0,1]
target = np.stack((list_times_to_event, list_status_event), axis = 1)
target = torch.tensor(target)

loss = loss_fn(risk_estimation, target)
print(loss)
```


