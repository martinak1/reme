//! Reme - A discord bot that reminds you of things
//!
//! Usage:
//!
//! !reme <USER_MSG> @ m/d/y hh:mm

// Handels time events/conversion
extern crate datetime;

// Handels discord events and establishes a connection to the service
extern crate discord;
use discord::Discord;
use discord::modal::Event;

// Used to create structs to insert into the DB
mod entry;
use entry::Entry;

extern crate lazy_static;

extern crate sqlite;
extern crate regex;

fn main() {
    println!("Hello, world!");
}
