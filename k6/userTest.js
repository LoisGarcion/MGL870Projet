import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 10, // Number of virtual users
  duration: '30s', // Duration of the test
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
  },
};

//Créer une methode de test pour tester l'API :
//Définir aléatoirement si il y a une anomalie ou non
//Au début de chaque tests créer un nouveau bloc k6 : http://user-app:8080/api/k6/createBlock et définir si il y a une anomalie ou non
//Si anomalie : faire un certains nombre de requêtes de création / all / update, ... et faire une exception entre la route http://user-app:8080/api/exception/exception1 et http://user-app:8080/api/exception/exception20
//Si pas d'anomalie : faire un certains nombre de requêtes de création / all / update, ... et ne pas faire d'exception

//ON POURRA COMME CA RECUP LES LOGS DONT LES TIMESTAMP SONT DANS LA PERIODE DE TEST ET LES ANALYSER
//EXEMPLE SI LE BLOCK 1 COMMENCE A 10:00:00 ET SE TERMINE A 10:00:30, ON POURRA RECUPERER LES LOGS DE 10:00:00 A 10:00:30 ET LES ANALYSER AVEC LE LABEL DE LA BDD DE K6

//Faire environ 5000 blocs avec jusqu'à 500 requêtes par blocks

export default function () {
  http.get('http://user-app:8080/api/user/all');
  sleep(1);
}