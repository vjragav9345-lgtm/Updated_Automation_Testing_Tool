"""Feature flags - the ONE place that switches these paused features on or off.

Each flag only DISABLES a feature; every line of the feature's code is still in
place. Setting a flag back to True restores the behaviour exactly as it was
before the flag existed. Restart the Flask app after changing a flag (the
replay script is generated from the template on every Replay, so new runs pick
the value up automatically; the live log page reads it when it is opened).

Used by:
  - backend/generator/script_generator.py (written into every generated
    replay script as a constant of the same name)
  - backend/executor/run_execution.py (OTP timeout buffer)
  - app.py (live log page)
"""

# PHASE 4 - OTP card in the live log.
# False: an OTP step is replayed like any normal text fill - the value typed
# during recording is typed again, no OTP card is shown and the replay never
# waits for OTP input (and gets no extra OTP wait time).
# To turn the OTP card back on, set this to True.
OTP_LIVE_ENTRY_ENABLED = False

# PHASE 5 - "Retry step" button on the live log's failure card.
# False: the button is not offered and a "retry" answer is ignored, so a
# failed step is handled exactly like a failure with no retry (the card is not
# shown at all when "Stop run" would be its only button).
# To turn the Retry button back on, set this to True.
LIVE_LOG_RETRY_ENABLED = False

# PHASE 5B - pause on an "already exists / already registered" website message
# (the keywords in config/message_keywords.json) with the field-error card.
# False: such a message never pauses the run and the field-error card never
# appears; the step is judged by the normal pass/fail rules.
# To turn the field-error pause back on, set this to True.
ALREADY_EXISTS_PAUSE_ENABLED = False
