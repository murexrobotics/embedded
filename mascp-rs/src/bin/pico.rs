#![no_std]
#![no_main]
#![feature(type_alias_impl_trait)]

use embassy_executor::Spawner;
use embassy_rp::gpio::{Level, Output};
use embassy_rp::{
    pwm::{Config as PWMConfig, Pwm},
    uart::{Config as UARTConfig, Uart},
};
use embassy_time::{Duration, Timer};
use fixed::{types::extra::U4, FixedU16};
use {defmt_rtt as _, panic_probe as _};

const ALL_CALL_ADDRESS: u8 = 0x00;
const ADDRESS: u8 = 0x01;

const UTF8_ALL_CALL_ADDRESS: u8 = 0x30; // 0 in UTF-8, 0x30 in hex, 48 in decimal
const UTF8_ADDRESS: u8 = 0x31; // 1 in UTF-8, 0x31 in hex, 49 in decimal

const MIN_DS: u16 = 0x0CCD; // 10% DS (1000 us pulse)
const STOP_DS: u16 = 0x1333; // 15% DS (1500 us pulse)
const MAX_DS: u16 = 0x1999; // 20% DS (2000 us pulse)


#[embassy_executor::main]
async fn main(_spawner: Spawner) {
    // initialize peripherals
    let p = embassy_rp::init(Default::default());

    // initialize LED
    let mut led = Output::new(p.PIN_25, Level::High);
    led.set_high();

    // initialize UART
    let uart_config = UARTConfig::default();
    let mut uart = Uart::new_blocking(p.UART0, p.PIN_0, p.PIN_1, uart_config);
    uart.set_baudrate(115_200);

    // initialize PWM
    let mut pwm_config = PWMConfig::default();
    pwm_config.compare_b = STOP_DS; // 15% duty cycle, 1500 us pulse, 0% thrust
    pwm_config.divider = FixedU16::<U4>::from_num(38.1469); // 50 Hz, magic const calculated from: https://www.desmos.com/calculator/3zuvddnhi6
    let mut pwm = Pwm::new_output_b(p.PWM_CH1, p.PIN_3, pwm_config.clone());

    // Delay for 7 seconds for thruster initialization
    // Timer::after(Duration::from_secs(7)).await;

    // UART buffer, [address, data]
    let mut buf = [0u8; 2];

    loop {
        // is the message for us?
        uart.blocking_read(&mut buf).unwrap();
        if buf[0] == ADDRESS
            || buf[0] == ALL_CALL_ADDRESS
            || buf[0] == UTF8_ADDRESS
            || buf[0] == UTF8_ALL_CALL_ADDRESS
        {
            // Awknowledge message, blink LED
            led.set_low();
            Timer::after(Duration::from_secs(1)).await;
            led.set_high();

            // Convert percentage to duty cycle value (0-65535)
            let duty =
                (((buf[1] as f32) / 255.0) * ((MAX_DS - MIN_DS) as f32) + (MIN_DS as f32)) as u16;

            // write new duty cycle
            pwm_config.compare_b = duty;
            pwm.set_config(&pwm_config)
        }
    }
}
