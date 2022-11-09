from textual.app import App, ComposeResult
from textual.widgets import Static


class HorizontalLayoutExample(App):
    CSS = """
        Screen {
            layout: horizontal;
        }

        .box {
            height: 100%;
            width: 1fr;
            border: solid green;
        }
        """

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")


if __name__ == "__main__":
    app = HorizontalLayoutExample()
    app.run()


class VerticalLayoutExample(App):
    CSS = """
        Screen {
            layout: vertical;
        }

        .box {
            height: 1fr;
            border: solid green;
        }
        """

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")


if __name__ == "__main__":
    app = VerticalLayoutExample()
    app.run()
