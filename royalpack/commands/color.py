import royalnet.engineer as engi


@engi.PartialCommand.new(syntax="")
async def color(*, _sentry: engi.Sentry, _msg: engi.Message, **__):
    """
    Invia un colore in chat...?
    """
    
    await _msg.reply(
        text="I am sorry, unknown error occured during working with your request, Admin were notified"
    )


__all__ = ("color",)
