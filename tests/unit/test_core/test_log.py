#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import io;
from unittest import TestCase;

from src.core import log;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_stdout = sys.stdout;
_stderr = sys.stderr;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UNIT TESTS: Log
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestLog(TestCase):
    bufferOUT: io.StringIO;
    bufferERR: io.StringIO;

    @property
    def consolelineOut(self):
        return self.bufferOUT.getvalue().rstrip();

    @property
    def consolelineErr(self):
        return self.bufferERR.getvalue().rstrip();

    def setUp(self):
        self.bufferOUT = io.StringIO();
        self.bufferERR = io.StringIO();
        sys.stdout = self.bufferOUT;
        sys.stderr = self.bufferERR;
        return;

    def tearDown(self):
        self.bufferOUT.close();
        self.bufferERR.close();
        sys.stdout = _stdout;
        sys.stderr = _stderr;
        return;

    def test_log_plain(self):
        log.logPlain('test plain message');
        assert self.consolelineOut.endswith('test plain message'), 'Should contain message in stdout';
        self.assertEqual(self.consolelineErr, '', 'Should not output to stderr');
        return;

    def test_log_multiline(self):
        log.logPlain('message line 1', 'message line 2', 'message line 3');
        lines = self.consolelineOut;
        self.assertEqual(len(lines.split('\n')), 3);
        return;

    def test_log_info(self):
        log.logInfo('test info message');
        assert self.consolelineOut.endswith('test info message'), 'Should contain message in stdout';
        self.assertEqual(self.consolelineErr, '', 'Should not output to stderr');
        return;

    def test_log_warn(self):
        # Should not raise exception
        with self.assertRaises(AssertionError):
            with self.assertRaises(Exception):
                log.logWarn('test warning');
        # Should not exit system
        with self.assertRaises(AssertionError):
            with self.assertRaises(SystemExit) as cmd:
                log.logWarn('test warning');
            self.assertEqual(cmd.exception.code, 0);
        assert self.consolelineOut.endswith('test warning'), 'Should contain message in stdout';
        self.assertEqual(self.consolelineErr, '', 'Should not output to stderr');
        return;

    def test_log_error(self):
        # Should not raise exception
        with self.assertRaises(AssertionError):
            with self.assertRaises(Exception):
                log.logError('test error message');
        # Should not exit system
        with self.assertRaises(AssertionError):
            with self.assertRaises(SystemExit):
                log.logError('test error message');
        self.assertEqual(self.consolelineOut, '', 'Should not output to stdout');
        assert self.consolelineErr.endswith('test error message'), 'Should contain message in stderr';
        return;

    def test_log_fatal(self):
        with self.assertRaises(SystemExit) as cmd:
            log.logFatal('test fatal message');
        self.assertEqual(cmd.exception.code, 1); # NOTE: these lines are accessed due to catch above
        self.assertEqual(self.consolelineOut, '', 'Should not output to stdout');
        assert self.consolelineErr.endswith('test fatal message'), 'Should contain message in stderr';
    pass;
