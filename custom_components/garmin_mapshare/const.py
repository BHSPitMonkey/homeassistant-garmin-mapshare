"""Constants for the Garmin MapShare integration."""

DOMAIN = "garmin_mapshare"

CONF_LINK_NAME = "link_name"
CONF_LINK_PASSWORD = "link_password"

# Using share.garmin.com seems to work in all regions; explore.garmin.com only worked for US accounts?
BASE_URL = "https://share.garmin.com/Feed/Share/"
WEB_BASE_URL = "https://share.garmin.com/share/"

MANUFACTURER = "Garmin"
PRODUCT_NAME = "Garmin MapShare"
DATA_ATTRIBUTION = PRODUCT_NAME

MOCK_LINK_NAME = "#dummy"
