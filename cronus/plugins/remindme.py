from cronus.plugin import Plugin, handler, plugin


@plugin(name="remindme", description="Remind me about things")
class RemindMe(Plugin):

    @handler("discord", "message")
    async def add_reminder(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)

    @handler("discord", "message")
    async def remove_reminder(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)

    @handler("discord", "message")
    async def edit_reminder(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)

    @handler("discord", "message")
    async def get_one_reminder(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)

    @handler("discord", "message")
    async def get_all_reminder(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)

    # start a reminder to run on the io event loop
    async def start_reminder_task(self, source: any, *args, **kwargs):
        self.logger.info("add_reminder: %s", source)
