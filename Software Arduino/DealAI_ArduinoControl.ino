//#include <Servo.h>
#include <math.h>
#include <AFMotor.h>
#include <VarSpeedServo.h>  // control velocidad servos


// DECLARAR MOTORES
VarSpeedServo servo1;
VarSpeedServo servo2;
AF_DCMotor servo3(1);
AF_DCMotor servo5(4);
AF_DCMotor motorS(3);    
VarSpeedServo servo4;



// DECLARAR SENSORES
const int Trigger = 2;   //Pin digital 2 para el Trigger del sensor
const int Echo = 3;   //Pin digital 3 para el Echo del sensor

// INICIALIZAR DISPOSITIVOS
void setup() {
  Serial.begin(9600);
  
  // sensor ultrasonido
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, LOW);//Inicializamos el pin con 0

  // Selenoide
  pinMode(13, OUTPUT);

  // servomotores
  //delay(30); 
  servo1.attach(10); 
  servo2.attach(9); // 9 es servo 2 motorShiel
  servo4.attach(11);
  
  servo1.write(90,25);
  delay(30);
  servo2.write(0,25);
  delay(30);
  servo4.write(0);
  delay(30);
  //delay(2000);
}

// DECLARAR VARIABLES
String str = "";
const char separator = ',';
const int dataLength = 4;
String ordenes[dataLength];
String orden;
float posY = 20;

#define DEBUG_ARRAY(a) {for (int index = 0; index < sizeof(a) / sizeof(a[0]); index++)    {Serial.print(a[index]); Serial.print('\t');} Serial.println();};
int nServo;
float angulo;

float obtenerDistancia()
{
  long t; //timepo que demora en llegar el eco
  long d; //distancia en centimetros

  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = t/59;             //escalamos el tiempo a una distancia en cm

  Serial.print("Distancia: ");
  Serial.print(d);      //Enviamos serialmente el valor de la distancia
  Serial.print("cm");
  Serial.println(); 
  
  return d;
  //delay(100);          //Hacemos una pausa de 100ms
}

// FUNCIONES MAIN
void ejecutarOrden(){
  char comanda = ordenes[0].charAt(0);
  //Serial.print(comanda);
  switch(comanda){
    // coger item
    case 'c':
      motorS.setSpeed(255); 
      motorS.run(FORWARD);
      delay(1000);
      motorS.setSpeed(0); 
      motorS.run(RELEASE);
      Serial.println("ESPERA PARA DEJAR");
      delay(4000);
      motorS.setSpeed(255); 
      motorS.run(BACKWARD);
      delay(1000);
      motorS.setSpeed(0); 
      motorS.run(RELEASE);
      break;
      
    // dejar item
    case 'e':
      Serial.println("Expulsando Objeto"); 
      digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);
      // wait for a second
      digitalWrite(13, LOW);
      break;
      
    // orden distancia
    case 'd':
      float distancia; distancia = obtenerDistancia() ; 
      Serial.println("Distancia");
      Serial.println(distancia);
      posY = distancia;
      break;

    // ordenes servomotores
    case 's':
      Serial.println("Comanda correcta");
      nServo = ordenes[1].toInt();
      angulo = ordenes[2].toFloat();
       
      switch(nServo){
        case 1: 
          Serial.print("Servo 1, Angulo: ");
          Serial.print(angulo);
          //Serial.println;
          servo1.write(angulo,25);
          break;
        case 2: 
          angulo = -(angulo-180);
          Serial.print("Servo 2, Angulo: ");
          Serial.print(angulo);
          Serial.println();
          servo2.write(angulo,25);
          break;
        case 3: 
          Serial.print("Servo 3, colcocarse en Y: ");
          float posicionY; posicionY = ordenes[2].toFloat();
          
          Serial.print(posicionY);
          Serial.println();
          // TURN on motor
          servo3.setSpeed(255); 
          servo5.setSpeed(255); 
          if(posicionY < posY){
            servo3.run(FORWARD);
            servo5.run(BACKWARD);
          }
          else{
            servo3.run(BACKWARD);
            servo5.run(FORWARD);
          }
          while (obtenerDistancia() != posicionY){
            // espera
          }
          servo3.setSpeed(0); 
          servo5.setSpeed(0);

          // actualizar variable global posY
          posY = posicionY;
          
          
           // 
          delay(1000);   
          break;
        case 4: 
          Serial.print("Servo 2, Angulo: ");
          Serial.print(angulo);
          Serial.println();
          servo4.write(angulo);
          delay(10); // ¿?
          break;
        default:
          Serial.println("Numero de servomotor incorrecto");
          break;
      }
      break; // case 's'

    default:
      Serial.println("Comanda incorrecta");
      break;
  } 
}


int str_len;
// BUCLE MAIN RECIBIR ORDENES
void loop() {
  // Comprovar si se ha enviado una cadena al puerto
  if (Serial.available())
   {
      str = Serial.readStringUntil('\n');
      str_len = str.length();
      // Guardar cadena "str" en ordenes[]
      if(str_len >19) {
        Serial.println("Comanda incorrecta ( larga )");
        return 0;
      }
      for (int i = 0; i < dataLength ; i++)
      {
         int index = str.indexOf(separator);
         orden =  str.substring(0, index);
         ordenes[i] = orden;
         str = str.substring(index + 1);
      }
      DEBUG_ARRAY(ordenes);
      
      ejecutarOrden();
      delay(20);
   }
  

     
}
