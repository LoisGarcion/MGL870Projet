import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 1, // Number of virtual users
  iterations: 5000, // Number of blocks.json to simulate
};

const BASE_URL = 'http://user-app:8080/api';
const ANOMALY_PROBABILITY = 0.3; // 30% chance of anomaly
const REQUESTS_PER_BLOCK = 500;

//Créer une methode de test pour tester l'API :
//Définir aléatoirement si il y a une anomalie ou non
//Au début de chaque tests créer un nouveau bloc k6 : http://user-app:8080/api/k6/createBlock et définir si il y a une anomalie ou non
//Si anomalie : faire un certains nombre de requêtes de création / all / update, ... et faire une exception entre la route http://user-app:8080/api/exception/exception1 et http://user-app:8080/api/exception/exception20
//Si pas d'anomalie : faire un certains nombre de requêtes de création / all / update, ... et ne pas faire d'exception

//ON POURRA COMME CA RECUP LES LOGS DONT LES TIMESTAMP SONT DANS LA PERIODE DE TEST ET LES ANALYSER
//EXEMPLE SI LE BLOCK 1 COMMENCE A 10:00:00 ET SE TERMINE A 10:00:30, ON POURRA RECUPERER LES LOGS DE 10:00:00 A 10:00:30 ET LES ANALYSER AVEC LE LABEL DE LA BDD DE K6

//Faire environ 5000 blocs avec jusqu'à 500 requêtes par blocks.json

export default function () {
  // Create a new block before starting the requests
  const isAnomalous = Math.random() < ANOMALY_PROBABILITY; // Randomly decide if this block has an anomaly

  const blockResponse = http.post(`${BASE_URL}/k6/createBlock`, JSON.stringify({ anomaly: isAnomalous }), {
    headers: { 'Content-Type': 'application/json' },
  });

  // Execute requests for the block
  for (let i = 0; i < REQUESTS_PER_BLOCK; i++) {
    // Perform create operation
    const createResponse = http.post(`${BASE_URL}/user/create`, JSON.stringify({ name: `test-${i}`, email: `test-${i}@mail.com` }), {
      headers: { 'Content-Type': 'application/json' },
    });

    // Perform read operation
    const readResponse = http.get(`${BASE_URL}/user/all`);

  }
  if (isAnomalous) {
    const exceptionId = Math.floor(Math.random() * 20) + 1;
    const exceptionResponse = http.get(`${BASE_URL}/exception/exception${exceptionId}`);
  }
  sleep(0.5);
}