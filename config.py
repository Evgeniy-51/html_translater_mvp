# MODE = "test"
MODE = "work"

INPUT_LANGUAGE = "english"
# INPUT_LANGUAGE = "chinese"
# INPUT_LANGUAGE = "german"
# INPUT_LANGUAGE = "spanish"
# INPUT_LANGUAGE = "french"
# INPUT_LANGUAGE = "italian"
# INPUT_LANGUAGE = "japanese"
# INPUT_LANGUAGE = "korean"
# INPUT_LANGUAGE = "russian"


TARGET_LANGUAGE = "russian"
# TARGET_LANGUAGE = "english"
# TARGET_LANGUAGE = "chinese"
# TARGET_LANGUAGE = "spanish"
# TARGET_LANGUAGE = "french"
# TARGET_LANGUAGE = "italian"
# TARGET_LANGUAGE = "japanese"
# TARGET_LANGUAGE = "german"

#                                Input	   Cached   Output
# OPENAI_MODEL = "gpt-5-mini"  # $0.25	$0.025	$2.00
# OPENAI_MODEL = "gpt-5-nano"    # $0.05	$0.005	$0.40
# OPENAI_MODEL = "gpt-4.1"       # $2.00	$0.50	$8.00
# OPENAI_MODEL = "gpt-4.1-mini"  # $0.40	$0.10	$1.60
# OPENAI_MODEL = "gpt-4.1-nano"  # $0.10	$0.025	$0.40
OPENAI_MODEL = "gpt-4o-mini"  # $0.15	$0.075	$0.60

sentence_endings = [".", "!", "?", ".."]
BATCH_LIMIT = 1500
