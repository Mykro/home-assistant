"""
Offer sun based automation rules.

For more details about this automation rule, please refer to the documentation
at https://home-assistant.io/components/automation/#sun-trigger
"""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_EVENT, CONF_OFFSET, CONF_PLATFORM, SUN_EVENT_SUNRISE)
from homeassistant.helpers.event import track_sunrise, track_sunset
import homeassistant.helpers.config_validation as cv

DEPENDENCIES = ['sun']

_LOGGER = logging.getLogger(__name__)

TRIGGER_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM): 'sun',
    vol.Required(CONF_EVENT): cv.sun_event,
    vol.Required(CONF_OFFSET, default=timedelta(0)): cv.time_period,
})


def trigger(hass, config, action):
    """Listen for events based on configuration."""
    event = config.get(CONF_EVENT)
    offset = config.get(CONF_OFFSET)

    def call_action():
        """Call action with right context."""
        action({
            'trigger': {
                'platform': 'sun',
                'event': event,
                'offset': offset,
            },
        })

    # Do something to call action
    if event == SUN_EVENT_SUNRISE:
        return track_sunrise(hass, call_action, offset)
    else:
        return track_sunset(hass, call_action, offset)
