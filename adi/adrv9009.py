# Copyright (C) 2019-2025 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

from adi.context_manager import context_manager
from adi.jesd import jesd as jesdadi
from adi.obs import obs
from adi.rx_tx import rx, rx_tx, tx
from adi.sync_start import sync_start


class adrv9009(rx_tx, context_manager, sync_start):
    """ADRV9009 Transceiver

    parameters:
        uri: type=string
            URI of context with ADRV9009
        jesd_monitor: type=boolean
            Boolean flag to enable JESD monitoring. jesd input is
            ignored otherwise.
        jesd: type=adi.jesd
            JESD object associated with ADRV9009
    """

    _complex_data = True
    _rx_channel_names = ["voltage0_i", "voltage0_q", "voltage1_i", "voltage1_q"]
    _tx_channel_names = ["voltage0", "voltage1", "voltage2", "voltage3"]
    _obs_channel_names = ["voltage0_i", "voltage0_q"]
    _device_name = ""

    def __init__(self, uri="", jesd_monitor=False, jesd=None):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = self._ctx.find_device("adrv9009-phy")
        self._rxadc = self._ctx.find_device("axi-adrv9009-rx-hpc")
        self._rxobs = self._ctx.find_device("axi-adrv9009-rx-obs-hpc")
        self._txdac = self._ctx.find_device("axi-adrv9009-tx-hpc")
        self._ctx.set_timeout(30000)  # Needed for loading profiles
        if jesdadi and jesd_monitor:
            self._jesd = jesd if jesd else jesdadi(address=uri)
        rx_tx.__init__(self)
        self.obs = obs(self._ctx, self._rxobs, self._obs_channel_names)

    @property
    def ensm_mode(self):
        """ensm_mode: Enable State Machine State Allows real time control over
        the current state of the device. Options are: radio_on, radio_off"""
        return self._get_iio_dev_attr_str("ensm_mode")

    @ensm_mode.setter
    def ensm_mode(self, value):
        self._set_iio_dev_attr_str("ensm_mode", value)

    @property
    def profile(self):
        """Load profile file. Provide path to profile file to attribute"""
        return self._get_iio_dev_attr("profile_config")

    @profile.setter
    def profile(self, value):
        with open(value, "r") as file:
            data = file.read()
        # Apply profiles in specific order if multiple phys found
        phys = [p for p in self.__dict__.keys() if "_ctrl" in p]
        phys = sorted(phys)
        for phy in phys[1:] + [phys[0]]:
            self._set_iio_dev_attr_str("profile_config", data, getattr(self, phy))

    @property
    def frequency_hopping_mode(self):
        """frequency_hopping_mode: Set Frequency Hopping Mode"""
        return self._get_iio_attr("TRX_LO", "frequency_hopping_mode", True)

    @frequency_hopping_mode.setter
    def frequency_hopping_mode(self, value):
        self._set_iio_attr("TRX_LO", "frequency_hopping_mode", True, value)

    @property
    def frequency_hopping_mode_en(self):
        """frequency_hopping_mode_en: Enable Frequency Hopping Mode"""
        return self._get_iio_attr("TRX_LO", "frequency_hopping_mode_enable", True)

    @frequency_hopping_mode_en.setter
    def frequency_hopping_mode_en(self, value):
        self._set_iio_attr("TRX_LO", "frequency_hopping_mode_enable", True, value)

    @property
    def calibrate_rx_phase_correction_en(self):
        """calibrate_rx_phase_correction_en: Enable RX Phase Correction Calibration"""
        return self._get_iio_dev_attr("calibrate_rx_phase_correction_en")

    @calibrate_rx_phase_correction_en.setter
    def calibrate_rx_phase_correction_en(self, value):
        self._set_iio_dev_attr_str("calibrate_rx_phase_correction_en", value)

    @property
    def calibrate_rx_qec_en(self):
        """calibrate_rx_qec_en: Enable RX QEC Calibration"""
        return self._get_iio_dev_attr("calibrate_rx_qec_en")

    @calibrate_rx_qec_en.setter
    def calibrate_rx_qec_en(self, value):
        self._set_iio_dev_attr_str("calibrate_rx_qec_en", value)

    @property
    def calibrate_tx_qec_en(self):
        """calibrate_tx_qec_en: Enable TX QEC Calibration"""
        return self._get_iio_dev_attr("calibrate_tx_qec_en")

    @calibrate_tx_qec_en.setter
    def calibrate_tx_qec_en(self, value):
        self._set_iio_dev_attr_str("calibrate_tx_qec_en", value)

    @property
    def calibrate(self):
        """calibrate: Trigger Calibration"""
        return self._get_iio_dev_attr("calibrate")

    @calibrate.setter
    def calibrate(self, value):
        self._set_iio_dev_attr_str("calibrate", value)

    @property
    def gain_control_mode_chan0(self):
        """gain_control_mode_chan0: Mode of receive path AGC. Options are:
        slow_attack, manual"""
        return self._get_iio_attr_str("voltage0", "gain_control_mode", False)

    @gain_control_mode_chan0.setter
    def gain_control_mode_chan0(self, value):
        self._set_iio_attr("voltage0", "gain_control_mode", False, value)

    @property
    def gain_control_mode_chan1(self):
        """gain_control_mode_chan1: Mode of receive path AGC. Options are:
        slow_attack, manual"""
        return self._get_iio_attr_str("voltage1", "gain_control_mode", False)

    @gain_control_mode_chan1.setter
    def gain_control_mode_chan1(self, value):
        self._set_iio_attr("voltage1", "gain_control_mode", False, value)

    @property
    def rx_quadrature_tracking_en_chan0(self):
        """Enable Quadrature tracking calibration for RX1"""
        return self._get_iio_attr("voltage0", "quadrature_tracking_en", False)

    @rx_quadrature_tracking_en_chan0.setter
    def rx_quadrature_tracking_en_chan0(self, value):
        self._set_iio_attr("voltage0", "quadrature_tracking_en", False, value)

    @property
    def rx_quadrature_tracking_en_chan1(self):
        """Enable Quadrature tracking calibration for RX2"""
        return self._get_iio_attr("voltage1", "quadrature_tracking_en", False)

    @rx_quadrature_tracking_en_chan1.setter
    def rx_quadrature_tracking_en_chan1(self, value):
        self._set_iio_attr("voltage1", "quadrature_tracking_en", False, value)

    @property
    def rx_powerdown_en_chan0(self):
        """rx_powerdown_en_chan0: Enables/disables the RX1 signal paths
        while in the ENSM radio_on state"""
        return self._get_iio_attr("voltage0", "powerdown", False)

    @rx_powerdown_en_chan0.setter
    def rx_powerdown_en_chan0(self, value):
        self._set_iio_attr("voltage0", "powerdown", False, value)

    @property
    def rx_powerdown_en_chan1(self):
        """rx_powerdown_en_chan1: Enables/disables the RX2 signal paths
        while in the ENSM radio_on state"""
        return self._get_iio_attr("voltage1", "powerdown", False)

    @rx_powerdown_en_chan1.setter
    def rx_powerdown_en_chan1(self, value):
        self._set_iio_attr("voltage1", "powerdown", False, value)

    @property
    def rx_hardwaregain_chan0(self):
        """rx_hardwaregain: Gain applied to RX path channel 0. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self._get_iio_attr("voltage0", "hardwaregain", False)

    @rx_hardwaregain_chan0.setter
    def rx_hardwaregain_chan0(self, value):
        if self.gain_control_mode_chan0 == "manual":
            self._set_iio_attr("voltage0", "hardwaregain", False, value)

    @property
    def rx_hardwaregain_chan1(self):
        """rx_hardwaregain: Gain applied to RX path channel 1. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self._get_iio_attr("voltage1", "hardwaregain", False)

    @rx_hardwaregain_chan1.setter
    def rx_hardwaregain_chan1(self, value):
        if self.gain_control_mode_chan1 == "manual":
            self._set_iio_attr("voltage1", "hardwaregain", False, value)

    @property
    def obs_powerdown_en(self):
        """obs_powerdown_en: Enables/disables the ORX signal paths
        while in the ENSM radio_on state"""
        return self._get_iio_attr("voltage2", "powerdown", False)

    @obs_powerdown_en.setter
    def obs_powerdown_en(self, value):
        self._set_iio_attr("voltage2", "powerdown", False, value)

    @property
    def aux_obs_lo(self):
        """aux_obs_lo: Carrier frequency of ORx path"""
        return self._get_iio_attr("altvoltage1", "frequency", True)

    @aux_obs_lo.setter
    def aux_obs_lo(self, value):
        self._set_iio_attr("altvoltage1", "frequency", True, value)

    @property
    def obs_quadrature_tracking_en(self):
        """Enable Quadrature tracking calibration for ORX"""
        return self._get_iio_attr("voltage2", "quadrature_tracking_en", False)

    @obs_quadrature_tracking_en.setter
    def obs_quadrature_tracking_en(self, value):
        self._set_iio_attr("voltage2", "quadrature_tracking_en", False, value)

    @property
    def obs_rf_port_select(self):
        """obs_rf_port_select: Observation path source for ORX. Options are:

        - OBS_TX_LO -
        - OBS_AUX_LO -

        """
        return self._get_iio_attr_str("voltage2", "rf_port_select", False)

    @obs_rf_port_select.setter
    def obs_rf_port_select(self, value):
        self._set_iio_attr("voltage2", "rf_port_select", False, value)

    @property
    def obs_hardwaregain(self):
        """obs_hardwaregain: Gain applied to Obs/Sniffer receive path ORX1."""
        return self._get_iio_attr("voltage2", "hardwaregain", False)

    @obs_hardwaregain.setter
    def obs_hardwaregain(self, value):
        self._set_iio_attr("voltage2", "hardwaregain", False, value)

    @property
    def tx_quadrature_tracking_en_chan0(self):
        """Enable Quadrature tracking calibration for TX1"""
        return self._get_iio_attr("voltage0", "quadrature_tracking_en", True)

    @tx_quadrature_tracking_en_chan0.setter
    def tx_quadrature_tracking_en_chan0(self, value):
        self._set_iio_attr("voltage0", "quadrature_tracking_en", True, value)

    @property
    def tx_quadrature_tracking_en_chan1(self):
        """Enable Quadrature tracking calibration for TX2"""
        return self._get_iio_attr("voltage1", "quadrature_tracking_en", True)

    @tx_quadrature_tracking_en_chan1.setter
    def tx_quadrature_tracking_en_chan1(self, value):
        self._set_iio_attr("voltage1", "quadrature_tracking_en", True, value)

    @property
    def tx_hardwaregain_chan0(self):
        """tx_hardwaregain: Attenuation applied to TX path channel 0"""
        return self._get_iio_attr("voltage0", "hardwaregain", True)

    @tx_hardwaregain_chan0.setter
    def tx_hardwaregain_chan0(self, value):
        self._set_iio_attr("voltage0", "hardwaregain", True, value)

    @property
    def tx_hardwaregain_chan1(self):
        """tx_hardwaregain: Attenuation applied to TX path channel 1"""
        return self._get_iio_attr("voltage1", "hardwaregain", True)

    @tx_hardwaregain_chan1.setter
    def tx_hardwaregain_chan1(self, value):
        self._set_iio_attr("voltage1", "hardwaregain", True, value)

    @property
    def rx_rf_bandwidth(self):
        """rx_rf_bandwidth: Bandwidth of front-end analog filter of RX path"""
        return self._get_iio_attr("voltage0", "rf_bandwidth", False)

    @property
    def tx_rf_bandwidth(self):
        """tx_rf_bandwidth: Bandwidth of front-end analog filter of TX path"""
        return self._get_iio_attr("voltage0", "rf_bandwidth", True)

    @property
    def rx_sample_rate(self):
        """rx_sample_rate: Sample rate RX path in samples per second"""
        return self._get_iio_attr("voltage0", "sampling_frequency", False)

    @property
    def orx_sample_rate(self):
        """orx_sample_rate: Sample rate ORX path in samples per second
        This value will reflect the correct value when 8x decimator is enabled
        """
        return self._get_iio_attr("voltage2", "sampling_frequency", False)

    @property
    def tx_sample_rate(self):
        """tx_sample_rate: Sample rate TX path in samples per second"""
        return self._get_iio_attr("voltage0", "sampling_frequency", True)

    @property
    def trx_lo(self):
        """trx_lo: Carrier frequency of TX and RX path"""
        return self._get_iio_attr("altvoltage0", "frequency", True)

    @trx_lo.setter
    def trx_lo(self, value):
        self._set_iio_attr("altvoltage0", "frequency", True, value)

    @property
    def jesd204_fsm_ctrl(self):
        """jesd204_fsm_ctrl: jesd204-fsm control"""
        return self._get_iio_dev_attr("jesd204_fsm_ctrl")

    @jesd204_fsm_ctrl.setter
    def jesd204_fsm_ctrl(self, value):
        self._set_iio_dev_attr_str("jesd204_fsm_ctrl", value)

    @property
    def jesd204_fsm_resume(self):
        """jesd204_fsm_resume: jesd204-fsm resume"""
        return self._get_iio_dev_attr("jesd204_fsm_resume")

    @jesd204_fsm_resume.setter
    def jesd204_fsm_resume(self, value):
        self._set_iio_dev_attr_str("jesd204_fsm_resume", value)

    @property
    def jesd204_fsm_state(self):
        """jesd204_fsm_state: jesd204-fsm state"""
        return self._get_iio_dev_attr_str("jesd204_fsm_state")

    @property
    def jesd204_fsm_paused(self):
        """jesd204_fsm_paused: jesd204-fsm paused"""
        return self._get_iio_dev_attr("jesd204_fsm_paused")

    @property
    def jesd204_fsm_error(self):
        """jesd204_fsm_error: jesd204-fsm error"""
        return self._get_iio_dev_attr("jesd204_fsm_error")


class adrv9008_1(rx, context_manager, sync_start):
    """ADRV9008-1 Receiver"""

    def __init__(self, uri="", jesd_monitor=False, jesd=None):
        self.adrv9009 = adrv9009(uri, jesd_monitor, jesd)

        self._rx_channel_names = self.adrv9009._rx_channel_names
        self._device_name = self.adrv9009._device_name
        self._ctrl = self.adrv9009._ctx.find_device("adrv9009-phy")
        self._rxadc = self.adrv9009._ctx.find_device("axi-adrv9009-rx-hpc")
        self.adrv9009._ctx.set_timeout(30000)  # Needed for loading profiles
        if jesdadi and jesd_monitor:
            self._jesd = jesd if jesd else jesdadi(uri=uri)
        rx.__init__(self)

    @property
    def ensm_mode(self):
        """ensm_mode: Enable State Machine State Allows real time control over
        the current state of the device. Options are: radio_on, radio_off"""
        return self.adrv9009.ensm_mode

    @ensm_mode.setter
    def ensm_mode(self, value):
        self.adrv9009.ensm_mode = value

    @property
    def profile(self):
        """Load profile file. Provide path to profile file to attribute"""
        return self.adrv9009.profile

    @profile.setter
    def profile(self, value):
        self.adrv9009.profile = value

    @property
    def frequency_hopping_mode(self):
        """frequency_hopping_mode: Set Frequency Hopping Mode"""
        return self._get_iio_attr("RX_LO", "frequency_hopping_mode", True)

    @frequency_hopping_mode.setter
    def frequency_hopping_mode(self, value):
        self._set_iio_attr("RX_LO", "frequency_hopping_mode", True, value)

    @property
    def frequency_hopping_mode_en(self):
        """frequency_hopping_mode_en: Enable Frequency Hopping Mode"""
        return self._get_iio_attr("RX_LO", "frequency_hopping_mode_enable", True)

    @frequency_hopping_mode_en.setter
    def frequency_hopping_mode_en(self, value):
        self._set_iio_attr("RX_LO", "frequency_hopping_mode_enable", True, value)

    @property
    def calibrate_rx_phase_correction_en(self):
        """calibrate_rx_phase_correction_en: Enable RX Phase Correction Calibration"""
        return self.adrv9009.calibrate_rx_phase_correction_en

    @calibrate_rx_phase_correction_en.setter
    def calibrate_rx_phase_correction_en(self, value):
        self.adrv9009.calibrate_rx_phase_correction_en = value

    @property
    def calibrate_rx_qec_en(self):
        """calibrate_rx_qec_en: Enable RX QEC Calibration"""
        return self.adrv9009.calibrate_rx_qec_en

    @calibrate_rx_qec_en.setter
    def calibrate_rx_qec_en(self, value):
        self.adrv9009.calibrate_rx_qec_en = value

    @property
    def calibrate(self):
        """calibrate: Trigger Calibration"""
        return self.adrv9009.calibrate

    @calibrate.setter
    def calibrate(self, value):
        self.adrv9009.calibrate = value

    @property
    def gain_control_mode_chan0(self):
        """gain_control_mode_chan0: Mode of receive path AGC. Options are:
        slow_attack, manual"""
        return self.adrv9009.gain_control_mode_chan0

    @gain_control_mode_chan0.setter
    def gain_control_mode_chan0(self, value):
        self.adrv9009.gain_control_mode_chan0 = value

    @property
    def gain_control_mode_chan1(self):
        """gain_control_mode_chan1: Mode of receive path AGC. Options are:
        slow_attack, manual"""
        return self.adrv9009.gain_control_mode_chan1

    @gain_control_mode_chan1.setter
    def gain_control_mode_chan1(self, value):
        self.adrv9009.gain_control_mode_chan1 = value

    @property
    def rx_quadrature_tracking_en_chan0(self):
        """Enable Quadrature tracking calibration for RX1"""
        return self.adrv9009.rx_quadrature_tracking_en_chan0

    @rx_quadrature_tracking_en_chan0.setter
    def rx_quadrature_tracking_en_chan0(self, value):
        self.adrv9009.rx_quadrature_tracking_en_chan0 = value

    @property
    def rx_quadrature_tracking_en_chan1(self):
        """Enable Quadrature tracking calibration for RX2"""
        return self.adrv9009.rx_quadrature_tracking_en_chan1

    @rx_quadrature_tracking_en_chan1.setter
    def rx_quadrature_tracking_en_chan1(self, value):
        self.adrv9009.rx_quadrature_tracking_en_chan1 = value

    @property
    def rx_powerdown_en_chan0(self):
        """rx_powerdown_en_chan0: Enables/disables the RX1 signal paths
        while in the ENSM radio_on state"""
        return self.adrv9009.rx_powerdown_en_chan0

    @rx_powerdown_en_chan0.setter
    def rx_powerdown_en_chan0(self, value):
        self.adrv9009.rx_powerdown_en_chan0 = value

    @property
    def rx_powerdown_en_chan1(self):
        """rx_powerdown_en_chan1: Enables/disables the RX2 signal paths
        while in the ENSM radio_on state"""
        return self.adrv9009.rx_powerdown_en_chan1

    @rx_powerdown_en_chan1.setter
    def rx_powerdown_en_chan1(self, value):
        self.adrv9009.rx_powerdown_en_chan1 = value

    @property
    def rx_hardwaregain_chan0(self):
        """rx_hardwaregain: Gain applied to RX path channel 0. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self.adrv9009.rx_hardwaregain_chan0

    @rx_hardwaregain_chan0.setter
    def rx_hardwaregain_chan0(self, value):
        if self.adrv9009.gain_control_mode_chan0 == "manual":
            self.adrv9009.rx_hardwaregain_chan0 = value

    @property
    def rx_hardwaregain_chan1(self):
        """rx_hardwaregain: Gain applied to RX path channel 1. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self.adrv9009.rx_hardwaregain_chan1

    @rx_hardwaregain_chan1.setter
    def rx_hardwaregain_chan1(self, value):
        if self.adrv9009.gain_control_mode_chan1 == "manual":
            self.adrv9009.rx_hardwaregain_chan1 = value

    @property
    def rx_rf_bandwidth(self):
        """rx_rf_bandwidth: Bandwidth of front-end analog filter of RX path"""
        return self.adrv9009.rx_rf_bandwidth

    @property
    def rx_sample_rate(self):
        """rx_sample_rate: Sample rate RX path in samples per second"""
        return self.adrv9009.rx_sample_rate

    @property
    def trx_lo(self):
        """trx_lo: Carrier frequency of TX and RX path"""
        return self.adrv9009.trx_lo

    @trx_lo.setter
    def trx_lo(self, value):
        self.adrv9009.trx_lo = value


class adrv9008_2(tx, context_manager, sync_start):
    """ADRV9008-2 Transmitter"""

    def __init__(self, uri="", jesd_monitor=False, jesd=None):
        self.adrv9009 = adrv9009(uri, jesd_monitor, jesd)

        self._tx_channel_names = self.adrv9009._tx_channel_names
        self._device_name = self.adrv9009._device_name
        self._ctrl = self.adrv9009._ctx.find_device("adrv9009-phy")
        self._txdac = self.adrv9009._ctx.find_device("axi-adrv9009-tx-hpc")
        self.adrv9009._ctx.set_timeout(30000)  # Needed for loading profiles
        if jesdadi and jesd_monitor:
            self._jesd = jesd if jesd else jesdadi(uri=uri)
        tx.__init__(self)

    @property
    def ensm_mode(self):
        """ensm_mode: Enable State Machine State Allows real time control over
        the current state of the device. Options are: radio_on, radio_off"""
        return self.adrv9009.ensm_mode

    @ensm_mode.setter
    def ensm_mode(self, value):
        self.adrv9009.ensm_mode = value

    @property
    def profile(self):
        """Load profile file. Provide path to profile file to attribute"""
        return self.adrv9009.profile

    @profile.setter
    def profile(self, value):
        self.adrv9009.profile = value

    @property
    def frequency_hopping_mode(self):
        """frequency_hopping_mode: Set Frequency Hopping Mode"""
        return self._get_iio_attr("TX_LO", "frequency_hopping_mode", True)

    @frequency_hopping_mode.setter
    def frequency_hopping_mode(self, value):
        self._set_iio_attr("TX_LO", "frequency_hopping_mode", True, value)

    @property
    def frequency_hopping_mode_en(self):
        """frequency_hopping_mode_en: Enable Frequency Hopping Mode"""
        return self._get_iio_attr("TX_LO", "frequency_hopping_mode_enable", True)

    @frequency_hopping_mode_en.setter
    def frequency_hopping_mode_en(self, value):
        self._set_iio_attr("TX_LO", "frequency_hopping_mode_enable", True, value)

    @property
    def calibrate_tx_qec_en(self):
        """calibrate_tx_qec_en: Enable TX QEC Calibration"""
        return self.adrv9009.calibrate_tx_qec_en

    @calibrate_tx_qec_en.setter
    def calibrate_tx_qec_en(self, value):
        self.adrv9009.calibrate_tx_qec_en = value

    @property
    def calibrate(self):
        """calibrate: Trigger Calibration"""
        return self.adrv9009.calibrate

    @calibrate.setter
    def calibrate(self, value):
        self.adrv9009.calibrate = value

    @property
    def tx_quadrature_tracking_en_chan0(self):
        """Enable Quadrature tracking calibration for TX1"""
        return self.adrv9009.tx_quadrature_tracking_en_chan0

    @tx_quadrature_tracking_en_chan0.setter
    def tx_quadrature_tracking_en_chan0(self, value):
        self.adrv9009.tx_quadrature_tracking_en_chan0 = value

    @property
    def tx_quadrature_tracking_en_chan1(self):
        """Enable Quadrature tracking calibration for TX2"""
        return self.adrv9009.tx_quadrature_tracking_en_chan1

    @tx_quadrature_tracking_en_chan1.setter
    def tx_quadrature_tracking_en_chan1(self, value):
        self.adrv9009.tx_quadrature_tracking_en_chan1 = value

    @property
    def tx_hardwaregain_chan0(self):
        """tx_hardwaregain: Attenuation applied to TX path channel 0"""
        return self.adrv9009.tx_hardwaregain_chan0

    @tx_hardwaregain_chan0.setter
    def tx_hardwaregain_chan0(self, value):
        self.adrv9009.tx_hardwaregain_chan0 = value

    @property
    def tx_hardwaregain_chan1(self):
        """tx_hardwaregain: Attenuation applied to TX path channel 1"""
        return self.adrv9009.tx_hardwaregain_chan1

    @tx_hardwaregain_chan1.setter
    def tx_hardwaregain_chan1(self, value):
        self.adrv9009.tx_hardwaregain_chan1 = value

    @property
    def tx_rf_bandwidth(self):
        """tx_rf_bandwidth: Bandwidth of front-end analog filter of TX path"""
        return self.adrv9009.tx_rf_bandwidth

    @property
    def tx_sample_rate(self):
        """tx_sample_rate: Sample rate TX path in samples per second"""
        return self.adrv9009.tx_sample_rate

    @property
    def trx_lo(self):
        """trx_lo: Carrier frequency of TX and RX path"""
        return self.adrv9009.trx_lo

    @trx_lo.setter
    def trx_lo(self, value):
        self.adrv9009.trx_lo = value

    @property
    def obs_powerdown_en(self):
        """obs_powerdown_en: Enables/disables the ORX signal paths
        while in the ENSM radio_on state"""
        return self.adrv9009.obs_powerdown_en

    @obs_powerdown_en.setter
    def obs_powerdown_en(self, value):
        self.adrv9009.obs_powerdown_en = value

    @property
    def aux_obs_lo(self):
        """aux_obs_lo: Carrier frequency of ORx path"""
        return self.adrv9009.aux_obs_lo

    @aux_obs_lo.setter
    def aux_obs_lo(self, value):
        self.adrv9009.aux_obs_lo = value

    @property
    def obs_quadrature_tracking_en(self):
        """Enable Quadrature tracking calibration for ORX"""
        return self.adrv9009.obs_quadrature_tracking_en

    @obs_quadrature_tracking_en.setter
    def obs_quadrature_tracking_en(self, value):
        self.adrv9009.obs_quadrature_tracking_en = value

    @property
    def obs_rf_port_select(self):
        """obs_rf_port_select: Observation path source for ORX. Options are:

        - OBS_TX_LO -
        - OBS_AUX_LO -

        """
        return self.adrv9009.obs_rf_port_select

    @obs_rf_port_select.setter
    def obs_rf_port_select(self, value):
        self.adrv9009.obs_rf_port_select = value

    @property
    def obs_hardwaregain(self):
        """obs_hardwaregain: Gain applied to Obs/Sniffer receive path ORX1."""
        return self.adrv9009.obs_hardwaregain

    @obs_hardwaregain.setter
    def obs_hardwaregain(self, value):
        self.adrv9009.obs_hardwaregain = value

    @property
    def orx_sample_rate(self):
        """orx_sample_rate: Sample rate ORX path in samples per second
        This value will reflect the correct value when 8x decimator is enabled
        """
        return self.adrv9009.orx_sample_rate
