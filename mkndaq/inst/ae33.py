# -*- coding: utf-8 -*-
"""
Define a class AE33 facilitating communication with a Magee Scientific AE33 instrument.

@author: joerg.klausen@meteoswiss.ch
"""

import logging
import os
import shutil
import socket
import re
import time
import zipfile

import colorama

from mkndaq.utils import datetimebin


class AE33:
    """
    Instrument of type Magee Scientific AE33 with methods, attributes for interaction.
    """

    __datadir = None
    __data_begin_read_id = None
    __datafile = None
    __file_to_stage = None
    __get_config = None
    # __id = None
    _log = None
    _logger = None
    __name = None
    __reporting_interval = None
    # __set_config = None
    __set_datetime = None
    __sockaddr = None
    __socksleep = None
    __socktout = None
    __staging = None
    __zip = False

    def __init__(self, name: str, config: dict, simulate=False) -> None:
        """
        Initialize instrument class.

        :param name: name of instrument
        :param config: dictionary of attributes defining instrument, serial port and more
            - config[name]['type']
            - config[name]['serial_number']
            - config[name]['socket']['host']
            - config[name]['socket']['port']
            - config[name]['socket']['timeout']
            - config[name]['socket']['sleep']
            - config[name]['get_config']
            - config[name]['set_config']
            - config[name]['get_data']
            - config[name]['set_datetime']
            - config['logs']
            - config[name]['sampling_interval']
            - config['staging']['path'])
            - config[name]['staging_zip']
        :param simulate: default=True, simulate instrument behavior. Assumes a serial loopback connector.
        """
        colorama.init(autoreset=True)

        try:
            self._simulate = simulate
            # setup logging
            if 'logs' in config.keys():
                self._log = True
                logs = os.path.expanduser(config['logs'])
                os.makedirs(logs, exist_ok=True)
                logfile = f"{time.strftime('%Y%m%d')}.log"
                self._logger = logging.getLogger(__name__)
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                    datefmt='%y-%m-%d %H:%M:%S',
                                    filename=str(os.path.join(logs, logfile)),
                                    filemode='a')

            # read instrument control properties for later use
            self.__name = name
            # self.__id = config[name]['id']
            self._type = config[name]['type']
            self.__serial_number = config[name]['serial_number']
            self.__get_config = config[name]['get_config']
            self.__set_config = config[name]['set_config']
            self.__set_datetime = config[name]['set_datetime']

            # configure tcp/ip
            self.__sockaddr = (config[name]['socket']['host'],
                             config[name]['socket']['port'])
            self.__socktout = config[name]['socket']['timeout']
            self.__socksleep = config[name]['socket']['sleep']

            # sampling, aggregation, reporting/storage
            self._sampling_interval = config[name]['sampling_interval']
            self.__reporting_interval = config['reporting_interval']

            # setup data directory
            datadir = os.path.expanduser(config['data'])
            self.__datadir = os.path.join(datadir, name)
            os.makedirs(self.__datadir, exist_ok=True)

            # staging area for files to be transfered
            self.__staging = os.path.expanduser(config['staging']['path'])
            self.__zip = config[name]['staging_zip']

            print(f"# Initialize AE33 (name: {self.__name}  S/N: {self.__serial_number})")
            self.get_config()
            if self.__set_datetime:
                self.set_datetime()

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    def tcpip_comm(self, cmd: str, tidy=True) -> str:
        """
        Send a command and retrieve the response. Assumes an open connection.

        :param cmd: command sent to instrument
        :param tidy: 
        :return: response of instrument, decoded
        """
        rcvd = b''
        try:
            # open socket connection as a client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, ) as s:
                # connect to the server
                s.settimeout(self.__socktout)
                s.connect(self.__sockaddr)

                # send data
                s.sendall((cmd + chr(13) + chr(10)).encode())
                time.sleep(self.__socksleep)

                # receive response
                while True:
                    data = s.recv(1024)
                    rcvd = rcvd + data
                    if chr(13).encode() in data:
                        break

            # decode response, tidy
            rcvd = rcvd.decode()
            if tidy:
                rcvd = rcvd.replace("\n", "").replace("\r", "").replace("AE33>", "")

            return rcvd

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    def fetch_from_table(self, name: str, rows=None, first=None, last=None) -> str:
        try:
            if name is None:
                raise("Table 'name' must be provided.")
            if first is None:
                if last is None:
                    if rows is None:
                        # fetch all data from table
                        cmd = f"FETCH {name} 1"
                    else:
                        # fetch number of rows from end of table
                        maxid = int(self.tcpip_comm(cmd=f"MAXID {name}", tidy=True))
                        cmd=f"FETCH {name} {maxid-rows}"                    
                elif rows is None:
                    raise("Number of 'rows' to read must be provided together with 'last'.")
                else:
                    # fetch number of rows up until last
                    cmd = f"FETCH {name} {last-rows} {last}"
            elif last is None:
                if rows is None:
                    # fetch all data starting at first
                    cmd = f"FETCH {name} {first}"
                else:
                    # fetch number of rows starting at first
                    cmd = f"FETCH {name} {first} {first+rows}"
            else:
                if rows is None:
                    cmd = f"FETCH {name} {first} {last}"
                else:
                    raise("Ambiguous request, cannot use all of 'first', 'last' and 'rows' at once.")
            
            resp = self.tcpip_comm(cmd=cmd, tidy=False)

            return cmd, resp
        except Exception as err:
            print(err)


    def set_datetime(self) -> None:
        """
        Synchronize date and time of instrument with computer time.

        :return:
        """
        try:
            cmd = f"$AE33:{time.strftime('T%Y%m%d%H%M%S')}"
            dtm = self.tcpip_comm(cmd)
            msg = f"DateTime of instrument {self._name} set to: {cmd}"
            print("%s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
            self._logger.info(msg)

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    def get_config(self) -> list:
        """
        Read current configuration of instrument and optionally write to log.

        :return (err, cfg) configuration or errors, if any.

        """
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} .get_config (name={self.__name})")
        cfg = []
        try:
            for cmd in self.__get_config:
                cfg.append(self.tcpip_comm(cmd))

            if self._log:
                self._logger.info(f"Current configuration of '{self.__name}': {cfg}")

            return cfg

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    # def set_config(self) -> list:
    #     """
    #     Set configuration of instrument and optionally write to log.

    #     :return (err, cfg) configuration set or errors, if any.
    #     """
    #     print("%s .set_config (name=%s)" % (time.strftime('%Y-%m-%d %H:%M:%S'), self.__name))
    #     cfg = []
    #     try:
    #         for cmd in self.__set_config:
    #             cfg.append(self.tcpip_comm(cmd))
    #         time.sleep(1)

    #         if self._log:
    #             self._logger.info("Configuration of '%s' set to: %s" % (self.__name, cfg))

    #         return cfg

    #     except Exception as err:
    #         if self._log:
    #             self._logger.error(err)
    #         print(err)


    # def get_latest_data(self, save=True) -> str:
    #     """
    #     Retrieve last record from Data table from instrument and optionally save.

    #     :param str cmd: command sent to instrument
    #     :param bln save: Should data be saved to file? default=True
    #     :return str response as decoded string
    #     """
    #     try:
    #         dtm = time.strftime('%Y-%m-%d %H:%M:%S')
    #         print(f"{dtm} .get_latest_data (name={self.__name}, save={save})")

    #         # read the last record from the Data table
    #         maxid = int(self.tcpip_comm(cmd="MAXID Data", tidy=True))
    #         cmd=f"FETCH Data {maxid}"                    
    #         data = self.tcpip_comm(cmd, tidy=True)

    #         if save:
    #             # generate the datafile name
    #             self.__datafile = os.path.join(self.__datadir,
    #                                            "".join([self.__name, "-",
    #                                                    datetimebin.dtbin(self.__reporting_interval), ".dat"]))

    #             # if not os.path.exists(self.__datafile):
    #             #     # if file doesn't exist, create and write header
    #             #     with open(self.__datafile, "at", encoding='utf8') as fh:
    #             #         fh.write(f"{self.__data_header}\n")
    #             #         fh.close()

    #             with open(self.__datafile, "at", encoding='utf8') as fh:
    #                 fh.write(f"{dtm} {data}\n")
    #                 fh.close()

    #             # stage data for transfer
    #             if self.__file_to_stage is None:
    #                 self.__file_to_stage = self.__datafile
    #             elif self.__file_to_stage != self.__datafile:
    #                 root = os.path.join(self.__staging, os.path.basename(self.__datadir))
    #                 os.makedirs(root, exist_ok=True)
    #                 if self.__zip:
    #                     # create zip file
    #                     archive = os.path.join(root, "".join([os.path.basename(self.__file_to_stage)[:-4], ".zip"]))
    #                     with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    #                         zf.write(self.__file_to_stage, os.path.basename(self.__file_to_stage))
    #                 else:
    #                     shutil.copyfile(self.__file_to_stage, os.path.join(root, os.path.basename(self.__file_to_stage)))
    #                 self.__file_to_stage = self.__datafile

    #         return data

    #     except Exception as err:
    #         if self._log:
    #             self._logger.error(err)
    #         print(err)


    def get_new_data(self, save=True) -> str:
        """
        Retrieve all records from table data that have not been read and optionally write to log.

        :param str cmd: command sent to instrument
        :param bln save: Should data be saved to file? default=True
        :return str response as decoded string
        """
        try:
            dtm = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{dtm} .get_new_data (name={self.__name}, save={save})")

            # get the maximum id in the Data table
            maxid = int(self.tcpip_comm(cmd="MAXID Data", tidy=True))

            # get data_begin_read_id
            if self.__data_begin_read_id:
                data_begin_read_id = self.__data_begin_read_id
            else:
                data_begin_read_id = maxid
            # read the last record from the Data table
            cmd=f"FETCH Data {data_begin_read_id} {maxid}"                    
            data = self.tcpip_comm(cmd, tidy=True)

            # set data_begin_read_id
            self.__data_begin_read_id = maxid + 1

            if save:
                # generate the datafile name
                self.__datafile = os.path.join(self.__datadir,
                                               "".join([self.__name, "-",
                                                       datetimebin.dtbin(self.__reporting_interval), ".dat"]))

                # if not os.path.exists(self.__datafile):
                #     # if file doesn't exist, create and write header
                #     with open(self.__datafile, "at", encoding='utf8') as fh:
                #         fh.write(f"{self.__data_header}\n")
                #         fh.close()

                with open(self.__datafile, "at", encoding='utf8') as fh:
                    fh.write(f"{dtm} {data}\n")
                    fh.close()

                # stage data for transfer
                self.stage_file()

            return data

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    def stage_file(self) -> None:
        """Stage a file if it is no longer written to. This is determined by checking if the path 
           of the file to be staged is different the path of the current (data)file.

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        try:
            if self.__datafile is None:
                raise ValueError("__datafile cannot be None.")
            if self.__staging is None:
                raise ValueError("__staging cannot be None.")
            if self.__datadir is None:
                raise ValueError("__datadir cannot be None.")

            if self.__file_to_stage is None:
                self.__file_to_stage = self.__datafile
            elif self.__file_to_stage != self.__datafile:
                root = os.path.join(self.__staging, os.path.basename(self.__datadir))
                os.makedirs(root, exist_ok=True)
                if self.__zip:
                    # create zip file
                    archive = os.path.join(root, "".join([os.path.basename(self.__file_to_stage)[:-4], ".zip"]))
                    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                        zf.write(self.__file_to_stage, os.path.basename(self.__file_to_stage))
                else:
                    shutil.copyfile(self.__file_to_stage, os.path.join(root, os.path.basename(self.__file_to_stage)))
                self.__file_to_stage = self.__datafile

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(err)


    def print_ae33(self) -> None:
        """Retrieve current record from Data table and print."""
        try:
            # read the last record from the Data table
            maxid = int(self.tcpip_comm(cmd="MAXID Data", tidy=True))
            cmd=f"FETCH Data {maxid}"                    
            data = self.tcpip_comm(cmd, tidy=True)

            # TODO: format data for printout

            print(colorama.Fore.GREEN + f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{self.__name}] {data}")

        except Exception as err:
            if self._log:
                self._logger.error(err)
            print(colorama.Fore.RED + f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{self.__name}] produced error {err}.")



# Header:
# Date(yyyy/MM/dd); Time(hh:mm:ss); Timebase; RefCh1; Sen1Ch1; Sen2Ch1; RefCh2; 
# Sen1Ch2; Sen2Ch2; RefCh3; Sen1Ch3; Sen2Ch3; RefCh4; Sen1Ch4; Sen2Ch4; RefCh5; 
# Sen1Ch5; Sen2Ch5; RefCh6; Sen1Ch6; Sen2Ch6; RefCh7; Sen1Ch7; Sen2Ch7; Flow1; Flow2; 
# FlowC; Pressure (Pa); Temperature (°C); BB (%); ContTemp; SupplyTemp; Status; ContStatus; 
# DetectStatus; LedStatus; ValveStatus; LedTemp; BC11; BC12; BC1; BC21; BC22; BC2; BC31; 
# BC32; BC3; BC41; BC42; BC4; BC51; BC52; BC5; BC61; BC62; BC6; BC71; BC72; BC7; 
# K1; K2; K3; K4; K5; K6; K7; TapeAdvCount; ID_com1; ID_com2; ID_com3; fields_i
# Data line:
# 2012/09/21 00:34:00 60 890416 524323 709193 823296 573862 756304 884844 619592 789142 
# 822391 673266 816066 792706 686925 828401 738101 718325 841075 789053 722690 833686 
# 3325 1674 4999 101325 21.11 -1 30 40 0 0 10 10 00000 0 1150 1290 1242 1166 1248 1215 
# 1150 1231 1190 1146 1196 1175 1214 1195 1234 1144 1114 1139 1180 1225 1174 0.00133 
# 0.00095 0.00092 0.00080 0.00057 -0.00024 -0.00025 12 0 2 0 21.1    

# Data field description:
# - Date (yyyy/MM/dd): date.
# - Time (hh:mm:ss): time. 
# - Timebase: timebase – units in seconds.
# - Ref1, Sen1Ch1, Sen2Ch1…: are the raw signal Reference (Ref), Sensing Spot 1 (Sen1) and 
# Sensing Spot 2 (Sen2) values from which the BC concentrations are calculated for channel 1 
# (Ch1), wavelength 370 nm. BC11 is the uncompensated BC calculated from the spot 1 for 
# channel 1. BC1 is the final result for the BC calculated from measurements for channel 1 
# (370 nm). This is repeated for channels 2 through 7 (wavelengths 470 ~ 950 nm).
# - Flow1; Flow2; FlowC: Measured flow in ml/min. Flow 1 is flow through the spot 1, FlowC 
# is common (total flow) through the optical chamber, Flow2 is the difference between these 
# two.
# - Pressure (Pa); Temperature (°C): These are the pressure and temperature which the 
# instrument uses to report flow. By choosing to report mass flow, the values of (101325 Pa, 
# 21.11 C) are used to convert the measured mass flow to reported volumetric flow at these 
# conditions, since these are values used by the flow sensors in the AE33. These values can 
# be exchanged for any other (Pressure, Temperature) values, if data reporting to other 
# standards is required. Optionally, you can choose the data to be reported as volumetric 
# flow at ambient conditions. In such a case, accessory measurements of the ambient 
# (Pressure, Temperature) are required. We offer different types of weather sensors to 
# provide this data automatically when connected to a COM port.
# - BB (%): the percentage of BC created by biomass burning, determined by the Sandradewi 
# model.
# - ContTemp; SupplyTemp: control and power supply board temperatures
# - Status; ContStatus; DetectStatus; LedStatus; ValveStatus; LedTemp: internal status codes 
# for the instrument.
# - BC11; BC12; BC1; BC21; BC22; BC2; BC31; BC32; BC3; BC41; BC42; BC4; BC51; BC52; 
# BC5; C61; BC62; BC6; BC71; BC72; BC7: BCn1 is the uncompensated BC calculated from 
# the spot 1 for channel n; BCn2 is the uncompensated BC calculated from the spot 2 for 
# channel n. BCn is the final result for the compensated BC calculated from measurements for 
# channel n.
# - K1; K2; K3; K4; K5; K6; K7: the K_n are the compensation parameters for wavelength
# channels n = 1 ~ 7
# - TapeAdvCount: TapeAdvCount – tape advances since start
# - ID_com1; ID_com2; ID_com3; The Fields_i: ID_com_i are the identifiers indicating which 
# auxiliary device is connected to which serial port (necessary because of the different data 
# structure). This is a 3 byte field: thus, 
# 0 2 0 21.1
# means that the “Comet temperature probe” (instrument code 2) is connected to COM2 and 
# nothing is connected to COM1 and COM3. The temperature is 21.1 C.
