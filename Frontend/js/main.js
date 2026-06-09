//Fast Api 
//Cambiar a la del servidor 
const SERVIDOR_URL = "http://127.0.0.1:8000/api"; 
let radarActivo = false;
let entidadesNodosMap = [];
let lineaEnlaceFibra = null;
let marcadorClicUsuario = null;
let listaNodosCache = [];
let vistaActual = "CESIUM_3D";
let latSincronizada = -24.7850;
let lonSincronizada = -65.4120;
let ultimoReporteTexto = "";