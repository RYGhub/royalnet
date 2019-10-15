class Config:
    __slots__ = "master_uri", "master_secret"

    def __init__(self,
                 master_uri: str,
                 master_secret: str):
        if not (master_uri.startswith("ws://")
                or master_uri.startswith("wss://")):
            raise ValueError("Invalid protocol (must be ws:// or wss://)")
        self.master_uri = master_uri
        self.master_secret = master_secret

    def __repr__(self):
        return f"{self.__class__.__qualname__}(master_uri={self.master_uri}, master_secret={self.master_secret})"
