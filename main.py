import asyncio
import json
from datetime import datetime
import pathlib
import toga
from toga.style import Pack

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


async def show_popup(app: toga.App, notification: Notification):
    if notification:
        app.main_window.dialog(
            toga.InfoDialog(title=notification.title, message=notification.message)
        )


async def notification_checker(notification_file_path: pathlib.Path, app: toga.App):
    while True:
        if notification_file_path.exists():
            try:
                notification = load_notification(notification_file_path)
                if notification:
                    asyncio.create_task(show_popup(app, notification))
                notification_file_path.unlink()
            except Exception as e:
                print(f"Error loading notification: {e}")
        await asyncio.sleep(5)


class NotificationApp(toga.App):
    async def app_startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        label = toga.Label(text="Notification Checker", style=Pack(padding=10))
        self.main_window.content = label
        self.main_window.show()
        notification_filepath = pathlib.Path(test_notification_file)
        asyncio.create_task(notification_checker(notification_filepath, self))


# run the toga app
def main():
    return NotificationApp(
        formal_name="Notification Checker", app_id="com.purcell-labs.notification"
    )


if __name__ == "__main__":
    main().main_loop()
