#include <Wire.h>
#include <MechaQMC5883.h>
#include <ros.h>
#include <std_msgs/Int32.h>

MechaQMC5883 qmc;

ros::NodeHandle nh;

std_msgs::Int32 head;
ros::Publisher compass("/compass_value", &head);

void setup() 
{
  Serial.begin(57600);
  Wire.begin(); //Begin I2C communication  
  qmc.init(); //Initialise the QMC5883 Sensor 
  nh.initNode();
  nh.advertise(compass);
}

void loop() 
{
  int x,y,z;
  qmc.read(&x,&y,&z); //Get the values of X,Y and Z from sensor 
  
  int heading=atan2(x, y)/0.0174532925; //Calculate the degree using X and Y parameters with this formulae 

 //Convert result into 0 to 360
  if(heading < 0) 
  heading+=360;
  heading = 360-heading;
  Serial.println(heading);
  head.data = int(heading);
  compass.publish( &head );
  nh.spinOnce();
  delay(200);
 
}
