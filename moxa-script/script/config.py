#----------------------------------------------------------------------------------------
# Config file.
# list of defines used, depend of ceilometer configuration.
# protocole :
#	RS232
#	RS485-2w
#	RS422/485-4w
#	serial_over_IP
#
# status sensor :
#	True - sensor enabled
#	False - sensor disabled
#
#
# sensors available :
#	SHM-30 (2 variables)
#	SDI_1x_APOGEE (3 variables)
#	SDI_2x_APOGEE (6 variables)
#	WS600 M0/M2
#----------------------------------------------------------------------------------------
_SLOPE_ANALYSER="0.8468"
_OFFSET_ANALYSER="0.6"
_OFFSET_PRESSURE="-2"
_SLOPE_PRECIP="0.685"

_STATUS_BULLETIN_RAW="0"
_STATUS_BULLETIN_DWH="1"
_ADDR_bulletin="/home/moxa/bulletin/"
_ADDR_data="/home/moxa/data/"
_ADDR_data_info="/home/moxa/current.txt"
_MHSRAW="VSRA02"
_MHSDWH="VRXA00"
_MHSQCT="VSRA29"
_INIT_TIME_BULLETIN_DWH="000"
_REPEAT_TIME_BULLETIN_DWH="600"
_INIT_TIME_BULLETIN_RAW="000"
_REPEAT_TIME_BULLETIN_RAW="600"

_DESC_SENSOR_1="WS 700 msg M0 2m"
_STATUS_SENSOR_1="1"
_STATUS_DWH_SENSOR_1="1"
_STATUS_RAW_SENSOR_1="1"
_TYPE_SENSOR_1="WS600"
_NOTE_SENSOR_1="M0"
_PROTOCOLE_SENSOR_1="RS485-2w"
_PORT_SENSOR_1="/dev/ttyM0"
_HOST_SENSOR_1="LinuxBox Front-face side"
_VAR_LIST_SENSOR_1="tre200s0 uor200s0 prestas0 fa1010z0 da1010z0 rre150z0"
_INIT_VAR_SENSOR_1="/ / / / / /"
_BAUDRATE_SENSOR_1="19200"
_NBITS_SENSOR_1="8"
_PARITY_SENSOR_1="NONE"
_STOPBIT_SENSOR_1="1"
_TIMEOUT_SENSOR_1="5"
_SIZE_SENSOR_1="68"
_INIT_TIME_SENSOR_1="560"
_REPEAT_TIME_SENSOR_1="600"
_CMD_SENSOR_1="M0\x0D"

_DESC_SENSOR_2="WS 600 msg M0 10m"
_STATUS_SENSOR_2="1"
_STATUS_DWH_SENSOR_2="1"
_STATUS_RAW_SENSOR_2="1"
_TYPE_SENSOR_2="WS600"
_NOTE_SENSOR_2="M0"
_PROTOCOLE_SENSOR_2="RS485-2w"
_PORT_SENSOR_2="/dev/ttyM1"
_HOST_SENSOR_2="LinuxBox Back-face side"
_VAR_LIST_SENSOR_2="ta1200s0 ua1200s0 pa1stas0 fkl010z0 dkl010z0 ra1150z0"
_INIT_VAR_SENSOR_2="/ / / / / /"
_BAUDRATE_SENSOR_2="19200"
_NBITS_SENSOR_2="8"
_PARITY_SENSOR_2="NONE"
_STOPBIT_SENSOR_2="1"
_TIMEOUT_SENSOR_2="5"
_SIZE_SENSOR_2="68"
_INIT_TIME_SENSOR_2="560"
_REPEAT_TIME_SENSOR_2="600"
_CMD_SENSOR_2="M0\x0D"

_DESC_SENSOR_3="WS 600 msg M2 10m"
_STATUS_SENSOR_3="1"
_STATUS_DWH_SENSOR_3="1"
_STATUS_RAW_SENSOR_3="1"
_TYPE_SENSOR_3="WS600"
_NOTE_SENSOR_3="M2"
_PROTOCOLE_SENSOR_3="RS485-2w"
_PORT_SENSOR_3="/dev/ttyM1"
_HOST_SENSOR_3="LinuxBox Back-face side"
_VAR_LIST_SENSOR_3="fkl010z1"
_INIT_VAR_SENSOR_3="/"
_BAUDRATE_SENSOR_3="19200"
_NBITS_SENSOR_3="8"
_PARITY_SENSOR_3="NONE"
_STOPBIT_SENSOR_3="1"
_TIMEOUT_SENSOR_3="5"
_SIZE_SENSOR_3="66"
_INIT_TIME_SENSOR_3="580"
_REPEAT_TIME_SENSOR_3="600"
_CMD_SENSOR_3="M2\x0D"

_DESC_SENSOR_4="WS 700 R1 2m"
_STATUS_SENSOR_4="1"
_STATUS_DWH_SENSOR_4="0"
_STATUS_RAW_SENSOR_4="0"
_TYPE_SENSOR_4="WS600"
_NOTE_SENSOR_4="R1"
_PROTOCOLE_SENSOR_4="RS485-2w"
_PORT_SENSOR_4="/dev/ttyM0"
_HOST_SENSOR_4="LinuxBox Front-face side"
_VAR_LIST_SENSOR_4="/"
_INIT_VAR_SENSOR_4="/"
_BAUDRATE_SENSOR_4="19200"
_NBITS_SENSOR_4="8"
_PARITY_SENSOR_4="NONE"
_STOPBIT_SENSOR_4="1"
_TIMEOUT_SENSOR_4="5"
_SIZE_SENSOR_4="8"
_INIT_TIME_SENSOR_4="0"
_REPEAT_TIME_SENSOR_4="600"
_CMD_SENSOR_4="R1\x0D"

_DESC_SENSOR_5="WS 600 R1 10m"
_STATUS_SENSOR_5="1"
_STATUS_DWH_SENSOR_5="0"
_STATUS_RAW_SENSOR_5="0"
_TYPE_SENSOR_5="WS600"
_NOTE_SENSOR_5="R1"
_PROTOCOLE_SENSOR_5="RS485-2w"
_PORT_SENSOR_5="/dev/ttyM1"
_HOST_SENSOR_5="LinuxBox Back-face side"
_VAR_LIST_SENSOR_5="/"
_INIT_VAR_SENSOR_5="/"
_BAUDRATE_SENSOR_5="19200"
_NBITS_SENSOR_5="8"
_PARITY_SENSOR_5="NONE"
_STOPBIT_SENSOR_5="1"
_TIMEOUT_SENSOR_5="5"
_SIZE_SENSOR_5="8"
_INIT_TIME_SENSOR_5="0"
_REPEAT_TIME_SENSOR_5="600"
_CMD_SENSOR_5="R1\x0D"

_DESC_SENSOR_6="WS 700 M4 2m"
_STATUS_SENSOR_6="1"
_STATUS_DWH_SENSOR_6="1"
_STATUS_RAW_SENSOR_6="1"
_TYPE_SENSOR_6="WS600"
_NOTE_SENSOR_6="M4"
_PROTOCOLE_SENSOR_6="RS485-2w"
_PORT_SENSOR_6="/dev/ttyM0"
_HOST_SENSOR_6="LinuxBox Front-face side"
_VAR_LIST_SENSOR_6="gor000z0"
_INIT_VAR_SENSOR_6="/"
_BAUDRATE_SENSOR_6="19200"
_NBITS_SENSOR_6="8"
_PARITY_SENSOR_6="NONE"
_STOPBIT_SENSOR_6="1"
_TIMEOUT_SENSOR_6="5"
_SIZE_SENSOR_6="65"
_INIT_TIME_SENSOR_6="580"
_REPEAT_TIME_SENSOR_6="600"
_CMD_SENSOR_6="M4\x0D"

_DESC_SENSOR_7="Rotronic RDD 2m"
_STATUS_SENSOR_7="1"
_STATUS_DWH_SENSOR_7="1"
_STATUS_RAW_SENSOR_7="1"
_TYPE_SENSOR_7="Rotronic"
_NOTE_SENSOR_7="RDD"
_PROTOCOLE_SENSOR_7="serial_over_IP"
_PORT_SENSOR_7="4001"
_HOST_SENSOR_7="10.182.255.2"
_VAR_LIST_SENSOR_7="ta2200s0 ua2200s0"
_INIT_VAR_SENSOR_7="/ /"
_BAUDRATE_SENSOR_7="19200"
_NBITS_SENSOR_7="8"
_PARITY_SENSOR_7="NONE"
_STOPBIT_SENSOR_7="1"
_TIMEOUT_SENSOR_7="5"
_SIZE_SENSOR_7="10"
_INIT_TIME_SENSOR_7="580"
_REPEAT_TIME_SENSOR_7="600"
_CMD_SENSOR_7="{H99RDD}\x0D"

_DESC_SENSOR_8=""
_STATUS_SENSOR_8="0"
_STATUS_DWH_SENSOR_8="0"
_STATUS_RAW_SENSOR_8="0"
_TYPE_SENSOR_8=""
_NOTE_SENSOR_8=""
_PROTOCOLE_SENSOR_8=""
_PORT_SENSOR_8=""
_HOST_SENSOR_8=""
_VAR_LIST_SENSOR_8=""
_INIT_VAR_SENSOR_8="/ / /"
_BAUDRATE_SENSOR_8=""
_NBITS_SENSOR_8=""
_PARITY_SENSOR_8=""
_STOPBIT_SENSOR_8=""
_TIMEOUT_SENSOR_8=""
_SIZE_SENSOR_8=""
_INIT_TIME_SENSOR_8="0"
_REPEAT_TIME_SENSOR_8=""
_CMD_SENSOR_8=""

_DESC_SENSOR_9=""
_STATUS_SENSOR_9="0"
_STATUS_DWH_SENSOR_9="0"
_STATUS_RAW_SENSOR_9="0"
_TYPE_SENSOR_9=""
_NOTE_SENSOR_9=""
_PROTOCOLE_SENSOR_9=""
_PORT_SENSOR_9=""
_HOST_SENSOR_9=""
_VAR_LIST_SENSOR_9=""
_INIT_VAR_SENSOR_9="/ / /"
_BAUDRATE_SENSOR_9=""
_NBITS_SENSOR_9=""
_PARITY_SENSOR_9=""
_STOPBIT_SENSOR_9=""
_TIMEOUT_SENSOR_9=""
_SIZE_SENSOR_9=""
_INIT_TIME_SENSOR_9="0"
_REPEAT_TIME_SENSOR_9=""
_CMD_SENSOR_9=""

_DESC_SENSOR_10=""
_STATUS_SENSOR_10="0"
_STATUS_DWH_SENSOR_10="0"
_STATUS_RAW_SENSOR_10="0"
_TYPE_SENSOR_10=""
_NOTE_SENSOR_10=""
_PROTOCOLE_SENSOR_10=""
_PORT_SENSOR_10=""
_HOST_SENSOR_10=""
_VAR_LIST_SENSOR_10=""
_INIT_VAR_SENSOR_10="/ / /"
_BAUDRATE_SENSOR_10=""
_NBITS_SENSOR_10=""
_PARITY_SENSOR_10=""
_STOPBIT_SENSOR_10=""
_TIMEOUT_SENSOR_10=""
_SIZE_SENSOR_10=""
_INIT_TIME_SENSOR_10="0"
_REPEAT_TIME_SENSOR_10=""
_CMD_SENSOR_10=""

_LIST_VAR_IRIDIUM="tre200s0 uor200s0 prestas0 dkl010z0 fkl010z0 gor000z0"
#_LIST_VAR_IRIDIUM="tre200s0 uor200s0 prestas0 dkl010z0 fkl010z0 itosurr0"
