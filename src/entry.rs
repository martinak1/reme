/* event.rs
 * Struct representation of a reme event and related fucntions
 */

// for time mgmt
use datetime::{FixedOffset, LocalDateTime, LocalTime, OffsetDateTime};
// for converting handeling discord messages
use discord::model::{Attachment, Message, User};
// for message parsing
use regex::{Captures, Match, Regex};


/* TODO
 * Add ability to send attachments
 * All the creation of reminders for multiple users
 * Encrypt messages before putting them in db?
 * Figure out how to support chron reminders
 */

 pub enum Unit {
     Day(str),
     Hour(str),
     Minute(str)
 }

/// A struct representing an event. This sctruct is inserted
/// into the database.
#[derive(DEBUG)]
pub struct Entry {
    /// Unique id for the database
    id: Option<i64, None>,
    /// User that created the event
    users: Option<Vec<User>>,
    /// The message sent to the user at exec_time
    msg: Option<String>,
    /// Message attachments
    attachments: Option<Vec<Attachment>>,
    /// When the even was created
    created: DateTime<FixedOffset>,
    /// When the reminder message should be sent
    exececuted: DateTime<FixedOffset>,
}


// Entry functions
impl Entry {
    /// Creates a new empty event
    fn new () -> Option<Entry, None> {

        Some(
            Entry {
                id: None,
                users: None,
                msg: "This is a test message.",
                attachments: None,
                created: LocalDateTime::now(),
                executed: LocalDateTime::now()
            }
        )
    }

    /// Creates an event from a string
    fn from_message (input: &Message) -> Option<Entry, None> {
        Some()
    }

    /// Convert time from message to a LocalDateTime
    fn convert_time (date: String, time: String) -> Option<LocalDateTime, None> {
        Some()
    }

    /// Parse a message with a regex for the user message and the execution time
    fn parse_content (msg: String) -> Option<((String, LocalDateTime))> {
        /*
         Example: !reme Take pizza out of the oven 4:30 (works)
                  !reme Take pizza out of the oven + 45m (works)
                  !reme DND Tonight! @ 5/22 17:00 (broken)
        */
        lazy_static {
            let msg_regex: Regex =
                Regex::new(
                    "^!reme (?<message>.*) (((@[ ]{0,1}(?<time>[0-24]:[0-59])))|(\+[ ]{0,1}(?<offset>\d+[DdHhMm])))"
                ).unwrap();
        }

        let groups = msg_regex.captures(msg).unwrap();

        let msg = groups.name("message").as_str();
        let date = groups.name("date").as_str();
        let offset = groups.name("offset").as_str();

        }
    }
}

// Entry methods
impl Entry {

}
