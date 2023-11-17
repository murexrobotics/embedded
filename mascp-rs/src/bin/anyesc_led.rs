#![no_std]
#![no_main]
#![feature(type_alias_impl_trait)]

use embassy_executor::Spawner;
use embassy_rp::gpio::{Level, Output};
use embassy_rp::{
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

    // initialize LEDs
    let _ = Output::new(p.PIN_0, Level::High);
    let mut led1 = Output::new(p.PIN_1, Level::Low);
    let mut led2 = Output::new(p.PIN_2, Level::Low);

    // initialize UART
    let uart_config = UARTConfig::default();
    let mut uart = Uart::new_blocking(p.UART0, p.PIN_12, p.PIN_13, uart_config);
    uart.set_baudrate(115_200);

    // UART buffer, [address, data]
    let mut buf = [0u8; 1];

    loop {
        // is the message for us?
        uart.blocking_read(&mut buf).unwrap();

        // Awknowledge that UART is working, turn on LED
        led2.set_high();

        if buf[0] == ADDRESS
            || buf[0] == ALL_CALL_ADDRESS
            || buf[0] == UTF8_ADDRESS
            || buf[0] == UTF8_ALL_CALL_ADDRESS
        {
            // Awknowledge message, blink LED
            led1.set_high();
            Timer::after(Duration::from_secs(1)).await;
            led1.set_low()
        }
    }
}
