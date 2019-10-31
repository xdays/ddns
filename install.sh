#!/bin/bash
# -*- coding: utf-8 -*-

cp systemd/* /etc/systemd/system/
systemctl daemon-reload
