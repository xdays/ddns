#!/bin/bash
# -*- coding: utf-8 -*-

cp ddns.{service,timer} /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now ddns.timer
