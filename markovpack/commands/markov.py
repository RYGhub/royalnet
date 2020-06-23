from typing import *
from royalnet.commands import *
import markovify
import os
import re


class MarkovCommand(Command):
    name: str = "markov"

    description: str = "Genera una frase da una catena di Markov."

    syntax: str = "[modello]"

    _texts: Dict[str, markovify.NewlineText] = {}

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        if interface.name == "telegram":
            files: List[str] = tuple(os.walk(self.config["Markov"]["models_directory"]))[0][2]
            for file in files:
                match = re.match(r"(\S+)\.json$", file)
                if match is None:
                    continue
                model_name = match.group(1)
                with open(os.path.join(self.config["Markov"]["models_directory"], file)) as f:
                    self._texts[model_name] = markovify.NewlineText.from_json(f.read())

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self.interface.name != "telegram":
            raise UnsupportedError("[c]markov[/c] funziona solo su Telegram.")
        model_name = args.optional(0, self.config["Markov"]["default_model"])
        while True:
            try:
                sentence = self._texts[model_name].make_sentence()
            except KeyError:
                models = []
                for mn in self._texts:
                    models.append(f"- [c]{mn}[/c]\n")
                raise InvalidInputError("Il modello richiesto non esiste."
                                        f"Modelli disponibili:\n{''.join(models)}")
            if sentence is None:
                continue
            if len(sentence.split()) < self.config["Markov"]["min_words"]:
                continue
            break
        await data.reply(f'💬 Il bot ([c]{model_name}[/c]) dice:\n{sentence}')
