#include <Wire.h>
#include<ros.h>
#include<sensor_msgs/Joy.h>

// 123 - right
// 456 - left

#define wheelCount 8
ros::NodeHandle nh;

//nh.getHardware()->setBaud(1000000)
// sda A4
// scl A5

/*union i2cTurn {
  char turn_data[4];
  float turnFloat;
}i2cturn;

union i2cVelocity {
  char data[4];
  float velocityFloat;
}i2cvelocity;*/


float turn = 0;
int8_t dir_velocity = 0;
float button[8];
float axis[8];





void rotateCallback(const sensor_msgs::Joy& msg){
  for (int i = 0; i < 8; i++){
    button[i]=float(msg.buttons[i]);
  }
  for (int i = 0; i < 8; i++){
    /*if( i == 0)
    turn = float(msg.axes[0]);
    if( i == 3)
    dir_velocity = float(msg.axes[3]);*/
    axis[i]=float(msg.axes[i]);
  }

 
  turn = axis[0];
  //dir_velocity = (int8_t)(axis[3] * 127); PUT A CONSTANT VALUE
 
  Serial.print("Direction :");
  Serial.print(turn);
 
  Serial.print("Forward or backward ");
  Serial.println(dir_velocity);


  //i2cvelocity.velocityFloat = dir_velocity;

  if(dir_velocity != 0)
  {
  if(turn == 0)
  {
    for(int x = 1; x <= wheelCount; x++)
    {
        Wire.beginTransmission(x);
        Wire.write(dir_velocity);
        Wire.endTransmission();
        Serial.print("No turn data : ");
       Serial.println(dir_velocity);
    }
   }
   else if(turn < 0)
   {
    for(int x = 1; x <= wheelCount/2; x++)
    {
        Wire.beginTransmission(x);
        Wire.write(dir_velocity);
        Wire.endTransmission();
        Serial.print("RightTurn data : ");
       Serial.println(dir_velocity);
   
     }
     
     dir_velocity *= -1; // left side oppsosite dir
     
     for(int x = wheelCount/2 + 1; x <= wheelCount; x++)
    {
     
        Wire.beginTransmission(x);
        Wire.write(dir_velocity);
        Wire.endTransmission();
        Serial.print("RightTurn data : ");
        Serial.println(dir_velocity);
      }
     
   }
   else if(turn > 0)
   {
    dir_velocity *= -1; // Right side oppsosite dir
    for(int x = 1; x <= wheelCount/2; x++)
    {
        Wire.beginTransmission(x);
        Wire.write(dir_velocity);
        Wire.endTransmission();
        Serial.print("LeftTurn data : ");
       Serial.println(dir_velocity);
   
     }
     
    dir_velocity *= -1; // left side actual dir
     
     for(int x = wheelCount/2 + 1; x <= wheelCount; x++)
    {
     
        Wire.beginTransmission(x);
        Wire.write(dir_velocity);
        Wire.endTransmission();
        Serial.print("LeftTurn data : ");
       Serial.println(dir_velocity);
      }
     
   }
}
else
{
  for(int x = 0; x <= wheelCount; x++)
    {
     
        Wire.beginTransmission(x);
        Wire.write(0);
        Wire.endTransmission();
        //Serial.print("No data ");
        //Serial.println(dir_velocity);
      }
}
}
 

 ros::Subscriber<sensor_msgs::Joy> sub("joy",&rotateCallback);  

 void setup() {
  Serial.begin(57600);
  Serial.println("Master");
  Wire.begin(); // join i2c bus (address optional for master)
  nh.initNode();
  nh.subscribe(sub);
 
  /*i2cturn.turnFloat = 0.0;
  i2cvelocity.velocityFloat = 0.0;*/
}

void loop(){
  /*for(int x = 0; x <= wheelCount; x++)
    {
     
        Wire.beginTransmission(x);
        Wire.write(0);
        Wire.endTransmission();
        //Serial.print("No data ");
        //Serial.println(dir_velocity);
      }*/
  nh.spinOnce();
  delay(1);
}
