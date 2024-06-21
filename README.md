# DIP-Contour-Detection

Progetto per Digital Image Processing

Il codice modicato del nostro progetto si trova interamente all'interno della cartella PEL_evaluation_nostro.

I vari file Phase contengono le classi che implementano la varie fasi dell'algoritmo, all'interno di un singolo file vi è una classe per ciascuna versione, quella base e quella integrata con Canny.

La cartella Data contiene le immagini utilizzate per testare i risultati dell'algoritmo.

Il file pel.py implementa l'esecuzione dell'algoritmo sia nella versione base che quella modificata, inoltre si occupa anche del calcolo delle funzioni definite in Evaluation e del salvataggio dei risultati delle valutazioni e deti tempi nel file results.csv e delle immagini risultanti nella cartella Data. Per testare l'algoritmo è necessario caricare l'immagine nella cartella Data e sostituire ai file nella lista images quelli desiderati su cui valutare l'algoritmo.

Il file results.csv contiene i risultati delle valutazioni delle immagini e le tempistiche di esecuzione dell'algoritmo sia per l'algoritmo base che per quello modificato.

Il jupyter notebook Valutazione legge il file results.csv e crea i grafici per la valutazione salvati nella cartella Evaluation.
