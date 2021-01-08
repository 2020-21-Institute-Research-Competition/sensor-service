#define SOIL_MOISTURE A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int soilMoisture = (1024.0 - analogRead(SOIL_MOISTURE)) / 1024 * 100;
  Serial.println(soilMoisture);
}
