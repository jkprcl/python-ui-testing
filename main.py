import asyncio
import json
from datetime import datetime
import pathlib
import toga

test_notification_file = "notification.json"


class Notification:
    def __init__(
        self,
        title: str,
        message: str,
        icon_path: str = None,
        closable: bool = True,
        minimizable: bool = True,
        expiry_time: datetime = None,
    ) -> None:
        if not title:
            raise ValueError("Title cannot be empty")
        if not message:
            raise ValueError("Message cannot be empty")
        self.title = title
        self.message = message
        self.icon_path = icon_path
        self.closable = closable
        self.minimizable = minimizable
        self.expiry_time = expiry_time


def load_notification(notification_file_path: pathlib.Path) -> Notification | None:
    assert pathlib.Path(notification_file_path).is_file(), "File does not exist"
    with open(notification_file_path, "r") as notification_file:
        json_data = json.load(notification_file)
    expiry_time = None
    if json_data["expiry_time"] is not None:
        try:
            expiry_time = datetime.fromisoformat(json_data["expiry_time"])
        except Exception as e:
            print(f"Error loading expiry time: {e}")
            return None
    try:
        notification = Notification(
            title=json_data["title"],
            message=json_data["message"],
            icon_path=json_data["icon_path"],
            closable=json_data["closable"],
            minimizable=json_data["minimizable"],
            expiry_time=expiry_time,
        )
    except Exception as e:
        print(f"Error loading notification: {e}")
        return None
    return notification


def save_notification(notification_file_path: pathlib.Path, notification: Notification):
    if not notification:
        raise ValueError("Notification cannot be empty")
    if not isinstance(notification, Notification):
        raise ValueError("notification must be a valid Notification object")
    try:
        pathlib.Path(notification_file_path).write_text(
            json.dumps(notification.__dict__, indent=4), encoding="utf-8"
        )
    except Exception as e:
        print(f"Error serializing notification: {e}")
        return


async def notification_checker(notification_file_path: pathlib.Path, app: toga.App):
    while True:
        if notification_file_path.exists():
            try:
                notification = load_notification(notification_file_path)
                if notification:
                    print(f"Loaded notification: {notification}")
                notification_file_path.unlink()
            except Exception as e:
                print(f"Error loading notification: {e}")
        await asyncio.sleep(5)

def build(app):
    box = toga.Box()
    title = "Notifier"
    message = "Message"
    label = toga.Label(text=message)
    box.add(label)

    return box

# run the toga app
if __name__ == "__main__":

