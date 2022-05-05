# ProgettoTCM
Progetto gruppo JQuelli
- Capelli Luca: 1064893
- Ragosta Stefano: 1064527
- Vedovati Matteo: 1064586

## Homework 1
Elenco componenti sviluppate per il primo compito:
- [Client Simulatore Gara](codice/SimulatoreGara/client.html): Esegue un upload dell’xml e delle credenziali (contemporaneamente)
- API Gateway (uploadAPI): Interfaccia per il metodo POST in /uploadXML
- [Authorizer (Lambda Function)](codice/lambda/authorizer.py): Legge il campo ‘Authorization’ nell’header della richiesta, contenente il token di autorizzazione, e lo confronta con quelli presenti nel database, se non ha corrispondenza l’upload dell’xml verrà rifiutato. I token vengono generati con Basic Auth.
- [uploadXML (Lambda Function)](codice/lambda/uploadXML.py): Prende l’xml in upload, esegue una convalida secondo le direttive del file .xsd dello standard IOF presente su github, aggiunge la gara all’interno del database e salva il file xml con un nome univoco. In caso fosse già presente la gara permette il suo aggiornamento (se non già finita).
- Bucket S3 (xmlresults): Contiene i file xml contenenti i dati
- DynamoDB: Contiene 2 tabelle:
+ ‘ListaGare’, con al suo interno le informazioni delle gare, data e ora di inizio e fine, nome della gara, l’URI del file salvato nel bucket S3 e id univoco.
+ ‘Accounts’ con al suo interno i token per l’autenticazione
