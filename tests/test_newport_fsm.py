import unittest
from unittest.mock import MagicMock
from hardware.newport_fsm import FSM


class TestFSM(unittest.TestCase):

    def setUp(self):
        self.fsm = FSM()

    def test_get_position(self):
        # Create a mock DAQ object that returns fixed voltages
        self.fsm.daq.read_analogue_voltage = MagicMock(return_value=[[1.0], [2.0]])
        # Call get_position() and check that it returns the expected position
        pos = self.fsm.get_position()
        self.assertEqual(pos, (2.5, 5.0))

    def test_voltage_to_position(self):
        # Test voltage_to_position() with a known input and expected output
        pos = self.fsm.voltage_to_position(1.0, 0.1)
        self.assertAlmostEqual(pos, 25.0)

    def test_scan_xy(self):
        # Create a mock DAQ object and check that scan_xy() calls it with the correct arguments
        self.fsm.daq.scan_xy = MagicMock()
        self.fsm.scan_xy(x=[1,2,3], y=[4,5,6], dwell_ms=5)
        self.fsm.daq.scan_xy.assert_called_once_with(x_waveform=[1,2,3], y_waveform=[4,5,6], dwell_ms=5)
