/* event.rs
 * Struct representation of a reme event and related fucntions
 */

// for time mgmt 
use datetime::{LocalDateTime, LocalTime, OffsetDateTime};
// for converting messages to events
use discord::model::Message;
// for message parsing
use regex::Regex;

// message regex - will move when I have a place for it
static message_regex: Regex = Regex::new(
   r"^!reme (?<msg>.*) @ (((?<month>[0-12])[-\/](?<day>[0-31]) (?<day_offset>[0-9]+)|(?<day_offset_unit>[HhMmSs]))|((?<offset>[0-9]+)(?<unit>[HhMmSs])))"
);

/* TODO 
 * Add ability to send attachments
 * All the creation of reminders for multiple users
 * Encrypt messages before putting them in db? 
 * Figure out how to support chron reminders
 */

/// A struct representing an event. This sctruct is converted SQL and inserted
/// into the database.
#[derive(DEBUG)]
struct Entry {
    /// Unique id for the database
    id: Option<i64, None>,
    /// User that created the event
    user: String,
    /// The message sent to the user at exec_time
    msg: String,
    /// When the even was created
    created: LocalDateTime 
    /// When the reminder message should be sent
    exececuted: LocalDateTime,
}


// Entry functions
impl Entry {
    /// Creates a new empty event
    fn new () -> Option<Entry, None> {
        let current_time: LocalDateTime = LocalDateTime::now() ;

        Some(
            Entry {
                id: None,
                user: "Fake_User",
                msg: "This is a test message.",
                created_time: current_time;
                executed: current_time.checked_add(5)
            }
        )
    }

    /// Creates an event from a string
    fn from_message (input: &Message) -> Option<Entry, None> {
        if ()
        Some (
            Entry {
                id: None,
                user: input.author,
                msg: input.content,
                created: LocalDateTime::now(),
                executed: LocalDateTime::hms(_,_,_)
            }
        )
    }

    /// Convert time from message to a LocalDateTime 
    fn convert_time (date: String, time: String) -> Option<LocalDateTime, None> {
        Some()
    }
}

// Entry methods
impl Entry {

}
