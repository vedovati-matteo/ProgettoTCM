# ProgettoTCM
Progetto gruppo JQuelli
- Capelli Luca: 1064893
- Ragosta Stefano: 1064527
- Vedovati Matteo: 1064586

## [Homework 1](Homework%201) - ([Presentazione](Homework%201/JQuelli%20-%20Presentazione%201%20AWS.pdf))
Elenco componenti sviluppate per il primo compito:
- [Client Simulatore Gara](Homework%201/codice/SimulatoreGara/client.html): Esegue un upload dell’xml e delle credenziali (contemporaneamente)
- API Gateway (uploadAPI): Interfaccia per il metodo POST in /uploadXML
- [Authorizer (Lambda Function)](Homework%201/codice/lambda/authorizer.py): Legge il campo ‘Authorization’ nell’header della richiesta, contenente il token di autorizzazione, e lo confronta con quelli presenti nel database, se non ha corrispondenza l’upload dell’xml verrà rifiutato. I token vengono generati con Basic Auth.
- [uploadXML (Lambda Function)](Homework%201/codice/lambda/uploadXML.py): Prende l’xml in upload, esegue una convalida secondo le direttive del file .xsd dello standard IOF presente su github, aggiunge la gara all’interno del database e salva il file xml con un nome univoco. In caso fosse già presente la gara permette il suo aggiornamento (se non già finita).
- Bucket S3 (xmlresults): Contiene i file xml contenenti i dati
- DynamoDB: Contiene 2 tabelle:
  + ‘ListaGare’, con al suo interno le informazioni delle gare, data e ora di inizio e fine, nome della gara, l’URI del file salvato nel bucket S3 e id univoco.
  + ‘Accounts’ con al suo interno i token per l’autenticazione

## [Homework 2](Homework%202) - ([Presentazione](Homework%202/JQuelli%20-%20Presentazione%202%20AWS.pdf))
Elenco componenti:
- [Authorizer (Lambda Function)](Homework%202/codice/lambda/authorizer.py)
- [RegisterRace (Lambda Function)](Homework%202/codice/lambda/registerRace.py): chiamata POST all'endpoint /register_race
- [UploadXML (Lambda Function)](Homework%202/codice/lambda/uploadXML.py): chiamata POST all'endpoint /uploadXML
- [GetListaGareJSON (Lambda Function)](Homework%202/codice/lambda/getListaGareJSON.py): chiamata GET all'endpoint /list_races
- [Placement (Lambda Function)](Homework%202/codice/lambda/placement.py): chiamate GET all'endpoint /results
- [GetGaraXML (Lambda Function)](Homework%202/codice/lambda/getGaraXML.py): chiamata GET all'endpoint /downloadxml

## [Homework 3](homework%203) - ([Presentazione](homework%203/JQuelli_-_Presentazione_3_Flutter.pdf))
Elenco Paginesviluppate in Flutter:
- [Home Page](homework%203/codice/flutter/lib/main.dart)
- [Pagina Gara](homework%203/codice/flutter/lib/event.dart) ([Categorie](homework%203/codice/flutter/lib/categories.dart), [Clubs](homework%203/codice/flutter/lib/clubs.dart))
- [Risultati Categoria](homework%203/codice/flutter/lib/categoriesResults.dart)
- [Risultato Atleta](homework%203/codice/flutter/lib/psplits.dart)
- [Risultati Club](homework%203/codice/flutter/lib/clubResults.dart)

Aggiunta funzione in Lambda per ottenere la lista dei Clubs: [OrganizationList](homework%203/codice/lambda/organizationList.py)

