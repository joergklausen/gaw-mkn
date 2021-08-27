# -*- coding: utf-8 -*-
"""
Define a class TEI49C facilitating communication with a Thermo TEI49c instrument.

@author: joerg.klausen@meteoswiss.ch
"""

import logging
import os
import serial
import shutil
import time
import zipfile
from mkndaq.utils import datetimebin


class TEI49C:
    """
    Instrument of type Thermo TEI 49C with methods, attributes for interaction.
    """

    _datadir = None
    _datafile = None
    _data_header = None
    _get_config = None
    _get_data = None
    _id = None
    _log = False
    _logger = None
    _name = None
    _reporting_interval = None
    _serial = None
    _set_config = None
    _simulate = None
    _staging = None
    _zip = False

    @classmethod
    def __init__(cls, name: str, config: dict, simulate=False) -> None:
        """
        Initialize instrument class.
        
        :param name: name of instrument
        :param config: dictionary of attributes defining the instrument, serial port and other information
            - config[name]['type']
            - config[name]['id']
            - config[name]['serial_number']
            - config[name]['get_config']
            - config[name]['set_config']
            - config[name]['get_data']
            - config[name]['data_header']
            - config[name]['port']
            - config[port]['baudrate']
            - config[port]['bytesize']
            - config[port]['parity']
            - config[port]['stopbits']
            - config[port]['timeout']
            - config[name]['sampling_interval']
            - config['data']
            - config[name]['logs']: default=True, write information to logfile
            - config['staging']['path']
            - config['staging']['zip']
        :param simulate: default=True, simulate instrument behavior. Assumes a serial loopback connector.
        """
        print("# Initialize TEI49C")

        try:
            cls._simulate = simulate
            # setup logging
            if config['logs']:
                cls._log = True
                logs = os.path.expanduser(config['logs'])
                os.makedirs(logs, exist_ok=True)
                logfile = '%s.log' % time.strftime('%Y%m%d')
                cls._logger = logging.getLogger(__name__)
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                    datefmt='%y-%m-%d %H:%M:%S',
                                    filename=str(os.path.join(logs, logfile)),
                                    filemode='a')

            # read instrument control properties for later use
            cls._name = name
            cls._id = config[name]['id'] + 128
            cls._type = config[name]['type']
            cls._serial_number = config[name]['serial_number']
            cls._get_config = config[name]['get_config']
            cls._set_config = config[name]['set_config']
            cls._get_data = config[name]['get_data']
            cls._data_header = config[name]['data_header']

            # configure serial port
            if not cls._simulate:
                port = config[name]['port']
                cls._serial = serial.Serial(port=port,
                                            baudrate=config[port]['baudrate'],
                                            bytesize=config[port]['bytesize'],
                                            parity=config[port]['parity'],
                                            stopbits=config[port]['stopbits'],
                                            timeout=config[port]['timeout'])
                if cls._serial.is_open:
                    cls._serial.close()

            # sampling, aggregation, reporting/storage
            cls._sampling_interval = config[name]['sampling_interval']
            cls._reporting_interval = config['reporting_interval']

            # setup data directory
            datadir = os.path.expanduser(config['data'])
            cls._datadir = os.path.join(datadir, name)
            os.makedirs(cls._datadir, exist_ok=True)

            # staging area for files to be transfered
            cls._staging = os.path.expanduser(config['staging']['path'])
            cls._zip = config['staging']['zip']

            # query instrument to see if communication is possible, set date and time
            if not cls._simulate:
                dte = cls.get_data('date', save=False)
                if dte:
                    tme = cls.get_data('time', save=False)
                    msg = "Instrument '%s' initialized. Instrument datetime is %s %s." % (cls._name, dte, tme)
                    cls._logger.info(msg)

                    # set date and time
                    cls.set_datetime()
                else:
                    msg = "Instrument '%s' did not respond as expected." % cls._name
                    cls._logger.error(msg)
                print("%s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

        except serial.SerialException as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def serial_comm(cls, cmd: str, tidy=True) -> str:
        """
        Send a command and retrieve the response. Assumes an open connection.

        :param cmd: command sent to instrument
        :param tidy: remove echo and checksum after '*'
        :return: response of instrument, decoded
        """
        _id = bytes([cls._id])
        rcvd = b''
        try:
            if cls._simulate:
                _id = b''
            cls._serial.write(_id + ('%s\x0D' % cmd).encode())
            time.sleep(0.5)
            while cls._serial.in_waiting > 0:
                rcvd = rcvd + cls._serial.read(1024)
                time.sleep(0.1)

            rcvd = rcvd.decode()
            if tidy:
                # - remove checksum after and including the '*'
                rcvd = rcvd.split("*")[0]
                # - remove echo before and including '\n'
                if cmd.join("\n") in rcvd:
                    rcvd = rcvd.split("\n")[1]
                # remove trailing '\r\n'
                rcvd = rcvd.rstrip()
            return rcvd

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def get_config(cls) -> list:
        """
        Read current configuration of instrument and optionally write to log.

        :return current configuration of instrument
        
        """
        print("%s .get_config (name=%s)" % (time.strftime('%Y-%m-%d %H:%M:%S'), cls._name))
        cfg = []
        try:
            cls._serial.open()
            for cmd in cls._get_config:
                cfg.append(cls.serial_comm(cmd))
            cls._serial.close()

            if cls._log:
                cls._logger.info("Current configuration of '%s': %s" % (cls._name, cfg))

            return cfg

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def set_datetime(cls) -> None:
        """
        Synchronize date and time of instrument with computer time.

        :return:
        """
        try:
            if cls._serial.is_open:
                cls._serial.close()

            cls._serial.open()
            dte = cls.serial_comm("set date %s" % time.strftime('%m-%d-%y'))
            cls._serial.close()
            msg = "Date of instrument %s set to: %s" % (cls._name, dte)
            print("%s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
            cls._logger.info(msg)

            cls._serial.open()
            tme = cls.serial_comm("set time %s" % time.strftime('%H:%M:%S'))
            cls._serial.close()
            msg = "Time of instrument %s set to: %s" % (cls._name, tme)
            print("%s %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
            cls._logger.info(msg)

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def set_config(cls) -> list:
        """
        Set configuration of instrument and optionally write to log.

        :return new configuration as returned from instrument
        """
        print("%s .set_config (name=%s)" % (time.strftime('%Y-%m-%d %H:%M:%S'), cls._name))
        cfg = []
        try:
            cls._serial.open()
            for cmd in cls._set_config:
                cfg.append(cls.serial_comm(cmd))
            cls._serial.close()
            time.sleep(1)

            if cls._log:
                cls._logger.info("Configuration of '%s' set to: %s" % (cls._name, cfg))

            return cfg

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def get_data(cls, cmd=None, save=True) -> str:
        """
        Retrieve long record from instrument and optionally write to log.

        :param str cmd: command sent to instrument
        :param bln save: Should data be saved to file? default=True
        :return str response as decoded string
        """
        try:
            dtm = time.strftime('%Y-%m-%d %H:%M:%S')
            if cls._simulate:
                print("%s .get_data (name=%s, save=%s, simulate=%s)" % (dtm, cls._name, save, cls._simulate))
            else:
                print("%s .get_data (name=%s, save=%s)" % (dtm, cls._name, save))

            if cmd is None:
                cmd = cls._get_data

            if cls._simulate:
                data = cls.simulate_get_data(cmd)
            else:
                if cls._serial.is_open:
                    cls._serial.close()

                cls._serial.open()
                data = cls.serial_comm(cmd)
                cls._serial.close()

            if save:
                # generate the datafile name
                cls._datafile = os.path.join(cls._datadir,
                                             "".join([cls._name, "-",
                                                      datetimebin.dtbin(cls._reporting_interval), ".dat"]))

                if not (os.path.exists(cls._datafile)):
                    # if file doesn't exist, create and write header
                    with open(cls._datafile, "at") as fh:
                        fh.write("%s\n" % cls._data_header)
                        fh.close()
                with open(cls._datafile, "at") as fh:
                    # add data to file
                    fh.write("%s %s\n" % (dtm, data))
                    fh.close()

                # stage data for transfer
                root = os.path.join(cls._staging, os.path.basename(cls._datadir))
                os.makedirs(root, exist_ok=True)
                if cls._zip:
                    # create zip file
                    archive = os.path.join(root, "".join([os.path.basename(cls._datafile[:-4]), ".zip"]))
                    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as fh:
                        fh.write(cls._datafile, os.path.basename(cls._datafile))
                else:
                    shutil.copyfile(cls._datafile, os.path.join(root, os.path.basename(cls._datafile)))

            return data

        except Exception as err:
            if cls._log:
                cls._logger.error(err)
            print(err)

    @classmethod
    def simulate_get_data(cls, cmd=None) -> str:
        """

        :param cmd:
        :return:
        """
        if cmd is None:
            cmd = 'lrec'

        dtm = time.strftime("%H:%M %m-%d-%y", time.gmtime())

        if cmd == 'lrec':
            data = "(simulated) %s  flags D800500 o3 0.394 cellai 123853.000 cellbi 94558.000 bncht 31.220 lmpt " \
                   "53.754 o3lt 68.363 flowa 0.000 flowb 0.000 pres 724.798" % dtm
        else:
            data = "(simulated) %s Sorry, I can only simulate lrec. " % dtm

        return data


if __name__ == "__main__":
    pass
