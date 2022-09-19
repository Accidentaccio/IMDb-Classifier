# IMDb-Classifier #
## Classificatore di recensioni di film dal sito IMDb##

Repository di lavoro per l'esame di "Elementi di intelligenza artificiale" del terzo anno di ingegneria informatica presso l'Università degli studi del Sannio.

Per utilizzare il progetto è necessario utilizzare Chrome Web Driver (rilasciato gratuitamente da Google) da posizionare nella directory principale.

Ho addestrato il classificatore con un file .csv di 50000 recensioni di dominio pubblico reperito in rete, creato basandosi su recensioni di innumerevoli film diversi.
Ho creato inoltre un dataset con tutte le recensioni di tutti i film del "Marvel Cinematic Universe" usciti fino a quel momento facendo scraping delle recensioni direttamente dal sito con Selenium.
Oltre alle recensioni ho prelevato anche le informazioni relative al voto attribuito in decimi dall'utente.

Le ho poi analizzate con il classificatore precedentemente addestrato e ho stilato diverse classifiche, comparando i risultati tra il mio classificatore, quello preaddestrato di "nltk" e la classifica basata sui voti in decimi.
I risultati del mio classificatore rispetto a quello preaddestrato sono molto diversi (come mi aspettavo) dal momento che il mio era addestrato per riconoscere recensioni solo positive o negative, mentre l'altro anche per quelle "neutre".
Invece la classifica ottenuta dall'analisi del mio classificatore sono molto simili a quella dei voti attribuiti dall'utente, segno che il classificatore ha fatto un ottimo lavoro.
Ho esportato tutti i risultati in un file Excel.

Nella cartella "Object" ho congelato i file .pkl che contengono il classificatore e tutto ciò che serve per farlo funzionare immediatamente senza doverlo riaddestrare.
Rilanciando il programma, se lo scraping di Selenium funziona ancora (i siti HTML sono in continua evoluzione e se cambiano sarebbe da correggere anche il file di scraping affinchè funzioni perfettamente) si otterranno nella cartella "Reviews" i file .csv con le recensioni aggiornate. Inoltre è possibile aggiungere al file della creazione del dataset i link dei film Marvel usciti dopo il mio esame o qualunque altro film su IMDb.
