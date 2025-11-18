import json
import glob

def concatena_json(cartella_input, file_output):
    """
    Legge tutti i file .json in una cartella e li concatena in un unico file.
    
    :param cartella_input: percorso della cartella con i file json
    :param file_output: percorso del file json finale
    """
    tutti_dati = []

    for file_path in glob.glob(f"{cartella_input}/*.json"):
        with open(file_path, "r") as f:
            dati = json.load(f)
            if isinstance(dati, list):
                tutti_dati.extend(dati)
            else:
                tutti_dati.append(dati)

    with open(file_output, "w") as f_out:
        json.dump(tutti_dati, f_out, indent=4)

