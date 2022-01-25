import re
from dataclasses import dataclass

# username here is allowed to be any number of non-whitespace characters.
# in reality it should be pretty much the same as the local-part of an email, but the rules for parsing that
# are unnecessary here.
USER_MENTION_REGEX = re.compile(r"<@(\w+)|(\S+)>")


@dataclass
class UserMention:
    slack_id: str
    username: str

    @classmethod
    def parse(cls, raw_mention: str) -> "UserMention":
        match = USER_MENTION_REGEX.match(raw_mention)
        if match:
            try:
                return cls(slack_id=match.group(1), username=match.group(2))
            except IndexError:
                raise ValueError(
                    f"Could not parse User mention: {raw_mention}. Not all match groups satisfied."
                )
        else:
            raise ValueError(
                f"Could not parse User mention: {raw_mention}. No matches for ID and username."
            )

    @property
    def encoded(self) -> str:
        return f"<@{self.slack_id}|{self.username}>"
