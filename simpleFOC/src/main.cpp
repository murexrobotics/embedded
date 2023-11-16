#include <SimpleFOC.h>

// BLDC motor instance BLDCMotor(polepairs, (R), (KV))
BLDCMotor motor = BLDCMotor(7, 0.24, 540);

// BLDC driver instance BLDCDriver6PWM(phA_h, phA_l, phB_h, phB_l, phC_h, phC_l, (en))
BLDCDriver6PWM driver = BLDCDriver6PWM(A_PHASE_UH, A_PHASE_UL, A_PHASE_VH, A_PHASE_VL, A_PHASE_WH, A_PHASE_WL);


// inline current sense instance InlineCurrentSense(R, gain, phA, phB, phC)
InlineCurrentSense currentsense = InlineCurrentSense(0.003, -64.0/7.0, A_OP1_OUT, A_OP2_OUT, A_OP3_OUT);

// commander instance
Commander command = Commander(Serial);
void doMotor(char* cmd) { command.motor(&motor, cmd); }

void setup() {
    // start serial
    Serial.begin(115200);

    // set power supply voltage
    driver.voltage_power_supply = 13;
    // set driver voltage limit, this phase voltage
    driver.voltage_limit = 15;
    // initialize driver
    driver.init();
    // link driver to motor
    motor.linkDriver(&driver);

    // link driver to current sense
    currentsense.linkDriver(&driver);

    // set motion control type to velocity openloop
    motor.controller = MotionControlType::velocity_openloop;

    // set torque control type to FOC current
    motor.torque_controller = TorqueControlType::voltage;

    // set motor voltage limit, this limits Vq
    motor.voltage_limit = 15;
    // set motor velocity limit
    motor.velocity_limit = 430;

    // use monitoring

    // initialize motor
    motor.init();

    // initialize current sensing and link it to the motor
    // https://docs.simplefoc.com/inline_current_sense#where-to-place-the-current_sense-configuration-in-your-foc-code
    currentsense.init();
    motor.linkCurrentSense(&currentsense);

    // add command to commander
    // command.add('m', doTarget, "target");
    command.add('M', doMotor, "motor");
    motor.useMonitoring(Serial);

    _delay(1000);
}

// int speed = 0;
void loop() {

    // this function can be run at much lower frequency than loopFOC()
    motor.move();
    // speed += 10;

    // significantly slowing the execution down
    motor.monitor();

    // _delay(1000);

    // user communication
    command.run();
}
