# Cartella dei Dataset

##
Questo repository contiene i due dataset utilizzati per la generazione del dataset di output relativo ai percorsi.
**Originary_dataset**
Il Dataset ufficiale di input.

Ogni file contiene 10 **mappe con i relativi obiettivi source-destination**. La mappa risulta duplicata per ognuno degli obiettivi ad essa associati:
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

**Modified_dataset**
Il Dataset ottenuto tramite una rielaborazione del primo in modo da rendere i file meno pesanti ma mantenendo la totalità del contenuto informativo

Ogni file contiene 10 **mappe**. I source e destination sono stati rimossi in quanto erronei nel primo dataset:
```json
{
  "map_id": 1,
  "size": 16,
  "percentage_obstacles": "0.00",
  "map": [[0,0,0,...], [0,0,0,...], ...],
}
```