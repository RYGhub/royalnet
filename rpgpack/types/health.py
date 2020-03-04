from typing import *
import re


class Health:
    def __init__(self,
                 initial_value: int,
                 max_value: int,
                 hidden: Optional[bool] = None,
                 temp_value: Optional[int] = None,
                 deathsave_successes: Optional[int] = None,
                 deathsave_failures: Optional[int] = None):
        self.value: int = 0
        self.max_value: int = max_value
        self.hidden: bool = hidden if hidden else False
        self.temp_value: int = temp_value if temp_value else 0
        self.deathsave_successes: int = deathsave_successes if deathsave_successes else 0
        self.deathsave_failures: int = deathsave_failures if deathsave_failures else 0
        self.change(initial_value)

    @classmethod
    def from_text(cls, text: str) -> "Health":
        match = re.match(r"(h)?([0-9]+)(?:\+([0-9]+))?/([0-9]+)(s{0,3})(f{0,3})", text)
        if not match:
            raise ValueError("Could not parse passed string.")
        hidden, value, temp_value, max_value, ds_successes, ds_failures = match.groups()
        return cls(initial_value=int(value),
                   max_value=int(max_value),
                   hidden=bool(hidden),
                   temp_value=int(temp_value) if temp_value else None,
                   deathsave_successes=len(ds_successes) if ds_successes else None,
                   deathsave_failures=len(ds_failures) if ds_failures else None)

    def to_text(self) -> str:
        string = []
        if self.hidden:
            string.append("h")
        string.append(f"{self.value}")
        if self.temp_value > 0:
            string.append(f"{self.temp_value:+}")
        string.append("/")
        string.append(f"{self.max_value}")
        string.append("s" * self.deathsave_successes)
        string.append("f" * self.deathsave_failures)
        return "".join(string)

    @property
    def dead(self) -> bool:
        return self.deathsave_failures >= 3

    @property
    def stable(self) -> bool:
        return self.deathsave_successes >= 3

    @property
    def dying(self) -> bool:
        return self.value <= 0

    @property
    def total_value(self) -> int:
        return self.value + self.temp_value

    def __str__(self):
        # Dead
        if self.dead:
            return "💀"
        # Stable
        if self.stable:
            return f"💔 {self.value}/{self.max_value} "
        # Dying
        if self.value <= 0:
            return "".join([
                f"💔 {self.value}/{self.max_value} ",
                "🔷" * self.deathsave_successes,
                "🔹" * (3 - self.deathsave_successes),
                " "
                "🔶" * self.deathsave_failures,
                "🔸" * (3 - self.deathsave_failures),
            ])
        # Hidden
        if self.hidden:
            return f"🖤 {self.value - self.max_value}"
        # Temporary HP
        if self.temp_value > 0:
            return f"💙 {self.value}+{self.temp_value}/{self.max_value}"
        # Default
        return f"❤️ {self.value}/{self.max_value}"

    def __repr__(self):
        return f"{self.__class__.__qualname__}.from_text({self.to_text()})"

    def change(self, amount) -> None:
        # Heal
        if amount > 0:
            self.value += amount
            # Cap at maximum
            if self.value >= self.max_value:
                self.value = self.max_value
            # Restore death saves
            self.deathsave_successes = 0
            self.deathsave_failures = 0
        # Damage
        else:
            # First remove temporary health
            self.temp_value += amount
            # Then damage health based on how much damage wasn't absorbed
            if self.temp_value < 0:
                self.value += self.temp_value
                self.temp_value = 0
            # Cap health at 0
            if self.value < 0:
                self.value = 0

    def deathsave_success(self) -> None:
        if not self.dying:
            raise ValueError("Can't roll death saves while alive")
        if self.stable:
            raise ValueError("Can't roll death saves while stable")
        if self.dead:
            raise ValueError("Can't roll death saves while dead")
        self.deathsave_successes += 1

    def deathsave_failure(self) -> None:
        if not self.dying:
            raise ValueError("Can't roll death saves while alive")
        if self.stable:
            raise ValueError("Can't roll death saves while stable")
        if self.dead:
            raise ValueError("Can't roll death saves while dead")
        self.deathsave_failures += 1
