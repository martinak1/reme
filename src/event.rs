/* event.rs
 * Struct representation of a reme event and related fucntions
 */

// for time mgmt 
use datetime::{LocalDateTime, LocalTime, OffsetDateTime};
// for converting messages to events
use discord::model::Message;

// Event counter - don't know if I should use this.
static mut event_counter: i64 = 0;

/* TODO 
 * Add ability to send attachments
 * All the creation of reminders for multiple users
 */
/// A struct representing an event. This sctruct is converted SQL and inserted
/// into the database.
#[derive(DEBUG)]
struct Event {
    /// Unique id for the database
    id: Option<i64, None>,
    /// User that created the event
    user: String,
    /// The message sent to the user at exec_time
    msg: String,
    /// When the even was created
    created_time: LocalDateTime 
    /// When the reminder message should be sent
    // TODO figure out how to support chron reminders
    exececuted: LocalDateTime,

}


// Event functions
impl Event {
    /// Creates a new empty event
    fn new () -> Option<Event, None> {
        let current_time: LocalDateTime = LocalDateTime::now() ;

        Some(
            Event {
                id: None,
                user: "Fake_User",
                msg: "This is a test message.",
                created_time: current_time;
                executed: current_time.checked_add(5)
            }
        )

    }

    /// Creates an event from a string
    fn from_message (input: &Message) -> Option<Event, None> {
        Some (
            Event {
                id: None,
                user: input.author,
                msg: input.content,
                created:
            }
        )
    
    }

    /// Convert time from message to a LocalDateTime 
    fn convert_time (date: String, time: String) -> Option<LocalDateTime, None> {

    }
}

// Event methods
impl Event {

}
