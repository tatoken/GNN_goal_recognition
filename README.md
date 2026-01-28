# 🗺️ Dataset Generator per Goal Recognition su Mappe a Griglia

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Dataset](https://img.shields.io/badge/dataset-generation-green)
![Status](https://img.shields.io/badge/status-in%20progress-yellow)


<p align="center">
    <img src="icon.png" width="300" alt="App Logo">
</p>

---

## 📖 Descrizione del Progetto
Questo repository contiene un programma Python che genera un **dataset di percorsi** su mappe a griglia *4-connected* (movimento solo orizzontale e verticale).  
Il dataset è pensato per essere usato in esperimenti di **Goal Recognition** tramite reti neurali grafiche (GNN), ad esempio con **PyTorch Geometric**.  

---

## 🎯 Obiettivo
- Prendere in ingresso una **mappa** in formato JSON contenente:  
  - la matrice della griglia (`map`)  
  - la coppia sorgente/destinazione (`source_destination`)  
  - metadati (`id`, `map_id`, `size`, `percentage_obstacles`)  
- Calcolare percorsi validi dalla sorgente alla destinazione (es. DFS con varianti per evitare soluzioni sub-ottimali).  
- Convertire ogni percorso in **entry di dataset** riutilizzabili in esperimenti di Goal Recognition.  

---

## 🗂️ Struttura del Dataset
Ogni riga del file iniziale rappresenta una **mappa**:
```json
{
  "map": [[0,0,0,...], [0,0,0,...], ...],
  "source_destination": [172, 255],
  "percentage_obstacles": "0.00",
  "id": 10000,
  "map_id": 1000,
  "size": 16
}
```

Dopo la generazione dei percorsi, ogni mappa produce più entry:
una per ciascun passo del percorso
con encoding che distingue:
celle libere,
posizione attuale dell’agente,
celle già visitate.

## 📦 Librerie Utilizzate
PyQt6
networkx

## 📌 Roadmap / ToDo
Implementare diversi algoritmi di pathfinding (DFS e varianti)
Aggiungere supporto a diverse dimensioni di griglia
Creare funzioni di esportazione diretta verso formato PYG
Integrare test automatici sul dataset

## 📚 Note Future
Il dataset generato sarà utilizzato in un progetto di Goal Recognition tramite Graph Neural Networks (GNN).
Questo repository si concentra solo sulla parte di dataset generation.



#  Path Dataset Generator - Goal Recognition su Mappe a Griglia

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10.2-brightgreen)
![GNN](https://img.shields.io/badge/GNN-PyTorch%20Geometric-orange)
![Status](https://img.shields.io/badge/status-active-success)

---

## Descrizione del Progetto

**Path Dataset Generator** è una suite completa per generare, visualizzare e analizzare dataset di percorsi su mappe a griglia per esperimenti di **Goal Recognition** tramite Graph Neural Networks (GNN).

Il progetto permette di:
- Generare mappe a griglia 4-connected (solo movimento orizzontale/verticale)
- Calcolare percorsi ottimali e sub-ottimali usando algoritmi come DFS con varianti
- Creare dataset strutturati con informazioni di stato (agente, celle visitate, obiettivo)
- Visualizzare interattivamente i percorsi e le mappe
- Addestrare modelli GNN per il riconoscimento del goal

---

## Caso d'Uso

Il progetto è progettato per il **Goal Recognition** - il problema di inferire l'obiettivo di un agente osservando la sua traiettoria parziale su una mappa.

**Input:** Sequenza di posizioni visitate da un agente  
**Output:** Previsione dell'obiettivo finale (cella destinazione)

---

## Struttura del Progetto

### File Principali
- **`main.py`** - Entry point principale con funzioni di pathfinding (DFS, DFS con RandomJump) e gestione GUI
- **`GNNGoalRecognizer.ipynb`** - Notebook Jupyter per l'addestramento e valutazione di modelli GNN
- **`requirements.txt`** - Dipendenze Python

### Directory Principali

#### `Map_Manager/`
Gestione delle mappe e dei percorsi:
- **`Map_graph_manager.py`** - Costruisce grafi dalle mappe e gestisce la topologia 4-connected
- **`Map_loader.py`** - Carica mappe da file JSON
- **`Maps_generator.py`** - Genera nuove mappe procedurali
- **`Output_instance_saver.py`** - Salva il dataset generato
- **`Data/`** - Classi dati per input/output (Map_input.py, Map_output.py, Map_path_solution_output.py)

#### `Datasets/`
Gestione dei dataset:
- **`Database_blender.py`** - Combina più file JSON in un unico dataset
- **`Modified_dataset/`** - Dataset processato (128x128, 32x32, 16x16, 8x8 grids)
- **`Originary_dataset/`** - Dataset grezzo originale
- **`Resulted_dataset/`** - Output finale dei percorsi generati (DfsRandomJump8/16/32/64)

#### `Path_Visualizer/`
GUI interattiva PyQt6:
- **`window.py`** - Finestra principale
- **`components/`** - Componenti di visualizzazione (grid renderer, heatmap, path renderer, zoom)
- **`config/`** - Gestione della configurazione e dei defaults
- **`IO_saver/`** - Salvataggio dei risultati della visualizzazione

#### `project_version/`
Cronologia delle versioni del progetto GNN (notebook evoluti numerati)

---

## Dipendenze

```
numpy==2.4.1      # Operazioni numeriche
PyQt6==6.10.2     # GUI desktop
pyqt6_sip==13.10.2
```

**Dipendenze aggiuntive consigliate** (dal notebook):
- `torch` e `torch_geometric` - Per addestramento GNN
- `wandb` - Per tracciamento degli esperimenti
- `networkx==3.4.2` - Analisi di grafi
- `matplotlib` - Visualizzazione
- `scikit-learn` - Algoritmi ML (es. t-SNE)

---

## Guida Rapida

### Generazione Dataset

```bash
python main.py
```

Questo avvia la generazione del dataset e l'eventuale visualizzazione. Tramite tale script è possibile:
1. Caricare una mappa
2. Definire source e destination
3. Scegliere algoritmo di pathfinding (DFS, DFS+RandomJump)
4. Visualizzare il percorso
5. Salvare il dataset

### Addestramento GNN

Apri e esegui il notebook:
```bash
jupyter notebook GNNGoalRecognizer.ipynb
```

Il notebook include:
- Caricamento e preprocessing del dataset
- Definizione dell'architettura GNN
- Training con W&B tracking
- Valutazione e metriche

---

## Formato del Dataset

### Mappa Input (JSON)
```json
{
  "map": [[0,0,0,...], [0,1,0,...], ...],
  "source_destination": [172, 255],
  "percentage_obstacles": "0.00",
  "id": 10000,
  "map_id": 1000,
  "size": 16
}
```

**Campi:**
- `map` - Matrice 2D (0=libero, 1=ostacolo)
- `source_destination` - [ID cella inizio, ID cella destinazione]
- `percentage_obstacles` - Percentuale di ostacoli nella mappa
- `id` - ID univoco della combinazione
- `map_id` - ID della mappa base
- `size` - Dimensione della griglia

### Entry Dataset Output
Ogni passo del percorso genera un'entry:
```json
{
  "map": encoded_map,
  "current_position": node_id,
  "visited": [node_ids],
  "goal": goal_node_id,
  "step": step_number
}
```

L'`encoded_map` contiene 3 canali:
- Celle libere (0) vs ostacoli (1)
- Posizione attuale dell'agente
- Celle già visitate

---

## Algoritmi Supportati

### DFS (Depth-First Search)
Percorso in profondità deterministico da source a destination. Utile per ottenere percorsi validi lungo le pareti.

### DFS + RandomJump
Variante randomizzata del DFS che esplora vicini in ordine casuale. Permette di generare percorsi sub-ottimali e aumenta la diversità del dataset per un migliore addestramento del modello GNN.

---

## Dimensioni Supportate

Il progetto supporta mappe a griglia di diverse dimensioni:
- **8x8** - Piccole e veloci, ideali per test
- **16x16** - Standard, buon compromesso tra velocità e complessità
- **32x32** - Medie, aumenta il numero di possibili percorsi
- **128x128** - Grandi e complesse, scenari realistici

---

## Estensioni Possibili

- [ ] Aggiungere algoritmi di pathfinding (A*, Dijkstra, BFS)
- [ ] Generazione proceduale avanzata di mappe (perlin noise, room generation)
- [ ] Export in formato PyTorch/TensorFlow/DGL
- [ ] Dashboard web di analisi dataset
- [ ] Multi-threading per generazione parallela
- [ ] Versione web della visualizzazione
- [ ] Metriche di qualità dataset automatiche

---

## Librerie Principali

| Libreria | Versione | Uso |
|----------|----------|-----|
| **numpy** | 2.4.1 | Operazioni numeriche su array |
| **PyQt6** | 6.10.2 | GUI desktop interattiva |
| **PyTorch** | latest | Reti neurali profonde |
| **PyTorch Geometric** | latest | Graph Neural Networks |
| **networkx** | 3.4.2 | Analisi e algoritmi su grafi |
| **matplotlib** | latest | Visualizzazione e plotting |
| **W&B** | latest | Tracking di esperimenti ML |

---

## Roadmap

### ✅ Completato
- [x] Generazione mappe a griglia 4-connected
- [x] Algoritmi di pathfinding (DFS base e DFS+RandomJump)
- [x] GUI di visualizzazione con PyQt6
- [x] Sistema di dataset blending e concatenazione
- [x] Supporto multi-dimensione (8/16/32/128)
- [x] Notebook di addestramento GNN con W&B

---

## Dettagli Tecnici

### Rappresentazione del Grafo
Le mappe vengono convertite in grafi dove:
- **Nodi** = celle libere (valore 0 nella matrice)
- **Archi** = connessioni 4-connected (up, down, left, right)
- **Ostacoli** = celle con valore 1 sono escluse

### Encoding del Dataset
Ogni entry del dataset contiene:
1. **Map Grid** - 3 canali (libero/ostacolo, agente corrente, celle visitate)
2. **Current Position** - ID nodo posizione agente
3. **Visited Set** - Lista di nodi visitati fino a questo punto
4. **Goal** - ID nodo destinazione
5. **Step** - Numero del passo nella sequenza

### Performance
- Generazione DFS: O(V + E) per mappa

---

## Note Importanti

- Il dataset generato è specificamente ottimizzato per esperimenti di **Goal Recognition tramite GNN**
- Le mappe utilizzano connettività **4-connected** (no diagonali) per semplicità
- Ogni percorso genera multiple entry di dataset (uno per passo) per catturare la progressione temporale
- La randomizzazione nel DFS permette di generare dataset diversi dalla stessa mappa base
- I dataset sono salvati in formato JSON per facilità di integrazione

---

## Contributi e Supporto

Per segnalare bug, proporre miglioramenti o chiarimenti, consultare la documentazione nel notebook principale o aprire una issue nel repository.

**Contributori:**

  Grazie alle persone che hanno reso possibile questo progetto:

  * [Simona Rusmini](https://github.com/AdelSimon)
  * [Nicolas Pollastri](https://github.com/NikPoll-99)

**Data Creazione:** 2025-2026  
**Versione:** 1.0
